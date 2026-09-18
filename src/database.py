"""Database setup and ETL pipeline for network logs."""
import sqlite3
import pandas as pd
from datetime import datetime
import os

class NetworkLogDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "../data/network_logs.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialize database schema."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Network logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                src_ip TEXT,
                dst_ip TEXT,
                src_port INTEGER,
                dst_port INTEGER,
                protocol TEXT,
                bytes_sent INTEGER,
                bytes_recv INTEGER,
                duration_sec INTEGER,
                flag TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id INTEGER,
                anomaly_type TEXT,
                severity TEXT,
                description TEXT,
                timestamp DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(log_id) REFERENCES network_logs(id)
            )
        ''')

        # Statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hourly_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hour_start DATETIME,
                total_connections INTEGER,
                anomaly_count INTEGER,
                total_bytes_sent INTEGER,
                total_bytes_recv INTEGER,
                unique_src_ips INTEGER,
                unique_dst_ips INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Indexes supporting time-window and per-host lookups
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_ts ON network_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_src ON network_logs(src_ip, timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_dst ON network_logs(dst_ip, timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_dst_port ON network_logs(dst_ip, dst_port, timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomalies_log ON anomalies(log_id)')

        self.conn.commit()
        print("Database initialized successfully")

    def load_logs_from_csv(self, csv_file):
        """Load network logs from CSV file."""
        df = pd.read_csv(csv_file)

        # Store timestamps in SQLite's own 'YYYY-MM-DD HH:MM:SS' form so that
        # string comparison in time-window queries is valid.
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

        cursor = self.conn.cursor()

        cursor.executemany('''
            INSERT INTO network_logs
            (timestamp, src_ip, dst_ip, src_port, dst_port, protocol,
             bytes_sent, bytes_recv, duration_sec, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', df[['timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port',
                 'protocol', 'bytes_sent', 'bytes_recv', 'duration_sec',
                 'flag']].itertuples(index=False, name=None))

        self.conn.commit()
        print(f"Loaded {len(df)} logs from CSV")

    def get_all_logs(self):
        """Get all logs as DataFrame."""
        query = "SELECT * FROM network_logs ORDER BY timestamp DESC"
        return pd.read_sql_query(query, self.conn)

    def latest_log_time(self):
        """Newest log timestamp, used as the anchor for time windows.

        The dataset carries its own clock, so windows are measured from the
        newest log rather than from the current wall-clock time.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(timestamp) FROM network_logs")
        return cursor.fetchone()[0]

    def get_recent_logs(self, hours=24):
        """Get logs from the last N hours of the dataset."""
        query = """
            SELECT * FROM network_logs
            WHERE timestamp > datetime((SELECT MAX(timestamp) FROM network_logs),
                                       ? || ' hours')
            ORDER BY timestamp DESC
        """
        return pd.read_sql_query(query, self.conn, params=('-%d' % hours,))

    def get_anomalies(self):
        """Get all detected anomalies."""
        query = """
            SELECT a.*, l.src_ip, l.dst_ip, l.dst_port, l.protocol
            FROM anomalies a
            JOIN network_logs l ON a.log_id = l.id
            ORDER BY a.timestamp DESC
        """
        return pd.read_sql_query(query, self.conn)

    def add_anomaly(self, log_id, anomaly_type, severity, description, timestamp=None):
        """Record detected anomaly against the time of the offending log."""
        cursor = self.conn.cursor()
        if timestamp is None:
            cursor.execute("SELECT timestamp FROM network_logs WHERE id = ?", (log_id,))
            row = cursor.fetchone()
            timestamp = row[0] if row else None
        cursor.execute('''
            INSERT INTO anomalies (log_id, anomaly_type, severity, description, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (log_id, anomaly_type, severity, description, timestamp))

    def compute_hourly_stats(self):
        """Compute hourly statistics."""
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM hourly_stats")

        query = """
            INSERT INTO hourly_stats
            (hour_start, total_connections, anomaly_count, total_bytes_sent,
             total_bytes_recv, unique_src_ips, unique_dst_ips)
            SELECT
                strftime('%Y-%m-%d %H:00:00', timestamp) as hour_start,
                COUNT(*) as total_connections,
                SUM(CASE WHEN flag='ANOMALY' THEN 1 ELSE 0 END) as anomaly_count,
                SUM(bytes_sent) as total_bytes_sent,
                SUM(bytes_recv) as total_bytes_recv,
                COUNT(DISTINCT src_ip) as unique_src_ips,
                COUNT(DISTINCT dst_ip) as unique_dst_ips
            FROM network_logs
            WHERE timestamp > datetime((SELECT MAX(timestamp) FROM network_logs),
                                       '-24 hours')
            GROUP BY hour_start
            ORDER BY hour_start DESC
        """

        cursor.execute(query)
        self.conn.commit()

    def get_top_ips(self, limit=10):
        """Get top source IPs by connection count."""
        query = f"""
            SELECT src_ip, COUNT(*) as count, SUM(bytes_sent) as total_bytes
            FROM network_logs
            GROUP BY src_ip
            ORDER BY count DESC
            LIMIT {limit}
        """
        return pd.read_sql_query(query, self.conn)

    def get_suspicious_ips(self, limit=10):
        """Get IPs with anomalies."""
        query = f"""
            SELECT DISTINCT l.src_ip, COUNT(a.id) as anomaly_count
            FROM network_logs l
            LEFT JOIN anomalies a ON l.id = a.log_id
            WHERE a.id IS NOT NULL
            GROUP BY l.src_ip
            ORDER BY anomaly_count DESC
            LIMIT {limit}
        """
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # Test database
    db = NetworkLogDatabase()
    csv_path = os.path.join(os.path.dirname(__file__), "../data/network_logs.csv")
    db.load_logs_from_csv(csv_path)
    db.compute_hourly_stats()

    logs = db.get_all_logs()
    print(f"\nTotal logs in database: {len(logs)}")
    print(f"Anomalies in logs: {len(logs[logs['flag'] == 'ANOMALY'])}")

    top_ips = db.get_top_ips()
    print("\nTop Source IPs:")
    print(top_ips)

    db.close()
