FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user for Hugging Face (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Copy and install requirements
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY --chown=user . .

# Grant execution permission to the start script
RUN chmod +x start.sh

# Hugging Face Spaces expects port 7860
EXPOSE 7860

# Launch both services
# Remove the old CMD lines and use only this one:
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 7860 --server.address 0.0.0.0"]