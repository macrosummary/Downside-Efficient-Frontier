import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging

# * Import helper functions
from helper_functions import *

# ---------------------------------- Program --------------------------------- #

def main():
    st.title("Downside/Upside Volatility Asset Comparison")
    st.write('To construct portfolios, assets are often compared based on their placement in the efficient frontier. However, under certain circumstances, this might not be enough, as upside volatility is not necessarily a bad thing, especially, when the asset shows some kind of volatility convexity.')
    st.write('This tool helps to compare assets based on their upside/downside volatility. It can be used not only for assets but also to compare funds and systematic strategies.')
    st.info('The results of this tool are not necessarily correct and no investment decision should be made on behalf of this. You should contact an investment advisor before making any investment decision.', icon="ℹ️")

    # put the widgets in a sidebar
    ticker_symbols_input = st.sidebar.text_input("Enter the Yahoo Finance Ticker Symbols (separated by commas):", "", key="ticker_symbols_input")
    ticker_symbols = [symbol.strip() for symbol in ticker_symbols_input.split(',')]
    period = st.sidebar.selectbox("Select the data frequency:", options=["1d", "1wk", "1mo"], key="period_select")
    if period == "1d":
        timescale = 252
    elif period == "1wk":
        timescale = 50
    elif period == "1mo":
        timescale = 12
    else:
        timescale = None
        logging.error(f"Period entered is invalid: {period}")

    start_date = st.sidebar.date_input("Select start date:", value=datetime(1950, 1, 1), key="start_date_slider")

    end_date = st.sidebar.date_input("Select end date:", value=datetime.today(), key="end_date_slider")

    if st.sidebar.button("Fetch data and analyze"):

        data = download_data(ticker_symbols, start_date, end_date, period)

        if data is not None:
            result_df = pd.DataFrame()
            for ticker_symbol in ticker_symbols:
                symbol_data = data[ticker_symbol]
                ret, vol = calculate_monthly_return_and_volatility(symbol_data, timescale)
                vola_df = pd.DataFrame({'Ticker': ticker_symbol, 'Return': [ret], 'Volatility': [vol], 'Type': 'Volatility'})
                down_ret, down_vol = calculate_monthly_return_and_downside_volatility(symbol_data, timescale)
                down_vola_df = pd.DataFrame({'Ticker': ticker_symbol, 'Return': [down_ret], 'Volatility': [down_vol], 'Type': 'Downside Volatility'})
                up_ret, up_vol = calculate_monthly_return_and_upside_volatility(symbol_data, timescale)
                up_vola_df = pd.DataFrame({'Ticker': ticker_symbol, 'Return': [up_ret], 'Volatility': [up_vol], 'Type': 'Upside Volatility'})
                result_df = pd.concat([result_df, vola_df, down_vola_df, up_vola_df])


            # Create a scatter plot
            fig = px.scatter(result_df, x='Volatility', y='Return', color='Ticker', hover_data=['Ticker', 'Return', 'Volatility', 'Type'], title='Return vs Volatility')
            fig.update_traces(showlegend=True)
            fig.update_traces(mode='markers', marker=dict(sizemode='diameter', sizeref=0.1, size=10))

            # Add annotation
            fig.add_annotation(
                x=0, y=0, # this positions the text at the bottom left of the x axis
                xref="paper", yref="paper", # this means the x and y coordinates are in fraction of the plot area (from 0 to 1)
                text="Created by Macro Summary", # text to be displayed
                showarrow=False, # don't show an arrow pointing from the text to a point
                font=dict(size=12) # adjust the font size to your liking
            )

            # Display the plot
            logging.info(f"Displaying scatter plot for {ticker_symbols}")
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
