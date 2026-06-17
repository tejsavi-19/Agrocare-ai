# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for graphics and compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire workspace into the container
COPY . .

# Install CPU-specific PyTorch wheels to minimize container size and load models quickly
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install backend requirements
RUN pip install --no-cache-dir -r AgroCareAI/backend/requirements.txt

# Set Python Path to include workspace root and cat directory
ENV PYTHONPATH="/app:/app/cat:${PYTHONPATH}"

# Expose the port (Hugging Face Spaces exposes 7860 by default)
EXPOSE 7860

# Run Flask server
CMD ["python", "AgroCareAI/backend/app.py"]
