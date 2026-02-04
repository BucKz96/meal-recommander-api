# ==========================================
# 🐳 Dockerfile API - Multi-Stage Build
# ==========================================
# 
# Multi-stage pour:
# 1. Image plus petite (supprime build dependencies)
# 2. Meilleure sécurité (pas de compilateurs en prod)
# 3. Build plus rapide avec cache layers

# Stage 1: Builder (compilation et installation)
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip wheel

# Copy project files required for installation
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install package with dependencies (non editable for smaller image)
RUN pip install --no-cache-dir .

# Stage 2: Production (runtime only)
FROM python:3.12-slim AS production

# Security: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY data/ ./data/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Health check - verifies API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run with Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
