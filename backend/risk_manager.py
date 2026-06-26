def calculate_trade_levels(current_price, signal, atr):

    current_price = float(current_price)
    atr = float(atr)

    if signal == "BUY":

        stop_loss = current_price - (1.5 * atr)

        target1 = current_price + (2 * atr)

        target2 = current_price + (4 * atr)

    elif signal == "SELL":

        stop_loss = current_price + (1.5 * atr)

        target1 = current_price - (2 * atr)

        target2 = current_price - (4 * atr)

    else:

        stop_loss = current_price - atr

        target1 = current_price + atr

        target2 = current_price + (2 * atr)

    risk = abs(current_price - stop_loss)

    reward = abs(target1 - current_price)

    rr_ratio = reward / risk if risk != 0 else 0

    return {

        "Entry": round(current_price,2),

        "Stop Loss": round(stop_loss,2),

        "Target 1": round(target1,2),

        "Target 2": round(target2,2),

        "Risk Reward": round(rr_ratio,2)

    }