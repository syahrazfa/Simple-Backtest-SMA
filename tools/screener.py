import pandas as pd
import os

datadir = os.path.join(os.path.dirname(__file__), '..', 'data')

# Collecting tickers from ..\\data folder
def ticker(name, path=datadir):
    """
    Function to collect the ticker data from data directory
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

    if name in stocks:
        return stocks[name]

    else:
        raise ValueError(f"{name} not found")


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
    df['fast_sma'] = df['Close'].rolling(fast).mean()
    df['medium_sma'] = df['Close'].rolling(medium).mean()
    df['slow_sma'] = df['Close'].rolling(slow).mean()
    df['Signal'] = 0

    # Indicating SMA Signals
    df.loc[(df['fast_sma'] > df['medium_sma']) & (df['medium_sma'] > df['slow_sma']), 'Signal'] = 1
    df.loc[(df['fast_sma'] < df['medium_sma']) & (df['medium_sma'] < df['slow_sma']), 'Signal'] = -1

    df['Trade'] = df['Signal'].diff()
    df.dropna(subset=['fast_sma', 'medium_sma', 'fast_sma'], inplace=True)

    df.reset_index(drop=True, inplace=True)
    print("Buy signals:", (df['Signal'] == 1).sum())
    print("Sell signals:", (df['Signal'] == -1).sum())

    return df