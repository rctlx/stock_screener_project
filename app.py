import streamlit as st
import yfinance as yf
import pandas as pd

# ✅ Page config (important)
st.set_page_config(
    layout="wide",
    page_title="Stock Dashboard",
)

# ✅ Custom styling (Zerodha-like clean UI)
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

/* Title */
h1 {
    text-align: center;
}

/* Metric cards */
.metric-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1a1f2b;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
    text-align: center;
}

/* Table styling */
.stDataFrame {
    font-size: 15px;
}

/* Hover highlight */
tr:hover {
    background-color: #2a2f3a;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# Title
# ==========================
st.markdown("<h1>📊 Smart Stock Dashboard</h1>", unsafe_allow_html=True)

# ==========================
# Load Nifty 500 symbols
# ==========================

@st.cache_data
def load_symbols():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    df = pd.read_csv(url)
    return [s + ".NS" for s in df["Symbol"].tolist()]

stocks = load_symbols()

# ==========================
# Fetch data
# ==========================

@st.cache_data
def load_data(stocks):
    data = []

    for symbol in stocks[:150]:  # performance balance
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            data.append({
                "Stock": symbol,
                "Name": info.get("longName"),
                "Sector": info.get("sector"),
                "Price": info.get("currentPrice"),
                "52W High": info.get("fiftyTwoWeekHigh"),
                "52W Low": info.get("fiftyTwoWeekLow"),
                "P/E": info.get("trailingPE")
            })
        except:
            continue

    return pd.DataFrame(data)

df = load_data(stocks)

# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header("🔍 Filters")

# Check if df is not empty and 'Sector' column exists
if not df.empty and "Sector" in df.columns:
    sectors = df["Sector"].dropna().unique()

    selected_sector = st.sidebar.selectbox(
        "Select Sector",
        ["All"] + list(sectors)
    )

    if selected_sector != "All":
        df = df[df["Sector"] == selected_sector]
else:
    st.sidebar.warning("Unable to load stock data or 'Sector' information is missing.")
    # If df is empty or 'Sector' is missing, then we should prevent further errors
    # by ensuring df is an empty DataFrame with the expected columns for later use.
    # This will cause the rest of the display to show empty data gracefully.
    df = pd.DataFrame(columns=["Stock", "Name", "Sector", "Price", "52W High", "52W Low", "P/E"])
    selected_sector = "All"

# ==========================
# ✅ Metrics (Top cards)
# ==========================


col1, col2 = st.columns(2)
col1.metric("Total Stocks", len(df))
col2.metric("Sectors", df["Sector"].nunique())

# ==========================
# ✅ Format data
# ==========================

df["Price"] = df["Price"].round(2)
df["52W High"] = df["52W High"].round(2)
df["52W Low"] = df["52W Low"].round(2)

# ✅ Optional: add % from high (very useful)
df["% from High"] = ((df["Price"] / df["52W High"]) - 1) * 100

# ==========================
# ✅ Sorting options
# ==========================

sort_by = st.selectbox(
    "Sort By",
    ["Price", "P/E", "% from High"]
)

df = df.sort_values(sort_by, ascending=False)

# ==========================
# ✅ Big table display
# ==========================

st.subheader("📈 Stocks")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)
