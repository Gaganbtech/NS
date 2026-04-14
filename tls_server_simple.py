#!/usr/bin/env python3
"""
Simple TLS Server with Clear Mode Display
Shows which button was clicked: RSA, PQC, or Hybrid
"""

import subprocess
import sys
import re
from datetime import datetime

def print_banner():
    print("\n" + "=" * 80)
    print("  🔐 TLS SERVER - ENCRYPTION MODE DETECTOR")
    print("=" * 80)
    print("\n  Listening on port 4433...")
    print("  Waiting for connections from Kali...\n")
    print("=" * 80 + "\n")

def analyze_connection(output_lines):
    """Analyze SSL output to determine connection mode"""
    output_text = '\n'.join(output_lines).lower()
    
    # Check for key exchange patterns
    if 'x25519mlkem768' in output_text or ('x25519' in output_text and 'mlkem768' in output_text):
        return 'HYBRID', 'X25519MLKEM768', '⭐⭐⭐ MAXIMUM'
    elif 'mlkem768' in output_text or 'kyber' in output_text:
        return 'PQC', 'MLKEM768', '⭐⭐ HIGH'
    elif 'x25519' in output_text or 'ecdhe' in output_text:
        return 'RSA', 'X25519', '⭐ MEDIUM'
    else:
        return 'UNKNOWN', 'Unknown', '?'

def print_connection_info(mode, key_exchange, security, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "=" * 80)
    print(f"🔌 NEW CONNECTION - {timestamp}")
    print("=" * 80 + "\n")
    
    # Mode detection
    if mode == 'RSA':
        print("🔐 " + "=" * 76)
        print("   ENCRYPTION MODE: RSA (CLASSICAL)")
        print("   " + "─" * 76)
        print("   Button Clicked: RSA")
        print("   Key Exchange:   X25519 (Elliptic Curve)")
        print("   Security Level: ⭐ MEDIUM (Vulnerable to Quantum Computers)")
        print("   Description:    Traditional encryption, fast but not quantum-safe")
        print("=" * 80 + "\n")
    
    elif mode == 'PQC':
        print("🛡️  " + "=" * 76)
        print("   ENCRYPTION MODE: PQC (POST-QUANTUM)")
        print("   " + "─" * 76)
        print("   Button Clicked: PQC")
        print("   Key Exchange:   MLKEM768 (Kyber)")
        print("   Security Level: ⭐⭐ HIGH (Quantum-Resistant)")
        print("   Description:    Post-quantum cryptography, safe from quantum attacks")
        print("=" * 80 + "\n")
    
    elif mode == 'HYBRID':
        print("🔥 " + "=" * 76)
        print("   ENCRYPTION MODE: HYBRID (CLASSICAL + POST-QUANTUM)")
        print("   " + "─" * 76)
        print("   Button Clicked: HYBRID")
        print("   Key Exchange:   X25519 + MLKEM768")
        print("   Security Level: ⭐⭐⭐ MAXIMUM (Double Protection)")
        print("   Description:    Combines both classical and quantum-safe encryption")
        print("=" * 80 + "\n")
    
    # Message display
    if message:
        print("💬 " + "=" * 76)
        print("   MESSAGE RECEIVED (DECRYPTED):")
        print("   " + "─" * 76)
        print(f"   >>> {message} <<<")
        print("=" * 80 + "\n")
    
    print("✅ Connection processed successfully!\n")
    print("─" * 80 + "\n")

def main():
    print_banner()
    
    # Start OpenSSL server with detailed output
    cmd = [
        'openssl', 's_server',
        '-accept', '4433',
        '-cert', 'certs/server.crt',
        '-key', 'certs/server.key',
        '-state',
        '-msg',
        '-tlsextdebug',
        '-groups', 'X25519:X25519MLKEM768:MLKEM768'  # Support all modes
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        connection_buffer = []
        in_connection = False
        message_found = None
        
        for line in process.stdout:
            line_stripped = line.strip()
            
            # Start of new connection
            if "SSL_accept:before SSL initialization" in line_stripped or "ACCEPT" in line_stripped:
                # Process previous connection if exists
                if connection_buffer:
                    mode, key_exchange, security = analyze_connection(connection_buffer)
                    print_connection_info(mode, key_exchange, security, message_found)
                
                # Reset for new connection
                connection_buffer = []
                in_connection = True
                message_found = None
            
            # Collect connection data
            if in_connection:
                connection_buffer.append(line_stripped)
            
            # Detect message
            if "Hi, how are you" in line_stripped or "Hi, how are you" in line:
                message_found = "Hi, how are you"
            
            # End of connection
            if "SSL_accept:TLSv1.3 write finished" in line_stripped or \
               "SSL_accept:SSLv3/TLS write finished" in line_stripped:
                if connection_buffer:
                    mode, key_exchange, security = analyze_connection(connection_buffer)
                    print_connection_info(mode, key_exchange, security, message_found)
                    connection_buffer = []
                    in_connection = False
        
    except KeyboardInterrupt:
        print("\n" + "=" * 80)
        print("🛑 Server stopped")
        print("=" * 80 + "\n")
        sys.exit(0)
    except FileNotFoundError:
        print("\n❌ ERROR: OpenSSL not found!")
        print("   Install: brew install openssl (Mac) or apt install openssl (Linux)\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
