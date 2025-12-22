FROM ollama/ollama:0.13.1

WORKDIR /app

# Install Python + venv + pip
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

# Copy app code
COPY agent.py llm.py main.py ./
COPY tools/ ./tools/

# Create data directory
RUN mkdir -p /app/data

# Copy entrypoint
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Start agent
ENTRYPOINT ["/app/docker-entrypoint.sh"]
