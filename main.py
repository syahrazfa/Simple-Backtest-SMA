import backtest
from tools import screener
import matplotlib.pyplot as plt



def plotting(df):
plt.figure(figsize=(20,10))
plt.plot(df['CLose'], label='Close Price', alpha=0.5)
plt.plot(df['fast_sma'], label='SMA', linestyle='dashed', linewidth=2)
plt.plot(df['medium_sma'], label='SMA', linestyle='dashed', linewidth=2)
plt.plot(df['slow_sma'], label='SMA', linestyle='dashed', linewidth=2)
