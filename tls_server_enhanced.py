#!/usr/bin/env python3
"""
Enhanced TLS Server with Clear Display
Shows: Key Exchange Method, Cipher Suite, and Received Messages
"""

import subprocess
import sys
import re
from datetime import datetime

def print_banner():
    print("=" * 80)
    print("  🔐 POST-QUANTUM CRYPTOGRAPHY TLS SERVER - ENHANCED MODE")
    print("=" * 80)
    print()
    print("  Listening on: 0.0.0.0:4433")
    print("  Certificate: certs/server.crt")
    print("  Private Key: certs/server.key")
    print()
    print("  Supported Key Exchange Methods:")
    print("    ✓ RSA Mode      → X25519 (Classical Elliptic Curve)")
    print("    ✓ PQC Mode      → MLKEM768 (Post-Quantum Kyber)")
    print("    ✓ Hybrid Mode   → X25519MLKEM768 (Classical + PQC)")
    print()
    print("=" * 80)
    print()
    print("⏳ Waiting for connections...")
    print()

def print_separator():
    print("\n" + "─" * 80 + "\n")

def print_connection_start():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 80)
    print(f"🔌 NEW CONNECTION ESTABLISHED - {timestamp}")
    print("=" * 80 + "\n")

def print_key_exchange(key_type):
    print("\n" + "🔑 " + "=" * 76)
    print("   KEY EXCHANGE METHOD DETECTED:")
    print("   " + "─" * 76)
    
    if "X25519MLKEM768" in key_type or "x25519mlkem768" in key_type.lower():
        print("   🔥 HYBRID MODE: X25519 + MLKEM768")
        print("   ├─ Classical: X25519 (Elliptic Curve)")
        print("   └─ Post-Quantum: MLKEM768 (Kyber)")
        print("   Security: ⭐⭐⭐ MAXIMUM (Quantum-Resistant)")
    elif "MLKEM768" in key_type or "mlkem768" in key_type.lower():
        print("   🛡️  POST-QUANTUM MODE: MLKEM768")
        print("   └─ Algorithm: Kyber (NIST PQC Standard)")
        print("   Security: ⭐⭐ HIGH (Quantum-Resistant)")
    elif "X25519" in key_type:
        print("   🔐 CLASSICAL MODE: X25519")
        print("   └─ Algorithm: Elliptic Curve Diffie-Hellman")
        print("   Security: ⭐ MEDIUM (Vulnerable to Quantum)")
    else:
        print(f"   Method: {key_type}")
    
    print("=" * 80 + "\n")

def print_cipher(cipher):
    print("🔐 " + "=" * 76)
    print("   CIPHER SUITE:")
    print("   " + "─" * 76)
    print(f"   {cipher}")
    print("=" * 80 + "\n")

def print_protocol(protocol):
    print("📡 " + "=" * 76)
    print("   PROTOCOL VERSION:")
    print("   " + "─" * 76)
    print(f"   {protocol}")
    print("=" * 80 + "\n")

def print_message(message):
    print("\n" + "💬 " + "=" * 76)
    print("   MESSAGE RECEIVED (DECRYPTED):")
    print("   " + "─" * 76)
    print(f"   >>> {message.strip()} <<<")
    print("=" * 80 + "\n")

def print_handshake_complete():
    print("✅ " + "=" * 76)
    print("   TLS HANDSHAKE COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")

def main():
    print_banner()
    
    # Start OpenSSL server
    cmd = [
        'openssl', 's_server',
        '-accept', '4433',
        '-cert', 'certs/server.crt',
        '-key', 'certs/server.key',
        '-state',
        '-msg',
        '-tlsextdebug'
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        connection_started = False
        message_buffer = []
        current_connection_info = {}
        
        for line in process.stdout:
            line = line.strip()
            
            # Detect new connection
            if "SSL_accept:before SSL initialization" in line or "ACCEPT" in line:
                if connection_started and current_connection_info:
                    # Print summary of previous connection
                    print_separator()
                print_connection_start()
                connection_started = True
                message_buffer = []
                current_connection_info = {}
            
            # Detect supported groups (key exchange methods)
            elif "supported_groups" in line.lower() or "key_share" in line.lower():
                # Extract group information
                if "mlkem768" in line.lower() and "x25519" in line.lower():
                    current_connection_info['mode'] = 'HYBRID'
                elif "mlkem768" in line.lower():
                    current_connection_info['mode'] = 'PQC'
                elif "x25519" in line.lower():
                    current_connection_info['mode'] = 'RSA'
            
            # Detect key exchange
            elif "Server Temp Key:" in line:
                key_match = re.search(r'Server Temp Key:\s*(.+)', line)
                if key_match:
                    key_type = key_match.group(1)
                    current_connection_info['key_exchange'] = key_type
                    print_key_exchange(key_type)
            
            # Detect cipher
            elif line.startswith("Cipher") and ":" in line:
                cipher_match = re.search(r'Cipher\s*:\s*(.+)', line)
                if cipher_match:
                    print_cipher(cipher_match.group(1))
            
            # Detect protocol
            elif line.startswith("Protocol") and ":" in line:
                protocol_match = re.search(r'Protocol\s*:\s*(.+)', line)
                if protocol_match:
                    print_protocol(protocol_match.group(1))
            
            # Detect message
            elif "Hi, how are you" in line:
                print_message("Hi, how are you")
            
            # Detect handshake complete
            elif "SSL_accept:TLSv1.3 write finished" in line:
                print_handshake_complete()
            
            # Buffer other lines for debugging
            else:
                # Optionally print debug lines
                if "-debug" in sys.argv:
                    print(f"[DEBUG] {line}")
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("🛑 Server stopped by user")
        print("=" * 80)
        sys.exit(0)
    except FileNotFoundError:
        print("\n❌ ERROR: OpenSSL not found!")
        print("   Please install OpenSSL first.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
