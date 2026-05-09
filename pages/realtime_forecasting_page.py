import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.express as px

from realtime_forecasting_utils import (
    forecast_next_headways,
    forecast_next_delays
)

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("Real‑Time Transit Forecasting")

# -----------------------------
# SAFE AUTO-REFRESH
# -----------------------------
st_autorefresh(interval=30_000, key="realtime_refresh")

st.write("Live headway + delay predictions using Prophet models.")

df = pd.read_csv("dummy_trip_updates.csv")

routes = sorted(df["route_id"].unique())
route = st.selectbox("Select Route", routes)

stops = sorted(df[df["route_id"] == route]["stop_id"].unique())
stop = st.selectbox("Select Stop", stops)

df_recent = df[(df["route_id"] == route) & (df["stop_id"] == stop)].tail(10)

if df_recent.empty:
    st.warning("No recent data available for this route/stop.")
    st.stop()

st.subheader("Recent Arrivals (Simulated Real‑Time Feed)")
st.dataframe(df_recent[["arrival_time", "delay", "stop_id"]])

st.subheader("🔮 Headway Forecast (Next 30 Minutes)")
try:
    forecast_hw = forecast_next_headways(route, stop, df_recent, 30)
    st.dataframe(forecast_hw)

    fig_hw = px.line(
        forecast_hw,
        x="ds",
        y="yhat",
        title="Predicted Headways (minutes)",
        markers=True
    )
    st.plotly_chart(fig_hw, use_container_width=True)
except Exception:
    st.error(f"Headway model not found for {route} / {stop}")
    st.stop()

st.subheader("⏱ Delay Forecast (Next 30 Minutes)")
try:
    forecast_dl = forecast_next_delays(route, stop, df_recent, 30)
    st.dataframe(forecast_dl)

    fig_dl = px.line(
        forecast_dl,
        x="ds",
        y="yhat",
        title="Predicted Delay (minutes)",
        markers=True
    )
    st.plotly_chart(fig_dl, use_container_width=True)
except Exception:
    st.error(f"Delay model not found for {route} / {stop}")
