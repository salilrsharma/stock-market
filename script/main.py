import pandas as pd
import ta.momentum
import ta.trend
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import ta
import pickle

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

def main():
    # Replace 'TICKER' with the symbol of the stock you want to analyze
    ticker_list = ['TSLA', 'AAPL', '^GSPC']
    # Replace 'START_DATE' and 'END_DATE' with the date range you want to analyze
    # Define start and end dates
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    st.title('Stock market data')

    buy_signal = []
    sell_signal = []

    # Fetch data from yfinance
    for t in ticker_list[:10]:
        data = yf.download(t, start=start_date, end=end_date)
        # Compute RSI from ta 
        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        data['MACD'] = ta.trend.MACD(data['Close']).macd()
        data['MACD_SIGNAL'] = ta.trend.MACD(data['Close']).macd_signal() 
        data['MACD_DIFF'] = data['MACD'] - data['MACD_SIGNAL']
        
        try:
            latest_rsi = data['RSI'].iloc[-1]
            latest_macd_diff = data['MACD_DIFF'].iloc[-1]
            if latest_rsi < 30 & latest_macd_diff > 0:
                buy_signal.append((t, latest_rsi))
            elif latest_rsi > 70 & latest_macd_diff < 0:
                sell_signal.append((t, latest_rsi))
            else:
                pass
        except IndexError:
            print("Exception")
    col1, col2 = st.tabs(['Buy signal', 'Sell signal'])
    with col1:
        # st.markdown('## Buy signal')
        for b in buy_signal:
            st.metric(label="RSI", value=b[0], delta=b[1], delta_color="normal")

    with col2:
        # st.markdown('## Sell signal')
        for s in sell_signal:
            st.metric(label="RSI", value=s[0], delta=s[1], delta_color="inverse")   

if __name__ == "__main__":
    main()

