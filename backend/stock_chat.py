from backend.config import GEMINI_API_KEY
from backend.llm_client import LLMClient
from backend.recommendation_engine import build_recommendation
import pandas as pd

try:
    import ta
    import yfinance as yf
except Exception:
    ta = None
    yf = None


class StockChat:

    def __init__(self, api_key=None):
        self.llm = LLMClient(api_key=api_key or GEMINI_API_KEY)

    def analyze(self, symbol, price, rsi, macd, sentiment, risk):
        if self.llm.is_connected():
            answer = self.llm.analyze_stock(
                symbol=symbol,
                price=price,
                rsi=rsi,
                macd=macd,
                sentiment=sentiment,
                risk=risk,
            )
            if self._is_stock_analysis(answer, symbol):
                return answer

        return self._fallback_analysis(
            symbol=symbol,
            price=price,
            rsi=rsi,
            macd=macd,
            sentiment=sentiment,
            risk=risk,
        )

    def analyze_symbol(self, symbol, sentiment="Neutral", risk="Medium"):
        market_data = self.get_market_data(symbol)

        if market_data["ok"]:
            price = market_data["price"]
            rsi = market_data["rsi"]
            macd = market_data["macd"]
            cleaned_symbol = market_data["symbol"]
        else:
            price = 100.0
            rsi = 50.0
            macd = 0.0
            cleaned_symbol = market_data["symbol"]

        return {
            "market_data": market_data,
            "analysis": self.analyze(
                symbol=cleaned_symbol,
                price=price,
                rsi=rsi,
                macd=macd,
                sentiment=sentiment,
                risk=risk,
            ),
        }

    def get_market_data(self, symbol):
        cleaned_symbol = symbol.strip().upper()

        if not cleaned_symbol:
            return {
                "ok": False,
                "symbol": "UNKNOWN",
                "error": "Please enter a stock symbol.",
            }

        if yf is None or ta is None:
            return {
                "ok": False,
                "symbol": cleaned_symbol,
                "error": "Market data libraries are unavailable. Manual fallback values were used.",
            }

        try:
            df = yf.download(
                tickers=cleaned_symbol,
                period="6mo",
                interval="1d",
                auto_adjust=True,
                progress=False,
                threads=False,
            )

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            if df.empty or "Close" not in df.columns:
                return {
                    "ok": False,
                    "symbol": cleaned_symbol,
                    "error": "No market data was found for this symbol. Manual fallback values were used.",
                }

            close = df["Close"].dropna()
            if len(close) < 35:
                return {
                    "ok": False,
                    "symbol": cleaned_symbol,
                    "error": "Not enough price history was found. Manual fallback values were used.",
                }

            rsi_series = ta.momentum.RSIIndicator(close=close, window=14).rsi()
            macd_series = ta.trend.MACD(close=close).macd()

            return {
                "ok": True,
                "symbol": cleaned_symbol,
                "price": float(close.iloc[-1]),
                "rsi": float(rsi_series.dropna().iloc[-1]),
                "macd": float(macd_series.dropna().iloc[-1]),
                "rows": len(df),
            }
        except Exception as exc:
            return {
                "ok": False,
                "symbol": cleaned_symbol,
                "error": f"Unable to fetch market data: {exc}. Manual fallback values were used.",
            }

    def _is_stock_analysis(self, answer, symbol):
        if not isinstance(answer, str):
            return False

        text = answer.strip().lower()
        if not text:
            return False

        generic_fallback_markers = [
            "i can help with financial analysis",
            "i can help with finance topics",
            "for a better answer",
            "try asking about",
            "what does rsi mean",
            "how do i read macd",
            "can you summarize this financial document",
            "please configure your gemini api key",
            "__llm_unavailable__",
        ]

        if any(marker in text for marker in generic_fallback_markers):
            return False

        required_sections = [
            "trend",
            "strength",
            "risk",
            "recommendation",
        ]
        has_symbol = symbol.lower() in text
        has_structure = all(
            section in text
            for section in required_sections
        )

        return has_symbol and has_structure

    def _fallback_analysis(self, symbol, price, rsi, macd, sentiment, risk):
        trend_label = self._trend_label(rsi, macd)
        strength_label = self._strength_label(rsi, sentiment)
        recommendation = self._recommendation(rsi, macd, sentiment, risk)
        rec = build_recommendation(
            symbol,
            recommendation["signal"],
            recommendation["confidence"],
            risk,
        )

        sentiment_lower = sentiment.lower()
        risk_lower = risk.lower()
        rsi_view = self._rsi_view(rsi)
        macd_view = self._macd_view(macd)

        return f"""
Let's re-analyze **{symbol}** with the current inputs and the selected **"{risk}" Risk Level**.

**Disclaimer:** This analysis is based solely on the limited information provided: Current Price, RSI, MACD, News Sentiment, and Risk Level. It does not constitute financial advice. Investors should conduct independent due diligence and consult a qualified financial advisor before making any investment decision.

---

## Stock Analysis: {symbol} ({risk} Risk)

**Provided Data:**

- **Symbol:** {symbol}
- **Current Price:** {price:.2f}
- **RSI:** {rsi:.2f}
- **MACD:** {macd:.2f}
- **News Sentiment:** {sentiment}
- **Risk Level:** {risk}

---

## 1. Trend

Based on the technical indicators:

- **RSI (Relative Strength Index) at {rsi:.2f}:** {rsi_view}
- **MACD (Moving Average Convergence Divergence) at {macd:.2f}:** {macd_view}

**Conclusion for Trend:** The current setup suggests a **{trend_label}** trend. If RSI and MACD are both neutral, the stock may be consolidating or waiting for a new catalyst. In a {risk_lower}-risk context, even neutral readings should be treated carefully.

---

## 2. Strength

The strength of **{symbol}**, based on the provided data, is limited and should be viewed with caution:

- **News Sentiment:** The selected sentiment is **{sentiment}**, which can influence short-term market perception.
- **Technical Position:** RSI at {rsi:.2f} indicates {self._rsi_short(rsi)}.
- **Momentum:** MACD at {macd:.2f} indicates {self._macd_short(macd)}.

**Conclusion for Strength:** The primary strength signal is **{strength_label}**. However, this must be weighed against the **{risk} Risk Level** and the fact that only a small number of data points are available.

---

## 3. Risks

The **"{risk} Risk Level"** is a major factor in this analysis.

- **Risk Classification:** A {risk_lower}-risk designation means the investor should demand stronger confirmation before acting.
- **Sentiment Risk:** A {sentiment_lower} news reading can change quickly as new information enters the market.
- **Technical Risk:** RSI and MACD are useful, but they do not capture fundamentals, earnings quality, valuation, debt, management quality, or sector pressure.
- **Limited Data Analysis:** This output does not include financial statements, historical price performance, valuation ratios, or macroeconomic context.

**Conclusion for Risks:** The risk profile should not be ignored. If the stock has elevated risk, positive technical or news signals should be verified through deeper research.

---

## 4. Recommendation

**Recommendation:** {recommendation["label"]}

**Rationale:**

- **Trend Signal:** {trend_label.capitalize()} based on RSI and MACD.
- **Sentiment Signal:** News sentiment is **{sentiment}**.
- **Risk Adjustment:** The risk level is **{risk}**, so position sizing and stop-loss planning are important.
- **AI Fallback Verdict:** {rec["verdict"]}

**Actionable Steps if Considering:**

1. Identify why the stock has this risk level.
2. Check company fundamentals, recent earnings, debt levels, and sector outlook.
3. Wait for stronger confirmation if signals are mixed.
4. Use a defined stop loss and avoid overexposure.

---

## 5. Educational Disclaimer

This analysis is for educational and illustrative purposes only. It should not be treated as financial advice, an investment recommendation, or an endorsement to buy or sell **{symbol}** or any other security. Past performance and technical indicators do not guarantee future results.
"""

    def _trend_label(self, rsi, macd):
        if rsi >= 60 and macd > 0:
            return "bullish"
        if rsi <= 40 and macd < 0:
            return "bearish"
        return "neutral or sideways"

    def _strength_label(self, rsi, sentiment):
        if sentiment == "Positive" and rsi >= 50:
            return "positive sentiment with acceptable momentum"
        if sentiment == "Negative":
            return "weak sentiment pressure"
        if rsi >= 60:
            return "technical momentum"
        return "mixed or limited strength"

    def _recommendation(self, rsi, macd, sentiment, risk):
        score = 0

        if rsi >= 60:
            score += 2
        elif rsi <= 40:
            score -= 2

        if macd > 0:
            score += 2
        elif macd < 0:
            score -= 2

        if sentiment == "Positive":
            score += 1
        elif sentiment == "Negative":
            score -= 1

        if risk == "High":
            score -= 2
        elif risk == "Medium":
            score -= 1

        if score >= 3:
            return {
                "signal": "BUY",
                "confidence": 70,
                "label": "Consider only after confirmation and proper risk controls.",
            }

        if score <= -2:
            return {
                "signal": "SELL",
                "confidence": 70,
                "label": "Avoid, reduce exposure, or wait for stronger evidence.",
            }

        return {
            "signal": "HOLD",
            "confidence": 55,
            "label": "Hold or wait for clearer confirmation.",
        }

    def _rsi_view(self, rsi):
        if rsi > 70:
            return "This is an overbought reading and may indicate stretched buying pressure."
        if rsi < 30:
            return "This is an oversold reading and may indicate heavy selling pressure."
        if rsi >= 55:
            return "This shows mild positive momentum, though not necessarily a confirmed breakout."
        if rsi <= 45:
            return "This shows mild weakness, though not necessarily a confirmed downtrend."
        return "This is a neutral reading, indicating neither overbought nor oversold conditions."

    def _macd_view(self, macd):
        if macd > 0:
            return "A positive MACD suggests upward momentum may be present."
        if macd < 0:
            return "A negative MACD suggests downward momentum may be present."
        return "A MACD near zero suggests neutral momentum or a possible transition zone."

    def _rsi_short(self, rsi):
        if rsi > 70:
            return "overbought conditions"
        if rsi < 30:
            return "oversold conditions"
        if rsi >= 55:
            return "moderately positive momentum"
        if rsi <= 45:
            return "moderately weak momentum"
        return "neutral momentum"

    def _macd_short(self, macd):
        if macd > 0:
            return "positive momentum"
        if macd < 0:
            return "negative momentum"
        return "neutral momentum"

    def compare(self, stock1, stock2):
        if self.llm.is_connected():
            return self.llm.compare_stocks(stock1, stock2)

        return (
            f"Comparison fallback:\n\n"
            f"{stock1} and {stock2} should be analyzed across revenue, profitability, "
            "risk and growth metrics. Use available fundamentals and technical indicators "
            "before making any investment decision."
        )

    def explain_indicator(self, indicator):
        if self.llm.is_connected():
            return self.llm.explain_indicator(indicator)

        return (
            f"{indicator} explanation is not available via Gemini. "
            "Please configure your Gemini API key or consult the built-in finance guide."
        )
