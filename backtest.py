def backtest(df, capital=100000):
    cash = capital
    position = 0       # was 'positions' — inconsistent naming, also used 'position' later
    trades = []
    returns = []
    portfolio_value = []
    trade_log = []
    buy_price = 0      # initialize here — was undefined if sell triggers before any buy

    for i in range(len(df)):
        price = df['Close'].iloc[i]    # .iloc[i] instead of [i] — safer with reset_index
        signal = df['Signal'].iloc[i]  # fix column name to match screener.py
        date = df['Date'].iloc[i]

        if signal == 1 and position == 0:   # position == 0 instead of cash > 0
            buy_price = price               # prevents double-buying
            position = cash / price
            cash = 0.0
            trade_log.append(('BUY', date, price))

        elif signal == -1 and position > 0:  # position > 0 instead of cash > 0
            sell_price = price               # was checking wrong variable
            cash = position * sell_price
            profit = (sell_price - buy_price) / buy_price
            returns.append(profit)
            trade_log.append(('SELL', date, price))
            position = 0.0

    # Portfolio Track
    final_value = cash + (position * df['Close'].iloc[-1])  # position * price, not cash
    portfolio_value.append(final_value)

    return {
        'final': round(final_value, 2),
        'return': round((final_value - capital) / capital * 100, 2),
        'returns': returns,
        'trade_log': trade_log,
        'portfolio_value': portfolio_value
    }