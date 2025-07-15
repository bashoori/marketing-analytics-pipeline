# Base image with Python
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && apt-get clean

# Set working directory
WORKDIR /workspace

# Optional: copy files into container
# COPY . /workspace