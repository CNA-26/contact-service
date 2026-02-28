FROM python:3.11-slim
WORKDIR /app

# Install dependencies first (for caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

# Set Python path for imports
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]