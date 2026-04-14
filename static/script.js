// Post-Quantum Cryptography TLS Dashboard - Client-side JavaScript

// Check server status on load
window.addEventListener('load', () => {
    checkServer();
    setInterval(checkServer, 30000); // Check every 30 seconds
});

// Run TLS test
async function runTest(mode) {
    const terminal = document.getElementById('terminal');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const connectionStatus = document.getElementById('connectionStatus');
    const lastMode = document.getElementById('lastMode');
    const timestamp = document.getElementById('timestamp');
    
    // Show loading
    loadingOverlay.style.display = 'flex';
    connectionStatus.textContent = 'Connecting...';
    connectionStatus.className = 'status-value status-idle';
    
    // Clear terminal
    terminal.innerHTML = '';
    
    // Add header
    const header = document.createElement('div');
    header.className = 'terminal-output';
    header.innerHTML = `
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Starting ${mode.toUpperCase()} TLS Connection Test                                          ║
║  Target: ${document.getElementById('serverHost').value}:${document.getElementById('serverPort').value}                                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

`;
    terminal.appendChild(header);
    
    try {
        // Make API call
        const response = await fetch(`/${mode}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        // Hide loading
        loadingOverlay.style.display = 'none';
        
        // Update status
        lastMode.textContent = data.mode;
        timestamp.textContent = data.timestamp;
        
        if (data.status === 'success') {
            connectionStatus.textContent = 'Success';
            connectionStatus.className = 'status-value status-success';
        } else {
            connectionStatus.textContent = 'Failed';
            connectionStatus.className = 'status-value status-failed';
        }
        
        // Display output
        const output = document.createElement('div');
        output.className = data.status === 'success' ? 'terminal-output terminal-success' : 'terminal-output terminal-error';
        output.textContent = data.output;
        terminal.appendChild(output);
        
        // Auto-scroll to bottom
        terminal.scrollTop = terminal.scrollHeight;
        
        // Parse and highlight key information
        highlightKeyInfo(terminal, data.output);
        
    } catch (error) {
        loadingOverlay.style.display = 'none';
        connectionStatus.textContent = 'Error';
        connectionStatus.className = 'status-value status-failed';
        
        const errorOutput = document.createElement('div');
        errorOutput.className = 'terminal-output terminal-error';
        errorOutput.textContent = `\n❌ ERROR: ${error.message}\n\nPlease check:\n  • Flask server is running\n  • Network connectivity\n  • Server configuration\n`;
        terminal.appendChild(errorOutput);
    }
}

// Highlight key information in terminal output
function highlightKeyInfo(terminal, output) {
    // Add summary section
    const summary = document.createElement('div');
    summary.className = 'terminal-output';
    summary.style.marginTop = '20px';
    summary.style.borderTop = '1px solid #00ff88';
    summary.style.paddingTop = '10px';
    
    let summaryText = '\n\n📊 KEY INFORMATION EXTRACTED:\n';
    summaryText += '─'.repeat(80) + '\n';
    
    // Extract cipher suite
    const cipherMatch = output.match(/Cipher\s*:\s*([^\n]+)/);
    if (cipherMatch) {
        summaryText += `🔐 Cipher Suite: ${cipherMatch[1]}\n`;
    }
    
    // Extract protocol version
    const protocolMatch = output.match(/Protocol\s*:\s*([^\n]+)/);
    if (protocolMatch) {
        summaryText += `📡 Protocol: ${protocolMatch[1]}\n`;
    }
    
    // Extract key exchange
    const keyExchangeMatch = output.match(/Server Temp Key:\s*([^\n]+)/);
    if (keyExchangeMatch) {
        summaryText += `🔑 Key Exchange: ${keyExchangeMatch[1]}\n`;
    }
    
    // Extract certificate info
    const certMatch = output.match(/subject=([^\n]+)/);
    if (certMatch) {
        summaryText += `📜 Certificate Subject: ${certMatch[1]}\n`;
    }
    
    // Check for PQC indicators
    if (output.includes('MLKEM') || output.includes('Kyber')) {
        summaryText += `✅ Post-Quantum Cryptography: DETECTED\n`;
    }
    
    if (output.includes('X25519')) {
        summaryText += `✅ Hybrid Mode: DETECTED (Classical + PQC)\n`;
    }
    
    // Verify result
    if (output.includes('Verify return code: 0')) {
        summaryText += `✅ Certificate Verification: SUCCESS\n`;
    } else if (output.includes('Verify return code:')) {
        const verifyMatch = output.match(/Verify return code:\s*(\d+)\s*\(([^)]+)\)/);
        if (verifyMatch) {
            summaryText += `⚠️  Certificate Verification: ${verifyMatch[2]}\n`;
        }
    }
    
    summaryText += '─'.repeat(80) + '\n';
    
    summary.textContent = summaryText;
    terminal.appendChild(summary);
}

// Check server status
async function checkServer() {
    const statusIndicator = document.getElementById('serverStatus');
    const statusText = document.getElementById('serverStatusText');
    
    try {
        const response = await fetch('/check_server');
        const data = await response.json();
        
        if (data.status === 'online') {
            statusIndicator.className = 'status-indicator status-online';
            statusText.textContent = 'Online';
        } else if (data.status === 'offline') {
            statusIndicator.className = 'status-indicator status-offline';
            statusText.textContent = 'Offline';
        } else {
            statusIndicator.className = 'status-indicator status-unknown';
            statusText.textContent = 'Unknown';
        }
    } catch (error) {
        statusIndicator.className = 'status-indicator status-unknown';
        statusText.textContent = 'Error';
    }
}

// Update configuration
async function updateConfig() {
    const host = document.getElementById('serverHost').value;
    const port = document.getElementById('serverPort').value;
    
    try {
        const response = await fetch('/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ host, port })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            alert(`✅ Configuration updated!\nServer: ${data.host}:${data.port}`);
            checkServer();
        }
    } catch (error) {
        alert(`❌ Failed to update configuration: ${error.message}`);
    }
}

// Clear terminal output
function clearOutput() {
    const terminal = document.getElementById('terminal');
    terminal.innerHTML = `
        <div class="terminal-welcome">
            <pre>
╔═══════════════════════════════════════════════════════════════════════════════╗
║                  POST-QUANTUM CRYPTOGRAPHY TLS ANALYZER                       ║
║                                                                               ║
║  This dashboard demonstrates real-world TLS connections using:               ║
║    • RSA (Classical) - Traditional public key cryptography                   ║
║    • MLKEM768 (PQC) - NIST-standardized post-quantum algorithm               ║
║    • Hybrid Mode - Combined classical + quantum-resistant security           ║
║                                                                               ║
║  Select a mode above to begin testing...                                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
            </pre>
        </div>
    `;
    
    // Reset status
    document.getElementById('connectionStatus').textContent = 'Idle';
    document.getElementById('connectionStatus').className = 'status-value status-idle';
    document.getElementById('lastMode').textContent = 'None';
    document.getElementById('timestamp').textContent = '-';
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        clearOutput();
    }
    
    // Ctrl/Cmd + 1/2/3 for quick test
    if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '3') {
        e.preventDefault();
        const modes = ['rsa', 'pqc', 'hybrid'];
        runTest(modes[parseInt(e.key) - 1]);
    }
});
