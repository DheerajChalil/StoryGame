# Use a lightweight Python 3.9.17 base image
FROM python:3.9.17-slim

# Set working directory inside the container
WORKDIR /StoryGame

# Install system dependencies for common Python packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app code
COPY main.py .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
