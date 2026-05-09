# ----------------------------------------------------
# TRANSIT ANALYTICS DASHBOARD — SINGLE FILE VERSION
# Modern UI • Plotly • 12 Pages • Light Theme
# ----------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import shap
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------
# PAGE CONFIG (LIGHT THEME)
# ----------------------------------------------------
st.set_page_config(
    page_title="Transit Analytics Dashboard",
    layout="wide",
    page_icon="🚍"
)

# ----------------------------------------------------
# GLOBAL STYLING
# ----------------------------------------------------
st.markdown("""
    <style>
        .big-title {
            font-size: 32px !important;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
        }
        .section-title {
            font-size: 22px !important;
            font-weight: 600;
            color: #333333;
            margin-top: 25px;
        }
        .metric-card {
            padding: 18px;
            border-radius: 12px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            text-align: center;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 700;
            color: #2a4d8f;
        }
        .metric-label {
            font-size: 14px;
            color: #555555;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR NAVIGATION (12 PAGES)
# ----------------------------------------------------
page = st.sidebar.radio(
    "📊 Select Dashboard View",
    [
        "Headways",
        "Delays",
        "Reliability",
        "Bunching Heatmap",
        "Route Performance Score",
        "Route Comparison",
        "Stop-Level Heatmap",
        "Delay Prediction",
        "Bunching Prediction",
        "Real-Time Forecasting",
        "Real-Time Alerts",
        "SHAP Explainability"
    ]
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:/Users/ADMIN/project/data/dummy_trip_updates.csv")

    df["arrival_dt"] = pd.to_datetime(df["arrival_time"], unit="s")
    df = df.sort_values(["route_id", "stop_id", "arrival_dt"])

    df["headway_sec"] = df.groupby(["route_id", "stop_id"])["arrival_dt"].diff().dt.total_seconds()
    df["headway_min"] = df["headway_sec"] / 60
    df["is_bunched"] = df["headway_min"] < 3

    df["delay_min"] = df["delay"] / 60.0
    df["on_time"] = df["delay_min"] <= 1

    df["hour"] = df["arrival_dt"].dt.hour
    df["day_of_week"] = df["arrival_dt"].dt.dayofweek

    df["prev_headway"] = df.groupby(["route_id", "stop_id"])["headway_min"].shift(1).fillna(10)
    df["prev_delay"] = df.groupby(["route_id", "stop_id"])["delay_min"].shift(1).fillna(0)

    return df

df = load_data()

# ----------------------------------------------------
# SUMMARIES
# ----------------------------------------------------
route_summary = df.groupby("route_id").agg(
    avg_headway=("headway_min", "mean"),
    min_headway=("headway_min", "min"),
    max_headway=("headway_min", "max"),
    std_headway=("headway_min", "std"),
    bunching_rate=("is_bunched", "mean")
).reset_index()

delay_route_summary = df.groupby("route_id").agg(
    avg_delay=("delay_min", "mean"),
    max_delay=("delay_min", "max"),
    pct_delayed=("delay_min", lambda x: (x > 0).mean())
).reset_index()

reliability_route_summary = df.groupby("route_id").agg(
    otp=("on_time", "mean"),
    headway_std=("headway_min", "std"),
    bunching_rate=("is_bunched", "mean")
).reset_index()

# ----------------------------------------------------
# UTILITY FUNCTIONS
# ----------------------------------------------------
def kpi_card(label, value):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)

def generate_alerts(df_rt):
    alerts = []
    for _, row in df_rt.iterrows():
        if row["delay_min"] >= 10:
            alerts.append({
                "route": row["route_id"],
                "severity": "HIGH",
                "message": f"Severe delay of {row['delay_min']:.1f} min at stop {row['stop_id']}"
            })
        if row["is_bunched"]:
            alerts.append({
                "route": row["route_id"],
                "severity": "MEDIUM",
                "message": f"Bunching detected near stop {row['stop_id']}"
            })
        if row["headway_min"] <= 2:
            alerts.append({
                "route": row["route_id"],
                "severity": "LOW",
                "message": f"Very short headway ({row['headway_min']:.1f} min)"
            })
    return pd.DataFrame(alerts)

# ====================================================
# PAGE 1 — HEADWAYS
# ====================================================
if page == "Headways":
    st.markdown("<div class='big-title'>🚍 Headway Analytics</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("Average Headway", f"{df['headway_min'].mean():.2f} min")
    with col2:
        kpi_card("Min Headway", f"{df['headway_min'].min():.2f} min")
    with col3:
        kpi_card("Bunching Rate", f"{df['is_bunched'].mean()*100:.1f}%")

    fig = px.histogram(
        df, x="headway_min",
        nbins=40,
        title="Distribution of Headways",
        color_discrete_sequence=["#4a90e2"]
    )
    fig.update_layout(bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Route-Level Headway Summary</div>", unsafe_allow_html=True)
    st.dataframe(route_summary)

# ====================================================
# PAGE 2 — DELAYS
# ====================================================
elif page == "Delays":
    st.markdown("<div class='big-title'>⏱️ Delay Analytics</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("Average Delay", f"{df['delay_min'].mean():.2f} min")
    with col2:
        kpi_card("Max Delay", f"{df['delay_min'].max():.2f} min")
    with col3:
        kpi_card("Delayed Trips", f"{(df['delay_min']>0).mean()*100:.1f}%")

    fig = px.histogram(
        df, x="delay_min",
        nbins=40,
        title="Distribution of Delays",
        color_discrete_sequence=["#e26a6a"]
    )
    fig.update_layout(bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Route-Level Delay Summary</div>", unsafe_allow_html=True)
    st.dataframe(delay_route_summary)

# ====================================================
# PAGE 3 — RELIABILITY
# ====================================================
elif page == "Reliability":
    st.markdown("<div class='big-title'>📈 Reliability Metrics</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("On-Time Performance", f"{df['on_time'].mean()*100:.1f}%")
    with col2:
        kpi_card("Bunching Rate", f"{df['is_bunched'].mean()*100:.1f}%")
    with col3:
        kpi_card("Avg Headway Std", f"{df['headway_min'].std():.2f} min")

    st.markdown("<div class='section-title'>Route Reliability Summary</div>", unsafe_allow_html=True)
    st.dataframe(reliability_route_summary)

# ====================================================
# PAGE 4 — BUNCHING HEATMAP
# ====================================================
elif page == "Bunching Heatmap":
    st.markdown("<div class='big-title'>🔥 Bunching Heatmap</div>", unsafe_allow_html=True)

    heatmap = df.groupby(["route_id", "hour"])["is_bunched"].mean().reset_index()

    fig = px.density_heatmap(
        heatmap,
        x="hour",
        y="route_id",
        z="is_bunched",
        color_continuous_scale="Reds",
        title="Bunching Intensity by Route & Hour"
    )
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Route ID")
    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# PAGE 5 — ROUTE PERFORMANCE SCORE
# ====================================================
elif page == "Route Performance Score":
    st.markdown("<div class='big-title'>🏆 Route Performance Score</div>", unsafe_allow_html=True)

    df_norm = reliability_route_summary.copy()
    df_norm["norm_headway_std"] = 1 - (df_norm["headway_std"] / df_norm["headway_std"].max())
    df_norm["norm_bunching"] = 1 - df_norm["bunching_rate"]
    df_norm["norm_otp"] = df_norm["otp"]

    df_norm["performance_score"] = (
        df_norm["norm_otp"] * 0.4 +
        df_norm["norm_headway_std"] * 0.3 +
        df_norm["norm_bunching"] * 0.3
    ) * 100

    df_norm = df_norm.sort_values("performance_score", ascending=False)

    fig = px.bar(
        df_norm,
        x="route_id",
        y="performance_score",
        title="Route Performance Score",
        color="performance_score",
        color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_title="Route ID", yaxis_title="Score")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Detailed Route Performance</div>", unsafe_allow_html=True)
    st.dataframe(df_norm)

# ====================================================
# PAGE 6 — ROUTE COMPARISON
# ====================================================
elif page == "Route Comparison":
    st.markdown("<div class='big-title'>🔍 Route Comparison</div>", unsafe_allow_html=True)

    routes = sorted(df["route_id"].unique())
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        r1 = st.selectbox("Select Route 1", routes, key="route1")
    with col_sel2:
        r2 = st.selectbox("Select Route 2", routes, key="route2")

    df1 = reliability_route_summary[reliability_route_summary["route_id"] == r1].iloc[0]
    df2 = reliability_route_summary[reliability_route_summary["route_id"] == r2].iloc[0]

    comparison = pd.DataFrame({
        "Metric": ["OTP", "Headway Std", "Bunching Rate"],
        r1: [df1["otp"], df1["headway_std"], df1["bunching_rate"]],
        r2: [df2["otp"], df2["headway_std"], df2["bunching_rate"]],
    })

    st.markdown("<div class='section-title'>Route Comparison Table</div>", unsafe_allow_html=True)
    st.dataframe(comparison)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["OTP", "Headway Std", "Bunching Rate"],
        y=[df1["otp"], df1["headway_std"], df1["bunching_rate"]],
        name=f"Route {r1}",
        marker_color="#4a90e2"
    ))
    fig.add_trace(go.Bar(
        x=["OTP", "Headway Std", "Bunching Rate"],
        y=[df2["otp"], df2["headway_std"], df2["bunching_rate"]],
        name=f"Route {r2}",
        marker_color="#e26a6a"
    ))
    fig.update_layout(barmode="group", title="Route Comparison Metrics")
    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# PAGE 7 — STOP-LEVEL HEATMAP
# ====================================================
elif page == "Stop-Level Heatmap":
    st.markdown("<div class='big-title'>🗺️ Stop-Level Bunching Heatmap</div>", unsafe_allow_html=True)

    stop_heatmap = df.groupby(["stop_id", "hour"])["is_bunched"].mean().reset_index()

    fig = px.density_heatmap(
        stop_heatmap,
        x="hour",
        y="stop_id",
        z="is_bunched",
        color_continuous_scale="Blues",
        title="Bunching Intensity by Stop & Hour"
    )
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Stop ID")
    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# PAGE 8 — DELAY PREDICTION
# ====================================================
elif page == "Delay Prediction":
    st.markdown("<div class='big-title'>🤖 Delay Prediction</div>", unsafe_allow_html=True)
    st.write("Predict whether a bus will be delayed using the trained ML model.")

    model = joblib.load("delay_prediction_model.pkl")
    le_route = joblib.load("route_encoder.pkl")
    le_stop = joblib.load("stop_encoder.pkl")

    routes = sorted(df["route_id"].unique())
    stops = sorted(df["stop_id"].unique())

    col1, col2 = st.columns(2)
    with col1:
        route = st.selectbox("Route", routes)
    with col2:
        stop = st.selectbox("Stop", stops)

    col3, col4, col5 = st.columns(3)
    with col3:
        headway = st.number_input("Headway (min)", 0.0, 60.0, 5.0)
    with col4:
        hour = st.slider("Hour", 0, 23, 8)
    with col5:
        dow = st.slider("Day of Week (0=Mon)", 0, 6, 2)

    prev_delay = st.number_input("Previous Delay (min)", 0.0, 30.0, 0.0)

    if st.button("Predict Delay"):
        X = np.array([[
            headway,
            1 if headway < 3 else 0,
            hour,
            dow,
            prev_delay,
            le_route.transform([route])[0],
            le_stop.transform([stop])[0]
        ]])

        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

        st.success(f"Prediction: {'Delayed' if pred == 1 else 'On Time'} ({prob:.2f} probability)")

# ====================================================
# PAGE 9 — BUNCHING PREDICTION
# ====================================================
elif page == "Bunching Prediction":
    st.markdown("<div class='big-title'>🤖 Bunching Prediction</div>", unsafe_allow_html=True)
    st.write("Predict whether the next bus will bunch (headway < 3 min).")

    model = joblib.load("bunching_prediction_model.pkl")
    le_route = joblib.load("bunch_route_encoder.pkl")
    le_stop = joblib.load("bunch_stop_encoder.pkl")

    routes = sorted(df["route_id"].unique())
    stops = sorted(df["stop_id"].unique())

    col1, col2 = st.columns(2)
    with col1:
        route = st.selectbox("Route", routes)
    with col2:
        stop = st.selectbox("Stop", stops)

    col3, col4, col5 = st.columns(3)
    with col3:
        headway = st.number_input("Current Headway (min)", 0.0, 60.0, 5.0)
    with col4:
        prev_headway = st.number_input("Previous Headway (min)", 0.0, 60.0, 10.0)
    with col5:
        hour = st.slider("Hour", 0, 23, 8)

    dow = st.slider("Day of Week (0=Mon)", 0, 6, 2)

    if st.button("Predict Bunching"):
        X = np.array([[
            headway,
            prev_headway,
            hour,
            dow,
            le_route.transform([route])[0],
            le_stop.transform([stop])[0]
        ]])

        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

        st.success(f"Prediction: {'Bunched' if pred == 1 else 'Normal'} ({prob:.2f} probability)")

# ====================================================
# PAGE 10 — REAL-TIME FORECASTING
# ====================================================
elif page == "Real-Time Forecasting":
    st.markdown("<div class='big-title'>📡 Real-Time Forecasting</div>", unsafe_allow_html=True)
    st.write("This page can be wired to a Prophet model for live headway forecasting.")

    st.info("Demo placeholder: integrate your Prophet model here using latest df tail and forecast future headways.")

    latest = df.sort_values("arrival_dt").tail(100)
    fig = px.line(
        latest,
        x="arrival_dt",
        y="headway_min",
        color="route_id",
        title="Recent Headways (Last 100 Records)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# PAGE 11 — REAL-TIME ALERTS
# ====================================================
elif page == "Real-Time Alerts":
    st.markdown("<div class='big-title'>🚨 Real-Time Alerts</div>", unsafe_allow_html=True)

    st_autorefresh(interval=30_000, key="alerts_refresh")

    df_rt = df.sort_values("arrival_dt").tail(50).copy()
    df_rt["headway_sec"] = df_rt.groupby(["route_id", "stop_id"])["arrival_dt"].diff().dt.total_seconds()
    df_rt["headway_min"] = df_rt["headway_sec"] / 60
    df_rt["is_bunched"] = df_rt["headway_min"] < 3
    df_rt["delay_min"] = df_rt["delay"] / 60.0

    st.markdown("<div class='section-title'>Live Feed (Last 20 Records)</div>", unsafe_allow_html=True)
    st.dataframe(df_rt.tail(20))

    alerts = generate_alerts(df_rt.tail(20))

    st.markdown("<div class='section-title'>Active Alerts</div>", unsafe_allow_html=True)

    if alerts.empty:
        st.success("No active alerts. System stable.")
    else:
        for _, row in alerts.iterrows():
            if row["severity"] == "HIGH":
                st.error(f"[{row['route']}] {row['message']}")
            elif row["severity"] == "MEDIUM":
                st.warning(f"[{row['route']}] {row['message']}")
            else:
                st.info(f"[{row['route']}] {row['message']}")

# ====================================================
# PAGE 12 — SHAP EXPLAINABILITY
# ====================================================
elif page == "SHAP Explainability":
    st.markdown("<div class='big-title'>🧠 SHAP Explainability</div>", unsafe_allow_html=True)
    st.write("This page explains why the delay prediction model makes certain predictions.")

    model = joblib.load("delay_prediction_model.pkl")

    df_shap = df.copy()
    df_shap = df_shap.dropna(subset=["headway_min", "delay_min"])

    feature_cols = ["headway_min", "is_bunched", "hour", "day_of_week", "delay_min"]
    X = df_shap[feature_cols]

    st.markdown("<div class='section-title'>Global Feature Importance</div>", unsafe_allow_html=True)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, X, show=False)
    st.pyplot(fig)

    st.markdown("<div class='section-title'>Local Explanation (Single Prediction)</div>", unsafe_allow_html=True)
    index = st.slider("Select a sample index", 0, len(X) - 1, 0)

    fig2, ax2 = plt.subplots()
    shap.force_plot(
        explainer.expected_value,
        shap_values[index],
        X.iloc[index],
        matplotlib=True,
        show=False
    )
    st.pyplot(fig2)
