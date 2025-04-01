# Stage 1: Builder (install dependencies)
FROM python:3.11-slim AS builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (lean image)
FROM python:3.11-slim
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x run.sh run_celery.sh run_migrations.sh

EXPOSE 5000
CMD ["./run.sh"]
