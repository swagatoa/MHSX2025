# extrapolation.py
from prophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

def parse_week_string(week_str):
    """
    1) If week_str is already a Timestamp or datetime.date, return it directly.
    2) If week_str is a string like "Week 42 (2024)", extract year=2024, week=42.
    3) If week_str is a string like "2024-42", extract year=2024, week=42.
    Return the corresponding datetime (Monday of that ISO week).
    On failure, return pd.NaT.
    """
    # 1) If the input is already datetime‐like, just return it
    if isinstance(week_str, (pd.Timestamp, datetime.date, datetime.datetime)):
        # Ensure it’s a pandas Timestamp under the hood
        return pd.to_datetime(week_str)

    # 2) If it’s a string, attempt to parse
    if isinstance(week_str, str):
        try:
            if week_str.startswith("Week"):
                # e.g. "Week 42 (2024)"
                parts = week_str.split()      # ["Week", "42", "(2024)"]
                week_num = int(parts[1])
                year = int(parts[2].strip("()"))
            else:
                # e.g. "2024-42"
                year, week_num = map(int, week_str.split("-"))
            # Convert to the Monday of that ISO week:
            #   - "%Y-%W-%w" with day-of-week = 1 → Monday
            dt = datetime.datetime.strptime(f"{year}-{week_num}-1", "%Y-%W-%w")
            return pd.to_datetime(dt)
        except Exception as e:
            print(f"Failed to parse string “{week_str}”: {e}")
            return pd.NaT

    # If it’s neither a Timestamp nor a recognized string, bail out
    print(f"Failed to parse (not string or datetime): {week_str!r}")
    return pd.NaT


def extrapolate(revenue, extrapolationlength=1):
    """
    revenue: a dict with
       - revenue["weeks"] = a list/array of either:
             * strings in the form "Week 42 (2024)"  OR
             * strings in the form "2024-42"          OR
             * actual datetime-like objects (pd.Timestamp / datetime.date)
       - revenue["data"]  = the corresponding numeric values (floats/ints)
    """
    np.random.seed(42)
    # Build the DataFrame
    df_revenue = pd.DataFrame({
        "ds": revenue["weeks"],
        "y": revenue["data"]
    })

    # 1) Convert every entry in "ds" to a true Timestamp (or NaT if unparsable)
    df_revenue["ds"] = df_revenue["ds"].apply(parse_week_string)

    # 2) Drop rows that still failed to parse (ds == NaT)
    before = len(df_revenue)
    df_revenue = df_revenue.dropna(subset=["ds"])
    after = len(df_revenue)
    if after < before:
        print(f"Dropped {before - after} rows because they could not be parsed into dates.")

    # 3) Now fit Prophet
    model_rev = Prophet()
    model_rev.seed = 42
    model_rev.fit(df_revenue)

    # 4) Make a "future" DataFrame at monthly frequency (freq='MS')
    future_rev = model_rev.make_future_dataframe(periods=extrapolationlength, freq="MS")
    forecast_rev = model_rev.predict(future_rev)

    return {
        "forecast": [
            forecast_rev["yhat_lower"].tolist(),
            forecast_rev["yhat_upper"].tolist()
        ],
        "forecast_line": {
            "weeks": forecast_rev["ds"].dt.strftime("%Y-%m-%d").tolist(),
            "data": forecast_rev["yhat_lower"].tolist()
        }
    }


if __name__ == "__main__":
    dates = pd.date_range(start="2020-01-01", end="2024-12-01", freq="MS")
    n = len(dates)
    np.random.seed(42)

    revenue_values = 50000 + np.linspace(0, 20000, n) + np.random.normal(0, 3000, n)
    result = extrapolate({"weeks": dates, "data": revenue_values}, extrapolationlength=2)
    print("Forecast returned keys:", result.keys())
    print("Example forecast_line:", result["forecast_line"]["weeks"][:5], result["forecast_line"]["data"][:5])