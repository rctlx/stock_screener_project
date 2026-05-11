
import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Sector-Based Stock Viewer (Nifty 500)")

# ✅ Load Nifty 500 automatically
@st.cache_data
def load_symbols():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    df = pd.read_csv(url)
    symbols = df["Symbol"].tolist()
    return [s + ".NS" for s in symbols]

stocks = load_symbols()

st.write(f"Loaded {len(stocks)} stocks")

# ✅ Fetch stock info
@st.cache_data
def load_data(stocks):
    data = []

    for symbol in stocks[:150]:   # ⚠️ limit for speed (can increase later)
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            data.append({
                "Stock": symbol,
                "Name": info.get("longName"),
                "Sector": info.get("sector")
            })
        except:
            continue

    return pd.DataFrame(data)

df = load_data(stocks)

# ✅ Dropdown
sectors = df["Sector"].dropna().unique()

selected_sector = st.selectbox(
    "Select Sector",
    ["All"] + list(sectors)
)

# ✅ Filter
if selected_sector != "All":
    filtered_df = df[df["Sector"] == selected_sector]
else:
    filtered_df = df

# ✅ Show results
st.subheader("📈 Stocks in Selected Sector")
st.dataframe(filtered_df)
