# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY main.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run your operator
CMD ["python", "main.py"]
