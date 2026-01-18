import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# --- DATA ENGINE ---
def get_detailed_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    
    # Calculations
    eps = info.get('trailingEps', 0)
    bvps = info.get('bookValue', 0)
    graham_num = np.sqrt(22.5 * eps * bvps) if eps > 0 and bvps > 0 else 0
    
    ebit = info.get('ebitda', 0) # Simplified proxy for EBIT
    ev = info.get('enterpriseValue', 1)
    earnings_yield = (ebit / ev) * 100 if ev > 0 else 0

    return {
        "Price": info.get('currentPrice'),
        "Graham Number": graham_num,
        "Earnings Yield (%)": earnings_yield,
        "Market Cap ($B)": info.get('marketCap', 0) / 1e9,
        "P/E": info.get('trailingPE'),
        "Description": info.get('longBusinessSummary')
    }

# --- UI LAYOUT ---
st.title("🚀 NA Equity Screener Pro")

search_ticker = st.text_input("Search Company (e.g., AAPL, VAC, MSFT)", "").upper()

if search_ticker:
    # --- COMPANY VIEW (Deep Dive) ---
    data = get_detailed_data(search_ticker)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${data['Price']}")
    col2.metric("Graham Number", f"${round(data['Graham Number'], 2)}")
    col3.metric("Earnings Yield", f"{round(data['Earnings Yield (%)'], 2)}%")
    
    st.subheader("Business Summary")
    st.write(data['Description'])
    
    # Simple Chart
    hist = yf.Ticker(search_ticker).history(period="1y")
    fig = px.line(hist, y="Close", title=f"{search_ticker} - 1 Year Trend")
    st.plotly_chart(fig, use_container_width=True)

else:
    # --- SCREENER VIEW (Table) ---
    st.info("Enter a ticker above for a deep dive, or view the mid-cap screen below.")
    # (Insert your previous filtering table code here)
