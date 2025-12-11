# Frontend - Multi-Agent ICS Fault Detection System

React dashboard for real-time monitoring of ICS fault detection.

## Features

- **Real-time WebSocket connection** to backend
- **Live charts** showing anomaly rates and risk scores
- **Control panel** to start/stop simulation
- **Detection results** display
- **Risk assessment** visualization (Cyber + Operational)
- **Automated decisions** and recommendations
- **Emergency contacts** display

## Components

- `App.js` - Main application with WebSocket management
- `ControlPanel.js` - Start/Stop/Reset controls
- `SystemStatus.js` - Connection and system state display
- `DetectionResults.js` - Anomaly detection metrics
- `RiskAssessment.js` - Cyber and operational risk visualization
- `Decisions.js` - Automated mitigation recommendations
- `RealTimeChart.js` - Live line chart with Recharts

## Running the Frontend

```bash
npm start
```

Runs on: **http://localhost:3000**

## Prerequisites

Backend must be running on: **http://localhost:5000**

## Usage

1. Ensure backend is running
2. Start frontend with `npm start`
3. Click "Start Simulation" to begin real-time monitoring
4. Watch live updates every 3 seconds
5. Click "Stop Simulation" to pause
6. Click "Reset" to clear history

## Tech Stack

- React 18
- Socket.IO Client (WebSocket)
- Recharts (Charts)
- Axios (HTTP requests)
