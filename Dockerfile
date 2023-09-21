# Use the official Python image as the base image
FROM python:3.10-slim AS builder

# Set environment variables for WeasyPrint dependencies on Linux
ENV WKHTMLTOPDF_DEB https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb

# Set the working directory
WORKDIR /app

# Copy your requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copy your Python script to the image
COPY main.py .

# Run your Python script
CMD ["python", "main.py"]
