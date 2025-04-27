# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install nginx and supervisor
RUN apt-get update && \
    apt-get install -y nginx supervisor && \
    apt-get clean

# Copy backend code
COPY backend/ /app/backend/
COPY database/ /app/database/
COPY models/ /app/models/
COPY routers/ /app/routers/
COPY auth.py /app/auth.py
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend files into nginx public directory
COPY frontend/ /usr/share/nginx/html/

# Copy custom nginx.conf to configure nginx (optional, if needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create supervisord config to run multiple processes
RUN mkdir -p /etc/supervisor/conf.d

RUN echo '[supervisord]\nnodaemon=true\n\n\
[program:uvicorn]\ncommand=uvicorn main:app --host 0.0.0.0 --port 8000\n\
directory=/app\n\
autostart=true\nautorestart=true\n\
stdout_logfile=/dev/stdout\n\
stderr_logfile=/dev/stderr\n\n\
[program:nginx]\ncommand=/usr/sbin/nginx -g "daemon off;"\n\
autostart=true\nautorestart=true\n\
stdout_logfile=/dev/stdout\n\
stderr_logfile=/dev/stderr\n' > /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80
EXPOSE 8000

# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
