import yfinance as yf
import requests
from bs4 import BeautifulSoup


def get_stock_news(symbol):

    try:

        stock = yf.Ticker(symbol)

        info = stock.info

        company = info.get("longName")

        if company is None:
            company = symbol.replace(".NS", "")

    except:

        company = symbol.replace(".NS", "")

    company = company.replace("Limited", "")
    company = company.replace("Ltd", "")
    company = company.strip()

    url = (
        "https://news.google.com/rss/search?"
        f"q={company}+stock"
    )

    try:

        xml = requests.get(
            url,
            timeout=10
        ).text

        soup = BeautifulSoup(
            xml,
            "xml"
        )

        items = soup.find_all("item")[:10]

        headlines = []

        positive = [
            "profit",
            "growth",
            "surge",
            "record",
            "buy",
            "strong",
            "expands",
            "beat",
            "rise",
            "bullish",
            "upgrade",
            "positive"
        ]

        negative = [
            "loss",
            "fall",
            "drop",
            "decline",
            "bearish",
            "downgrade",
            "crash",
            "weak",
            "cuts",
            "fraud",
            "lawsuit",
            "negative"
        ]

        score = 0

        for item in items:

            title = item.title.text

            source = item.source.text if item.source else ""

            headlines.append(
                {
                    "headline": title,
                    "source": source
                }
            )

            text = title.lower()

            for word in positive:
                if word in text:
                    score += 1

            for word in negative:
                if word in text:
                    score -= 1

        if score >= 3:
            sentiment = "POSITIVE"

        elif score <= -3:
            sentiment = "NEGATIVE"

        else:
            sentiment = "NEUTRAL"

        return {
            "news": headlines,
            "sentiment": sentiment,
            "score": score
        }

    except Exception:

        return {
            "news": [],
            "sentiment": "UNKNOWN",
            "score": 0
        }