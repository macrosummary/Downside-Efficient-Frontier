import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging

def calculate_monthly_return_and_volatility(series, timescale=252):
    # Calculate the daily returns
    daily_returns = series.pct_change()

    # Calculate the mean daily return and daily volatility
    mean_daily_return = daily_returns.mean()
    daily_volatility = daily_returns.std()

    # Calculate the monthly return and volatility
    monthly_return = mean_daily_return * timescale  # There are approximately 21 trading days in a month
    monthly_volatility = daily_volatility * (timescale ** 0.5)  # Square root of 21 to annualize the volatility

    return monthly_return, monthly_volatility


def calculate_monthly_return_and_downside_volatility(series, timescale=21):
    # Calculate the daily returns
    daily_returns = series.pct_change()

    # Calculate the mean daily return
    mean_daily_return = daily_returns.mean()

    # Calculate the daily downside volatility
    downside_returns = daily_returns[daily_returns < 0]
    daily_downside_volatility = downside_returns.std()

    # Calculate the monthly return and downside volatility
    monthly_return = mean_daily_return * timescale
    monthly_downside_volatility = daily_downside_volatility * (timescale ** 0.5)

    return monthly_return, monthly_downside_volatility

def calculate_monthly_return_and_upside_volatility(series, timescale=21):
    # Calculate the daily returns
    daily_returns = series.pct_change()

    # Calculate the mean daily return
    mean_daily_return = daily_returns.mean()

    # Calculate the daily downside volatility
    upside_returns = daily_returns[daily_returns > 0]
    daily_upside_volatility = upside_returns.std()

    # Calculate the monthly return and downside volatility
    monthly_return = mean_daily_return * timescale
    monthly_upside_volatility = daily_upside_volatility * (timescale ** 0.5)

    return monthly_return, monthly_upside_volatility


def download_data(ticker_symbols, start_date, end_date, period):
    logging.info(f"Fetching data for {ticker_symbols} from {start_date} to {end_date} with {period} frequency")
    try:
        data = yf.download(ticker_symbols, start=start_date, end=end_date, interval=period)
        return data
    except Exception as e:
        logging.error(f"Error occurred while fetching data: {e}")
        st.error(f"An error occurred while fetching data.")
        return None

def main():
    st.title("Yahoo Finance Ticker Symbol Data Analysis")

    ticker_symbols_input = st.text_input("Enter the Yahoo Finance Ticker Symbols (separated by commas):", "", key="ticker_symbols_input")
    ticker_symbols = [symbol.strip() for symbol in ticker_symbols_input.split(',')]
    period = st.selectbox("Select the data frequency:", options=["1d", "1wk", "1mo"], key="period_select")
    if period == "1d":
        timescale = 252
    elif period == "1wk":
        timescale = 50
    elif period == "1mo":
        timescale = 12
    else:
        timescale = None
        logging.error(f"Period entered is invalid: {period}")

    # if 'start_date' not in st.session_state:
        # st.session_state['start_date'] = datetime(2020, 1, 1)
    start_date = st.date_input("Select start date:", value=st.session_state['start_date'], key="start_date_slider")
    # st.session_state['start_date'] = start_date

    # if 'end_date' not in st.session_state:
    #     st.session_state['end_date'] = datetime.today()
    end_date = st.date_input("Select end date:", value=st.session_state['end_date'], key="end_date_slider")
    # st.session_state['end_date'] = end_date

    if st.button("Fetch data and analyze"):
        # # Check if data already exists in session state
        # if "data" in st.session_state:
        #     data = st.session_state["data"]
        # else:
        data = download_data(ticker_symbols, start_date, end_date, period)
            # st.session_state["data"] = data

        if data is not None:
            result_df = pd.DataFrame()
            for ticker_symbol in ticker_symbols:
                symbol_data = data['Close'][ticker_symbol]
                ret, vol = calculate_monthly_return_and_downside_volatility(symbol_data, timescale)
                temp_df = pd.DataFrame({'Return': [ret], 'Volatility': [vol]}, index=[ticker_symbol])
                result_df = pd.concat([result_df, temp_df])


            # Create a scatter plot
            fig = px.scatter(result_df, x='Volatility', y='Return', title='Return vs Volatility')
            fig.update_traces(mode='markers', marker=dict(sizemode='diameter', sizeref=0.1, size=10))


            # Display the plot
            logging.info(f"Displaying scatter plot for {ticker_symbols}")
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
