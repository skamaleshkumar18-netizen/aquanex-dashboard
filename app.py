
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="AQUANEX Dashboard",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 AQUANEX")
st.subheader("Ocean Observation Platform")
st.caption("Low-Cost Environmental Monitoring | SIH26065")

st.warning("DEMO MODE: Readings are simulated, not real sensor data.")

if "history" not in st.session_state:
    st.session_state.history = []

temperature = round(random.uniform(20, 28), 2)
turbidity = round(random.uniform(10, 80), 2)
now = datetime.now()

alerts = []
if temperature > 27:
    alerts.append("High water temperature detected.")
if turbidity > 70:
    alerts.append("High turbidity detected.")

status = "WARNING" if alerts else "NORMAL"

col1, col2, col3 = st.columns(3)
col1.metric("Water Temperature", f"{temperature} °C")
col2.metric("Turbidity", f"{turbidity} NTU")
col3.metric("Platform Status", status)

st.divider()
st.subheader("Anomaly Detection")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No demo anomalies detected.")

if st.button("Generate New Demo Reading"):
    st.rerun()

st.session_state.history.append({
    "Timestamp": now.strftime("%H:%M:%S"),
    "Temperature (°C)": temperature,
    "Turbidity (NTU)": turbidity,
    "Status": status
})

st.session_state.history = st.session_state.history[-50:]
df = pd.DataFrame(st.session_state.history)

st.divider()
st.subheader("Temperature History")
st.line_chart(df, x="Timestamp", y="Temperature (°C)")

st.subheader("Turbidity History")
st.line_chart(df, x="Timestamp", y="Turbidity (NTU)")

st.subheader("Recent Sensor Readings")
st.dataframe(df.tail(10), use_container_width=True, hide_index=True)

csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Readings as CSV",
    data=csv_data,
    file_name="aquanex_readings.csv",
    mime="text/csv"
)

st.divider()
st.subheader("System Information")
st.write("**Controller:** ESP32 DevKit")
st.write("**Wireless:** LoRa SX1278")
st.write("**Temperature Sensor:** DS18B20")
st.write("**Turbidity Sensor:** Pending integration")
st.write("**Data Source:** Simulated")

st.caption("AQUANEX | Prototype Dashboard")
