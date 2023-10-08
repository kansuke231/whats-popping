# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Define the env vars for AWS credentials
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Set environment variables
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV production

# Install system dependencies
RUN apt-get update -y && apt-get install -y gcc

# Install Python dependencies
COPY ./backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application
COPY ./backend /app
ENV WEB_APP_DIR=/app
WORKDIR /app

# Copy React frontend's build
COPY ./frontend/build /app/frontend/build

# Specify port number that needs to be exposed
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
