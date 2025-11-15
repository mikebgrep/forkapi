# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libpcre2-dev \
    curl \
    libpq-dev \
    python-dev-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /forkapi


# Copy the project
COPY /forkapi /forkapi
COPY ./requirements.txt /forkapi/requirements.txt
COPU /scripts/playwright-test.py /forkapi/playwright-test.py

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps firefox || \
    playwright install firefox --force

# Verify Firefox was installed correctly and can launch
RUN python playwright-test.py
