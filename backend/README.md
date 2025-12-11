# Multi-Agent ICS Fault Detection System - Backend

## 🎯 Overview

This is the **Flask backend** for your Multi-Agent Industrial Control System (ICS) fault detection system. It wraps your existing agent code with a professional REST API and WebSocket support for real-time monitoring.

## 📂 Project Structure

```
backend/
├── agents.py                   # Your multi-agent system code
├── app.py                      # Flask server with WebSocket
├── generate_dummy_data.py      # Generates demonstration datasets
├── setup.py                    # Automated setup script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/                       # Generated datasets (created by setup)
│   ├── output1.csv            # Training data (with attacks)
│   ├── output.csv             # Normal operation data
│   ├── test_data.csv          # Test dataset
│   └── realtime_data.csv      # Real-time simulation data
├── models/                     # Trained models (you need to create these)
│   ├── perception_agent.pkl   # Saved perception agent
│   └── fault_detection_model.pkl  # Saved ML model
└── logs/                       # Application logs
```

## 🚀 Quick Start

### 1. Run Setup Script

```bash
python setup.py
```

This will:
- Create directory structure (data/, models/, logs/)
- Generate dummy CSV data for demonstration
- Check for required files
- Optionally install dependencies

### 2. Install Dependencies (if not done by setup)

```bash
pip install -r requirements.txt
```

### 3. Train Models

You need to train the models before running the backend. Create a file called `train_models.py`:

```python
from agents import *

# Train your agents
system_results = main(
    file1_path='data/output1.csv',
    file2_path='data/output.csv'
)

print("\n✓ Models trained and saved successfully!")
print("  - models/perception_agent.pkl")
print("  - models/fault_detection_model.pkl")
```

Run it:
```bash
python train_models.py
```

### 4. Start Backend Server

```bash
python app.py
```

Server will start at: `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "system_state": "READY",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Initialize System
```http
POST /api/system/initialize
```

Response:
```json
{
  "status": "success",
  "message": "System initialized successfully",
  "system_state": "READY"
}
```

### Get System Status
```http
GET /api/system/status
```

Response:
```json
{
  "status": "success",
  "system_state": "READY",
  "simulation_running": false,
  "data_index": 0,
  "total_samples": 10000
}
```

### Process Batch
```http
POST /api/process/batch
Content-Type: application/json

{
  "batch_size": 100,
  "scenario": "mixed"  // "attack", "normal", or "mixed"
}
```

Response:
```json
{
  "status": "success",
  "timestamp": "2024-01-15T10:30:00",
  "batch_info": {
    "total_samples": 100,
    "anomalies_detected": 15,
    "anomaly_rate": 0.15
  },
  "detection": {
    "num_anomalies": 15,
    "anomaly_rate": 0.15,
    "attack_probabilities": [0.92, 0.15, ...],
    "predictions": [1, 0, 1, ...],
    "confidence": [0.95, 0.88, ...]
  },
  "cyber_risk": {
    "score": 0.75,
    "level": "high",
    "attack_signature": "Persistent Attack",
    "threat_assessment": "High cyber threat level! Immediate attention required."
  },
  "operational_risk": {
    "score": 0.68,
    "level": "high",
    "fault_severity": "High",
    "affected_systems": ["Primary Treatment", "Control System"],
    "estimated_downtime": 120,
    "safety_impact": "Moderate - Safety monitoring required"
  },
  "decisions": {
    "primary_threat": "Cyber Attack",
    "recommended_actions": ["Isolate affected network segments", ...],
    "response_timeline": "URGENT (5-15 minutes)",
    "requires_human_approval": true
  },
  "metrics": {
    "accuracy": 0.98,
    "precision": 0.97,
    "recall": 0.99,
    "f1_score": 0.98
  }
}
```

### Upload CSV
```http
POST /api/upload
Content-Type: multipart/form-data

file: <your_csv_file>
```

## 🔌 WebSocket Events

### Client → Server

**Connect**
```javascript
socket.connect()
```

**Start Simulation**
```javascript
socket.emit('start_simulation', {
  batch_size: 50,
  delay: 3  // seconds between batches
})
```

**Stop Simulation**
```javascript
socket.emit('stop_simulation')
```

**Reset Simulation**
```javascript
socket.emit('reset_simulation')
```

### Server → Client

**Connection Response**
```javascript
socket.on('connection_response', (data) => {
  // data: { status: 'connected' }
})
```

**Real-time Update**
```javascript
socket.on('real_time_update', (data) => {
  // data: Full detection results (same format as /api/process/batch)
})
```

**Simulation Started**
```javascript
socket.on('simulation_started', (data) => {
  // data: { status: 'success', batch_size: 50, delay: 3 }
})
```

**Simulation Stopped**
```javascript
socket.on('simulation_stopped', (data) => {
  // data: { status: 'success' }
})
```

**Error**
```javascript
socket.on('error', (data) => {
  // data: { message: 'Error description' }
})
```

## 🧪 Testing the Backend

### Using curl

```bash
# Health check
curl http://localhost:5000/api/health

# Get system status
curl http://localhost:5000/api/system/status

# Process a batch
curl -X POST http://localhost:5000/api/process/batch \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 50, "scenario": "mixed"}'
```

### Using Python

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Process batch
response = requests.post('http://localhost:5000/api/process/batch',
                        json={'batch_size': 100, 'scenario': 'attack'})
print(response.json())
```

### Using WebSocket (Python)

```python
import socketio

sio = socketio.Client()

@sio.on('real_time_update')
def on_update(data):
    print(f"Received update: {data['detection']['num_anomalies']} anomalies detected")

sio.connect('http://localhost:5000')
sio.emit('start_simulation', {'batch_size': 50, 'delay': 2})
```

## 🎓 For Your Professor Demo

### Demo Flow

1. **Start the backend**
   ```bash
   python app.py
   ```

2. **Backend loads**:
   - Pre-trained models
   - Test data for simulation
   - Initializes all agents

3. **Start simulation** (via frontend or API):
   - Data streams every 3 seconds
   - Each batch processed through all agents
   - Results sent to frontend in real-time

4. **Show live monitoring**:
   - Anomaly detection
   - Cyber risk assessment
   - Operational risk assessment
   - Automated decision-making
   - Mitigation recommendations

### What Makes This Impressive

✅ **Professional Architecture** - Industry-standard tech stack (Flask, WebSocket, REST API)
✅ **Real-time Capabilities** - Continuous monitoring like production ICS systems
✅ **Scalable Design** - Can handle actual sensor data with minimal changes
✅ **Complete Pipeline** - All agents working together seamlessly
✅ **Realistic Simulation** - Demonstrates without expensive hardware

## 🔧 Configuration

You can adjust simulation parameters in `app.py`:

```python
# DataSimulator configuration
data_simulator = DataSimulator(
    test_data,
    batch_size=50,      # Samples per batch
    delay=3             # Seconds between batches
)
```

## 🐛 Troubleshooting

### "System not initialized"
- Train models using `train_models.py`
- Ensure models are in `models/` directory

### "Module 'agents' not found"
- Ensure `agents.py` exists in the backend directory
- Check all imports are correct

### "No data files found"
- Run `python setup.py` to generate data
- Or run `python generate_dummy_data.py` directly

### WebSocket connection fails
- Check if Flask-SocketIO is installed
- Verify CORS settings in `app.py`
- Ensure no firewall blocking port 5000

### Port already in use
- Stop other Flask applications
- Or change port in `app.py`: `socketio.run(app, port=5001)`

## 📊 Data Files

### Generated by `generate_dummy_data.py`

- **output1.csv** - Training data (10,000 samples, 20% attacks)
- **output.csv** - Additional normal data (5,000 samples)
- **test_data.csv** - Test data (3,000 samples, mixed)
- **realtime_data.csv** - Simulation data (10,000 samples, 15% attacks)

### Sensor Features (51 total)

- Flow meters (FIT-XXX)
- Level sensors (LIT-XXX)
- Pressure sensors (PIT-XXX, DPIT-XXX)
- Analyzers (AIT-XXX)
- Pumps (P-XXX)
- Valves (MV-XXX)

## 🤝 Integration with Frontend

The backend is designed to work with a React frontend. The frontend will:

1. Connect via WebSocket
2. Start/stop simulation
3. Display real-time results
4. Show charts and visualizations
5. List recommended actions

## 📝 Notes

- This backend simulates a real ICS environment for demonstration
- In production, replace DataSimulator with actual sensor data streams
- Models are pre-trained and loaded at startup for fast inference
- All agent logic remains unchanged from your original implementation

## 📚 Next Steps

1. ✅ Backend is ready
2. ⏳ Build React frontend (next phase)
3. ⏳ Connect frontend to backend
4. ⏳ Add visualizations and charts
5. ⏳ Prepare final demo

---

**Need help?** Check the troubleshooting section or review the code comments in `app.py`.
