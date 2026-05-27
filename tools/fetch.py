import yfinance as yf
import os
import pandas as pd

def fetch(tickers, start, end):

    folder = os.path.join(os.path.dirname(__file__), '..', 'data')  # absolute path

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    for ticker in tickers:
        print(f'{ticker} loading data...')

        filedir = os.path.join(folder, f"{ticker}.csv")

        data = yf.download(ticker, start, end)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data.reset_index(inplace=True)
        data['Date'] = data['Date'].astype(str)

        if os.path.exists(filedir):
            old_data = pd.read_csv(filedir)
            old_data['Date'] = old_data['Date'].astype(str)
            combined = pd.concat([old_data, data])
            combined.drop_duplicates(subset='Date', inplace=True)
            combined.sort_values(by='Date', inplace=True)
            combined.to_csv(filedir, index=False)
            print(f'{ticker} data updated.')
        else:
            data.to_csv(filedir, index=False)
            print(f'{ticker} created.')