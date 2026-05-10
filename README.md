# Real-Time-Transit-Analytics-Forecasting-System-GTFS-ML-

# 🚌 Transit Analytics & Real-Time Forecasting System

A complete end-to-end transit intelligence platform that transforms raw GTFS data into actionable operational insights - combining machine learning, time-series forecasting, real-time alerting, and an interactive Streamlit dashboard.

> Built using Auckland Transport GTFS static data. Real-time GTFS-RT Trip Updates were simulated via a dummy dataset due to API access constraints.

---

## 📸 Dashboard Preview

| Headway Analytics | Delay Analytics |
|---|---|
|<img width="1827" height="810" alt="image" src="https://github.com/user-attachments/assets/6d5a592f-127d-4043-bd06-36e38cbe0e5d" />
| <img width="1852" height="847" alt="ss2" src="https://github.com/user-attachments/assets/63ef21ba-aa4b-4bb6-aafd-b667cc1b6c70" />
|

| Route Comparison | Real-Time Forecasting |
|---|---|
| <img width="1827" height="810" alt="ss3" src="https://github.com/user-attachments/assets/ce6ca146-755d-4717-8359-2e2a7c874095" />
| <img width="1782" height="840" alt="ss4" src="https://github.com/user-attachments/assets/ff128c04-8ec0-4973-a0c2-0443d062a36c" />
|

---

## 🗂 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Machine Learning Models](#machine-learning-models)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Dashboard Pages](#dashboard-pages)
- [Deployment](#deployment)
- [Limitations & Future Work](#limitations--future-work)

---

## Overview

Traditional transit dashboards are retrospective - they show what went wrong, not what's about to. This system addresses that gap by:

- Predicting delays and bus bunching before they escalate
- Forecasting headways 15–60 minutes ahead using Prophet
- Generating real-time alerts (HIGH / MEDIUM / LOW) for operators
- Explaining model predictions via SHAP for transparency

---

## System Architecture

The pipeline is organized into seven layers:

```
┌─────────────────────────────────────────────┐
│           1. Data Ingestion Layer           │
│   GTFS Static + Dummy GTFS-RT Trip Updates  │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│     2. Data Processing & Feature Eng.       │
│  Headways · Delays · Bunching · Lag Features│
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│         3. Machine Learning Models          │
│  Delay Classifier · Bunching Classifier     │
│         Prophet Headway Forecaster          │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│           4. Real-Time Engine               │
│   Live Feed Simulation · Alerts Engine      │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│         5. Streamlit Dashboard              │
│  Analytics · Predictions · Alerts · SHAP   │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│             6. AI Layer                     │
│   SHAP Explainability · Azure OpenAI NLG    │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│            7. Deployment Layer              │
│  Streamlit Cloud · Azure App Service        │
└─────────────────────────────────────────────┘
```

---

## Features

**Analytics**
- Headway distribution and trend analysis
- Delay pattern breakdown by route, stop, and time of day
- On-time performance (OTP) and reliability metrics
- Bunching heatmaps by hour and day
- Route performance scoring and comparison
- Stop-level heatmaps

**Predictions**
- Delay severity classification (on-time / slight / severe)
- Bus bunching probability prediction
- 15–60 minute headway forecasting with confidence intervals

**Real-Time Operations**
- Live feed simulation from dummy GTFS-RT data
- Automated alert engine with three severity levels:
  - 🔴 HIGH — severe delays
  - 🟡 MEDIUM — active bunching
  - 🔵 LOW — short headways / early warnings

**AI & Explainability**
- SHAP feature importance for delay predictions
- Azure OpenAI integration for natural-language performance summaries

---

## Machine Learning Models

| Model | Type | Target |
|---|---|---|
| Delay Prediction | RandomForest / XGBoost Classifier | On-time / Slight delay / Severe delay |
| Bunching Prediction | Binary Classifier | Bunching likelihood (True/False) |
| Headway Forecasting |  Prophet | Future headway (min) with upper/lower bounds |

**Key features used:** previous delays, headway variance, lag features, route/stop IDs (encoded), hour of day, day of week, peak/off-peak flag.

All models are persisted via `joblib` in the `/models` directory.

---

## Project Structure

```
transit-analytics/
│
├── data/
│   ├── gtfs_static/          # GTFS schedule files (routes, stops, trips, stop_times)
│   └── dummy_trip_updates/   # Simulated GTFS-RT feed (CSV/JSON)
│
├── models/
│   ├── delay_prediction_model.pkl
│   ├── bunching_prediction_model.pkl
│   ├── headway_forecast_model.pkl
│   ├── route_encoder.pkl
│   └── stop_encoder.pkl
│
├── pages/
│   ├── headways.py
│   ├── delays.py
│   ├── reliability.py
│   ├── bunching_heatmap.py
│   ├── route_comparison.py
│   ├── stop_level_heatmap.py
│   ├── delay_prediction.py
│   ├── bunching_prediction.py
│   ├── realtime_forecasting.py
│   ├── realtime_alerts.py
│   └── shap_explainability.py
│
├── utils/
│   ├── data_processing.py    # Feature engineering pipeline
│   ├── realtime_engine.py    # Alert detection logic
│   └── forecasting.py        # Prophet wrapper
│
├── app.py                    # Main Streamlit entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/your-username/transit-analytics.git
cd transit-analytics
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run app.py
```

### Train Models

```bash
python utils/train_models.py
```

### Key Dependencies

```
streamlit
pandas
numpy
scikit-learn
xgboost
prophet
shap
joblib
plotly
openai  
```

---

## Dashboard Pages

| Page | Description |
|---|---|
| **Headways** | Historical headway distributions and route-level trends |
| **Delays** | Delay patterns, peak-hour analysis, route distributions |
| **Reliability** | OTP, headway variability, bunching rates |
| **Bunching Heatmap** | Bunching intensity across routes and hours |
| **Route Performance Score** | Composite scoring per route |
| **Route Comparison** | Side-by-side OTP, headway std, bunching rate |
| **Stop-Level Heatmap** | Delay/bunching intensity by stop × hour |
| **Delay Prediction** | ML-based delay severity prediction |
| **Bunching Prediction** | Bunching likelihood for route/stop inputs |
| **Real-Time Forecasting** | Prophet headway forecast with confidence bounds |
| **Real-Time Alerts** | Live alert feed from the alerts engine |
| **SHAP Explainability** | Feature importance and local prediction explanations |

---

## Deployment

| Platform | Use Case |
|---|---|
| **Streamlit Cloud** | Demos, prototypes, lightweight production |
| **Azure App Service** | Enterprise hosting with scaling and monitoring |
| **Azure Machine Learning** | Model versioning, retraining, inference endpoints |
| **Power BI Service** | Business-level KPI dashboards for non-technical stakeholders |

### Deploy to Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set entry point to `app.py`
4. Deploy

---

## Limitations & Future Work

**Current Limitations**
- All real-time data is simulated — no live GTFS-RT feed is connected
- Models are trained on dummy data; accuracy on real-world data is untested
- Prophet forecasting page is partially scaffolded (placeholder visible in demo)
- Only route 30 is shown in the real-time feed screenshots

**Planned Extensions**
- [ ] Connect live Auckland Transport GTFS-RT feed once API access is granted
- [ ] Retrain models on real delay and headway data
- [ ] Reinforcement learning for optimal bus dispatch intervals
- [ ] Route-wide Prophet forecasting (currently single-route)
- [ ] Mobile-responsive dashboard layout

---

## Data Sources

- **GTFS Static**: Auckland Transport public feed
- **GTFS-RT Trip Updates**: Simulated dummy dataset (real access not granted during development)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
