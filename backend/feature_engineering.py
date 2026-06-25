import pandas as pd
import ta
import os
from glob import glob

DATA_FOLDER = "data"

all_data = []

csv_files = glob(os.path.join(DATA_FOLDER, "*.csv"))

print(f"Found {len(csv_files)} files")

for file in csv_files:

    try:

        print(f"\nProcessing {file}")

        df = pd.read_csv(file)

        df.columns = [str(col).strip() for col in df.columns]

        required_cols = ["Open", "High", "Low", "Close", "Volume"]

        if not all(col in df.columns for col in required_cols):

            print(f"Skipping {file} - Missing columns")
            continue

        for col in required_cols:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df.dropna(
            subset=required_cols,
            inplace=True
        )

        if len(df) < 60:

            print(f"Skipping {file} - Too few rows")
            continue

        # ---------------- TECHNICAL INDICATORS ---------------- #

        df["RSI"] = ta.momentum.RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()

        macd = ta.trend.MACD(
            close=df["Close"]
        )

        df["MACD"] = macd.macd()

        bb = ta.volatility.BollingerBands(
            close=df["Close"],
            window=20
        )

        df["BB_Upper"] = bb.bollinger_hband()
        df["BB_Lower"] = bb.bollinger_lband()

        atr = ta.volatility.AverageTrueRange(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            window=14
        )

        df["ATR"] = atr.average_true_range()

        df["Returns"] = df["Close"].pct_change()

        df["Volatility"] = (
            df["Returns"]
            .rolling(20)
            .std()
        )

        df["SMA20"] = (
            df["Close"]
            .rolling(20)
            .mean()
        )

        df["SMA50"] = (
            df["Close"]
            .rolling(50)
            .mean()
        )

        df["EMA20"] = ta