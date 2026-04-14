#!/usr/bin/env python3
"""
Post-Quantum Cryptography TLS Dashboard
Real-world OpenSSL/OQS integration for quantum-safe communication analysis
Enhanced with advanced metrics and visualization
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import time
import os
import signal
import re

app = Flask(__name__)

# Global variables for process management
current_process = None
process_lock = threading.Lock()

# Server configuration
SERVER_HOST = "192.168.0.104"
SERVER_PORT = "4433"

# Store test results for comparison
test_results = {
    'rsa': None,
    'pqc': None,
    'hybrid': None
}


def parse_tls_details(output):
    """Extract TLS handshake details from OpenSSL output"""
    details = {
        'tls_version': 'Unknown',
        'cipher': 'Unknown',
        'key_exchange': 'Unknown'
    }
    
    # Extract Protocol/TLS Version
    protocol_match = re.search(r'Protocol\s*:\s*(\S+)', output)
    if protocol_match:
        details['tls_version'] = protocol_match.group(1)
    
    # Extract Cipher Suite
    cipher_match = re.search(r'Cipher\s*:\s*([^\n]+)', output)
    if cipher_match:
        details['cipher'] = cipher_match.group(1).strip()
    
    # Extract Key Exchange (Server Temp Key)
    key_match = re.search(r'Server Temp Key:\s*([^\n]+)', output)
    if key_match:
        details['key_exchange'] = key_match.group(1).strip()
    
    return details


def get_security_level(mode):
    """Determine security level based on mode"""
    security_levels = {
        'rsa': {'level': 'Medium', 'icon': '⚠️', 'color': '#ffa502'},
        'pqc': {'level': 'High', 'icon': '✅', 'color': '#00ff88'},
        'hybrid': {'level': 'Very High', 'icon': '🔥', 'color': '#00d4ff'}
    }
    return security_levels.get(mode, {'level': 'Unknown', 'icon': '❓', 'color': '#a1a1aa'})


def kill_process_tree(pid):
    """Kill process and all its children"""
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    except:
        pass


@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index_enhanced.html')


@app.route('/rsa', methods=['POST'])
def run_rsa():
    """Execute RSA-based TLS connection with enhanced metrics"""
    global current_process, test_results
    
    with process_lock:
        # Kill any existing process
        if current_process and current_process.poll() is None:
            kill_process_tree(current_process.pid)
        
        try:
            # Start timing
            start_time = time.time()
            
            # OpenSSL command for RSA TLS
            cmd = [
                'openssl', 's_client',
                '-connect', f'{SERVER_HOST}:{SERVER_PORT}',
                '-showcerts',
                '-state'
            ]
            
            # Execute command
            current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )
            
            # Send mode identifier and message to server
            current_process.stdin.write("MODE:RSA\n")
            current_process.stdin.write("Hi, how are you\n")
            current_process.stdin.flush()
            
            # Wait a moment for message to be sent
            time.sleep(0.5)
            
            # Send quit command
            current_process.stdin.write("Q\n")
            current_process.stdin.flush()
            
            # Wait for output with timeout
            try:
                output, _ = current_process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                kill_process_tree(current_process.pid)
                output = "Connection timeout - server may not be running"
            
            # End timing
            end_time = time.time()
            execution_time = round(end_time - start_time, 3)
            
            # Calculate packet size
            packet_size = len(output.encode('utf-8'))
            
            # Parse TLS details
            tls_details = parse_tls_details(output)
            
            # Get security level
            security = get_security_level('rsa')
            
            # Parse output for key information
            status = "success" if "Cipher" in output else "failed"
            
            # Store result for comparison
            result = {
                'mode': 'RSA',
                'execution_time': execution_time,
                'packet_size': packet_size,
                'security_level': security['level'],
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange']
            }
            test_results['rsa'] = result
            
            return jsonify({
                'status': status,
                'output': output,
                'mode': 'RSA (Classical TLS)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': execution_time,
                'packet_size': packet_size,
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange'],
                'security_level': security['level'],
                'security_icon': security['icon'],
                'security_color': security['color']
            })
            
        except FileNotFoundError:
            return jsonify({
                'status': 'failed',
                'output': 'ERROR: OpenSSL not found. Please install OpenSSL first.\n\nInstallation:\n  Ubuntu/Debian: sudo apt install openssl\n  macOS: brew install openssl',
                'mode': 'RSA (Classical TLS)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': 0,
                'packet_size': 0
            })
        except Exception as e:
            return jsonify({
                'status': 'failed',
                'output': f'ERROR: {str(e)}',
                'execution_time': 0,
                'packet_size': 0,
                'mode': 'RSA (Classical TLS)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })


@app.route('/pqc', methods=['POST'])
def run_pqc():
    """Execute Post-Quantum (Kyber/MLKEM768) TLS connection with enhanced metrics"""
    global current_process, test_results
    
    with process_lock:
        # Kill any existing process
        if current_process and current_process.poll() is None:
            kill_process_tree(current_process.pid)
        
        try:
            # Start timing
            start_time = time.time()
            
            # OpenSSL command for PQC TLS (MLKEM768 = Kyber)
            cmd = [
                'openssl', 's_client',
                '-connect', f'{SERVER_HOST}:{SERVER_PORT}',
                '-groups', 'MLKEM768',
                '-showcerts',
                '-state'
            ]
            
            # Execute command
            current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )
            
            # Send mode identifier and message to server
            current_process.stdin.write("MODE:PQC\n")
            current_process.stdin.write("Hi, how are you\n")
            current_process.stdin.flush()
            
            # Wait a moment for message to be sent
            time.sleep(0.5)
            
            # Send quit command
            current_process.stdin.write("Q\n")
            current_process.stdin.flush()
            
            # Wait for output
            try:
                output, _ = current_process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                kill_process_tree(current_process.pid)
                output = "Connection timeout - server may not be running or PQC not supported"
            
            # End timing
            end_time = time.time()
            execution_time = round(end_time - start_time, 3)
            
            # Calculate packet size
            packet_size = len(output.encode('utf-8'))
            
            # Parse TLS details
            tls_details = parse_tls_details(output)
            
            # Get security level
            security = get_security_level('pqc')
            
            status = "success" if "Cipher" in output else "failed"
            
            # Store result for comparison
            result = {
                'mode': 'PQC',
                'execution_time': execution_time,
                'packet_size': packet_size,
                'security_level': security['level'],
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange']
            }
            test_results['pqc'] = result
            
            return jsonify({
                'status': status,
                'output': output,
                'mode': 'PQC (MLKEM768/Kyber)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': execution_time,
                'packet_size': packet_size,
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange'],
                'security_level': security['level'],
                'security_icon': security['icon'],
                'security_color': security['color']
            })
            
        except FileNotFoundError:
            return jsonify({
                'status': 'failed',
                'output': 'ERROR: OpenSSL with OQS support not found.\n\nYou need OQS-enabled OpenSSL for Post-Quantum Cryptography.\n\nInstallation:\n  See: https://github.com/open-quantum-safe/openssl\n  Or use the setup script: ./scripts/setup_oqs.sh',
                'mode': 'PQC (MLKEM768/Kyber)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': 0,
                'packet_size': 0
            })
        except Exception as e:
            return jsonify({
                'status': 'failed',
                'output': f'ERROR: {str(e)}',
                'execution_time': 0,
                'packet_size': 0,
                'mode': 'PQC (MLKEM768/Kyber)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })


@app.route('/hybrid', methods=['POST'])
def run_hybrid():
    """Execute Hybrid (X25519 + MLKEM768) TLS connection with enhanced metrics"""
    global current_process, test_results
    
    with process_lock:
        # Kill any existing process
        if current_process and current_process.poll() is None:
            kill_process_tree(current_process.pid)
        
        try:
            # Start timing
            start_time = time.time()
            
            # OpenSSL command for Hybrid TLS
            cmd = [
                'openssl', 's_client',
                '-connect', f'{SERVER_HOST}:{SERVER_PORT}',
                '-groups', 'X25519MLKEM768',
                '-showcerts',
                '-state'
            ]
            
            # Execute command
            current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )
            
            # Send mode identifier and message to server
            current_process.stdin.write("MODE:HYBRID\n")
            current_process.stdin.write("Hi, how are you\n")
            current_process.stdin.flush()
            
            # Wait a moment for message to be sent
            time.sleep(0.5)
            
            # Send quit command
            current_process.stdin.write("Q\n")
            current_process.stdin.flush()
            
            # Wait for output
            try:
                output, _ = current_process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                kill_process_tree(current_process.pid)
                output = "Connection timeout - server may not be running or hybrid mode not supported"
            
            # End timing
            end_time = time.time()
            execution_time = round(end_time - start_time, 3)
            
            # Calculate packet size
            packet_size = len(output.encode('utf-8'))
            
            # Parse TLS details
            tls_details = parse_tls_details(output)
            
            # Get security level
            security = get_security_level('hybrid')
            
            status = "success" if "Cipher" in output else "failed"
            
            # Store result for comparison
            result = {
                'mode': 'Hybrid',
                'execution_time': execution_time,
                'packet_size': packet_size,
                'security_level': security['level'],
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange']
            }
            test_results['hybrid'] = result
            
            return jsonify({
                'status': status,
                'output': output,
                'mode': 'Hybrid (X25519 + MLKEM768)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': execution_time,
                'packet_size': packet_size,
                'tls_version': tls_details['tls_version'],
                'cipher': tls_details['cipher'],
                'key_exchange': tls_details['key_exchange'],
                'security_level': security['level'],
                'security_icon': security['icon'],
                'security_color': security['color']
            })
            
        except FileNotFoundError:
            return jsonify({
                'status': 'failed',
                'output': 'ERROR: OpenSSL with OQS support not found.\n\nYou need OQS-enabled OpenSSL for Hybrid Cryptography.\n\nInstallation:\n  See: https://github.com/open-quantum-safe/openssl\n  Or use the setup script: ./scripts/setup_oqs.sh',
                'mode': 'Hybrid (X25519 + MLKEM768)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': 0,
                'packet_size': 0
            })
        except Exception as e:
            return jsonify({
                'status': 'failed',
                'output': f'ERROR: {str(e)}',
                'execution_time': 0,
                'packet_size': 0,
                'mode': 'Hybrid (X25519 + MLKEM768)',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })


@app.route('/comparison', methods=['GET'])
def get_comparison():
    """Get comparison data for all test results"""
    return jsonify({
        'results': test_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/check_server', methods=['GET'])
def check_server():
    """Check if TLS server is running using OpenSSL"""
    try:
        # Use openssl s_client with -brief flag for quick check
        cmd = [
            'openssl', 's_client',
            '-connect', f'{SERVER_HOST}:{SERVER_PORT}',
            '-brief'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            input='Q\n'
        )
        
        output = result.stdout + result.stderr
        
        # Check for successful connection indicators
        # Look for "Cipher" or "Protocol" which indicate successful TLS handshake
        if 'Cipher' in output or 'Protocol' in output:
            # Self-signed certificate warnings (verify return code 18 or 19) are OK
            # These should NOT be treated as failures
            return jsonify({
                'status': 'success',
                'message': f'Server {SERVER_HOST}:{SERVER_PORT} is reachable'
            })
        else:
            # Connection failed
            return jsonify({
                'status': 'failed',
                'message': f'Server {SERVER_HOST}:{SERVER_PORT} is not responding or TLS handshake failed'
            })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'failed',
            'message': f'Connection timeout - server {SERVER_HOST}:{SERVER_PORT} not responding'
        })
    except FileNotFoundError:
        return jsonify({
            'status': 'failed',
            'message': 'OpenSSL not found. Please install OpenSSL.'
        })
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'message': f'Error checking server: {str(e)}'
        })


@app.route('/config', methods=['GET', 'POST'])
def config():
    """Get or update server configuration"""
    global SERVER_HOST, SERVER_PORT
    
    try:
        if request.method == 'POST':
            data = request.json
            if not data:
                return jsonify({'status': 'failed', 'message': 'No data provided'}), 400
            
            SERVER_HOST = data.get('host', SERVER_HOST)
            SERVER_PORT = data.get('port', SERVER_PORT)
            return jsonify({'status': 'success', 'host': SERVER_HOST, 'port': SERVER_PORT})
        else:
            return jsonify({'host': SERVER_HOST, 'port': SERVER_PORT})
    except Exception as e:
        return jsonify({'status': 'failed', 'message': f'Configuration error: {str(e)}'}), 500


if __name__ == '__main__':
    print("=" * 80)
    print("  POST-QUANTUM CRYPTOGRAPHY TLS DASHBOARD")
    print("  Real-world OpenSSL/OQS Integration")
    print("=" * 80)
    print(f"\n🌐 Starting Flask server...")
    print(f"📍 Dashboard: http://localhost:5000")
    print(f"🔒 Target TLS Server: {SERVER_HOST}:{SERVER_PORT}")
    print(f"\n⚠️  Make sure your TLS server is running before testing!")
    print(f"   Use: ./scripts/start_server.sh\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
