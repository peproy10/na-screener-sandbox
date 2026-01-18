import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Global Equity Insights", layout="wide")

# --- HEADER & SEARCH ---
st.title("📊 North America Stock Quote")
ticker_input = st.text_input("Enter Ticker (e.g., AAPL, MSFT, SHOP.TO):", "AAPL").upper()

stock = yf.Ticker(ticker_input)
info = stock.info

# --- TOP STATS (REPLICATING MONEYCONTROL QUOTE SECTION) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
col2.metric("Day High", f"${info.get('dayHigh', 'N/A')}")
col3.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
col4.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")

# --- TABS (REPLICATING MONEYCONTROL SUB-PAGES) ---
tab1, tab2, tab3 = st.tabs(["Overview", "Financial Results", "Insider Tracker"])

with tab1:
    st.subheader("Interactive Price Chart")
    hist = stock.history(period="1y")
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'])])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Key Ratios")
    r1, r2, r3 = st.columns(3)
    r1.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
    r2.write(f"**Market Cap:** ${info.get('marketCap', 0)/1e9:.2f}B")
    r3.write(f"**ROE:** {info.get('returnOnEquity', 0)*100:.2f}%")

with tab2:
    st.subheader("Annual Financial Statements (Last 3 Years)")
    # Transposing to show years as columns like Moneycontrol
    income = stock.financials.iloc[:, :3]
    st.table(income)

with tab3:
    st.subheader("Insider Transactions")
    insiders = stock.insider_transactions
    if insiders is not None:
        st.dataframe(insiders.head(10), use_container_width=True)
    else:
        st.write("No recent insider data available.")
