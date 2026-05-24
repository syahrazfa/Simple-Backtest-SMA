import yfinance as yf
import os
from stumpy import filepath

def fetch(tickers, start, end):

    folder = "../data"

    # creating the data store directory if not exist
    if not os.path.exists(folder):
        os.mkdir(folder)

    for ticker in tickers:
        print(f'{ticker} loading data...')

        filedir = f"{folder}/{ticker}.csv"

        # download stock data
        data = yf.download(ticker, start, end)

        # convert date to column
        data.reset_index(inplace=True)

        # combining old csv (if exist) with the new one
        if os.path.exists(filedir):

            old_data = data.read_csv(filedir)

            # combine old + new

            combined = data.concat([old_data, data])

            # remove duplicate
            combined.drop_duplicates(Subset='Date' ,inplace=True)

            # sort by date
            combined.sort_values(by=['Date'], inplace=True)

            # save to csv
            combined.to_csv(filepath, index=False)

            print(f'{ticker} data updated.')
        else:
            data.to_csv(filedir, index=False)
            print(f'{ticker} created.')


n = ['AAPL', 'MSFT', 'TSLA']

fetch(n, "2024-01-01", "2024-12-31")


