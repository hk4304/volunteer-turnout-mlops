# Use the latest stable Python 3.12 slim image for Ubuntu compatibility
FROM python:3.12-slim

# Set environment variables for performance & reliability
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first for caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY metrics/ ./metrics/
COPY params.yaml .

# Build arguments for version tracking
ARG GIT_COMMIT=unknown
ARG BUILD_TIME=unknown
ARG MODEL_VERSION=unknown

# Set as environment variables so app can access them
ENV GIT_COMMIT=${GIT_COMMIT} \
    BUILD_TIME=${BUILD_TIME} \
    MODEL_VERSION=${MODEL_VERSION}

# Create version info file
RUN echo "Git Commit: ${GIT_COMMIT}" > /app/version.txt && \
    echo "Build Time: ${BUILD_TIME}" >> /app/version.txt && \
    echo "Model Version: ${MODEL_VERSION}" >> /app/version.txt

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Add a health check endpoint (requires /health in app)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fs http://localhost:5000/health || exit 1

# Run with Gunicorn for production (optimized settings)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "2", "--threads", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", "--error-logfile", "-", \
     "app.app:app"]
