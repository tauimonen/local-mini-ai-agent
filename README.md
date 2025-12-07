[![Project Status: Work in Progress](https://img.shields.io/badge/Project%20Status-Work%20in%20Progress-orange.svg)](https://img.shields.io/badge/Project%20Status-Work%20in%20Progress-orange.svg)

# Local AI Agent

This project is a lightweight ReAct-style AI agent that uses a fully local LLM through Ollama (e.g., llama3.2:3b).

### The agent supports:
- Reasoning
- Tool usage
- Reading and writing files
- Evaluating mathematical expressions

Everything runs offline, as long as Ollama and the selected model are installed locally. Docker support included for easy deployment.

## Features
- ReAct loop (reason → act → observe → repeat)
- LLM communication via Ollama local REST API
- Safe mathematical evaluator (via Python AST)
- File read/write operations restricted to the project directory
- Easily extensible with new tools
- Docker Compose setup for one-command deployment

--
# AI Agent Quick Start Guide

Get your local AI agent running in 5 minutes with Docker!

## Prerequisites

- **Docker Desktop** installed ([download here](https://www.docker.com/products/docker-desktop))
- **4GB free disk space** (for Ollama model)
- **8GB+ RAM** recommended

## Installation

### Step 1: Clone or Create Project

```bash
# Create project directory
mkdir simple_agent
cd simple_agent

# Create subdirectories
mkdir tools data
```

### Step 2: Add Project Files

Copy all the following files to your project directory:

```
simple_agent/
├── docker-compose.yml
├── Dockerfile
├── docker-entrypoint.sh
├── .dockerignore
├── requirements.txt
├── main.py
├── agent.py
├── llm.py
└── tools/
    ├── __init__.py
    ├── file_tool.py
    └── calculator.py
```

### Step 3: Make Entrypoint Executable

```bash
chmod +x docker-entrypoint.sh
```

### Step 4: Start Everything

```bash
# Start Ollama and Agent containers
docker-compose up -d
```

**First run will:**
- Download Ollama Docker image (~1GB)
- Download llama3.2:3b model (~2GB)
- Build the agent container
- **This takes 5-10 minutes** depending on your internet connection

### Step 5: Watch the Progress

```bash
# Follow the logs to see what's happening
docker-compose logs -f agent
```

You should see:
```
Connected to Ollama at http://ollama:11434 Downloading llama3.2:3b model...
Model downloaded successfully
Starting AI Agent...
```

## Usage

### Run Example Queries

```bash
# Run the built-in examples
docker-compose exec agent python main.py
```

### Run Custom Query

```bash
# One-off calculation
docker-compose exec agent python -c "
from agent import Agent
agent = Agent()
print(agent.run('What is 123 multiplied by 456?'))
"
```

### Work with Files

```bash
# Create a test file on your host
echo "Hello from Docker! This is test data." > data/myfile.txt

# Ask the agent to read it
docker-compose exec agent python -c "
from agent import Agent
agent = Agent()
print(agent.run('Read the file myfile.txt'))
"

# Ask agent to process and save
docker-compose exec agent python -c "
from agent import Agent
agent = Agent()
print(agent.run('Calculate 50 * 30 and save the result to calculation.txt'))
"

# Check the result
cat data/calculation.txt
```

### Interactive Python Shell

```bash
# Open Python shell in the agent container
docker-compose exec agent python

# Then run:
from agent import Agent
agent = Agent()
result = agent.run("Your query here")
print(result)
```

## Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f agent

# Restart after code changes
docker-compose restart agent

# Check service status
docker-compose ps

# Open bash shell in agent container
docker-compose exec agent bash

# Stop and remove everything (including model data)
docker-compose down -v
```

## Verify Installation

```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Should return JSON with available models
```

## Troubleshooting

### "Cannot connect to Docker daemon"

```bash
# Make sure Docker Desktop is running
# On Mac: Check menu bar for Docker icon
# On Linux: sudo systemctl start docker
```

### "Port 11434 already in use"

```bash
# Stop local Ollama if running
pkill ollama

# Or change the port in docker-compose.yml:
# ports:
#   - "11435:11434"  # Use different external port
```

### "Out of memory" errors

```bash
# Option 1: Use smaller model
# In docker-entrypoint.sh, change to:
# "llama3.2:1b"  # Smaller, faster model

# Option 2: Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory → 8GB+
```

### Model download is slow

```bash
# Download model manually in background
docker-compose exec ollama ollama pull llama3.2:3b

# Then restart agent
docker-compose restart agent
```

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Ollama     │    │    Agent     │  │
│  │  Container   │◄───│  Container   │  │
│  │              │    │              │  │
│  │ llama3.2:3b  │    │  Python 3.11 │  │
│  │ Port: 11434  │    │  ReAct Loop  │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │          │
│    [Model Data]         [./data/]      │
│     (Volume)            (Mounted)      │
└─────────────────────────────────────────┘
          │                    │
     Persisted          Your local files
     between runs       accessible from host
```

## What's Running?

- **Ollama Container**: Serves the LLM on internal port 11434
- **Agent Container**: Runs your Python agent, communicates with Ollama
- **Shared Volume**: `./data/` directory is accessible from both host and container

## Next Steps

- **Modify queries**: Edit `main.py` to add your own example queries
- **Add tools**: Create new tools in `tools/` directory
- **Try different models**: Change model in `docker-entrypoint.sh`
- **Build applications**: Use the agent as a foundation for your projects

## Development Workflow

1. Edit code on your host machine (VS Code, etc.)
2. Restart agent: `docker-compose restart agent`
3. Test: `docker-compose exec agent python main.py`
4. View logs: `docker-compose logs -f agent`

## GPU Acceleration (Optional)

If you have an NVIDIA GPU:

1. Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
2. Uncomment GPU section in `docker-compose.yml`
3. Restart: `docker-compose down && docker-compose up -d`

## Clean Up

```bash
# Stop and remove containers (keeps model data)
docker-compose down

# Remove everything including downloaded models
docker-compose down -v

# Remove Docker images
docker-compose down --rmi all
```

## Support

- **Ollama Documentation**: https://ollama.ai
- **Docker Documentation**: https://docs.docker.com
- **Check logs**: `docker-compose logs agent`

## Success Indicators

You'll know everything is working when you see:

```
Connected to Ollama at http://ollama:11434
Model already downloaded
 Starting AI Agent...
=== Simple Local AI Agent ===

Query 1: What is 25 multiplied by 47?
Thought: I need to calculate this
Action: calculate(25*47)
Observation: Result: 1175
Final Answer: The result is 1175
```
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

