#!/bin/bash
set -e

echo "Starting AI Agent container..."
OLLAMA_HOST="${OLLAMA_HOST:-http://ollama:11434}"
echo "Ollama host: $OLLAMA_HOST"

# Wait until Ollama server is ready
MAX_ATTEMPTS=30
attempt=1
while ! curl -sf "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; do
    echo "Waiting for Ollama ($attempt/$MAX_ATTEMPTS)..."
    attempt=$((attempt+1))
    if [ $attempt -gt $MAX_ATTEMPTS ]; then
        echo "Ollama not responding. Entering debug mode."
        tail -f /dev/null
    fi
    sleep 2
done
echo "Ollama is ready!"

# Keep container alive for debugging
echo "Container is now alive. Exec into it to debug."
tail -f /dev/null
