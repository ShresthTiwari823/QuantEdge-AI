import yfinance as yf
import ta


def compare_stocks(symbols):

    if isinstance(symbols, str):
        symbols = [symbols]

    symbols = [s.strip().upper() for s in symbols if s and s.strip()]
    result = []

    for symbol in symbols:

        df = yf.download(
            symbol,
            period="1y",
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            continue

        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"]

        rsi = ta.momentum.RSIIndicator(close).rsi().iloc[-1]

        macd = ta.trend.MACD(close).macd().iloc[-1]

        info = yf.Ticker(symbol).info

        result.append({
            "Stock": symbol,
            "Current Price": round(float(close.iloc[-1]), 2),
            "Market Cap": info.get("marketCap", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "RSI": round(float(rsi), 2),
            "MACD": round(float(macd), 2)
        })

    return result