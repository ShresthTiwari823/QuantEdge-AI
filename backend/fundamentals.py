import requests
from config import ALPHA_API_KEY

def get_company_overview(symbol):

    ticker = symbol.replace(".NS", "")

    url = (
        "https://www.alphavantage.co/query?"
        f"function=OVERVIEW"
        f"&symbol={ticker}"
        f"&apikey={ALPHA_API_KEY}"
    )

    try:

        data = requests.get(url).json()

        return {
            "MarketCap":
            data.get("MarketCapitalization", "N/A"),

            "PE":
            data.get("PERatio", "N/A"),

            "EPS":
            data.get("EPS", "N/A"),

            "Sector":
            data.get("Sector", "N/A")
        }

    except:

        return {}