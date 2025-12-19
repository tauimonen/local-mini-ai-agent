#!/bin/bash

echo "Starting AI Agent container..."
echo "Ollama host: ${OLLAMA_HOST:-http://ollama:11434}"

# Wait until Ollama server is ready
MAX_ATTEMPTS=30
attempt=1
while ! curl -sf "${OLLAMA_HOST}/api/tags" > /dev/null 2>&1; do
    echo "Waiting for Ollama... (attempt $attempt/$MAX_ATTEMPTS)"
    attempt=$((attempt + 1))
    if [ $attempt -gt $MAX_ATTEMPTS ]; then
        echo "Warning: Ollama not responding. Container will stay alive for debugging."
        tail -f /dev/null
    fi
    sleep 2
done
echo "Ollama is ready!"

# Copy project root example.txt to /app/data if it doesn't exist
if [ ! -f /app/data/example.txt ]; then
    echo "Copying example.txt to data folder..."
    cp /app/example.txt /app/data/example.txt
fi

echo ""
echo "Starting AI Agent..."
echo "================================"
echo ""

# Run the agent and keep container alive if it crashes
python -u main.py || {
    echo "Agent crashed! Keeping container alive for debugging..."
    tail -f /dev/null
}
