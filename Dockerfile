FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x run_migrations.sh run.sh run_celery.sh

# Expose port
EXPOSE 5000

# Run the application
CMD ["./run.sh"] 