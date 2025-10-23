import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Denver Temperature Timeline", page_icon="🌡️", layout="wide")

LAT, LON = 39.7392, -104.9903

WEATHER_URL = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&hourly=temperature_2m,wind_speed_10m"
    f"&past_days=1"
    f"&forecast_days=1"
    f"&timezone=America/Denver"
)

@st.cache_data(ttl=600)
def fetch_weather_series(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        json = resp.json()
        times = pd.to_datetime(json["hourly"]["time"])
        temps = json["hourly"]["temperature_2m"]
        wind = json["hourly"]["wind_speed_10m"]
        df = pd.DataFrame(
            {"time": times, "temperature": temps, "wind": wind}
        )
        return df
    except Exception:
        return None

st.title("🌡️ Denver Temperature – Timeline Chart")

refresh_sec = st.slider("Auto-refresh every seconds", min_value=10, max_value=300, value=60)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
last_refresh = st.empty()

df = fetch_weather_series(WEATHER_URL)

if df is not None and len(df) > 1:
    st.metric("Latest Temp (°C)", df["temperature"].iloc[-1])
    st.metric("Latest Wind (m/s)", df["wind"].iloc[-1])
    fig = px.line(df, x="time", y="temperature", title="Denver Temperature Last 48 Hours")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.tail(24), use_container_width=True)
else:
    st.warning("No time series data available from the API.")

last_refresh.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

if auto_refresh:
    time.sleep(refresh_sec)
    fetch_weather_series.clear()  # Clear cache before rerun
    st.rerun()
