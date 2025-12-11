# ============================================
# Multi-Stage Dockerfile for ICS Multi-Agent Backend
# ============================================
# This Dockerfile builds both the React frontend and Python backend
# for the ICS Fault Detection System in an optimized container.
#
# Build: docker build -t ics-multi-agent .
# Run:   docker run -p 3000:80 -p 5000:5000 ics-multi-agent
# ============================================

# ============================================
# STAGE 1: Build React Frontend
# ============================================
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci --only=production --silent

# Copy frontend source code
COPY frontend/ ./

# Build production React bundle
RUN npm run build

# ============================================
# STAGE 2: Python Backend with ML Models
# ============================================
FROM python:3.9-slim AS backend

# Set working directory
WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend application code
COPY backend/ ./backend/

# Create necessary directories
RUN mkdir -p /app/backend/logs

# Copy pre-trained models and data
# These are required for the application to run
COPY backend/models/ ./backend/models/
COPY backend/data/ ./backend/data/

# ============================================
# STAGE 3: Final Production Image
# ============================================
FROM python:3.9-slim

WORKDIR /app

# Install nginx for serving frontend and system utilities
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend stage
COPY --from=backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin

# Copy backend application
COPY --from=backend /app/backend /app/backend

# Copy frontend build from frontend-builder stage
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html

# Configure nginx
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    # Frontend routes \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # Proxy API requests to backend \
    location /api { \
        proxy_pass http://localhost:5000; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    # Proxy WebSocket connections \
    location /socket.io { \
        proxy_pass http://localhost:5000; \
        proxy_http_version 1.1; \
        proxy_buffering off; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
    } \
}' > /etc/nginx/sites-available/default

# Configure supervisor to run both nginx and Python backend
RUN echo '[supervisord] \n\
nodaemon=true \n\
logfile=/var/log/supervisor/supervisord.log \n\
pidfile=/var/run/supervisord.pid \n\
\n\
[program:nginx] \n\
command=/usr/sbin/nginx -g "daemon off;" \n\
autostart=true \n\
autorestart=true \n\
stdout_logfile=/dev/stdout \n\
stdout_logfile_maxbytes=0 \n\
stderr_logfile=/dev/stderr \n\
stderr_logfile_maxbytes=0 \n\
\n\
[program:backend] \n\
command=python /app/backend/app.py \n\
directory=/app/backend \n\
autostart=true \n\
autorestart=true \n\
stdout_logfile=/dev/stdout \n\
stdout_logfile_maxbytes=0 \n\
stderr_logfile=/dev/stderr \n\
stderr_logfile_maxbytes=0' > /etc/supervisor/conf.d/supervisord.conf

# Create supervisor log directory
RUN mkdir -p /var/log/supervisor

# Expose ports
EXPOSE 80 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=False

# Start supervisor to run both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
