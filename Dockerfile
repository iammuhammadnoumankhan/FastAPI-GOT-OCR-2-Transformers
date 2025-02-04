# File: Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary Python files
COPY globe.py render.py main.py ./

# Copy the entire render_tools/ directory
COPY render_tools/ ./render_tools/

# Download the model during the build process
RUN python -c "from transformers import AutoModelForImageTextToText, AutoProcessor; \
AutoProcessor.from_pretrained('stepfun-ai/GOT-OCR-2.0-hf'); \
AutoModelForImageTextToText.from_pretrained('stepfun-ai/GOT-OCR-2.0-hf', low_cpu_mem_usage=True)"

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]