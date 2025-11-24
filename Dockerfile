# Production Dockerfile for Upgrad OSP
FROM python:3.13-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    cp /root/.local/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv
ENV PATH="/usr/local/bin:$PATH"

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/bash -m appuser

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install dependencies
RUN chown -R appuser:appuser /app && \
    su appuser -c "uv sync --frozen --no-dev"

# Copy application code
COPY --chown=appuser:appuser . .

# Create required directories with explicit permissions
RUN mkdir -p frontend/static frontend/templates uploads && \
    chmod 755 uploads && \
    chown appuser:appuser frontend/static frontend/templates uploads

# Copy and setup entrypoint script
COPY --chown=root:root docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use entrypoint to fix permissions at runtime
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Run application with uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
