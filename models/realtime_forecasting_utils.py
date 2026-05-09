import pandas as pd
import joblib
from pathlib import Path

HEADWAY_MODELS_DIR = Path("headway_models")
DELAY_MODELS_DIR = Path("delay_models")

def load_headway_model(route_id: str, stop_id: int):
    path = HEADWAY_MODELS_DIR / f"headway_{route_id}_{stop_id}.pkl"
    return joblib.load(path)

def load_delay_model(route_id: str, stop_id: int):
    path = DELAY_MODELS_DIR / f"delay_{route_id}_{stop_id}.pkl"
    return joblib.load(path)

def build_realtime_series(df_recent: pd.DataFrame):
    df_recent = df_recent.copy()
    df_recent["arrival_dt"] = pd.to_datetime(df_recent["arrival_time"], unit="s")
    df_recent = df_recent.sort_values("arrival_dt")
    df_recent["headway_sec"] = df_recent["arrival_dt"].diff().dt.total_seconds()
    df_recent["headway_min"] = df_recent["headway_sec"] / 60
    return df_recent

def forecast_next_headways(route_id: str, stop_id: int, df_recent: pd.DataFrame, minutes_ahead: int = 30):
    model = load_headway_model(route_id, stop_id)
    df_recent = build_realtime_series(df_recent)
    last_time = df_recent["arrival_dt"].max()

    future = model.make_future_dataframe(periods=minutes_ahead, freq="min")
    future = future[future["ds"] > last_time]

    forecast = model.predict(future)
    return forecast[["ds", "yhat"]]

def forecast_next_delays(route_id: str, stop_id: int, df_recent: pd.DataFrame, minutes_ahead: int = 30):
    model = load_delay_model(route_id, stop_id)
    df_recent = df_recent.copy()
    df_recent["arrival_dt"] = pd.to_datetime(df_recent["arrival_time"], unit="s")
    last_time = df_recent["arrival_dt"].max()

    future = model.make_future_dataframe(periods=minutes_ahead, freq="min")
    future = future[future["ds"] > last_time]

    forecast = model.predict(future)
    return forecast[["ds", "yhat"]]
