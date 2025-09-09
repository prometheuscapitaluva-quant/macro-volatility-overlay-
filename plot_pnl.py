import pandas as pd
import matplotlib.pyplot as plt

# Load trades
trades = pd.read_csv("results/trades.csv", parse_dates=['date'])

# Calculate P&L per trade
trades['pnl'] = trades['premium'] * trades['contracts']

# Aggregate daily P&L
daily_pnl = trades.groupby('date')['pnl'].sum().cumsum()

# Plot
plt.figure(figsize=(12,6))
plt.plot(daily_pnl.index, daily_pnl.values, marker='o')
plt.title("Cumulative P&L - Macro Volatility Overlay")
plt.xlabel("Date")
plt.ylabel("Cumulative P&L (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()
