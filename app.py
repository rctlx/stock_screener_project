
import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Sector-Based Stock Screener")

stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS",
    "HDFCBANK.NS","SBIN.NS","ITC.NS",
    "LT.NS","BAJFINANCE.NS","AXISBANK.NS"
]

# Load data
@st.cache_data
def load_data():
    results = []

    for symbol in stocks:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            results.append({
                "Stock": symbol,
                "Sector": info.get("sector"),
                "P/E": info.get("trailingPE"),
                "ROE (%)": info.get("returnOnEquity"),
                "Debt": info.get("debtToEquity")
            })
        except:
            continue

    return pd.DataFrame(results)

df = load_data()

# ==========================
# ✅ SECTOR FILTER (Dropdown)
# ==========================

sectors = df["Sector"].dropna().unique()

selected_sector = st.selectbox(
    "Select Sector",
    ["All"] + list(sectors)
)

# Apply filter
if selected_sector != "All":
    df = df[df["Sector"] == selected_sector]

# ==========================
# Extra filters (optional)
# ==========================

st.sidebar.header("Advanced Filters")

min_roe = st.sidebar.slider("Min ROE (%)", 0, 50, 15)
max_pe = st.sidebar.slider("Max P/E", 5, 100, 40)
max_debt = st.sidebar.slider("Max Debt", 0.0, 2.0, 1.0)

df = df[
    (df["ROE (%)"] > min_roe/100) &
    (df["P/E"] < max_pe) &
    (df["Debt"] < max_debt)
]

# ==========================
# Display
# ==========================

st.subheader("📈 Filtered Stocks")
st.dataframe(df.sort_values("ROE (%)", ascending=False))
