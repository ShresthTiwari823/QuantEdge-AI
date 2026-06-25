import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import joblib
import plotly.graph_objects as go

st.set_page_config(
    page_title="QuantEdge AI",
    layout="wide"
)

st.title("📈 QuantEdge AI")
st.subheader("Intelligent Trading & Risk Analytics Platform")

model = joblib.load(
    "models/random_forest.pkl"
)

symbol = st.text_input(
    "Enter Stock Symbol",
    "TCS.NS"
).strip().upper()

if st.button("Analyze"):

    try:

        df = yf.download(
            tickers=symbol,
            period="1y",
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False
        )

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty:
            st.error(
                f"No data found for {symbol}"
            )
            st.stop()

        close = df["Close"].squeeze()
        high = df["High"].squeeze()
        low = df["Low"].squeeze()

        # Indicators

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

        probabilities = model.predict_proba(X)[0]

        sell_confidence = round(
            probabilities[0] * 100,
            2
        )

        buy_confidence = round(
            probabilities[1] * 100,
            2
        )

        if buy_confidence >= 58:
            signal = "BUY"

        elif sell_confidence >= 58:
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

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Current Price",
            round(float(latest["Close"]), 2)
        )

        col2.metric(
            "Buy %",
            buy_confidence
        )

        col3.metric(
            "Sell %",
            sell_confidence
        )

        col4.metric(
            "Risk",
            risk
        )

        if signal == "BUY":
            st.success("🟢 BUY SIGNAL")

        elif signal == "SELL":
            st.error("🔴 SELL SIGNAL")

        else:
            st.warning("🟡 HOLD SIGNAL")

        trend = "Uptrend"

        if latest["MACD"] < 0:
            trend = "Downtrend"

        st.info(f"📉 {trend}")

        # Candlestick Chart

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"]
                )
            ]
        )

        fig.update_layout(
            title=f"{symbol} Candlestick Chart",
            xaxis_rangeslider_visible=False,
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("RSI")
        st.line_chart(df["RSI"])

        st.subheader("MACD")
        st.line_chart(df["MACD"])

        st.subheader("Volatility")
        st.line_chart(df["Volatility"])

        st.subheader("Technical Summary")

        st.write(
            f"RSI: {round(float(latest['RSI']),2)}"
        )

        st.write(
            f"MACD: {round(float(latest['MACD']),2)}"
        )

        st.write(
            f"ATR: {round(float(latest['ATR']),2)}"
        )

        st.write(
            f"Volatility: {round(float(latest['Volatility']),4)}"
        )

        st.write(
            f"BB Upper: {round(float(latest['BB_Upper']),2)}"
        )

        st.write(
            f"BB Lower: {round(float(latest['BB_Lower']),2)}"
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )