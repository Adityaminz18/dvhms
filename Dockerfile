# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install nginx and supervisor
RUN apt-get update && \
    apt-get install -y nginx supervisor && \
    apt-get clean

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Prepare nginx frontend
RUN rm -rf /usr/share/nginx/html/*
RUN cp -r /app/frontend/* /usr/share/nginx/html/

# ✅ Copy your custom nginx.conf to nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Supervisor to run both uvicorn + nginx
RUN mkdir -p /etc/supervisor/conf.d

RUN echo '[supervisord]\n\
nodaemon=true\n\n\
[program:uvicorn]\n\
command=uvicorn main:app --host 0.0.0.0 --port 8000\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stderr_logfile=/dev/stderr\n\n\
[program:nginx]\n\
command=/usr/sbin/nginx -g "daemon off;"\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stderr_logfile=/dev/stderr\n' > /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80
EXPOSE 8000

# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
