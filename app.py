
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="AQUANEX | Ocean Intelligence",
    page_icon="🌊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top right,
        #123F60 0%, #071B30 42%, #030B17 100%);
    color: #EAF8FF;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1 {
    color: #75E8FF !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: 3px;
}
h2, h3 {
    color: #8BEAFF !important;
}
p, label, .stCaption {
    color: #B7D8E9 !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg,
        rgba(16,57,83,0.95),
        rgba(7,25,45,0.95));
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #23617C;
    box-shadow: 0 0 18px rgba(0,190,255,0.09);
}
[data-testid="stMetricLabel"] {
    color: #B7D8E9 !important;
}
[data-testid="stMetricValue"] {
    color: #70E7FF !important;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(90deg, #087EA4, #10B9CF);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
}
hr {
    border-color: #24516A;
}
</style>
""", unsafe_allow_html=True)

# Readings history
if "readings" not in st.session_state:
    st.session_state.readings = []
    temp = 26.4
    turbidity = 850

    for _ in range(10):
        temp += random.uniform(-0.3, 0.3)
        turbidity += random.randint(-35, 35)

        st.session_state.readings.append({
            "Timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Water Temperature (°C)": round(temp, 2),
            "Turbidity Signal (ADC)": max(
                0, min(4095, turbidity)
            )
        })

# Header
st.title("🌊 AQUANEX")
st.subheader("AUTONOMOUS OCEAN OBSERVATION PLATFORM")

left, right = st.columns([2.5, 1])

with left:
    st.markdown(
        "Ocean Intelligence  |  Environmental Monitoring"
    )

with right:
    if st.button("↻  REFRESH LATEST READING",
                 type="primary",
                 use_container_width=True):
        prev = st.session_state.readings[-1]

        st.session_state.readings.append({
            "Timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Water Temperature (°C)": round(
                max(0, prev["Water Temperature (°C)"]
                    + random.uniform(-0.4, 0.4)), 2
            ),
            "Turbidity Signal (ADC)": max(
                0, min(
                    4095,
                    prev["Turbidity Signal (ADC)"]
                    + random.randint(-50, 50)
                )
            )
        })

        st.session_state.readings = (
            st.session_state.readings[-100:]
        )
        st.rerun()

df = pd.DataFrame(st.session_state.readings)
latest = df.iloc[-1]
temp = float(latest["Water Temperature (°C)"])

# Illustrative temperature status thresholds
if temp < 20 or temp > 32:
    status = "Critical"
elif temp < 23 or temp > 30:
    status = "Warning"
else:
    status = "Normal"

st.divider()
st.markdown("## PLATFORM STATUS")

s1, s2, s3 = st.columns(3)

with s1:
    if status == "Normal":
        st.success("● NORMAL")
    elif status == "Warning":
        st.warning("● WARNING")
    else:
        st.error("● CRITICAL")
    st.caption("Temperature-based status")

with s2:
    st.markdown("### 🌡️ Temperature")
    st.caption("Environmental parameter")

with s3:
    st.markdown("### 💧 Turbidity")
    st.caption("Sensor signal monitoring")

st.divider()
st.markdown("## LATEST OBSERVATIONS")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("WATER TEMPERATURE",
              f"{temp:.2f} °C")

with m2:
    st.metric("TURBIDITY SIGNAL",
              f"{int(latest['Turbidity Signal (ADC)'])} ADC")

with m3:
    st.metric("TOTAL RECORDS", len(df))

st.divider()
st.markdown("## OCEAN DATA ANALYTICS")

g1, g2 = st.columns(2)

with g1:
    st.markdown("### Temperature Trend")
    st.line_chart(
        df.set_index("Timestamp")[["Water Temperature (°C)"]]
    )

with g2:
    st.markdown("### Turbidity Trend")
    st.line_chart(
        df.set_index("Timestamp")[["Turbidity Signal (ADC)"]]
    )

st.divider()
st.markdown("## OBSERVATION HISTORY")

st.dataframe(
    df.iloc[::-1],
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇  DOWNLOAD READINGS (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="aquanex_ocean_readings.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()
st.caption(
    "AQUANEX  •  Autonomous Ocean Observation Platform"
)
