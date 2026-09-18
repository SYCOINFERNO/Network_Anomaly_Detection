"""Anomaly detection rules for network traffic."""
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta

class NetworkAnomalyDetector:
    def __init__(self, db):
        self.db = db
        self.suspicious_ips = set()

    def _window_query(self, sql, params, log_ts, time_window_seconds):
        """Run a windowed aggregate over the logs preceding a given log.

        The window ends at the log's own timestamp, so results depend only on
        the data and never on the current wall-clock time or timezone.
        """
        cursor = self.db.conn.cursor()
        cursor.execute(sql, params + (log_ts, '-%d seconds' % time_window_seconds, log_ts))
        row = cursor.fetchone()
        return row[0] if row else None

    def detect_port_scanning(self, src_ip, log_ts, time_window_seconds=300):
        """Detect port scanning activity (many different ports from same IP)."""
        sql = """
            SELECT COUNT(DISTINCT dst_port)
            FROM network_logs
            WHERE src_ip = ?
            AND timestamp > datetime(?, ?)
            AND timestamp <= ?
        """
        port_count = self._window_query(sql, (src_ip,), log_ts, time_window_seconds)

        if port_count is not None and port_count > 10:
            return True, f"Port scanning detected: {port_count} unique ports"
        return False, None

    def detect_ddos(self, dst_ip, log_ts, time_window_seconds=60, packet_threshold=100):
        """Detect DDoS attacks (high connection count to same destination)."""
        sql = """
            SELECT COUNT(*)
            FROM network_logs
            WHERE dst_ip = ?
            AND timestamp > datetime(?, ?)
            AND timestamp <= ?
        """
        connection_count = self._window_query(sql, (dst_ip,), log_ts, time_window_seconds)

        if connection_count is not None and connection_count > packet_threshold:
            return True, f"DDoS detected: {connection_count} connections in {time_window_seconds}s"
        return False, None

    def detect_brute_force(self, dst_ip, dst_port, log_ts, time_window_seconds=300, attempt_threshold=20):
        """Detect brute force attacks (multiple connection attempts to SSH/common ports)."""
        sql = """
            SELECT COUNT(*)
            FROM network_logs
            WHERE dst_ip = ? AND dst_port = ?
            AND timestamp > datetime(?, ?)
            AND timestamp <= ?
        """
        attempt_count = self._window_query(sql, (dst_ip, dst_port), log_ts, time_window_seconds)

        if attempt_count is not None and attempt_count > attempt_threshold:
            return True, f"Brute force detected: {attempt_count} attempts on port {dst_port}"
        return False, None

    def detect_data_exfiltration(self, src_ip, log_ts, time_window_seconds=600, bytes_threshold=10000000):
        """Detect data exfiltration (large data transfer outbound)."""
        sql = """
            SELECT SUM(bytes_sent)
            FROM network_logs
            WHERE src_ip = ?
            AND timestamp > datetime(?, ?)
            AND timestamp <= ?
        """
        total_bytes = self._window_query(sql, (src_ip,), log_ts, time_window_seconds)

        if total_bytes is not None and total_bytes > bytes_threshold:
            return True, f"Data exfiltration suspected: {total_bytes/1e6:.2f}MB transferred"
        return False, None

    def detect_uncommon_ports(self, dst_port, common_ports=None):
        """Detect traffic on uncommon/dangerous ports."""
        if common_ports is None:
            common_ports = {80, 443, 22, 21, 25, 53, 110, 143, 3306, 5432, 8080}

        dangerous_ports = {
            23: "Telnet",
            139: "NetBIOS",
            445: "SMB",
            3389: "RDP",
            1433: "SQL Server",
            27017: "MongoDB"
        }

        if dst_port in dangerous_ports:
            return True, f"Dangerous port {dst_port} ({dangerous_ports[dst_port]}) accessed"

        if dst_port not in common_ports and dst_port < 1024:
            return True, f"Uncommon privileged port {dst_port} accessed"

        return False, None

    def detect_geographical_anomaly(self, src_ip):
        """Detect suspicious geographic patterns."""
        suspicious_ranges = [
            "203.0.113.",  # TEST-NET-3
            "198.51.100.",  # TEST-NET-2
            "192.0.2."     # TEST-NET-1
        ]

        for range_prefix in suspicious_ranges:
            if src_ip.startswith(range_prefix):
                return True, f"Suspicious IP range detected: {src_ip}"

        return False, None

    def detect_all_anomalies(self):
        """Scan all logs and detect anomalies."""
        logs = self.db.get_all_logs()

        anomalies_count = 0

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT DISTINCT log_id FROM anomalies")
        processed = {row[0] for row in cursor.fetchall()}

        for _, log in logs.iterrows():
            log_id = log['id']

            # Skip if already processed
            if log_id in processed:
                continue

            src_ip = log['src_ip']
            dst_ip = log['dst_ip']
            dst_port = log['dst_port']
            log_ts = log['timestamp']

            # Rule 1: Port scanning
            is_anomaly, desc = self.detect_port_scanning(src_ip, log_ts)
            if is_anomaly:
                self.db.add_anomaly(log_id, "PORT_SCAN", "MEDIUM", desc, log_ts)
                anomalies_count += 1
                continue

            # Rule 2: DDoS
            is_anomaly, desc = self.detect_ddos(dst_ip, log_ts)
            if is_anomaly:
                self.db.add_anomaly(log_id, "DDOS", "HIGH", desc, log_ts)
                anomalies_count += 1
                continue

            # Rule 3: Brute force
            is_anomaly, desc = self.detect_brute_force(dst_ip, dst_port, log_ts)
            if is_anomaly:
                self.db.add_anomaly(log_id, "BRUTE_FORCE", "HIGH", desc, log_ts)
                anomalies_count += 1
                continue

            # Rule 4: Data exfiltration
            is_anomaly, desc = self.detect_data_exfiltration(src_ip, log_ts)
            if is_anomaly:
                self.db.add_anomaly(log_id, "DATA_EXFIL", "CRITICAL", desc, log_ts)
                anomalies_count += 1
                continue

            # Rule 5: Uncommon ports
            is_anomaly, desc = self.detect_uncommon_ports(dst_port)
            if is_anomaly:
                self.db.add_anomaly(log_id, "UNCOMMON_PORT", "LOW", desc, log_ts)
                anomalies_count += 1
                continue

            # Rule 6: Suspicious IPs
            is_anomaly, desc = self.detect_geographical_anomaly(src_ip)
            if is_anomaly:
                self.db.add_anomaly(log_id, "SUSPICIOUS_IP", "MEDIUM", desc, log_ts)
                anomalies_count += 1

        self.db.conn.commit()

        print(f"Detected {anomalies_count} anomalies")
        return anomalies_count

if __name__ == "__main__":
    from database import NetworkLogDatabase

    db = NetworkLogDatabase()
    detector = NetworkAnomalyDetector(db)

    detector.detect_all_anomalies()

    anomalies = db.get_anomalies()
    print(f"\nTotal anomalies detected: {len(anomalies)}")
    print("\nTop anomalies:")
    print(anomalies[['anomaly_type', 'severity', 'src_ip', 'timestamp']].head(10))

    db.close()
