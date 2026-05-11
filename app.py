import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Smart Stock Screener Dashboard (India)")

@st.cache_data
def load_symbols():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    df = pd.read_csv(url)
    symbols = df["Symbol"].tolist()
    return [s + ".NS" for s in symbols]

stocks = load_symbols()

st.write(f"Loaded {len(stocks)} stocks")

def score_pe(pe):
    if pe is None: return 0
    elif pe < 15: return 10
    elif pe < 25: return 7
    else: return 4

def score_roe(roe):
    if roe is None: return 0
    elif roe > 0.20: return 10
    elif roe > 0.15: return 7
    else: return 4

def score_debt(debt):
    if debt is None: return 0
    elif debt < 0.5: return 10
    elif debt < 1: return 7
    else: return 4

def score_momentum(symbol):
    try:
        data = yf.download(symbol, period="6mo", progress=False)
        returns = (data["Close"][-1] / data["Close"][0]) - 1

        if returns > 0.30: return 10
        elif returns > 0.15: return 7
        else: return 4
    except:
        return 0

sector_filter = st.sidebar.text_input("Sector filter")
run = st.sidebar.button("Run Screener")

if run:
    results = []

    for symbol in stocks[:50]:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            pe = info.get("trailingPE")
            roe = info.get("returnOnEquity")
            debt = info.get("debtToEquity")
            sector = info.get("sector")

            score = (
                score_pe(pe)*0.25 +
                score_roe(roe)*0.30 +
                score_debt(debt)*0.20 +
                score_momentum(symbol)*0.25
            )

            results.append({
                "Stock": symbol,
                "Sector": sector,
                "Score": round(score,2),
            })

        except:
            continue

    df = pd.DataFrame(results)

    if sector_filter:
        df = df[df["Sector"].str.contains(sector_filter, na=False)]

    df = df.sort_values("Score", ascending=False)

    st.dataframe(df.head(10))
