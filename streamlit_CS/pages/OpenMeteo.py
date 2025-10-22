import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Live Weather (Denver)", page_icon="🌡️", layout="wide")
st.markdown("""
    <br>  [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
      transition: none !important;
      opacity: 1 !important;
    }
""", unsafe_allow_html=True)

st.title("🌡️ Live Denver Temperature (Open-Meteo)")
st.caption("Auto-refreshing live weather: current temperature and wind speed from Open-Meteo.")

# --- Weather API Config ---
LAT, LON = 39.7392, -104.9903
WEATHER_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,wind_speed_10m"

@st.cache_data(ttl=600)
def fetch_weather(url: str):
    """Return (df, error_message) — never raise."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        j = resp.json()["current"]
        df = pd.DataFrame([{
            "time": pd.to_datetime(j["time"]),
            "temperature": j["temperature_2m"],
            "wind": j["wind_speed_10m"]
        }])
        return df, None
    except requests.RequestException as e:
        return None, f"Network/API error: {e}"

# --- Auto Refresh Controls ---
st.subheader("🔁 Auto Refresh Settings")
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

# --- Main View ---
st.subheader("Denver Weather")
df, err = fetch_weather(WEATHER_URL)
if err or df is None:
    st.warning("Can't load live weather. Try again later!")
else:
    st.metric("Current Temperature (°C)", df["temperature"].iloc[-1])
    st.metric("Wind Speed (m/s)", df["wind"].iloc[-1])
    fig = px.line(df, x="time", y="temperature", title="Denver Temperature (°C) — Live")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True)

if auto_refresh:
    time.sleep(refresh_sec)
    fetch_weather.clear()
    st.rerun()
