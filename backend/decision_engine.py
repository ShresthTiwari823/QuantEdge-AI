def get_final_signal(
    buy_confidence,
    sell_confidence,
    rsi,
    macd,
    volatility,
    news_sentiment
):

    """
    Hybrid AI Decision Engine
    """

    buy_score = float(buy_confidence)
    sell_score = float(sell_confidence)

    # -------------------------
    # RSI
    # -------------------------

    if rsi < 30:
        buy_score += 12

    elif rsi > 70:
        sell_score += 12

    elif 45 <= rsi <= 60:
        buy_score += 5

    # -------------------------
    # MACD
    # -------------------------

    if macd > 0:
        buy_score += 8
    else:
        sell_score += 8

    # -------------------------
    # Volatility
    # -------------------------

    if volatility < 0.01:
        buy_score += 5

    elif volatility > 0.03:
        sell_score += 5

    # -------------------------
    # News Sentiment
    # -------------------------

    sentiment = str(news_sentiment).upper()

    if sentiment == "POSITIVE":
        buy_score += 10

    elif sentiment == "NEGATIVE":
        sell_score += 10

    # -------------------------
    # Limit Scores
    # -------------------------

    buy_score = min(buy_score, 100)
    sell_score = min(sell_score, 100)

    # -------------------------
    # Final Decision
    # -------------------------

    difference = abs(buy_score - sell_score)

    if buy_score > sell_score and difference >= 8:
        signal = "BUY"

    elif sell_score > buy_score and difference >= 8:
        signal = "SELL"

    else:
        signal = "HOLD"

    # -------------------------
    # Risk
    # -------------------------

    if volatility < 0.01:
        risk = "LOW"

    elif volatility < 0.03:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    return {
        "signal": signal,
        "buy_score": round(buy_score, 2),
        "sell_score": round(sell_score, 2),
        "risk": risk
    }


# -------------------------
# Testing
# -------------------------

if __name__ == "__main__":

    result = get_final_signal(
        buy_confidence=60,
        sell_confidence=40,
        rsi=45,
        macd=1.2,
        volatility=0.02,
        news_sentiment="POSITIVE"
    )

    print("\nHybrid AI Decision Engine\n")
    print(result)