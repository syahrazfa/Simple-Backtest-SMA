import pandas as pd
import os

datadir = os.path.join(os.path.dirname(__file__), '..', 'data')

# Collecting tickers from ..\\data folder
def ticker(path):
    """
    Function to collect the ticker data from ../data
    Based on the parameter path
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data directory not found: {path}")

    stocks = {}

    for i in os.listdir(path):

        if i.endswith('.csv'):
            tick = i.replace('.csv', '')

            fullpath = os.path.join(path, i)

            data = pd.read_csv(fullpath)

            stocks[tick] = data

    return stocks


# Creating SMA Function
def signals(df, fast=50, medium=100, slow=200):
    """
    Simple Moving Average an analytics indicator to smoothening the price fluctuations
    and identifying market trend directions.

    :param df: DataFrame
    :param fast: Short Period
    :param medium: Medium Period
    :param slow: Long Period
    :return:
    """
    df = df.copy()
    fast_sma = df['Close'].rolling(fast).mean()
    medium_sma = df['Close'].rolling(medium).mean()
    slow_sma = df['Close'].rolling(slow).mean()
    df['Signals'] = 0

    # Indicating SMA Signals
    df.loc[(fast_sma > medium_sma) & (medium_sma > slow_sma), 'Signal'] = 1
    df.loc[(fast_sma < medium_sma) & (medium_sma < slow_sma), 'Signal'] = -1

    df['Trade'] = df['Signals'].diff()

    return df