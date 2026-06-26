import yfinance as yf

portfolio = []


def add_stock(symbol, quantity, buy_price):

    symbol = symbol.upper()

    try:
        current_price = float(
            yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
        )
    except:
        current_price = float(buy_price)

    # Merge if stock already exists
    for stock in portfolio:

        if stock["Stock"] == symbol:

            total_qty = stock["Quantity"] + quantity

            avg_buy = (
                stock["Buy Price"] * stock["Quantity"] +
                buy_price * quantity
            ) / total_qty

            stock["Quantity"] = total_qty
            stock["Buy Price"] = round(avg_buy, 2)

            investment = total_qty * avg_buy
            current_value = total_qty * current_price
            profit = current_value - investment
            percent = (profit / investment) * 100

            stock["Current Price"] = round(current_price, 2)
            stock["Investment"] = round(investment, 2)
            stock["Current Value"] = round(current_value, 2)
            stock["Profit"] = round(profit, 2)
            stock["Return %"] = round(percent, 2)

            return

    investment = quantity * buy_price
    current_value = quantity * current_price
    profit = current_value - investment
    percent = (profit / investment) * 100

    portfolio.append({
        "Stock": symbol,
        "Quantity": quantity,
        "Buy Price": round(buy_price, 2),
        "Current Price": round(current_price, 2),
        "Investment": round(investment, 2),
        "Current Value": round(current_value, 2),
        "Profit": round(profit, 2),
        "Return %": round(percent, 2)
    })


def remove_stock(symbol):

    global portfolio

    symbol = symbol.upper()

    portfolio = [
        stock
        for stock in portfolio
        if stock["Stock"] != symbol
    ]


def get_portfolio():

    return portfolio