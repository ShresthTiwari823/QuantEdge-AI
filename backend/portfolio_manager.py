from backend.portfolio import get_portfolio


def get_portfolio_summary():

    portfolio = get_portfolio()

    if len(portfolio) == 0:
        return None

    total_investment = 0
    total_current = 0
    total_profit = 0

    allocation = []

    best_stock = max(portfolio, key=lambda x: x["Profit"])
    worst_stock = min(portfolio, key=lambda x: x["Profit"])

    for stock in portfolio:

        total_investment += stock["Investment"]
        total_current += stock["Current Value"]
        total_profit += stock["Profit"]

        allocation.append({
            "Symbol": stock.get("Stock", stock.get("Symbol", "Unknown")),
            "Investment": stock["Investment"]
        })

    profit_percent = (
        total_profit / total_investment * 100
        if total_investment > 0 else 0
    )

    return {
        "investment": total_investment,
        "current": total_current,
        "profit": total_profit,
        "profit_percent": profit_percent,
        "allocation": allocation,
        "best_stock": best_stock.get("Stock", best_stock.get("Symbol", "Unknown")),
        "worst_stock": worst_stock.get("Stock", worst_stock.get("Symbol", "Unknown")),
        "stock_count": len(portfolio)
    }