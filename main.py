from tools import screener
from tools import fetch as fetcher
from backtest import backtest
import matplotlib.pyplot as plt


def plotting(df, symbol, trade_log):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10), gridspec_kw={'height_ratios': [3, 1]})

    # --- Price + SMAs ---
    ax1.plot(df['Close'], label='Close Price', alpha=0.5, color='#607d8b')
    ax1.plot(df['fast_sma'], label='SMA Fast', linestyle='dashed', linewidth=2, color='#2196F3')
    ax1.plot(df['medium_sma'], label='SMA Medium', linestyle='dashed', linewidth=2, color='#FF9800')
    ax1.plot(df['slow_sma'], label='SMA Slow', linestyle='dashed', linewidth=2, color='#9C27B0')

    # --- Trade signals ---
    buys = df[df['Trade'] == 1.0]
    sells = df[df['Trade'] == -1.0]
    ax1.scatter(buys.index, buys['Close'], label='Buy Signal', color='green', marker='^', s=100, zorder=5)
    ax1.scatter(sells.index, sells['Close'], label='Sell Signal', color='red', marker='v', s=100, zorder=5)

    # --- Stop Loss ---
    stops = df[df.index.isin([t[1] for t in trade_log if t[0] == 'STOP'])]
    ax1.scatter(stops.index, stops['Close'], label='Stop Loss', color='orange', marker='x', s=150, zorder=5)

    ax1.set_title(f"SMA Crossover Strategy — {symbol}", fontsize=18)
    ax1.set_ylabel("Price ($)")
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # --- Volume ---
    colors = ['green' if df['Close'].iloc[i] >= df['Close'].iloc[i - 1] else 'red'
              for i in range(len(df))]
    ax2.bar(df.index, df['Volume'], color=colors, alpha=0.5, width=0.8)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Volume")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'plot/{symbol}_backtest.png', dpi=150, bbox_inches='tight')
    plt.show()


def run(symbol):
    fetcher.fetch([symbol], "2020-01-01", "2024-12-31")
    df = screener.ticker(symbol)
    df = screener.signals(df)

    result = backtest(df)

    print(f"\n{'=' * 40}")
    print(f"  {symbol} Backtest Results")
    print(f"{'=' * 40}")
    print(f"  Final Value : ${result['final']:,.2f}")
    print(f"  Return      : {result['return']:+.2f}%")
    print(f"  Trades      : {len(result['trade_log'])}")
    print(f"{'=' * 40}\n")

    for entry in result['trade_log']:
        action, date, price = entry
        print(f"  {action:4s}  {date}  ${price:,.2f}")

    plotting(df, symbol, result['trade_log'])


if __name__ == '__main__':
    for symbol in ['AAPL', 'MSFT', 'TSLA']:
        run(symbol)