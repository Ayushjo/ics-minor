# Complete Setup Instructions - ICS Multi-Agent Backend

## 🎯 For New Users: Give This to Claude Code

If you're receiving this project and need help setting it up, **copy the text in the "Claude Prompt" section below** and paste it into Claude Code. Claude will guide you through the entire setup process.

---

## 📋 Claude Prompt (Copy Everything Below This Line)

```
I've just cloned/received the ICS Multi-Agent Backend project from GitHub.
I need help setting it up on my system. Here's what I need you to do:

1. Check what's already installed on my system (Python, Node.js, Docker, Git)
2. Install anything that's missing
3. Set up the project dependencies
4. Generate training data and train ML models if needed
5. Get both the backend and frontend running
6. Verify everything works

Please guide me step-by-step for my operating system. Ask me questions if you need
to know anything about my setup.

Project location: [PASTE YOUR PROJECT PATH HERE]
```

---

## 🚀 Manual Setup Guide (Without Claude)

If you prefer to set up manually, follow these instructions for your operating system.

---

## Prerequisites Check

Before starting, you need these tools installed:

- [ ] **Python 3.9+** - Backend server and ML models
- [ ] **Node.js 14+** - Frontend build and development
- [ ] **Git** - Version control (already have if you cloned)
- [ ] **Docker** (Optional) - For containerized deployment

---

## Installation Instructions by Operating System

### 🪟 Windows Setup

#### Step 1: Install Python

```bash
# Check if Python is installed
python --version

# If not installed:
# 1. Download from https://www.python.org/downloads/
# 2. Download Python 3.9 or higher
# 3. IMPORTANT: Check "Add Python to PATH" during installation
# 4. Verify installation:
python --version
pip --version
```

#### Step 2: Install Node.js

```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed:
# 1. Download from https://nodejs.org/
# 2. Download LTS version (18.x or higher)
# 3. Run installer with default settings
# 4. Verify installation:
node --version
npm --version
```

#### Step 3: Install Docker Desktop (Optional)

```bash
# Download from https://www.docker.com/products/docker-desktop
# Install and restart computer
# Verify:
docker --version
docker-compose --version
```

#### Step 4: Set Up Project

```bash
# Navigate to project directory
cd path\to\ics-multi-agent-backend

# Set up backend
cd backend
pip install -r requirements.txt
python generate_dummy_data.py
python train_models.py

# Set up frontend
cd ..\frontend
npm install

# Return to root
cd ..
```

#### Step 5: Run the Application

```bash
# Option A: Using Docker (Recommended)
docker-compose up --build

# Option B: Manual (two terminals needed)
# Terminal 1 - Backend:
cd backend
python app.py

# Terminal 2 - Frontend:
cd frontend
npm start
```

#### Step 6: Access

- Frontend: http://localhost:3000
- Backend: http://localhost:5000/api/health

---

### 🍎 macOS Setup

#### Step 1: Install Homebrew (if not installed)

```bash
# Check if Homebrew is installed
brew --version

# If not installed:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
# Check Python version
python3 --version

# Install Python 3.9+
brew install python@3.9

# Verify
python3 --version
pip3 --version
```

#### Step 3: Install Node.js

```bash
# Check Node.js version
node --version

# Install Node.js
brew install node

# Verify
node --version
npm --version
```

#### Step 4: Install Docker Desktop (Optional)

```bash
# Download from https://www.docker.com/products/docker-desktop
# Or use Homebrew:
brew install --cask docker

# Start Docker Desktop from Applications
# Verify:
docker --version
docker-compose --version
```

#### Step 5: Set Up Project

```bash
# Navigate to project directory
cd /path/to/ics-multi-agent-backend

# Set up backend
cd backend
pip3 install -r requirements.txt
python3 generate_dummy_data.py
python3 train_models.py

# Set up frontend
cd ../frontend
npm install

# Return to root
cd ..
```

#### Step 6: Run the Application

```bash
# Option A: Using Docker (Recommended)
docker-compose up --build

# Option B: Manual (two terminals needed)
# Terminal 1 - Backend:
cd backend
python3 app.py

# Terminal 2 - Frontend:
cd frontend
npm start
```

#### Step 7: Access

- Frontend: http://localhost:3000
- Backend: http://localhost:5000/api/health

---

### 🐧 Linux (Ubuntu/Debian) Setup

#### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Python

```bash
# Check Python version
python3 --version

# Install Python 3.9+ and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify
python3 --version
pip3 --version
```

#### Step 3: Install Node.js

```bash
# Check Node.js version
node --version

# Install Node.js 18.x LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
npm --version
```

#### Step 4: Install Docker (Optional)

```bash
# Install Docker
sudo apt install docker.io docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect

# Verify
docker --version
docker-compose --version
```

#### Step 5: Set Up Project

```bash
# Navigate to project directory
cd /path/to/ics-multi-agent-backend

# Set up backend
cd backend
pip3 install -r requirements.txt
python3 generate_dummy_data.py
python3 train_models.py

# Set up frontend
cd ../frontend
npm install

# Return to root
cd ..
```

#### Step 6: Run the Application

```bash
# Option A: Using Docker (Recommended)
docker-compose up --build

# Option B: Manual (two terminals needed)
# Terminal 1 - Backend:
cd backend
python3 app.py

# Terminal 2 - Frontend:
cd frontend
npm start
```

#### Step 7: Access

- Frontend: http://localhost:3000
- Backend: http://localhost:5000/api/health

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "Python is not recognized"

**Windows:**
```bash
# Add Python to PATH manually:
# 1. Search "Environment Variables" in Windows
# 2. Edit "Path" in System Variables
# 3. Add: C:\Python39\ and C:\Python39\Scripts\
# 4. Restart terminal
```

**Mac/Linux:**
```bash
# Use python3 instead of python
python3 --version
pip3 --version
```

### Issue 2: "pip install fails"

```bash
# Windows:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Mac/Linux:
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# If still fails, try with user flag:
pip install --user -r requirements.txt
```

### Issue 3: "npm install fails"

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json  # Mac/Linux
rmdir /s node_modules & del package-lock.json  # Windows

# Reinstall
npm install
```

### Issue 4: "Port already in use"

```bash
# Check what's using port 5000 or 3000

# Windows:
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# Mac/Linux:
lsof -i :5000
lsof -i :3000

# Kill the process or change ports in:
# backend/app.py (line with socketio.run)
# frontend/package.json (add "PORT=3001" to start script)
```

### Issue 5: "Models not found"

```bash
# Generate data and train models
cd backend
python generate_dummy_data.py
python train_models.py

# Verify files exist:
ls models/
# Should show:
# - perception_agent.pkl
# - fault_detection_model.pkl
```

### Issue 6: "Docker build fails"

```bash
# Ensure Docker Desktop is running
docker ps

# If not running, start Docker Desktop

# Try building again with no cache:
docker-compose build --no-cache
docker-compose up
```

### Issue 7: "Cannot connect to backend"

```bash
# Check backend is running:
curl http://localhost:5000/api/health

# If curl fails, check backend logs
# Look for error messages
# Common issues:
# - Models not loaded (run train_models.py)
# - Port conflict (change port)
# - Firewall blocking (allow port 5000)
```

### Issue 8: "Frontend shows blank page"

```bash
# Check browser console for errors (F12)
# Common fixes:

# 1. Clear browser cache (Ctrl+Shift+Delete)
# 2. Rebuild frontend:
cd frontend
rm -rf node_modules build
npm install
npm start
```

---

## 📦 What Gets Installed

### Backend Python Packages (~500 MB):

- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- Flask-SocketIO 5.3.4 - WebSocket support
- pandas 2.0.3 - Data manipulation
- numpy 1.24.3 - Numerical computing
- scikit-learn 1.3.0 - Machine learning
- joblib 1.3.2 - Model serialization
- matplotlib 3.7.2 - Plotting
- seaborn 0.12.2 - Statistical visualization

### Frontend Node Packages (~600 MB):

- react 18.2.0 - UI framework
- react-dom 18.2.0 - React rendering
- axios 1.4.0 - HTTP client
- socket.io-client 4.5.4 - WebSocket client
- recharts 2.5.0 - Charts
- framer-motion 12.23.24 - Animations
- lucide-react 0.554.0 - Icons

### Data Files Generated (~50 MB):

- output1.csv - Training data with attacks
- output.csv - Normal operation data
- test_data.csv - Test dataset
- realtime_simulation_v2.csv - Simulation data

### Model Files (~2 MB):

- perception_agent.pkl - Data preprocessor
- fault_detection_model.pkl - Random Forest classifier

---

## 🎓 Verification Steps

After setup, verify everything works:

### 1. Check Backend

```bash
# Backend should be running on port 5000
curl http://localhost:5000/api/health

# Expected output:
# {"status":"healthy","system_state":"READY","timestamp":"..."}
```

### 2. Check Frontend

```bash
# Open browser: http://localhost:3000
# You should see:
# - Dashboard with multiple panels
# - "Start Simulation" button
# - Charts and gauges
# - Alert system
```

### 3. Test Simulation

```bash
# In the frontend dashboard:
# 1. Click "Start Simulation"
# 2. Watch data flow in real-time
# 3. Charts should update every 3 seconds
# 4. Alerts may appear if anomalies detected
# 5. Click "Stop Simulation" to stop
```

### 4. Check API Endpoints

```bash
# Test system status
curl http://localhost:5000/api/system/status

# Process a batch
curl -X POST http://localhost:5000/api/process/batch \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 50, "scenario": "mixed"}'
```

---

## 🐳 Docker Quick Setup (Easiest Method)

If you have Docker installed, this is the fastest way:

```bash
# One command to rule them all:
docker-compose up --build

# Wait 5-10 minutes for first build
# Access: http://localhost:3000

# To stop:
# Press Ctrl+C or run:
docker-compose down
```

That's it! No Python, Node.js, or dependency management needed.

---

## 📁 File Structure After Setup

```
ics-multi-agent-backend/
│
├── backend/
│   ├── data/                  ✅ Generated (50 MB)
│   │   ├── output1.csv
│   │   ├── output.csv
│   │   ├── test_data.csv
│   │   └── realtime_simulation_v2.csv
│   │
│   ├── models/                ✅ Generated (2 MB)
│   │   ├── perception_agent.pkl
│   │   └── fault_detection_model.pkl
│   │
│   ├── logs/                  ✅ Created automatically
│   │
│   └── [source files]
│
├── frontend/
│   ├── node_modules/          ✅ Installed (600 MB)
│   ├── build/                 ⚠️ Only after npm run build
│   └── [source files]
│
└── [config files]
```

---

## 🚨 Important Notes

### Data Files in Git

The data files (`*.csv`) and model files (`*.pkl`) are **included in the repository** for easy setup. This means:

✅ **Pros:**
- Clone and run immediately
- No need to generate data or train models
- Perfect for demonstrations

⚠️ **Cons:**
- Larger repository size (~50 MB)
- May take longer to clone

If you want to exclude these files, add them to `.gitignore`:

```bash
# Add to .gitignore:
backend/data/*.csv
backend/models/*.pkl
```

Then users will need to run:

```bash
python generate_dummy_data.py
python train_models.py
```

### Virtual Environments (Optional but Recommended)

For cleaner Python dependency management:

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# To deactivate when done:
deactivate
```

---

## 💡 Tips for Success

1. **Always check versions first:**
   ```bash
   python --version  # Should be 3.9+
   node --version    # Should be 14+
   ```

2. **Use Docker if possible:**
   - Simplest setup
   - No dependency conflicts
   - Works the same on all OS

3. **Read error messages:**
   - They usually tell you what's wrong
   - Google the exact error if unclear

4. **Check logs:**
   ```bash
   # Backend logs in terminal
   # Frontend logs in browser console (F12)
   ```

5. **One step at a time:**
   - Don't skip verification steps
   - Ensure each step works before moving on

---

## 🆘 Getting Help

If you're stuck:

1. **Check this file's troubleshooting section**

2. **Use Claude Code:**
   - Copy the Claude Prompt from the top
   - Claude will help debug

3. **Check the documentation:**
   - README.md - General overview
   - DOCKER_DEPLOYMENT.md - Docker specifics
   - backend/README.md - Backend details

4. **Common commands to share with Claude:**
   ```bash
   # Share these outputs when asking for help:
   python --version
   node --version
   docker --version

   # And any error messages you're seeing
   ```

---

## ✅ Setup Complete Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 14+ installed
- [ ] Docker installed (optional)
- [ ] Project cloned/downloaded
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Training data generated (CSV files in `backend/data/`)
- [ ] ML models trained (PKL files in `backend/models/`)
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can access http://localhost:5000/api/health
- [ ] Simulation starts and shows real-time data

---

## 🎉 You're Done!

If you've completed the checklist above, your ICS Multi-Agent Backend is fully operational!

**Next steps:**
- Explore the dashboard
- Start a simulation
- Read the README.md for detailed documentation
- Check out the API endpoints
- Try the Docker deployment

**Happy monitoring! 🚀**
