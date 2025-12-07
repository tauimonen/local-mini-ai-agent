FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and install dependencies
COPY pyproject.toml ./
# If you have poetry.lock, copy it too (optional but recommended)
# COPY poetry.lock ./

# Install dependencies using pip (reads pyproject.toml)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application code
COPY agent.py llm.py main.py ./
COPY tools/ ./tools/

# Create data directory for file operations
RUN mkdir -p /app/data

# Create a startup script that pulls the model and runs the agent
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]