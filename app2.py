import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Streamlit UI
st.title("NSE Algo Trading Dashboard 📈")

# User input for stock selection
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS):", "RELIANCE.NS")

# Moving Averages
short_window = st.slider("Short Moving Average Window", 5, 50, 10)
long_window = st.slider("Long Moving Average Window", 20, 200, 50)

# Fetch stock data
@st.cache_data(ttl=60)
def fetch_data(symbol):
    df = yf.download(symbol, period="7d", interval="15m")
    df["SMA_Short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_Long"] = df["Close"].rolling(window=long_window).mean()
    df["Signal"] = np.where(df["SMA_Short"] > df["SMA_Long"], "BUY", "SELL")
    return df

# Display Data
if st.button("Get Live Data"):
    data = fetch_data(symbol)
    st.write(f"Latest Price for {symbol}: {data['Close'].iloc[-1]:.2f} INR")
    
    # Show trading signals
    st.subheader("Trading Signals")
    st.dataframe(data[["Close", "SMA_Short", "SMA_Long", "Signal"]].dropna().tail(10))

    # Plot
    st.line_chart(data[["Close", "SMA_Short", "SMA_Long"]])

# Refresh Data
st.write("Live updates every 60 seconds")
time.sleep(60)
st.experimental_rerun()
