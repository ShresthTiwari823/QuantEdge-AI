import pandas as pd
import numpy as np


def forecast_next_7_days(df):
    """
    Simple AI-like 7-day price forecast based on
    recent trend and volatility.
    """

    close = df["Close"].copy()

    last_price = float(close.iloc[-1])

    returns = close.pct_change().dropna()

    trend = returns.tail(30).mean()

    volatility = returns.tail(30).std()

    predictions = []

    price = last_price

    np.random.seed(42)

    for _ in range(7):

        random_noise = np.random.normal(0, volatility * 0.3)

        daily_return = trend + random_noise

        price *= (1 + daily_return)

        predictions.append(round(price, 2))

    forecast = pd.DataFrame({
        "Day": [f"Day {i}" for i in range(1, 8)],
        "Predicted Price": predictions
    })

    return forecast