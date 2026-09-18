# Quick Start Guide - Network Anomaly Detection

## For Tomorrow's Demo (Friday)

### Option 1: Quick Setup (5 minutes)

```bash
# 1. Navigate to project
cd network_anomaly_detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run dashboard (it will auto-generate data)
streamlit run src/dashboard.py
```

The dashboard will automatically:
- Generate network logs
- Load them into database
- Detect anomalies
- Display interactive visualizations

### Option 2: Step-by-Step Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate network logs (5000 records)
python3 src/log_generator.py

# 3. Load logs into database
python3 src/database.py

# 4. Detect anomalies
python3 src/anomaly_detector.py

# 5. Launch dashboard
streamlit run src/dashboard.py
```

Then open: **http://localhost:8501**

## What You'll See in Demo

### Dashboard Features:
1. **Overview Tab**
   - Total connections, anomalies detected, unique IPs
   - Anomaly type distribution pie chart
   - Severity distribution bar chart

2. **Anomalies Tab**
   - List of 200+ detected anomalies
   - Filter by severity and type
   - Detailed descriptions (port scans, DDoS, brute force, etc.)

3. **Traffic Analysis Tab**
   - Top source IPs
   - Protocol distribution
   - Traffic timeline

4. **Threat Heatmap**
   - Severity distribution over time
   - Visual pattern of attacks

5. **Details Tab**
   - System statistics
   - Database info
   - Sample logs

## Project Structure

```
network_anomaly_detection/
├── data/
│   ├── network_logs.csv      (5000 network records)
│   └── network_logs.db       (SQLite database)
├── src/
│   ├── log_generator.py      (Generate synthetic logs)
│   ├── database.py           (ETL & SQL operations)
│   ├── anomaly_detector.py   (Detection rules)
│   └── dashboard.py          (Streamlit UI)
├── requirements.txt          (Dependencies)
└── README.md                 (Full documentation)
```

## Anomaly Detection Rules (What's Detected)

1. **Port Scanning** - 10+ different ports from same IP
2. **DDoS Attacks** - 100+ connections to same destination in 60s
3. **Brute Force** - 20+ connection attempts on SSH in 5 min
4. **Data Exfiltration** - 10MB+ data transfer outbound
5. **Uncommon Ports** - Traffic on dangerous/rare ports
6. **Suspicious IPs** - Known malicious IP ranges

## Demo Talking Points

- "Built a data engineering pipeline that ingests 5000 network logs"
- "Implemented 6 detection rules for various attack patterns"
- "Detected 200+ anomalies with rule-based engine"
- "Interactive Streamlit dashboard for real-time monitoring"
- "SQLite database for efficient querying"
- "Can be extended with ML models for improved accuracy"

## System Requirements

- Python 3.8+
- pip
- ~500MB disk space
- Internet (for pip install only)

## Troubleshooting

**Error: "streamlit: command not found"**
```bash
pip install streamlit
```

**Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Error: "port 8501 already in use"**
```bash
streamlit run src/dashboard.py --server.port 8502
```

## Next Steps (by Wednesday)

For the full project, we'll add:
- ✅ Basic detection rules (DONE)
- ✅ Interactive dashboard (DONE)
- 📅 ML-based anomaly detection (Isolation Forest)
- 📅 Real-time streaming processing
- 📅 Advanced network visualizations
- 📅 Predictive alerting system

---

**Ready to demo?** Run: `streamlit run src/dashboard.py`
