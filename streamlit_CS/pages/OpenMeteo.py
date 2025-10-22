import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Denver Weather (Temperature)", page_icon="🌡️", layout="wide")

st.title("🌡️ Denver Temperature Over Time")
st.caption("Live temperature data from Open-Meteo API, cached for efficiency.")

LAT, LON = 39.7392, -104.9903
WEATHER_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,wind_speed_10m"

@st.cache_data(ttl=600)
def get_weather():
    try:
        r = requests.get(WEATHER_URL, timeout=10)
        r.raise_for_status()
        j = r.json()["current"]
        df = pd.DataFrame([{
            "time": pd.to_datetime(j["time"]),
            "temperature": j["temperature_2m"],
            "wind": j["wind_speed_10m"]
        }])
        return df, None
    except Exception as e:
        return None, f"Error: {e}"

df, error = get_weather()
if error or df is None:
    st.warning("Could not load live weather data.")
else:
    st.metric("Current Temperature (°C)", df["temperature"].iloc[-1])
    st.metric("Wind Speed (m/s)", df["wind"].iloc[-1])
    fig = px.line(df, x="time", y="temperature", title="Denver Temperature Over Time (°C)")
    st.plotly_chart(fig, use_container_width=True)
