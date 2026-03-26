# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs show immediately
ENV PYTHONUNBUFFERED=1

# Install system dependencies (important for faiss + bcrypt)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Default command (runs full pipeline)
CMD ["python", "-m", "pipeline.pipeline"]