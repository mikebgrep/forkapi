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

# Install dependencies

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers – this works on Ubuntu 24.04, Raspberry Pi OS, Debian 12/13, etc.
RUN playwright install --with-deps firefox || \
    playwright install firefox --force

RUN python -c "from playwright.sync_api import sync_playwright; \
    with sync_playwright() as p: p.firefox.launch(headless=True).close(); print('Firefox OK')"
