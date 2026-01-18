import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="NA Stock Screener", layout="wide")
st.title("📊 North America Mid-Cap Screener")

# 2. Define your "Universe" (e.g., S&P 400 MidCap or a manual list)
# For this example, let's use a small sample list.
ticker_list = ['VAC', 'ALA.TO', 'ADTN', 'WRB', 'ENOV', 'CRMT', 'EXEL']

@st.cache_data(ttl=3600) # Caches data for 1 hour to stay "live" but fast
def get_data(tickers):
    stocks_data = []
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            info = stock.info
            # Fetching Screener.in style ratios
            stocks_data.append({
                "Ticker": t,
                "Name": info.get("shortName"),
                "Price": info.get("currentPrice"),
                "Market Cap ($B)": info.get("marketCap", 0) / 1e9,
                "P/E Ratio": info.get("trailingPE"),
                "Debt/Equity": info.get("debtToEquity"),
                "ROE (%)": info.get("returnOnEquity", 0) * 100
            })
        except:
            continue
    return pd.DataFrame(stocks_data)

# 3. Sidebar Filters
st.sidebar.header("Filters (Screener.in Style)")
min_cap, max_cap = st.sidebar.slider("Market Cap ($B)", 0.0, 10.0, (1.0, 5.0))
max_pe = st.sidebar.number_input("Max P/E Ratio", value=30.0)

# 4. Main Display
df = get_data(ticker_list)
filtered_df = df[(df['Market Cap ($B)'].between(min_cap, max_cap)) & 
                 (df['P/E Ratio'] <= max_pe)]

st.subheader(f"Found {len(filtered_df)} Companies")
st.dataframe(filtered_df, use_container_width=True)

# 5. Insider Buying Section (Manual or API-driven)
st.divider()
st.subheader("🕵️ Recent Insider Buying (Last 3 Months)")
st.info("Note: Real-time insider data often requires a paid API like Finnhub or SEC-API.io.")
# Displaying the table we discussed earlier
insider_data = {
    "Ticker": ["VAC", "ALA", "WRB", "ENOV"],
    "Insider": ["Cluster Buy", "Cluster Buy", "W.R. Berkley", "Exec Team"],
    "Value": ["$6.2M", "$2.5M", "$535K", "42K Shares"]
}
st.table(insider_data)
