import requests
from config import FINNHUB_API_KEY

def get_stock_news(symbol):

    ticker = symbol.replace(".NS", "")

    url = (
        f"https://finnhub.io/api/v1/company-news"
        f"?symbol={ticker}"
        f"&from=2025-01-01"
        f"&to=2026-12-31"
        f"&token={FINNHUB_API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        headlines = []

        positive_words = [
            "gain", "growth", "profit", "surge",
            "bullish", "buy", "record", "strong"
        ]

        negative_words = [
            "loss", "fall", "drop", "bearish",
            "sell", "weak", "decline", "crash"
        ]

        sentiment_score = 0

        for item in data[:10]:

            headline = item.get("headline", "")

            headlines.append({
                "headline": headline,
                "source": item.get("source", "")
            })

            text = headline.lower()

            for word in positive_words:
                if word in text:
                    sentiment_score += 1

            for word in negative_words:
                if word in text:
                    sentiment_score -= 1

        if sentiment_score > 2:
            sentiment = "POSITIVE"

        elif sentiment_score < -2:
            sentiment = "NEGATIVE"

        else:
            sentiment = "NEUTRAL"

        return {
            "news": headlines,
            "sentiment": sentiment,
            "score": sentiment_score
        }

    except Exception:

        return {
            "news": [],
            "sentiment": "UNKNOWN",
            "score": 0
        }