def build_recommendation(symbol, signal, confidence, risk):
    header = f"{symbol} Recommendation"

    if signal == "BUY":
        verdict = "BUY"
        explanation = (
            "The market momentum is positive, technical indicators favor a bullish view, "
            "and model confidence is strong."
        )
        action = (
            "Consider initiating a position with a clear stop-loss and continue monitoring "
            "for support levels."
        )
    elif signal == "SELL":
        verdict = "SELL"
        explanation = (
            "Price action appears weak, technical momentum is negative, "
            "and risk factors are elevated."
        )
        action = (
            "Consider reducing exposure or closing positions while waiting for a clearer trend reversal."
        )
    else:
        verdict = "HOLD"
        explanation = (
            "The market is indecisive and indicators are mixed, so it is safer to wait for confirmation."
        )
        action = (
            "Maintain current holdings and only act when a stronger buy or sell signal appears."
        )

    return {
        "symbol": symbol,
        "verdict": verdict,
        "confidence": f"{confidence:.2f}%",
        "risk": risk,
        "explanation": explanation,
        "action": action,
        "disclaimer": (
            "This recommendation is for informational purposes only and does not constitute "
            "financial advice. Always do your own research before trading."
        )
    }
