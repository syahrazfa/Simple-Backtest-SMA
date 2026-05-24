import pandas as pd
import os

datadir = '..\\data'


def ticker(name):
    """
    Function to collect the ticker data from ../data
    Based on the parameter name
    """
    stocks = {}

    for i in os.listdir(datadir):

        if i.endswith('.csv'):

            ticker = i.replace('.csv', '')

            path = os.path.join(datadir, i)

            data = pd.read_csv(path)

            stocks[ticker] = data

    return stocks

