import yfinance as yf


def get_company_insights(symbol):

    try:

        stock = yf.Ticker(symbol)

        info = stock.info

        return {

            "Company": info.get("longName", "N/A"),

            "Sector": info.get("sector", "N/A"),

            "Industry": info.get("industry", "N/A"),

            "Market Cap": info.get("marketCap", "N/A"),

            "PE Ratio": info.get("trailingPE", "N/A"),

            "EPS": info.get("trailingEps", "N/A"),

            "Dividend Yield": info.get("dividendYield", "N/A"),

            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),

            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),

            "Employees": info.get("fullTimeEmployees", "N/A"),

            "Country": info.get("country", "N/A"),

            "Website": info.get("website", "N/A"),

            "Business Summary": info.get("longBusinessSummary", "N/A")

        }

    except Exception:

        return None