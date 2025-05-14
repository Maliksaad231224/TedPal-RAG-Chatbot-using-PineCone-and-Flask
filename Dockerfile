FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set cache directory for models (accessible to all users)
ENV TRANSFORMERS_CACHE=/app/models
RUN mkdir -p /app/models && chmod 777 /app/models

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8080
CMD ["python", "app.py"]