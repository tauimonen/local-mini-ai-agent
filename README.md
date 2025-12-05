# Simple Local AI Agent

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
