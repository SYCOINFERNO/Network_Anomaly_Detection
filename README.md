# Network Logs Anomaly Detection System

A data engineering project that detects suspicious network activity using Python, SQLite, and Streamlit.

## Project Overview

This system:
- **Generates** realistic network logs with normal and anomalous traffic
- **Loads** logs into SQLite database
- **Detects** anomalies using rule-based detection
- **Visualizes** threats in an interactive Streamlit dashboard

## Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Network Logs
```bash
python src/log_generator.py
```
This creates `data/network_logs.csv` with 5000 sample network records.

### 3. Load Logs & Detect Anomalies
```bash
python src/database.py
```
This initializes the database and loads all logs.

### 4. Run Dashboard
```bash
streamlit run src/dashboard.py
```
Opens interactive dashboard at `http://localhost:8501`

## Project Structure
```
network_anomaly_detection/
├── data/                 # CSV logs and SQLite database
├── src/
│   ├── log_generator.py  # Generate network logs
│   ├── database.py       # Database setup and ETL
│   ├── anomaly_detector.py  # Detection rules
│   └── dashboard.py      # Streamlit dashboard
├── models/              # ML models (future)
├── requirements.txt     # Python dependencies
└── README.md
```

## Anomaly Detection Rules

1. **Port Scanning** - Multiple ports from same IP in short time
2. **DDoS Attack** - High connection count to same destination
3. **Brute Force** - Multiple SSH/connection attempts in short time
4. **Data Exfiltration** - Large data transfer outbound
5. **Uncommon Ports** - Traffic on dangerous/rare ports
6. **Suspicious IPs** - Traffic from known suspicious IP ranges

## Dashboard Features

- **Overview**: Anomaly type and severity distribution
- **Anomalies**: Detailed list of detected anomalies with filters
- **Traffic Analysis**: Top IPs, protocols, traffic timeline
- **Threat Heatmap**: Severity distribution over time
- **Details**: System statistics and sample logs

## Future Enhancements (by Wednesday)

- Machine Learning model (Isolation Forest)
- Real-time streaming processing
- Advanced network graph visualization
- Predictive alerting
- Historical trend analysis

## Tech Stack

- **Language**: Python 3.8+
- **Database**: SQLite
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **ML**: Scikit-learn (future)

## Timeline

- **Friday Demo**: Basic detection + dashboard ✅
- **Wednesday Final**: ML model + advanced features 📅
