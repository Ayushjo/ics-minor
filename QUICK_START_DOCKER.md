# Quick Start - Docker Deployment

## For Someone Receiving This Project

This is a complete guide to get the ICS Multi-Agent Fault Detection System running using Docker.

---

## What You Need

1. **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
2. **2GB free disk space**
3. **Ports 3000 and 5000 available**

---

## Start the Application (3 Steps)

### Step 1: Open Terminal/Command Prompt

Navigate to the project directory:

```bash
cd ics-multi-agent-backend
```

### Step 2: Build and Start

Run this single command:

```bash
docker-compose up --build
```

**Wait 5-10 minutes** for the build to complete (first time only).

You'll see:
```
✓ Building frontend...
✓ Installing Python dependencies...
✓ Creating final image...
✓ Starting services...
✓ Backend ready on port 5000
✓ Frontend ready on port 80
```

### Step 3: Access the Application

Open your web browser:

**http://localhost:3000**

You should see the ICS Fault Detection Dashboard.

---

## Stop the Application

Press `Ctrl+C` in the terminal where docker-compose is running.

Or run:

```bash
docker-compose down
```

---

## Running in Background

To run detached (in background):

```bash
docker-compose up -d
```

View logs:

```bash
docker-compose logs -f
```

Stop:

```bash
docker-compose down
```

---

## Verify Everything Works

### 1. Check Backend Health

Open in browser or use curl:

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "system_state": "READY",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Check Frontend

Open browser: **http://localhost:3000**

You should see:
- Dashboard with charts
- Real-time monitoring section
- Alert system
- Risk gauges
- Start/Stop simulation buttons

### 3. Start Simulation

Click **"Start Simulation"** button in the dashboard.

You should see:
- Real-time data flowing
- Charts updating
- Alerts appearing (if anomalies detected)
- Risk scores changing

---

## Troubleshooting

### Problem: Port already in use

**Solution:** Change ports in `docker-compose.yml`:

```yaml
ports:
  - "8080:80"      # Changed from 3000
  - "8000:5000"    # Changed from 5000
```

Then access via: http://localhost:8080

### Problem: Docker build fails

**Solution:** Ensure you have:
1. Docker Desktop running
2. Internet connection (for downloading dependencies)
3. At least 2GB free disk space

### Problem: "Models not found"

**Solution:** The models are included in the build. If missing:

```bash
# Go to backend directory
cd backend

# Install Python (if not installed)
# Then run:
pip install -r requirements.txt
python train_models.py

# Return to root and rebuild
cd ..
docker-compose up --build
```

### Problem: Frontend shows "Cannot connect to backend"

**Solution:**
1. Check backend is running: `curl http://localhost:5000/api/health`
2. Check docker logs: `docker-compose logs backend`
3. Restart: `docker-compose restart`

---

## What's Running Inside the Container?

The container runs **two services**:

1. **Nginx** (port 80 → your port 3000)
   - Serves the React frontend
   - Proxies API calls to backend

2. **Flask Backend** (port 5000)
   - REST API endpoints
   - WebSocket for real-time data
   - ML model inference
   - Multi-agent processing

Both are managed by Supervisor and start automatically.

---

## File Structure (What's Important)

```
ics-multi-agent-backend/
├── Dockerfile              ← Docker build instructions
├── docker-compose.yml      ← Easy start command config
├── .dockerignore           ← Files to exclude from build
│
├── backend/
│   ├── models/            ← Trained ML models (REQUIRED)
│   ├── data/              ← CSV datasets (REQUIRED)
│   └── app.py             ← Backend server code
│
└── frontend/
    └── src/               ← React frontend code
```

**Important:** The `backend/models/` and `backend/data/` directories must exist with their files before building.

---

## Configuration (Optional)

### Change Simulation Speed

Edit `docker-compose.yml`:

```yaml
environment:
  - BATCH_SIZE=50          # Samples per batch
  - DELAY_SECONDS=3        # Seconds between batches
```

### Enable Debug Mode

```yaml
environment:
  - FLASK_ENV=development
  - FLASK_DEBUG=True
```

---

## Data Persistence

Logs are saved to `backend/logs/` on your host machine (persists after container stops).

To save other data, add volume mounts in `docker-compose.yml`:

```yaml
volumes:
  - ./backend/logs:/app/backend/logs
  - ./custom_data:/app/backend/data
```

---

## Commands Cheat Sheet

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Check status
docker-compose ps

# Remove everything (including volumes)
docker-compose down -v
```

---

## System Requirements

- **OS:** Windows 10/11, macOS, Linux
- **RAM:** 2GB minimum, 4GB recommended
- **CPU:** 2 cores minimum
- **Disk:** 2GB for Docker image
- **Docker:** Version 20.10+
- **Docker Compose:** Version 1.29+

---

## What the Dashboard Shows

Once running, the dashboard displays:

1. **System Status**
   - Current state (READY, PROCESSING, etc.)
   - Uptime
   - Total samples processed

2. **Real-Time Charts**
   - Anomaly detection over time
   - Cyber risk score
   - Operational risk score

3. **Alerts**
   - Active threats
   - Severity levels
   - Recommendations

4. **Risk Gauges**
   - Current cyber risk level
   - Current operational risk level
   - Visual color-coded indicators

5. **Recommended Actions**
   - Mitigation steps
   - Response timeline
   - Approval requirements

6. **Sensor Heatmap**
   - 51 sensor status visualization
   - Anomaly highlighting

---

## For Demonstrations

### Best Demo Flow:

1. **Start Docker container**
   ```bash
   docker-compose up -d
   ```

2. **Open dashboard**
   - Navigate to http://localhost:3000

3. **Explain the interface**
   - Show the 6-agent architecture diagram
   - Explain each component

4. **Start simulation**
   - Click "Start Simulation"
   - Watch real-time data flow

5. **Show detection in action**
   - Point out anomalies detected
   - Show risk assessment
   - Highlight recommendations

6. **Explain ML model**
   - 99.83% accuracy
   - Random Forest with 200 trees
   - 51 sensor features

7. **Show API endpoints**
   - http://localhost:5000/api/health
   - Show WebSocket connection in browser dev tools

---

## Sharing This Project

To share with someone else:

### Option 1: Share Everything

Zip the entire directory and share:
- All source code
- Dockerfile
- docker-compose.yml
- Documentation

Recipient runs: `docker-compose up --build`

### Option 2: Share Docker Image

```bash
# Save image to file
docker save ics-multi-agent:latest | gzip > ics-multi-agent.tar.gz

# Share the .tar.gz file

# Recipient loads and runs:
docker load < ics-multi-agent.tar.gz
docker run -p 3000:80 -p 5000:5000 ics-multi-agent:latest
```

### Option 3: Push to Docker Hub

```bash
docker tag ics-multi-agent:latest yourusername/ics-multi-agent:latest
docker push yourusername/ics-multi-agent:latest

# Share: "docker pull yourusername/ics-multi-agent:latest"
```

---

## Additional Documentation

- **Complete README:** `README.md`
- **Full Docker Guide:** `DOCKER_DEPLOYMENT.md`
- **Backend Details:** `backend/README.md`
- **Frontend Details:** `frontend/README.md`

---

## Support

If something doesn't work:

1. **Check Docker is running**
   ```bash
   docker ps
   ```

2. **Check logs**
   ```bash
   docker-compose logs
   ```

3. **Verify ports are free**
   ```bash
   # Windows
   netstat -an | findstr "3000 5000"

   # Mac/Linux
   lsof -i :3000
   lsof -i :5000
   ```

4. **Rebuild from scratch**
   ```bash
   docker-compose down
   docker-compose up --build --force-recreate
   ```

---

## That's It!

You now have a fully functional ICS Fault Detection System running in Docker.

**Access:** http://localhost:3000

**Enjoy!** 🚀
