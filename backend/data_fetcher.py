import yfinance as yf
import os

# =========================
# INDIAN STOCKS
# =========================

stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "SBIN.NS","AXISBANK.NS","KOTAKBANK.NS","INDUSINDBK.NS",
    "BAJFINANCE.NS","BAJAJFINSV.NS","HCLTECH.NS","TECHM.NS",
    "WIPRO.NS","LT.NS","ULTRACEMCO.NS","ASIANPAINT.NS",
    "TITAN.NS","MARUTI.NS","TATAMOTORS.NS","M&M.NS",
    "HEROMOTOCO.NS","EICHERMOT.NS","BHARTIARTL.NS",
    "ITC.NS","HINDUNILVR.NS","NESTLEIND.NS","BRITANNIA.NS",
    "SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS","DIVISLAB.NS",
    "ONGC.NS","BPCL.NS","IOC.NS","POWERGRID.NS","NTPC.NS",
    "TATASTEEL.NS","JSWSTEEL.NS","HINDALCO.NS",
    "ADANIENT.NS","ADANIPORTS.NS","ADANIGREEN.NS",
    "COALINDIA.NS","GRASIM.NS","SHRIRAMFIN.NS",
    "ZOMATO.NS","PAYTM.NS","NYKAA.NS"
]

# =========================
# MARKET INDEXES
# =========================

indexes = [
    "^NSEI",
    "^BSESN",
    "^NSEBANK",
    "^CNXIT",
    "^CNXAUTO",
    "^CNXPHARMA"
]

# =========================
# US STOCKS
# =========================

us_stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "TSLA",
    "AMD",
    "NFLX",
    "JPM",
    "BAC",
    "GS",
    "V",
    "MA"
]

# =========================
# GLOBAL INDEXES
# =========================

global_indexes = [
    "^GSPC",
    "^DJI",
    "^IXIC",
    "^RUT",
    "^FTSE",
    "^N225",
    "^HSI"
]

# =========================
# COMMODITIES
# =========================

commodities = [
    "GC=F",   # Gold
    "SI=F",   # Silver
    "CL=F",   # Crude Oil
    "NG=F",   # Natural Gas
    "HG=F"    # Copper
]

# =========================
# FOREX
# =========================

forex = [
    "USDINR=X",
    "EURINR=X",
    "GBPINR=X",
    "JPYINR=X",
    "EURUSD=X",
    "GBPUSD=X"
]

# =========================
# CRYPTO
# =========================

crypto = [
    "BTC-USD",
    "ETH-USD",
    "BNB-USD",
    "SOL-USD",
    "XRP-USD"
]

# =========================
# COMBINE EVERYTHING
# =========================

all_symbols = (
    stocks
    + indexes
    + us_stocks
    + global_indexes
    + commodities
    + forex
    + crypto
)

# =========================
# CREATE DATA FOLDER
# =========================

os.makedirs("data", exist_ok=True)

# =========================
# DOWNLOAD DATA
# =========================

for symbol in all_symbols:

    try:

        print(f"Downloading {symbol}")

        df = yf.download(
            symbol,
            period="5y",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if len(df) == 0:
            print(f"No data for {symbol}")
            continue

        filename = (
            symbol.replace("^", "")
                  .replace("=", "_")
                  .replace("/", "_")
        )

        df.to_csv(f"data/{filename}.csv")

        print(f"Saved {symbol}")

    except Exception as e:

        print(f"Error downloading {symbol}: {e}")

print("\nALL DATASETS DOWNLOADED SUCCESSFULLY")