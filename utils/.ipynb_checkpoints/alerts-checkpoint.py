import pandas as pd

def generate_alerts(df_rt: pd.DataFrame) -> pd.DataFrame:
    alerts = []

    for _, row in df_rt.iterrows():

        # Rule 1 — Severe delay
        if row["delay_minutes"] >= 10:
            alerts.append({
                "route": row["route_id"],
                "severity": "HIGH",
                "message": f"Severe delay of {row['delay_minutes']} min at stop {row['stop_id']}"
            })

        # Rule 2 — Bunching
        if "bunching_flag" in row and row["bunching_flag"] == 1:
            alerts.append({
                "route": row["route_id"],
                "severity": "MEDIUM",
                "message": f"Bunching detected near stop {row['stop_id']}"
            })

        # Rule 3 — Headway instability
        if row["headway_minutes"] <= 2:
            alerts.append({
                "route": row["route_id"],
                "severity": "LOW",
                "message": f"Very short headway ({row['headway_minutes']} min) — possible bunching"
            })

    return pd.DataFrame(alerts)
