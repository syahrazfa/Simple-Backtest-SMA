from tools import screener

def backtest(df, capital=100000):
    cash = capital
    positions = 0
    trades = []
    returns = []
    portfolio_value = []
    trade_log = []

    for i in range(len(df)):
        price = df['Close'][i]
        signals = df['Signals'][i]
        date = df['Date'][i]

        if signals == 1 and cash > 0:
            # BUY
            buy_price = price
            position = cash / price
            cash = 0.0
            trade_log.append(('BUY', date, price))

        elif signals == -1 and cash > 0:
            sell_price = price
            cash = position * sell_price
            profit = (sell_price - buy_price) / buy_price
            returns.append(profit)
            trade_log.append(('SELL', date, price))
            position = 0.0

    # Portfolio Track
    total_cash = cash + (position * cash)
    portfolio_value.append(total_cash)
