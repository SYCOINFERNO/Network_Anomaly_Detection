"""Generate synthetic network logs with normal and anomalous traffic patterns."""
import csv
import random
from datetime import datetime, timedelta
import os

def generate_network_logs(num_records=5000, output_file=None, seed=None):
    """Generate network logs with normal and anomalous patterns.

    Pass a seed to reproduce an identical dataset.
    """
    if seed is not None:
        random.seed(seed)

    if output_file is None:
        output_file = os.path.join(os.path.dirname(__file__), "../data/network_logs.csv")

    # Common IPs (internal network)
    internal_ips = [f"192.168.1.{i}" for i in range(10, 100)]

    # External IPs (some legitimate, some suspicious)
    legitimate_external = [
        "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
        "208.67.222.222", "208.67.220.220"
    ]

    suspicious_ips = [
        f"203.0.113.{i}" for i in range(1, 50)
    ] + [
        f"198.51.100.{i}" for i in range(1, 50)
    ]

    common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 3306, 5432]

    logs = []
    start_time = datetime.now() - timedelta(days=7)
    window_seconds = 604800  # seven days

    def record(timestamp, src_ip, dst_ip, dst_port, protocol,
               bytes_sent, bytes_recv, duration, flag):
        return {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': random.randint(1024, 65535),
            'dst_port': dst_port,
            'protocol': protocol,
            'bytes_sent': bytes_sent,
            'bytes_recv': bytes_recv,
            'duration_sec': duration,
            'flag': flag
        }

    def campaign_start(duration_seconds):
        """Pick a start time leaving room for a burst of the given length."""
        return start_time + timedelta(
            seconds=random.randint(0, window_seconds - duration_seconds))

    # Attack traffic is emitted in bursts. A scan, a flood or a brute force
    # attempt is only recognisable as a pattern when its connections are
    # packed into a short window, so each campaign shares one attacker, one
    # target and a tight span of time.

    def port_scan_campaign(connections=25, span_seconds=150):
        """One host probing many ports on one target."""
        src_ip = random.choice(suspicious_ips)
        dst_ip = random.choice(internal_ips)
        begin = campaign_start(span_seconds)
        ports = random.sample(range(1, 65536), connections)
        for offset, dst_port in enumerate(ports):
            timestamp = begin + timedelta(
                seconds=int(offset * span_seconds / connections))
            logs.append(record(timestamp, src_ip, dst_ip, dst_port, 'TCP',
                               random.randint(40, 100), random.randint(0, 50),
                               random.randint(1, 5), 'ANOMALY'))

    def ddos_campaign(connections=160, span_seconds=40):
        """A botnet flooding one target with connections."""
        dst_ip = random.choice(internal_ips)
        begin = campaign_start(span_seconds)
        for _ in range(connections):
            timestamp = begin + timedelta(seconds=random.randint(0, span_seconds))
            logs.append(record(timestamp, random.choice(suspicious_ips), dst_ip,
                               random.choice([80, 443]), 'TCP',
                               random.randint(1000, 50000), random.randint(100, 5000),
                               random.randint(1, 30), 'ANOMALY'))

    def brute_force_campaign(attempts=35, span_seconds=240):
        """Repeated SSH login attempts against one host."""
        src_ip = random.choice(suspicious_ips)
        dst_ip = random.choice(internal_ips)
        begin = campaign_start(span_seconds)
        for _ in range(attempts):
            timestamp = begin + timedelta(seconds=random.randint(0, span_seconds))
            logs.append(record(timestamp, src_ip, dst_ip, 22, 'TCP',
                               random.randint(100, 500), random.randint(50, 300),
                               random.randint(1, 60), 'ANOMALY'))

    def data_exfil_campaign(transfers=6, span_seconds=420):
        """One internal host pushing a large volume outbound."""
        src_ip = random.choice(internal_ips)
        dst_ip = random.choice(suspicious_ips)
        begin = campaign_start(span_seconds)
        for _ in range(transfers):
            timestamp = begin + timedelta(seconds=random.randint(0, span_seconds))
            logs.append(record(timestamp, src_ip, dst_ip,
                               random.choice([443, 80, 8080]), 'TCP',
                               random.randint(2500000, 4000000), random.randint(100, 1000),
                               random.randint(10, 300), 'ANOMALY'))

    def legacy_service_traffic(events=12):
        """Isolated connections to dangerous legacy ports (Telnet, SMB, RDP).

        These carry no burst pattern, so they reach the uncommon-port rule
        rather than one of the time-window rules.
        """
        for _ in range(events):
            timestamp = start_time + timedelta(seconds=random.randint(0, window_seconds))
            logs.append(record(timestamp, random.choice(internal_ips),
                               random.choice(internal_ips),
                               random.choice([23, 139, 445, 3389, 1433, 27017]),
                               'TCP', random.randint(200, 8000),
                               random.randint(100, 20000),
                               random.randint(1, 120), 'ANOMALY'))

    ddos_campaign()
    for _ in range(2):
        port_scan_campaign()
    brute_force_campaign()
    for _ in range(3):
        data_exfil_campaign()
    legacy_service_traffic()

    # Normal traffic fills the rest of the week at an even rate.
    for _ in range(num_records - len(logs)):
        timestamp = start_time + timedelta(seconds=random.randint(0, window_seconds))
        logs.append(record(timestamp, random.choice(internal_ips),
                           random.choice(legitimate_external),
                           random.choice(common_ports),
                           random.choice(['TCP', 'UDP']),
                           random.randint(100, 10000), random.randint(100, 50000),
                           random.randint(1, 300), 'NORMAL'))

    logs.sort(key=lambda log: log['timestamp'])

    # Write to CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port',
            'protocol', 'bytes_sent', 'bytes_recv', 'duration_sec', 'flag'
        ])
        writer.writeheader()
        writer.writerows(logs)

    print(f"Generated {num_records} network logs to {output_file}")

    # Print summary
    anomalies = sum(1 for log in logs if log['flag'] == 'ANOMALY')
    print(f"  - Normal traffic: {num_records - anomalies}")
    print(f"  - Anomalous traffic: {anomalies}")

if __name__ == "__main__":
    generate_network_logs()
