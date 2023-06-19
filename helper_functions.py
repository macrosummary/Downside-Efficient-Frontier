import numpy as np
import logging
import yfinance as yf

# ----------------------------- Helper functions ----------------------------- #

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
    """Downloads price data from yahoo finance.

    Args:
        ticker_symbols (string): string of comma separated tickers
        start_date (string): date to start download price data
        end_date (string): date to end download price data
        period (string): daily, weekly, monthly data

    Returns:
        DataFrame: Dataframe of yahoo price data
    """
    logging.info(f"Fetching data for {ticker_symbols} from {start_date} to {end_date} with {period} frequency")
    try:
        data = yf.download(ticker_symbols, start=start_date, end=end_date, interval=period)
        return data['Close']
    except Exception as e:
        logging.error(f"Error occurred while fetching data: {e}")
        return None

