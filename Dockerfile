FROM python:3.11-slim

WORKDIR /app

# Asenna curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD
# Copy pyproject.toml and install dependencies
COPY pyproject.toml ./
# If you have poetry.lock, copy it too (optional but recommended)
# COPY poetry.lock ./

# Install dependencies using pip (reads pyproject.toml)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .
=======
# Kopioi ja asenna Python-dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
>>>>>>> 2f649a0 (Make agent container stable in Docker/WSL and handle example.txt correctly)

# Kopioi sovelluskoodi
COPY agent.py llm.py main.py ./ 
COPY tools/ ./tools/

# Luo data-hakemisto
RUN mkdir -p /app/data

# Kopioi entrypoint
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# ENTRYPOINT pitää konttisi käynnissä
ENTRYPOINT ["/app/docker-entrypoint.sh"]
