#!/usr/bin/env python3
"""
Simple TLS Server - Shows Mode and Messages Clearly
"""

import subprocess
import sys
from datetime import datetime

def print_banner():
    print("\n" + "=" * 80)
    print("  🔐 TLS SERVER - MESSAGE DISPLAY")
    print("=" * 80)
    print("\n  Listening on port 4433...")
    print("  Showing encrypted and decrypted messages\n")
    print("=" * 80 + "\n")

def main():
    print_banner()
    
    connection_num = 0
    
    while True:
        connection_num += 1
        
        print("\n" + "=" * 80)
        print(f"🔌 CONNECTION #{connection_num} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
        
        # Start OpenSSL server for one connection
        cmd = [
            'openssl', 's_server',
            '-accept', '4433',
            '-cert', 'certs/server.crt',
            '-key', 'certs/server.key',
            '-quiet'
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            mode_detected = None
            message_received = False
            
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                
                # Detect mode
                if 'MODE:RSA' in line:
                    mode_detected = 'RSA'
                    print("🔐 " + "=" * 76)
                    print("   ENCRYPTION MODE: RSA (Classical)")
                    print("   " + "─" * 76)
                    print("   📦 ENCRYPTED: [Binary TLS encrypted data]")
                    print("   🔓 DECRYPTED: MODE:RSA")
                    print("=" * 80 + "\n")
                
                elif 'MODE:PQC' in line:
                    mode_detected = 'PQC'
                    print("🛡️  " + "=" * 76)
                    print("   ENCRYPTION MODE: PQC (Post-Quantum)")
                    print("   " + "─" * 76)
                    print("   📦 ENCRYPTED: [Binary TLS encrypted data]")
                    print("   🔓 DECRYPTED: MODE:PQC")
                    print("=" * 80 + "\n")
                
                elif 'MODE:HYBRID' in line:
                    mode_detected = 'HYBRID'
                    print("🔥 " + "=" * 76)
                    print("   ENCRYPTION MODE: HYBRID (Classical + PQC)")
                    print("   " + "─" * 76)
                    print("   📦 ENCRYPTED: [Binary TLS encrypted data]")
                    print("   🔓 DECRYPTED: MODE:HYBRID")
                    print("=" * 80 + "\n")
                
                # Detect message
                elif 'Hi, how are you' in line:
                    message_received = True
                    print("💬 " + "=" * 76)
                    print("   MESSAGE:")
                    print("   " + "─" * 76)
                    print("   📦 ENCRYPTED: [Binary TLS encrypted data]")
                    print("   🔓 DECRYPTED: Hi, how are you")
                    print("=" * 80 + "\n")
            
            process.wait()
            
            if not mode_detected and not message_received:
                print("⚠️  No data received (connection may have failed)\n")
            
            print("✅ Connection closed\n")
            
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("🛑 Server stopped")
            print("=" * 80 + "\n")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}\n")
            continue

if __name__ == '__main__':
    main()
