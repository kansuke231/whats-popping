# Start from a base Python image
FROM python:3.9-slim

# Define the env vars for AWS credentials
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Set a working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Scrapy project into the container
COPY . .

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh
CMD ["/startup.sh"]

