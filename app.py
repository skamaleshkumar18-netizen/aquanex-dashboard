
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AQUANEX Dashboard",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 AQUANEX")
st.subheader("SIH26065 | Ocean Observation Platform")
st.caption("Low-Cost Autonomous Environmental Monitoring")

st.success("ESP32 Software Test: PASSED")
st.info("Sensor Status: Waiting for hardware connection")

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Water Temperature", "-- °C")
col2.metric("Turbidity", "--")
col3.metric("Platform Status", "READY")

st.divider()
st.subheader("System Information")

st.write("**Controller:** ESP32 DevKit")
st.write("**Wireless Communication:** LoRa SX1278")
st.write("**Temperature Sensor:** DS18B20")
st.write("**Turbidity Sensor:** Pending connection")

st.caption(
    "Dashboard prototype | " +
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

st.warning(
    "No live sensor data yet. Values will be displayed "
    "after the hardware and data connection are completed."
)
