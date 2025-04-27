# Final Correct Dockerfile for Hospital Management System

# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install nginx and supervisor
RUN apt-get update &&     apt-get install -y nginx supervisor &&     apt-get clean

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove default nginx web content
RUN rm -rf /usr/share/nginx/html/*

# Copy frontend files to nginx web root
RUN cp -r /app/frontend/* /usr/share/nginx/html/

# Copy your custom nginx.conf to nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose only port 80
EXPOSE 80

# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
