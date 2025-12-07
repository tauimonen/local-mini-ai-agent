[![Project Status: Work in Progress](https://img.shields.io/badge/Project%20Status-Work%20in%20Progress-orange.svg)](https://img.shields.io/badge/Project%20Status-Work%20in%20Progress-orange.svg)

# Local AI Agent

This project is a lightweight ReAct-style AI agent that uses a fully local LLM through Ollama (e.g., llama3.2:3b).

### The agent supports:
- Reasoning
- Tool usage
- Reading and writing files
- Evaluating mathematical expressions

Everything runs offline, as long as Ollama and the selected model are installed locally.

## Features
- ReAct loop (reason → act → observe → repeat)
- LLM communication via Ollama local REST API
- Safe mathematical evaluator (via Python AST)
- File read/write operations restricted to the project directory
- Easily extensible with new tools

--
## Running Ollama on Windows and Connecting from WSL
This guide assumes Ollama is installed on Windows and you want to run your Python program in WSL (Ubuntu) while connecting to Ollama.

### 1. Start Ollama 
```powershell
.\ollama.exe serve
```

### 2. Allow Ollama port 11434 through Windows Firewall
Open PowerShell as Administrator and run:
```powershell
netsh advfirewall firewall add rule name="Ollama 11434" dir=in action=allow protocol=TCP localport=11434
```

### 3. Forward all TCP traffic arriving at any interface on Windows port 11434 to 192.168.101.100:11434, allowing access to a service running on that IP through the Windows machine.
```powershell
netsh interface portproxy add v4tov4 listenport=11434 listenaddress=0.0.0.0 connectport=11434 connectaddress=192.168.101.100
```

### 4. Test Ollama from Windows
```powershell
curl http://127.0.0.1:11434/api/tags
```
You should get a response like:
```powershell
{"models":[]}
```
Or a list of available models.

### 5. Test Ollama from WSL
Open your WSL terminal and use the Windows host IP instead of localhost:
```bash
curl http://<WINDOWS_IP>:11434/api/tags
```
```bash
curl http://192.168.101.100:11434/api/tags
```
Expected output:
```json
{"models":[]}
```

### 6. Update Python code in WSL
Modify your Python code to use the Windows host IP instead of localhost:
```python
# Example in llm.py
self.base_url = "http://xxx.xxx.xxx.xxx:11434"

