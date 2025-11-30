# Backend Dockerfile for Disease Prediction API
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip (more reliable in Docker)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# Copy dependency files and application code (needed for uv sync to install the project)
COPY pyproject.toml uv.lock ./
COPY app/ ./app/

# Install Python dependencies using uv sync
RUN uv sync --frozen --no-dev

# Copy remaining application files
COPY ml/ ./ml/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY scripts/ ./scripts/


# Convert line endings (CRLF to LF) and make entrypoint script executable
RUN sed -i 's/\r$//' scripts/docker-entrypoint.sh && \
    chmod +x scripts/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]

# Default command
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
