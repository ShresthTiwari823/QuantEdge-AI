import yfinance as yf
import pandas as pd
import ta
import joblib

model = joblib.load("models/random_forest.pkl")

symbol = input(
"Enter Stock Symbol: "
).strip().upper()

df = yf.download(
symbol,
period="1y",
auto_adjust=True,
progress=False
)

if df.empty:
print("No data found")
exit()

close = df["Close"].squeeze()
high = df["High"].squeeze()
low = df["Low"].squeeze()

df["RSI"] = ta.momentum.RSIIndicator(
close=close,
window=14
).rsi()

macd = ta.trend.MACD(
close=close
)

df["MACD"] = macd.macd()

atr = ta.volatility.AverageTrueRange(
high=high,
low=low,
close=close,
window=14
)

df["ATR"] = atr.average_true_range()

bb = ta.volatility.BollingerBands(
close=close
)

df["BB_Upper"] = bb.bollinger_hband()
df["BB_Lower"] = bb.bollinger_lband()

df["Returns"] = close.pct_change(
fill_method=None
)

df["Volatility"] = (
df["Returns"]
.rolling(20)
.std()
)

df.dropna(inplace=True)

latest = df.iloc[-1]

X = pd.DataFrame([{
"RSI": latest["RSI"],
"MACD": latest["MACD"],
"ATR": latest["ATR"],
"Volatility": latest["Volatility"],
"BB_Upper": latest["BB_Upper"],
"BB_Lower": latest["BB_Lower"]
}])

prediction = model.predict(X)[0]

probabilities = model.predict_proba(X)[0]

sell_confidence = round(
probabilities[0] * 100,
2
)

buy_confidence = round(
probabilities[1] * 100,
2
)

if buy_confidence >= 65:
signal = "BUY"

elif sell_confidence >= 65:
signal = "SELL"

else:
signal = "HOLD"

volatility = float(
latest["Volatility"]
)

if volatility < 0.01:
risk = "LOW"

elif volatility < 0.03:
risk = "MEDIUM"

else:
risk = "HIGH"

print("\n====================")

print(
"Current Price:",
round(float(latest["Close"]), 2)
)

print("Signal:", signal)

print(
"Buy Confidence:",
buy_confidence,
"%"
)

print(
"Sell Confidence:",
sell_confidence,
"%"
)

print(
"Risk Level:",
risk
)

print("====================")