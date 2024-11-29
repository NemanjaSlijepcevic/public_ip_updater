# Use the official Python image from Docker Hub
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY *py .

# Default command
CMD ["python", "main.py"]
