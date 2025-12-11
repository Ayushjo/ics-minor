# Docker Deployment Guide - ICS Multi-Agent Backend

## Overview

This guide explains how to build and deploy the ICS Multi-Agent Fault Detection System using Docker.

---

## Prerequisites

- Docker 20.10+ installed
- Docker Compose 1.29+ (optional, but recommended)
- At least 2GB free disk space
- Port 3000 and 5000 available

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api/health

### Option 2: Using Docker CLI

```bash
# Build the image
docker build -t ics-multi-agent .

# Run the container
docker run -d \
  --name ics-multi-agent \
  -p 3000:80 \
  -p 5000:5000 \
  ics-multi-agent

# View logs
docker logs -f ics-multi-agent

# Stop the container
docker stop ics-multi-agent

# Remove the container
docker rm ics-multi-agent
```

---

## Dockerfile Architecture

The Dockerfile uses a **multi-stage build** approach for optimal image size:

### Stage 1: Frontend Builder
- Base: `node:18-alpine`
- Builds React production bundle
- Output: Optimized static files

### Stage 2: Backend Preparation
- Base: `python:3.9-slim`
- Installs Python dependencies
- Prepares ML models and data

### Stage 3: Final Production Image
- Base: `python:3.9-slim`
- Combines frontend + backend
- Uses `nginx` for frontend serving
- Uses `supervisor` to run both services
- Minimal size, production-ready

---

## Container Services

The container runs **two services** managed by Supervisor:

1. **Nginx** (Port 80 inside container → 3000 outside)
   - Serves React frontend
   - Proxies `/api/*` requests to backend
   - Proxies `/socket.io/*` WebSocket connections

2. **Flask Backend** (Port 5000)
   - Handles API requests
   - Manages WebSocket connections
   - Runs ML inference

---

## Port Mapping

| Service        | Container Port | Host Port | Description                |
|----------------|----------------|-----------|----------------------------|
| Frontend       | 80             | 3000      | React dashboard (nginx)    |
| Backend API    | 5000           | 5000      | Flask REST API + WebSocket |

**Note:** You can change host ports in `docker-compose.yml` or `-p` flag.

---

## Environment Variables

You can customize the container behavior using environment variables:

```yaml
# In docker-compose.yml
environment:
  - FLASK_ENV=production        # Flask environment
  - FLASK_DEBUG=False            # Disable debug mode
  - PYTHONUNBUFFERED=1          # Python logging
```

Or with Docker CLI:

```bash
docker run -d \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=False \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

---

## Volume Mounts (Optional)

### Persist Logs

```yaml
# In docker-compose.yml
volumes:
  - ./backend/logs:/app/backend/logs
```

Or with Docker CLI:

```bash
docker run -d \
  -v "$(pwd)/backend/logs:/app/backend/logs" \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

### Use Custom Data Files

If you want to use different CSV data:

```bash
docker run -d \
  -v "$(pwd)/custom_data:/app/backend/data" \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

---

## Health Checks

The container includes a health check that verifies the backend is responding:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1
```

Check health status:

```bash
docker ps
# Look for "healthy" status

# Or detailed health info
docker inspect --format='{{json .State.Health}}' ics-multi-agent
```

---

## Building for Production

### Optimize Image Size

The multi-stage build already optimizes size, but you can further reduce:

```bash
# Build with specific Python version
docker build \
  --build-arg PYTHON_VERSION=3.9-slim \
  -t ics-multi-agent:prod .

# View image size
docker images ics-multi-agent
```

### Tag for Registry

```bash
# Tag for your registry
docker tag ics-multi-agent:latest your-registry.com/ics-multi-agent:v1.0

# Push to registry
docker push your-registry.com/ics-multi-agent:v1.0
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs ics-multi-agent

# Interactive shell into container
docker exec -it ics-multi-agent /bin/bash

# Check if services are running inside container
docker exec ics-multi-agent supervisorctl status
```

### Port conflicts

If ports 3000 or 5000 are already in use:

```bash
# Use different host ports
docker run -d \
  -p 8080:80 \
  -p 8000:5000 \
  ics-multi-agent

# Access via http://localhost:8080
```

### Frontend can't connect to backend

If WebSocket connection fails:

1. Check nginx is proxying correctly:
   ```bash
   docker exec ics-multi-agent cat /etc/nginx/sites-available/default
   ```

2. Test backend directly:
   ```bash
   curl http://localhost:5000/api/health
   ```

3. Check browser console for CORS errors

### Models not found

Ensure models exist before building:

```bash
# Check if models directory exists
ls backend/models/

# Should show:
# - perception_agent.pkl
# - fault_detection_model.pkl

# If missing, train models first:
cd backend
python train_models.py
```

### High memory usage

ML models can consume memory. Monitor usage:

```bash
# Check container stats
docker stats ics-multi-agent

# Limit memory (4GB max)
docker run -d \
  --memory="4g" \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

---

## Advanced Usage

### Run with Custom Configuration

Create a `.env` file:

```bash
FLASK_ENV=production
FLASK_PORT=5000
LOG_LEVEL=INFO
```

Then:

```bash
docker run -d \
  --env-file .env \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

### Multi-Container Deployment

If you want to separate frontend and backend:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/data:/app/data
      - ./backend/models:/app/models

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://backend:5000
    depends_on:
      - backend
```

### Enable Debug Mode

For development/debugging:

```bash
docker run -d \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=True \
  -p 3000:80 -p 5000:5000 \
  ics-multi-agent
```

---

## Performance Tuning

### Optimize Nginx

Edit nginx config in Dockerfile for production:

```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Optimize Python

Add gunicorn for production WSGI server:

```dockerfile
# In Dockerfile, replace python app.py with:
CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", \
     "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Models are trained (`backend/models/*.pkl` exist)
- [ ] Data files exist (`backend/data/*.csv`)
- [ ] Environment variables set correctly
- [ ] FLASK_DEBUG=False in production
- [ ] Health check is working
- [ ] Logs are being collected
- [ ] Firewall rules allow ports 3000, 5000
- [ ] SSL/TLS configured (if needed)
- [ ] Backup strategy for data/models
- [ ] Monitoring/alerting configured

---

## Docker Image Specifications

**Expected Image Size:** ~1.5-2GB
- Python dependencies: ~500MB
- Node modules (build time only): Not included in final image
- ML models: ~2MB
- CSV data: ~50MB
- System packages: ~300MB
- Frontend build: ~5MB

**Build Time:** 5-10 minutes (first build)

**Startup Time:** 10-30 seconds

---

## Shipping to Someone Else

To share this application with someone:

### Option 1: Share Docker Image

```bash
# Save image to tar file
docker save ics-multi-agent:latest | gzip > ics-multi-agent.tar.gz

# Share the file (upload to cloud, USB drive, etc.)

# Recipient loads the image
docker load < ics-multi-agent.tar.gz

# Recipient runs the container
docker run -d -p 3000:80 -p 5000:5000 ics-multi-agent:latest
```

### Option 2: Share Source Code + Dockerfile

Share these files:
```
.
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── DOCKER_DEPLOYMENT.md
├── backend/
└── frontend/
```

Recipient runs:
```bash
docker-compose up --build
```

### Option 3: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag ics-multi-agent:latest yourusername/ics-multi-agent:latest

# Push to Docker Hub
docker push yourusername/ics-multi-agent:latest

# Share the image name with recipient
# They run: docker pull yourusername/ics-multi-agent:latest
```

---

## Testing the Deployment

After starting the container:

```bash
# 1. Check container is running
docker ps | grep ics-multi-agent

# 2. Test backend health
curl http://localhost:5000/api/health

# Expected output:
# {"status":"healthy","system_state":"READY","timestamp":"..."}

# 3. Test frontend
# Open browser: http://localhost:3000

# 4. Test WebSocket (optional, using wscat)
npm install -g wscat
wscat -c ws://localhost:5000/socket.io/?transport=websocket

# 5. Check logs
docker logs ics-multi-agent

# Should see:
# - Nginx started
# - Backend started
# - Models loaded
# - System initialized
```

---

## Support

For issues:

1. Check logs: `docker logs ics-multi-agent`
2. Verify health: `curl http://localhost:5000/api/health`
3. Check ports: `netstat -an | grep -E "3000|5000"`
4. Review backend README: `backend/README.md`

---

**Ready to deploy!** Run `docker-compose up --build` and access http://localhost:3000
