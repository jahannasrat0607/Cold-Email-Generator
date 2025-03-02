# Use Python 3.10 as the base image
FROM python:3.10-slim

# Install system dependencies (e.g., SQLite3)
RUN apt-get update && apt-get install -y sqlite3

# Set the working directory
WORKDIR /code

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Expose ports for Streamlit and ChromaDB
EXPOSE 8501 8000

# Start ChromaDB server and Streamlit app using the shell script
CMD ["./start.sh"]
