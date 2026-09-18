"""Streamlit dashboard for network anomaly detection."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database import NetworkLogDatabase
from anomaly_detector import NetworkAnomalyDetector
from datetime import datetime, timedelta
import os

# Set page config
st.set_page_config(
    page_title="Network Anomaly Detection",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .anomaly-high {
        color: #d32f2f;
        font-weight: bold;
    }
    .anomaly-medium {
        color: #f57c00;
        font-weight: bold;
    }
    .anomaly-low {
        color: #fbc02d;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def init_database():
    """Initialize database connection."""
    db = NetworkLogDatabase()
    return db

def load_and_process_data(db):
    """Load data and detect anomalies."""
    csv_file = os.path.join(os.path.dirname(__file__), "../data/network_logs.csv")

    # Check if logs already in database
    existing_logs = db.get_all_logs()

    if len(existing_logs) == 0 and os.path.exists(csv_file):
        db.load_logs_from_csv(csv_file)
        db.compute_hourly_stats()

        detector = NetworkAnomalyDetector(db)
        detector.detect_all_anomalies()

# Main app
st.title("🔒 Network Anomaly Detection System")
st.markdown("Real-time monitoring and detection of suspicious network activities")

# Initialize database
db = init_database()

# Load data
load_and_process_data(db)

# Get data
all_logs = db.get_all_logs()
anomalies = db.get_anomalies()
top_ips = db.get_top_ips(10)

if len(all_logs) == 0:
    st.warning("No data loaded. Please run log_generator.py first.")
    st.stop()

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Connections", f"{len(all_logs):,}")

with col2:
    anomaly_count = len(anomalies)
    st.metric("Anomalies Detected", f"{anomaly_count:,}", delta=f"{(anomaly_count/len(all_logs)*100):.1f}%")

with col3:
    unique_ips = len(all_logs['src_ip'].unique())
    st.metric("Unique Source IPs", f"{unique_ips:,}")

with col4:
    total_data = all_logs['bytes_sent'].sum() / 1e9
    st.metric("Total Data Sent (GB)", f"{total_data:.2f}")

st.divider()

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🚨 Anomalies",
    "📈 Traffic Analysis",
    "🔴 Threat Heatmap",
    "ℹ️ Details"
])

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Anomaly Types Distribution")
        if len(anomalies) > 0:
            anomaly_counts = anomalies['anomaly_type'].value_counts()
            fig = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No anomalies detected")

    with col2:
        st.subheader("Severity Distribution")
        if len(anomalies) > 0:
            severity_counts = anomalies['severity'].value_counts()
            colors = {'CRITICAL': '#d32f2f', 'HIGH': '#f57c00', 'MEDIUM': '#fbc02d', 'LOW': '#388e3c'}
            fig = go.Figure(data=[
                go.Bar(
                    y=severity_counts.index,
                    x=severity_counts.values,
                    orientation='h',
                    marker=dict(color=[colors.get(s, '#999999') for s in severity_counts.index])
                )
            ])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No anomalies detected")

# Tab 2: Anomalies
with tab2:
    st.subheader("Detected Anomalies")

    if len(anomalies) > 0:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            severity_filter = st.multiselect(
                "Filter by Severity",
                options=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                default=['CRITICAL', 'HIGH']
            )
        with col2:
            type_filter = st.multiselect(
                "Filter by Type",
                options=anomalies['anomaly_type'].unique(),
                default=anomalies['anomaly_type'].unique()
            )
        with col3:
            st.write("")  # Spacer

        # Apply filters
        filtered_anomalies = anomalies[
            (anomalies['severity'].isin(severity_filter)) &
            (anomalies['anomaly_type'].isin(type_filter))
        ]

        if len(filtered_anomalies) > 0:
            display_cols = ['timestamp', 'anomaly_type', 'severity', 'src_ip', 'dst_ip', 'description']
            st.dataframe(
                filtered_anomalies[display_cols].sort_values('timestamp', ascending=False),
                use_container_width=True,
                height=500
            )
        else:
            st.info("No anomalies match the selected filters")
    else:
        st.info("No anomalies detected in the network logs")

# Tab 3: Traffic Analysis
with tab3:
    st.subheader("Network Traffic Patterns")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Source IPs")
        if len(top_ips) > 0:
            fig = px.bar(
                top_ips,
                x='count',
                y='src_ip',
                orientation='h',
                labels={'count': 'Connections', 'src_ip': 'IP Address'},
                color='total_bytes'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Protocol Distribution")
        protocol_counts = all_logs['protocol'].value_counts()
        fig = px.pie(
            values=protocol_counts.values,
            names=protocol_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Traffic Timeline (Last 24 Hours)")
    all_logs['hour'] = pd.to_datetime(all_logs['timestamp']).dt.floor('h')
    hourly_traffic = all_logs.groupby('hour').agg({
        'id': 'count',
        'bytes_sent': 'sum',
        'bytes_recv': 'sum'
    }).reset_index()
    hourly_traffic.columns = ['hour', 'connections', 'bytes_sent', 'bytes_recv']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_traffic['hour'],
        y=hourly_traffic['connections'],
        mode='lines+markers',
        name='Connections'
    ))
    fig.update_layout(height=400, title="Connections per Hour")
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Threat Heatmap
with tab4:
    st.subheader("Threat Activity Heatmap")

    if len(anomalies) > 0:
        anomalies['hour'] = pd.to_datetime(anomalies['timestamp']).dt.floor('h')
        threat_matrix = anomalies.groupby(['hour', 'severity']).size().unstack(fill_value=0)

        fig = px.imshow(
            threat_matrix,
            labels=dict(x="Severity", y="Hour", color="Count"),
            color_continuous_scale="RdYlGn_r"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No anomalies to display in heatmap")

# Tab 5: Details
with tab5:
    st.subheader("System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Database Statistics**")
        st.write(f"- Total Records: {len(all_logs):,}")
        st.write(f"- Anomalies Found: {len(anomalies):,}")
        st.write(f"- Detection Rate: {(len(anomalies)/len(all_logs)*100):.2f}%")
        st.write(f"- Unique Source IPs: {all_logs['src_ip'].nunique():,}")
        st.write(f"- Unique Destination IPs: {all_logs['dst_ip'].nunique():,}")

    with col2:
        st.write("**Traffic Summary**")
        st.write(f"- Total Bytes Sent: {all_logs['bytes_sent'].sum()/1e9:.2f} GB")
        st.write(f"- Total Bytes Received: {all_logs['bytes_recv'].sum()/1e9:.2f} GB")
        st.write(f"- Average Connection Duration: {all_logs['duration_sec'].mean():.1f}s")
        st.write(f"- Time Range: {all_logs['timestamp'].min()} to {all_logs['timestamp'].max()}")

    st.divider()
    st.subheader("Sample Network Logs")
    st.dataframe(
        all_logs[['timestamp', 'src_ip', 'dst_ip', 'dst_port', 'protocol', 'bytes_sent', 'flag']].head(20),
        use_container_width=True
    )

st.divider()
st.markdown("---")
st.markdown("🔒 **Network Anomaly Detection System** | Built with Streamlit | Data Engineering Project")
