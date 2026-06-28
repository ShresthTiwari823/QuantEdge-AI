class FinanceQA:

    def __init__(self):

        self.answers = {

            "rsi":
            """
RSI (Relative Strength Index)

• Measures momentum.

• Range : 0 to 100

• Above 70 = Overbought

• Below 30 = Oversold

Traders use RSI to identify potential reversal zones.
""",

            "macd":
            """
MACD (Moving Average Convergence Divergence)

• Measures trend strength.

• MACD above Signal Line = Bullish

• MACD below Signal Line = Bearish

Positive MACD indicates upward momentum.
""",

            "ema":
            """
EMA (Exponential Moving Average)

EMA gives more weight to recent prices.

EMA20 above EMA50

= Bullish Trend

EMA20 below EMA50

= Bearish Trend
""",

            "bollinger":
            """
Bollinger Bands

Upper Band

Middle Band

Lower Band

Price near Upper Band

= Strong momentum

Price near Lower Band

= Possible buying opportunity.
""",

            "atr":
            """
ATR (Average True Range)

Measures market volatility.

Higher ATR

= High volatility

Lower ATR

= Stable market.
""",

            "support":
            """
Support

Support is a price level where buyers usually enter.

Price often bounces upward from support.
""",

            "resistance":
            """
Resistance

Resistance is a level where sellers become active.

Price often reverses downward.
""",

            "stop loss":
            """
Stop Loss

A predefined exit price.

Helps reduce losses if the market moves against you.
""",

            "risk reward":
            """
Risk Reward Ratio

Compares possible profit with possible loss.

1:2 means

Risk ₹1

Potential Reward ₹2
""",

            "buy":
            """
BUY means

Technical indicators

+

AI Model

+

News Sentiment

indicate bullish momentum.

Buying may be considered after your own research.
""",

            "sell":
            """
SELL means

Technical indicators suggest weakness.

Momentum is bearish.

Risk may be increasing.
""",

            "hold":
            """
HOLD means

Current indicators are mixed.

Wait until stronger confirmation appears.
""",

            "forecast":
            """
Forecast predicts future stock prices using

Historical Prices

Machine Learning

Trend Analysis

Technical Indicators

The prediction is probabilistic, not guaranteed.
""",

            "sentiment":
            """
News Sentiment

Positive

Neutral

Negative

News articles are analyzed to estimate market mood.
""",

            "portfolio":
            """
Portfolio Tracker

Tracks

Investment

Current Value

Profit/Loss

Returns

Allocation
""",

            "watchlist":
            """
Watchlist

Stores favorite stocks.

Allows quick monitoring without investing.
""",

            "pdf":
            """
Financial PDF Analyzer

Reads Annual Reports

Quarterly Reports

Balance Sheets

Investor Presentations

and generates

Summary

Risks

Sentiment

Investment Recommendation.
"""
        }

    def get_answer(self, question):

        q = question.lower().strip()

        if not q:
            return "Please ask a finance or stock-related question."

        long_prompt = len(q) > 180 or any(word in q for word in ["summarize", "report", "document", "pdf", "analysis", "question", "explain", "compare", "recommendation", "outlook", "opportunities", "risks"])

        if long_prompt:
            return """
I can help with financial analysis, stock concepts, and PDF report questions.

For a better answer, ask a specific question such as:
• What does RSI mean?
• How do I read MACD?
• What are the key risks in this report?
• Can you summarize this financial document?
"""

        for keyword in self.answers:

            if keyword in q:

                return self.answers[keyword]

        return """
I can help with finance topics and market concepts.

Try asking about:
• RSI, MACD, EMA, ATR, Bollinger Bands
• stock analysis basics
• portfolio and risk concepts
• uploaded financial PDFs
"""