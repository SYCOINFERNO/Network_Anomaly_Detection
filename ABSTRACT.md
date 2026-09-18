# Network Logs Anomaly Detection

## Abstract

Network intrusion attempts leave traces in connection logs, but the volume of
those logs makes manual inspection impractical. This project builds an
end-to-end pipeline that ingests network traffic logs, stores them in a
queryable form, and flags suspicious activity through a set of rule-based
detectors.

A synthetic dataset of 5,000 connection records spanning seven days is
generated to model a small internal network. The dataset combines ordinary
outbound traffic with five classes of simulated attack — port scanning,
distributed denial of service, SSH brute force, data exfiltration, and access
to legacy services on dangerous ports. Attack traffic is emitted in bursts
rather than as isolated events, because the temporal density of connections is
itself the signal a detector relies on.

An ETL stage normalises these records and loads them into a SQLite database
with indexes supporting time-window queries. Six detection rules then evaluate
each record against the traffic that preceded it, using windows anchored on the
record's own timestamp so that results depend only on the data and never on the
time of execution. The system flags approximately 5.4% of records as anomalous
and attributes each to a specific rule and severity. Results are presented in
an interactive Streamlit dashboard providing summary metrics, filtering, traffic
analysis, and threat visualisation.

**Keywords:** network security, anomaly detection, ETL pipeline, intrusion
detection, data engineering, SQLite, Streamlit

---

## Summary

### What the project does

The system takes network connection logs and finds the suspicious ones. It runs
in four stages:

1. **Generate** — produce 5,000 synthetic log records covering seven days of
   traffic on a `192.168.1.x` network, mixing normal activity with simulated
   attacks.
2. **Load** — parse the records, normalise timestamps, and insert them into a
   SQLite database with indexes on time, source, and destination.
3. **Detect** — run six rules over every record and write each match to an
   `anomalies` table with a type, severity, and description.
4. **Display** — serve an interactive dashboard summarising what was found.

### The six detection rules

| Rule | Triggers when | Severity |
|---|---|---|
| Port scanning | One source contacts more than 10 distinct ports within 5 minutes | Medium |
| DDoS | One destination receives more than 100 connections within 60 seconds | High |
| Brute force | One host receives more than 20 connections on port 22 within 5 minutes | High |
| Data exfiltration | One source sends more than 10 MB outbound within 10 minutes | Critical |
| Uncommon port | Traffic reaches a dangerous port (Telnet, SMB, RDP, SQL Server, MongoDB) | Low |
| Suspicious IP | Source address falls in a known-suspicious range | Medium |

### Typical results

From 5,000 records, the system flags around 268 anomalies — a detection rate of
roughly 5.4%. A representative breakdown:

| Anomaly type | Count |
|---|---|
| Suspicious IP | 78 |
| Brute force | 77 |
| DDoS | 60 |
| Port scan | 30 |
| Uncommon port | 12 |
| Data exfiltration | 10 |

### Technology

Python 3, SQLite for storage, pandas for data handling, Streamlit and Plotly for
the dashboard. The full pipeline runs in about 1.2 seconds.

### Design points worth mentioning in a viva

- **Detection windows are anchored on log time, not wall-clock time.** Each rule
  measures the traffic preceding the record it is examining. Running the
  detector at a different hour, or in a different timezone, produces identical
  output.
- **Detection is idempotent.** Re-running the detector over an already-scanned
  database adds nothing, because processed log IDs are tracked.
- **The dataset is reproducible.** Passing a seed to the generator produces a
  byte-identical file, so a demonstration can be repeated exactly.
- **All queries are parameterised**, so no value is ever interpolated into SQL
  as a string.
