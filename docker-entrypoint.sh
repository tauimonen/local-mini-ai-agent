#!/bin/bash
set -e

echo "Starting AI Agent container..."
echo "Ollama host: ${OLLAMA_HOST}"

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until curl -sf "${OLLAMA_HOST}/api/tags" > /dev/null 2>&1; do
    echo "   Waiting for Ollama..."
    sleep 2
done
echo "✓ Ollama is ready!"

# Check if model is already downloaded
echo "Checking for llama3.2:3b model..."
if curl -sf "${OLLAMA_HOST}/api/tags" | grep -q "llama3.2:3b"; then
    echo "✓ Model already downloaded"
else
    echo "Downloading llama3.2:3b model (this may take a few minutes)..."
    curl -X POST "${OLLAMA_HOST}/api/pull" \
        -H "Content-Type: application/json" \
        -d '{"name": "llama3.2:3b"}' \
        --no-buffer
    echo "✓ Model downloaded successfully"
fi

# Create example file if it doesn't exist
if [ ! -f /app/data/example.txt ]; then
    echo "Creating example.txt..."
    echo "Hello from Docker! This is a test file for the AI agent." > /app/data/example.txt
fi

echo ""
echo "Starting AI Agent..."
echo "================================"
echo ""

# Run the agent
exec python main.py