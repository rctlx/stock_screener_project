
import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Sector-Based Stock Viewer (Nifty 500)")

# ✅ Load Nifty 500
@st.cache_data
def load_symbols():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    df = pd.read_csv(url)
    return [s + ".NS" for s in df["Symbol"].tolist()]

stocks = load_symbols()

st.write(f"Loaded {len(stocks)} stocks")

# ✅ Load stock data with extra fields
@st.cache_data
def load_data(stocks):
    data = []

    for symbol in stocks[:100]:   # limit for speed
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            data.append({
                "Stock": symbol,
                "Name": info.get("longName"),
                "Sector": info.get("sector"),
                "Last Price": info.get("currentPrice"),
                "52W High": info.get("fiftyTwoWeekHigh"),
                "52W Low": info.get("fiftyTwoWeekLow"),
                "P/E": info.get("trailingPE")
            })
        except:
            continue

    return pd.DataFrame(data)

df = load_data(stocks)

# ==========================
# ✅ DROPDOWN FILTER
# ==========================

sectors = df["Sector"].dropna().unique()

selected_sector = st.selectbox(
    "Select Sector",
    ["All"] + list(sectors)
)

# ✅ Apply filter
if selected_sector != "All":
    filtered_df = df[df["Sector"] == selected_sector]
else:
    filtered_df = df

st.subheader("📈 Stocks in Selected Sector")

st.dataframe(
    filtered_df,
    use_container_width=True,  # ✅ makes table full width
    height=600                 # ✅ increases table height
)

# ==========================
# ✅ DISPLAY TABLE
# ==========================

st.subheader("📈 Stocks in Selected Sector")

st.dataframe(
    filtered_df.sort_values("Last Price", ascending=False),
    use_container_width=True
)
