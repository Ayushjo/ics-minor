# ICS Multi-Agent Fault Detection System

## Overview

A sophisticated **Industrial Control System (ICS) Fault Detection System** that uses a multi-agent AI architecture to monitor and detect cyber attacks and operational anomalies in real-time. Built for Secure Water Treatment (SWaT) facilities with 51 sensor monitoring points.

### Key Features

- **6-Agent AI System:** Coordinated intelligent agents for comprehensive threat detection
- **Real-time Monitoring:** WebSocket-based live data streaming and analysis
- **99.83% Detection Accuracy:** Random Forest ML model with proven performance
- **Complete Dashboard:** React-based interactive visualization and control panel
- **Production Ready:** Dockerized deployment with nginx + Flask backend

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                           │
│  Dashboard • Charts • Alerts • Risk Assessment • Controls     │
└────────────────────────┬─────────────────────────────────────┘
                         │ WebSocket + REST API
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                  BACKEND (Flask + SocketIO)                   │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         CoordinationAgent (Orchestrator)                │  │
│  └──────────────┬─────────────────────────────────────────┘  │
│                 │                                              │
│     ┌───────────┼───────────┬──────────────┐                 │
│     ↓           ↓           ↓              ↓                 │
│  ┌─────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐       │
│  │Perception│ │  Fault   │ │   Cyber    │ │Operation │       │
│  │  Agent  │ │Detection │ │    Risk    │ │   Risk   │       │
│  └─────────┘ └──────────┘ └────────────┘ └──────────┘       │
│                                           ┌──────────┐        │
│                                           │ Decision │        │
│                                           │  Making  │        │
│                                           └──────────┘        │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Python 3.9+** - Core language
- **Flask 2.3.3** - Web framework
- **Flask-SocketIO 5.3.4** - Real-time WebSocket
- **scikit-learn 1.3.0** - Machine learning
- **pandas 2.0.3** - Data processing
- **numpy 1.24.3** - Numerical computing

### Frontend
- **React 18.2.0** - UI framework
- **recharts 2.5.0** - Data visualization
- **socket.io-client 4.5.4** - WebSocket client
- **axios 1.4.0** - HTTP client
- **framer-motion 12.23.24** - Animations

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:5000
```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed Docker instructions.

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Generate training data
python generate_dummy_data.py

# Train ML models
python train_models.py

# Start backend server
python app.py
```

Backend runs on: **http://localhost:5000**

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

---

## Project Structure

```
ics-multi-agent-backend/
│
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml            # Docker Compose configuration
├── .dockerignore                 # Docker build exclusions
├── DOCKER_DEPLOYMENT.md          # Complete Docker guide
│
├── backend/                      # Python Backend
│   ├── app.py                   # Flask server (MAIN ENTRY)
│   ├── agents.py                # Multi-agent AI system
│   ├── requirements.txt         # Python dependencies
│   ├── train_models.py          # Model training script
│   ├── generate_dummy_data.py   # Data generation
│   ├── enhanced_features.py     # Advanced analytics
│   ├── README.md                # Backend documentation
│   │
│   ├── data/                    # CSV datasets (44 MB)
│   │   ├── output1.csv          # Training data with attacks
│   │   ├── output.csv           # Normal operation data
│   │   ├── test_data.csv        # Test dataset
│   │   ├── realtime_simulation_v2.csv  # Active simulation
│   │   └── [other datasets]
│   │
│   ├── models/                  # Trained ML models
│   │   ├── perception_agent.pkl          # Preprocessor
│   │   └── fault_detection_model.pkl     # Random Forest
│   │
│   └── logs/                    # Application logs
│
└── frontend/                    # React Frontend
    ├── src/
    │   ├── App.js              # Main React component
    │   ├── App.css             # Main styles
    │   └── components/         # UI Components
    │       ├── Header.js
    │       ├── RealTimeChart.js
    │       ├── AlertSystem.js
    │       ├── RiskGauge.js
    │       ├── Decisions.js
    │       ├── SensorHeatmap.js
    │       ├── AttackPatterns.js
    │       ├── DetectionResults.js
    │       └── [12+ components]
    │
    ├── public/
    │   └── index.html          # HTML entry point
    │
    ├── package.json            # Node dependencies
    └── README.md               # Frontend documentation
```

---

## How It Works

### Multi-Agent System

The system uses **6 cooperating AI agents** that work together:

1. **PerceptionAgent**
   - Preprocesses sensor data
   - Normalizes features using StandardScaler
   - Applies PowerTransformer for distribution normalization

2. **FaultDetectionAgent**
   - Random Forest classifier (200 trees)
   - Detects anomalies with 99.83% accuracy
   - Provides confidence scores for predictions

3. **CyberRiskAssessmentAgent**
   - Analyzes attack patterns
   - Calculates cyber threat scores
   - Classifies risk levels (low/medium/high/critical)

4. **OperationalRiskAssessmentAgent**
   - Evaluates system impact
   - Estimates downtime
   - Assesses safety implications

5. **DecisionMakingAgent**
   - Recommends mitigation actions
   - Provides response timelines
   - Flags actions requiring human approval

6. **CoordinationAgent**
   - Orchestrates all agents
   - Manages data flow through pipeline
   - Consolidates results for frontend

### Data Flow

```
Sensor Data (51 features)
    ↓
PerceptionAgent (normalize)
    ↓
FaultDetectionAgent (classify)
    ↓
CyberRiskAgent (assess threat)
    ↓
OperationalRiskAgent (impact analysis)
    ↓
DecisionMakingAgent (recommendations)
    ↓
CoordinationAgent (consolidate)
    ↓
WebSocket → Frontend Dashboard
```

---

## API Endpoints

### REST API

```http
GET  /api/health
     Check system health status

POST /api/system/initialize
     Initialize all agents and load models

GET  /api/system/status
     Get current system state

POST /api/process/batch
     Process a batch of sensor data
     Body: { batch_size: int, scenario: "attack|normal|mixed" }

POST /api/upload
     Upload CSV file for processing
     Body: multipart/form-data with CSV file
```

### WebSocket Events

**Client → Server:**
- `start_simulation` - Start real-time data stream
- `stop_simulation` - Stop data stream
- `reset_simulation` - Reset to beginning

**Server → Client:**
- `connection_response` - Connection confirmation
- `real_time_update` - Continuous analysis results
- `simulation_started` - Simulation start confirmation
- `simulation_stopped` - Simulation stop confirmation
- `error` - Error messages

---

## Machine Learning Model

### Random Forest Classifier

- **Trees:** 200
- **Max Depth:** 20
- **Class Weight:** Balanced
- **Features:** 51 sensor readings
- **Classes:** 2 (Normal, Attack)

### Performance Metrics

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 99.83% |
| Precision | 0.98   |
| Recall    | 0.99   |
| F1-Score  | 0.98   |

### Sensor Features (51 Total)

- **Flow Meters:** FIT-101, FIT-201, FIT-301, FIT-401, FIT-501, FIT-601
- **Level Sensors:** LIT-101, LIT-301, LIT-401
- **Pressure Sensors:** PIT-501, PIT-502, PIT-503, DPIT-301
- **Analyzers:** AIT-201, AIT-202, AIT-203, AIT-401, AIT-402
- **Pumps:** P-101, P-102, P-201, P-202, P-203, P-204, P-205, P-206
- **Valves:** MV-101, MV-201, MV-301, MV-302, MV-303, MV-304
- **Control Systems:** Plus 20 additional control points

---

## Configuration

### Environment Variables

```bash
# Backend (optional, defaults in app.py)
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Frontend (optional, defaults in App.js)
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
```

### Simulation Parameters

Edit in `backend/app.py`:

```python
data_simulator = DataSimulator(
    test_data,
    batch_size=50,      # Samples per batch
    delay=3             # Seconds between batches
)
```

---

## Deployment

### For Docker Deployment

See complete guide: [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

**Quick commands:**

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### For Production (Manual)

```bash
# Backend with gunicorn
pip install gunicorn gevent-websocket
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
  -w 4 -b 0.0.0.0:5000 app:app

# Frontend with nginx
npm run build
# Serve build/ directory with nginx
```

---

## Testing

### Backend Tests

```bash
cd backend
python test_backend.py
```

### API Testing

```bash
# Health check
curl http://localhost:5000/api/health

# Process batch
curl -X POST http://localhost:5000/api/process/batch \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 50, "scenario": "mixed"}'
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Troubleshooting

### Backend Issues

**Problem:** "System not initialized"
- **Solution:** Run `python train_models.py` to create model files

**Problem:** "Module 'agents' not found"
- **Solution:** Ensure `agents.py` exists in backend directory

**Problem:** Port 5000 already in use
- **Solution:** Change port in `app.py` or kill process using port

### Frontend Issues

**Problem:** Cannot connect to backend
- **Solution:** Verify backend is running on port 5000
- Check CORS settings in `app.py`

**Problem:** npm install fails
- **Solution:** Delete `node_modules/` and `package-lock.json`, retry

### Docker Issues

**Problem:** Models not found in container
- **Solution:** Ensure `backend/models/*.pkl` exist before building

**Problem:** Container exits immediately
- **Solution:** Check logs with `docker logs ics-multi-agent`

---

## Performance

### Resource Requirements

- **RAM:** 2-4 GB (ML models + data processing)
- **CPU:** 2+ cores recommended
- **Disk:** 2 GB for Docker image, 100 MB for source
- **Network:** Minimal (WebSocket connections)

### Optimization Tips

- Use `FLASK_DEBUG=False` in production
- Enable gzip compression in nginx
- Use gunicorn with multiple workers
- Cache static frontend assets
- Consider Redis for session storage

---

## Security Considerations

### Current Setup (Development)

- CORS enabled for all origins (`*`)
- Debug mode enabled
- No authentication
- No HTTPS

### Production Recommendations

- [ ] Restrict CORS to specific domains
- [ ] Disable Flask debug mode
- [ ] Add authentication (JWT, OAuth)
- [ ] Enable HTTPS with SSL certificates
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Use environment variables for secrets
- [ ] Set up logging and monitoring

---

## Use Cases

### Research & Academic

- Demonstrating multi-agent AI systems
- ICS security research
- Anomaly detection studies
- Machine learning demonstrations

### Industry Applications

- Water treatment facility monitoring
- Critical infrastructure protection
- Real-time threat detection
- Operational risk management

### Training & Education

- Cybersecurity training
- Industrial control systems education
- AI/ML education
- DevOps deployment practices

---

## Future Enhancements

- [ ] Add historical data analysis dashboard
- [ ] Implement user authentication system
- [ ] Add email/SMS alert notifications
- [ ] Create mobile-responsive design
- [ ] Add export functionality (PDF reports)
- [ ] Implement model retraining pipeline
- [ ] Add support for multiple facilities
- [ ] Create admin configuration panel
- [ ] Add audit logging
- [ ] Integrate with SIEM systems

---

## Contributing

This is an academic/demonstration project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request with detailed description

---

## License

This project is provided for educational and research purposes.

---

## Credits

### Technologies Used

- Flask - Web framework
- React - Frontend framework
- scikit-learn - Machine learning
- Socket.IO - Real-time communication
- Docker - Containerization
- nginx - Web server

### Dataset

Based on SWaT (Secure Water Treatment) testbed architecture with simulated sensor data.

---

## Support & Documentation

- **Backend Documentation:** [backend/README.md](backend/README.md)
- **Frontend Documentation:** [frontend/README.md](frontend/README.md)
- **Docker Guide:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- **Quick Start:** [backend/QUICK_START.md](backend/QUICK_START.md)

---

## Quick Reference

### Start Everything (Docker)

```bash
docker-compose up --build
```

### Start Everything (Manual)

```bash
# Terminal 1 - Backend
cd backend && python app.py

# Terminal 2 - Frontend
cd frontend && npm start
```

### Access Points

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

---

## Contact & Issues

For questions, issues, or contributions, please refer to the project documentation or create an issue in the repository.

---

**Built with ❤️ for Industrial Control System Security Research**
