import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import joblib
import plotly.graph_objects as go
import os
import sys

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, ROOT)

from backend.decision_engine import get_final_signal
from backend.news_fetcher import get_stock_news
from backend.forecast import forecast_next_7_days
from backend.portfolio import (
    add_stock,
    get_portfolio
)
from backend.watchlist import (
    add_to_watchlist,
    get_watchlist,
    remove_from_watchlist
)
from backend.company_insights import get_company_insights
from backend.risk_manager import calculate_trade_levels
from backend.portfolio_manager import get_portfolio_summary

st.set_page_config(
    page_title="QuantEdge AI",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background:#F5F7FB;
}

.block-container{
    padding-top:1.5rem;
}

.metric-container{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,.08);
}

</style>
""", unsafe_allow_html=True)

st.title("📈 QuantEdge AI")

st.caption("AI Powered Stock Prediction & Risk Analytics Platform")

try:
    model = joblib.load("models/random_forest.pkl")
except Exception:
    st.error(
        "Unable to load the prediction model. Please verify that models/random_forest.pkl exists."
    )
    st.stop()


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def load_watchlist_symbol(stock):
    st.session_state["symbol_to_load"] = stock
    rerun_app()


def remove_watchlist_symbol(stock):
    remove_from_watchlist(stock)
    rerun_app()


if "symbol_to_load" in st.session_state:
    st.session_state["symbol_input"] = st.session_state.pop("symbol_to_load")


default_symbol = st.session_state.get("symbol_input", "")

symbol_input = st.text_input(
    "Enter Stock Symbol",
    value=default_symbol,
    placeholder="Example: TCS.NS, SBIN.NS, AAPL, TSLA, BTC-USD",
    key="symbol_input"
)

symbol = symbol_input.strip().upper()

symbols = [s.strip().upper() for s in symbol.split(",") if s.strip()]

if symbols:
    for current_symbol in symbols:
        symbol = current_symbol
        st.subheader(f"📌 Analysis for {symbol}")
        try:
            with st.spinner(f"Analyzing {symbol}..."):
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
                st.error(f"Invalid Stock Symbol: {symbol}")
                continue

            close = df["Close"]
            high = df["High"]
            low = df["Low"]

            df["RSI"] = ta.momentum.RSIIndicator(
                close=close,
                window=14
            ).rsi()

            macd = ta.trend.MACD(close=close)
            df["MACD"] = macd.macd()

            atr = ta.volatility.AverageTrueRange(
                high=high,
                low=low,
                close=close,
                window=14
            )
            df["ATR"] = atr.average_true_range()

            bb = ta.volatility.BollingerBands(close=close)
            df["BB_Upper"] = bb.bollinger_hband()
            df["BB_Lower"] = bb.bollinger_lband()

            df["EMA20"] = close.ewm(span=20).mean()
            df["EMA50"] = close.ewm(span=50).mean()

            df["SMA20"] = close.rolling(20).mean()
            df["SMA50"] = close.rolling(50).mean()

            df["Momentum"] = close.diff(10)
            df["Trend"] = (df["EMA20"] > df["EMA50"]).astype(int)

            df["Returns"] = close.pct_change()
            df["Volatility"] = df["Returns"].rolling(20).std()

            df.dropna(inplace=True)

            latest = df.iloc[-1]
            X = pd.DataFrame([{
                "RSI": latest["RSI"],
                "MACD": latest["MACD"],
                "ATR": latest["ATR"],
                "Volatility": latest["Volatility"],
                "BB_Upper": latest["BB_Upper"],
                "BB_Lower": latest["BB_Lower"],
                "EMA20": latest["EMA20"],
                "EMA50": latest["EMA50"],
                "SMA20": latest["SMA20"],
                "SMA50": latest["SMA50"],
                "Momentum": latest["Momentum"],
                "Trend": latest["Trend"]
            }])

            probabilities = model.predict_proba(X)[0]
            sell_confidence = round(probabilities[0] * 100, 2)
            buy_confidence = round(probabilities[1] * 100, 2)

            news = get_stock_news(symbol)

            decision = get_final_signal(
                buy_confidence=buy_confidence,
                sell_confidence=sell_confidence,
                rsi=float(latest["RSI"]),
                macd=float(latest["MACD"]),
                volatility=float(latest["Volatility"]),
                news_sentiment=news["sentiment"]
            )

            signal = decision["signal"]
            buy_confidence = decision["buy_score"]
            sell_confidence = decision["sell_score"]
            risk = decision["risk"]

            st.divider()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 Current Price", f"₹ {float(latest['Close']):.2f}")
            c2.metric("🟢 Buy %", f"{buy_confidence}%")
            c3.metric("🔴 Sell %", f"{sell_confidence}%")
            c4.metric("⚠ Risk", risk)

            if signal == "BUY":
                st.success("🟢 STRONG BUY SIGNAL")
            elif signal == "SELL":
                st.error("🔴 STRONG SELL SIGNAL")
            else:
                st.warning("🟡 HOLD / WAIT")

            if latest["MACD"] > 0:
                st.info("📈 Overall Trend : Uptrend")
            else:
                st.info("📉 Overall Trend : Downtrend")

            st.divider()
            st.header("🤖 AI Decision Report")
            st.metric("AI Confidence", f"{buy_confidence:.2f}%")
            st.progress(buy_confidence / 100)

            st.subheader("Decision Factors")

            report = []
            score = 0

            if latest["RSI"] >= 60:
                report.append(("RSI", "🟢 Bullish", "+15"))
                score += 15
            elif latest["RSI"] <= 40:
                report.append(("RSI", "🔴 Bearish", "-15"))
                score -= 15
            else:
                report.append(("RSI", "🟡 Neutral", "0"))

            if latest["MACD"] > 0:
                report.append(("MACD", "🟢 Positive", "+15"))
                score += 15
            else:
                report.append(("MACD", "🔴 Negative", "-15"))
                score -= 15

            if latest["EMA20"] > latest["EMA50"]:
                report.append(("EMA Trend", "🟢 Bullish", "+20"))
                score += 20
            else:
                report.append(("EMA Trend", "🔴 Bearish", "-20"))
                score -= 20

            if latest["Volatility"] < 0.02:
                report.append(("Volatility", "🟢 Low Risk", "+10"))
                score += 10
            else:
                report.append(("Volatility", "🟡 High Volatility", "-5"))
                score -= 5

            if news["sentiment"] == "POSITIVE":
                report.append(("News", "🟢 Positive", "+20"))
                score += 20
            elif news["sentiment"] == "NEGATIVE":
                report.append(("News", "🔴 Negative", "-20"))
                score -= 20
            else:
                report.append(("News", "🟡 Neutral", "0"))

            if latest["Close"] > latest["EMA20"]:
                report.append(("Price Trend", "🟢 Above EMA20", "+10"))
                score += 10
            else:
                report.append(("Price Trend", "🔴 Below EMA20", "-10"))
                score -= 10

            report_df = pd.DataFrame(
                report,
                columns=["Factor", "Status", "Impact"]
            )

            st.dataframe(
                report_df,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("📋 AI Explanation")

            if signal == "BUY":
                st.success(
                    f"""
The AI recommends **BUY** because the stock is showing
strong technical momentum.

• RSI indicates bullish strength.

• MACD remains positive.

• EMA20 is above EMA50 confirming an uptrend.

• News sentiment is **{news['sentiment']}**.

• Current market risk is **{risk}**.

Overall technical score: **{score}**
"""
                )

            elif signal == "SELL":
                st.error(
                    f"""
The AI recommends **SELL** because multiple
technical indicators are weakening.

• Momentum is slowing.

• Trend indicators are bearish.

• News sentiment is **{news['sentiment']}**.

• Risk level is **{risk}**.

Overall technical score: **{score}**
"""
                )

            else:
                st.warning(
                    f"""
The AI recommends **HOLD**.

Current indicators are mixed.

• Wait for stronger confirmation.

• News sentiment is **{news['sentiment']}**.

• Risk level is **{risk}**.

Overall technical score: **{score}**
"""
                )

            st.info(
                """
⚠ Disclaimer

This recommendation is generated using Machine Learning,
technical indicators, and market sentiment.

It is intended for educational purposes and should not be
considered financial advice.
"""
            )

            st.divider()
            st.header("🎯 AI Trade Setup")

            trade = calculate_trade_levels(
                latest["Close"],
                signal,
                latest["ATR"]
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "💰 Entry",
                    f"₹ {trade['Entry']}"
                )

                st.metric(
                    "🛑 Stop Loss",
                    f"₹ {trade['Stop Loss']}"
                )

            with c2:

                st.metric(
                    "🎯 Target 1",
                    f"₹ {trade['Target 1']}"
                )

                st.metric(
                    "🎯 Target 2",
                    f"₹ {trade['Target 2']}"
                )

            with c3:

                st.metric(
                    "⚖ Risk Reward",
                    f"1 : {trade['Risk Reward']}"
                )

                if signal == "BUY":

                    st.success("📈 Long Trade")

                elif signal == "SELL":

                    st.error("📉 Short Trade")

                else:

                    st.warning("⏳ Wait for Confirmation")

            st.divider()
            st.header("📰 AI News & Market Sentiment")
            st.success(f"Overall News Sentiment : {news['sentiment']}")

            if len(news["news"]) == 0:
                st.warning("No latest news found.")
            else:
                for item in news["news"]:
                    st.write(f"• {item['headline']}")

            st.divider()
            st.header("🏢 Company Insights")

            company = get_company_insights(symbol)

            if company:

                c1, c2 = st.columns(2)

                with c1:
                    st.metric("🏢 Company", company["Company"])
                    st.metric("🏭 Sector", company["Sector"])
                    st.metric("🏢 Industry", company["Industry"])
                    st.metric("🌍 Country", company["Country"])
                    st.metric("👨‍💼 Employees", company["Employees"])

                with c2:
                    st.metric("💰 Market Cap", company["Market Cap"])
                    st.metric("📈 PE Ratio", company["PE Ratio"])
                    st.metric("💵 EPS", company["EPS"])
                    st.metric("📊 52W High", company["52 Week High"])
                    st.metric("📉 52W Low", company["52 Week Low"])

                st.subheader("🌐 Website")
                st.write(company["Website"])

                st.subheader("📝 Company Overview")
                st.write(company["Business Summary"])

            else:
                st.warning("Company information not available.")

            st.divider()
            st.header("� Advanced Professional Trading Chart")
            # Added chart improvements

            fig = go.Figure()
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="Candlestick"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["EMA20"],
                    mode="lines",
                    name="EMA 20",
                    line=dict(color="blue", width=2)
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["EMA50"],
                    mode="lines",
                    name="EMA 50",
                    line=dict(color="orange", width=2)
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BB_Upper"],
                    mode="lines",
                    name="BB Upper",
                    line=dict(color="green", dash="dot")
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BB_Lower"],
                    mode="lines",
                    name="BB Lower",
                    line=dict(color="red", dash="dot")
                )
            )
            # ==============================
            # AI BUY / SELL Marker
            # ==============================
            marker_symbol = "triangle-up"
            marker_color = "green"
            marker_text = "BUY"

            if signal == "SELL":
                marker_symbol = "triangle-down"
                marker_color = "red"
                marker_text = "SELL"

            elif signal == "HOLD":
                marker_symbol = "circle"
                marker_color = "orange"
                marker_text = "HOLD"

            fig.add_trace(
                go.Scatter(
                    x=[df.index[-1]],
                    y=[latest["Close"]],
                    mode="markers",
                    marker=dict(
                        symbol=marker_symbol,
                        size=22,
                        color=marker_color,
                        line=dict(width=2, color="black")
                    ),
                    hovertemplate=f"AI Signal: {marker_text}<extra></extra>",
                    name="AI Signal"
                )
            )
            fig.add_annotation(
                x=df.index[-1],
                y=latest["Close"],
                text=f"<b>{marker_text}</b>",
                showarrow=False,
                yshift=-30,
                font=dict(size=14, color="black", family="Arial"),
                align="center",
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                borderpad=3,
                opacity=0.85
            )
            # =========================================
            # Support & Resistance Levels
            # =========================================
            support = df["Low"].tail(20).min()
            resistance = df["High"].tail(20).max()

            fig.add_hline(
                y=support,
                line_dash="dash",
                line_color="green",
                annotation_text=f"Support ₹{support:.2f}",
                annotation_position="bottom left"
            )

            fig.add_hline(
                y=resistance,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Resistance ₹{resistance:.2f}",
                annotation_position="top left"
            )
            fig.update_layout(
                template="plotly_white",
                height=700,
                title=f"{symbol} Professional Trading Chart",
                xaxis_rangeslider_visible=False,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info(f"""
🟢 Support Level : ₹{support:.2f}

🔴 Resistance Level : ₹{resistance:.2f}
""")

            st.subheader("📊 Trading Volume")

            vol_fig = go.Figure()
            vol_fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["Volume"],
                    name="Volume"
                )
            )
            vol_fig.update_layout(
                title="Trading Volume",
                template="plotly_white",
                height=300
            )
            st.plotly_chart(vol_fig, use_container_width=True)

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 RSI")
                st.line_chart(df["RSI"])
                st.subheader("📉 MACD")
                st.line_chart(df["MACD"])

            with col2:
                st.subheader("📊 Volatility")
                st.line_chart(df["Volatility"])
                st.subheader("📋 Technical Summary")
                st.metric("RSI", round(float(latest["RSI"]), 2))
                st.metric("MACD", round(float(latest["MACD"]), 2))
                st.metric("ATR", round(float(latest["ATR"]), 2))
                st.metric("Volatility", round(float(latest["Volatility"]), 4))
                st.metric("EMA20", round(float(latest["EMA20"]), 2))
                st.metric("EMA50", round(float(latest["EMA50"]), 2))

            st.divider()

            st.header("🔮 AI Price Forecast (Next 7 Days)")
            forecast = forecast_next_7_days(df)
            st.dataframe(forecast, use_container_width=True)

            forecast_fig = go.Figure()
            forecast_fig.add_trace(
                go.Scatter(
                    x=forecast["Day"],
                    y=forecast["Predicted Price"],
                    mode="lines+markers",
                    name="Forecast"
                )
            )
            forecast_fig.update_layout(
                title="7-Day AI Forecast",
                template="plotly_white",
                height=450
            )
            st.plotly_chart(forecast_fig, use_container_width=True)

            st.divider()

            st.header("💼 Portfolio Tracker")
            qty = st.number_input(
                "Quantity",
                min_value=1,
                value=10
            )
            buy_price = st.number_input(
                "Buy Price",
                min_value=1.0,
                value=float(latest["Close"])
            )

            if st.button("Add to Portfolio"):
                add_stock(symbol, qty, buy_price)
                st.success(f"{symbol} added successfully.")

            portfolio = get_portfolio()
            if len(portfolio) > 0:
                pdf = pd.DataFrame(portfolio)
                pdf = pdf.rename(columns={"Stock": "Symbol"})
                styled_pdf = pdf.style.format({
                    "Buy Price": "₹ {:,.2f}",
                    "Current Price": "₹ {:,.2f}",
                    "Investment": "₹ {:,.2f}",
                    "Current Value": "₹ {:,.2f}",
                    "Profit": "₹ {:,.2f}",
                    "Return %": "{:.2f}%"
                })
                st.dataframe(styled_pdf, use_container_width=True)

                summary = get_portfolio_summary()
                if summary:
                    st.divider()
                    st.header("📊 Portfolio Analytics")
                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "Investment",
                        f"₹ {summary['investment']:.2f}"
                    )
                    c2.metric(
                        "Current Value",
                        f"₹ {summary['current']:.2f}"
                    )
                    c3.metric(
                        "Profit / Loss",
                        f"₹ {summary['profit']:.2f}"
                    )
                    c4.metric(
                        "Return %",
                        f"{summary['profit_percent']:.2f}%"
                    )

                    st.subheader("📌 Portfolio Insights")
                    a1, a2, a3 = st.columns(3)

                    a1.metric(
                        "🏆 Best Performer",
                        summary["best_stock"]
                    )
                    a2.metric(
                        "📉 Worst Performer",
                        summary["worst_stock"]
                    )
                    a3.metric(
                        "📦 Total Stocks",
                        summary["stock_count"]
                    )

                    st.subheader("🥧 Portfolio Allocation")
                    allocation = summary["allocation"]
                    pie = go.Figure(
                        data=[
                            go.Pie(
                                labels=[x["Symbol"] for x in allocation],
                                values=[x["Investment"] for x in allocation],
                                hole=0.4
                            )
                        ]
                    )
                    pie.update_layout(
                        template="plotly_white",
                        height=500
                    )
                    st.plotly_chart(
                        pie,
                        use_container_width=True
                    )
            else:
                st.info("Portfolio is currently empty.")

            st.divider()
            st.header("⭐ Watchlist")

            if st.button("⭐ Add Current Stock"):
                add_to_watchlist(symbol)
                st.success(f"{symbol} added to Watchlist!")

            watchlist = get_watchlist()

            if watchlist:

                st.subheader("Saved Stocks")

                for stock in watchlist:

                    c1, c2, c3 = st.columns([6, 2, 2])

                    with c1:
                        st.write(f"📈 {stock}")

                    with c2:
                        if st.button("Load", key=f"load_{stock}"):
                            load_watchlist_symbol(stock)

                    with c3:
                        if st.button("Remove", key=f"remove_{stock}"):
                            remove_watchlist_symbol(stock)

            else:
                st.info("Watchlist is empty.")

        except Exception as e:
            st.error(f"❌ {str(e)}")
