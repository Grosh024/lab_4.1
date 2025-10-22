import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Denver Temp Timeline", page_icon="🌡️", layout="wide")

LAT, LON = 39.7392, -104.9903
WEATHER_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,wind_speed_10m"

@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        j = resp.json()["current"]
        return pd.DataFrame([{
            "time": pd.to_datetime(j["time"]),
            "temperature": j["temperature_2m"],
            "wind": j["wind_speed_10m"]
        }])
    except Exception:
        return None

if "weather_history" not in st.session_state:
    st.session_state.weather_history = pd.DataFrame(columns=["time", "temperature", "wind"])

df = fetch_weather(WEATHER_URL)
if df is not None:
    st.session_state.weather_history = pd.concat([st.session_state.weather_history, df]).drop_duplicates(subset=["time"], keep="last")

st.title("🌡️ Denver Temperature – Live Timeline")
st.metric("Current Temp (°C)", df["temperature"].iloc[-1] if df is not None else "N/A")
st.metric("Wind Speed (m/s)", df["wind"].iloc[-1] if df is not None else "N/A")

if len(st.session_state.weather_history) > 1:
    fig = px.line(st.session_state.weather_history, x="time", y="temperature", title="Denver Temperature Over Time (°C)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Waiting for multiple readings to show a line chart. Leave this page open or refresh.")

st.dataframe(st.session_state.weather_history, use_container_width=True)

refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto-refresh", value=False)

if auto_refresh:
    time.sleep(refresh_sec)
    st.rerun()
