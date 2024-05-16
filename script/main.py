import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def compute_rsi(data, window=14):
    delta = data['Adj Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    # Replace 'TICKER' with the symbol of the stock you want to analyze
    ticker_list = ['TSLA', 'AAPL']
    # Replace 'START_DATE' and 'END_DATE' with the date range you want to analyze
    # Define start and end dates
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')
    
    st.title('Stock market data')

    buy_signal = []
    sell_signal = []

    # Fetch data from yfinance
    for t in ticker_list:
        data = yf.download(t, start=start_date, end=end_date)
        # Compute RSI
        data['RSI'] = compute_rsi(data)
        latest_rsi = data['RSI'].iloc[-1]
        if latest_rsi < 30:
            buy_signal.append((t, latest_rsi))
        elif latest_rsi > 70:
            sell_signal.append((t, latest_rsi))
        else:
            pass
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Buy signal')
        for b in buy_signal:
            st.metric(label="RSI", value=b[0], delta=b[1], delta_color="normal")

    with col2:
        st.markdown('## Sell signal')
        for s in sell_signal:
            st.metric(label="RSI", value=s[0], delta=s[1], delta_color="inverse")   

if __name__ == "__main__":
    main()

