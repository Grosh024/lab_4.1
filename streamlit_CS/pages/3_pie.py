import streamlit as st
import pandas as pd
from pathlib import Path
from io import StringIO, BytesIO

import plotly.express as px

st.set_page_config(page_title="Pie Demo", layout="centered")

st.title("Pie Demo — load pie_demo.csv")

# Try to find pie_demo.csv in the repo (search current working dir)
def find_pie_csv():
    cwd = Path.cwd()
    matches = list(cwd.rglob("pie_demo.csv"))
    return matches[0] if matches else None

csv_path = find_pie_csv()

uploaded = None
if csv_path:
    st.success(f"Found CSV: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Failed to read {csv_path}: {e}")
        df = None
else:
    st.info("pie_demo.csv not found in the project. You can upload it manually.")
    uploaded = st.file_uploader("Upload pie_demo.csv", type=["csv"])
    if uploaded is not None:
        # uploaded can be BytesIO or StringIO depending on uploader
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")
            df = None
    else:
        df = None

if df is None:
    st.stop()

st.subheader("Preview")
st.dataframe(df.head())

if df.shape[1] < 2:
    st.error("CSV must contain at least two columns (labels and values).")
    st.stop()

# Let user choose label and value columns (defaults: first two)
label_col = st.selectbox("Label column", options=list(df.columns), index=0)
value_col = st.selectbox("Value column (numeric)", options=list(df.columns), index=1)

# Ensure values are numeric
values = pd.to_numeric(df[value_col], errors="coerce")
if values.isna().all():
    st.error(f"Selected value column '{value_col}' does not contain any numeric data.")
    st.stop()

plot_df = df.copy()
plot_df[value_col] = values.fillna(0)

st.subheader("Pie Chart")
fig = px.pie(plot_df, names=label_col, values=value_col, title=f"Pie of {value_col}")
st.plotly_chart(fig, use_container_width=True)