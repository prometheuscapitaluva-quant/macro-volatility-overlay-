# macro-volatility-overlay-
Python Back test for a macro volatility overlay strategy across KC, SPX, and EUR/USD, including realistic execution delay and slippage.
# Macro Volatility Overlay Backtest

This repository contains a **Python backtest for a macro volatility overlay strategy** across Coffee (KC), S&P 500 (SPX), and EUR/USD.

## Strategy Overview

- **Objective:** Harvest volatility risk premia and tail convexity in macro instruments.
- **Trade Type:** Iron Condors and ATM straddles.
- **Time Horizon:** 30-day options.
- **Position Sizing:** €150k notional per product.
- **Execution Model:** Includes realistic broker execution delay (40–120 minutes) and bid/ask slippage (0.1%).

## Current Market Conditions (Sep 2025)

| Instrument | Spot     | Implied Volatility | Realized Volatility |
|------------|----------|--------------------|---------------------|
| Coffee (KC)| $390.00  | 44%                | 30%                 |
| SPX        | 6,495.15 | 11.82%             | 10.5%               |
| EUR/USD    | 1.1736   | 8.1%               | 5%                  |

## Estimated P&L (Realistic)

| Instrument | Premium Collected | Max Risk | Net Credit | Max Loss | Risk/Reward Ratio |
|------------|-------------------|----------|------------|----------|-------------------|
| Coffee (KC)| $1,200            | $1,800   | $1,200     | $1,800   | 1:1.5             |
| SPX        | $9,000            | $13,500  | $9,000     | $13,500  | 1:1.5             |
| EUR/USD    | $2,675            | $4,012.5 | $2,675     | $4,012.5 | 1:1.5             |

## Usage

#Please use the following python scripts for best free usage of the data sets you will need. Quandl (https://data.nasdaq.com/?utm_source) and specific Brokerage Exchange data will have paywalls.'

import yfinance as yf

# Coffee
kc = yf.download("KC=F", start="2023-01-01", end="2025-09-01")
kc[['Close']].to_csv("data/kc.csv", index_label='date')

# SPX
spx = yf.download("^GSPC", start="2023-01-01", end="2025-09-01")
spx[['Close']].to_csv("data/spx.csv", index_label='date')

# EUR/USD
eurusd = yf.download("EURUSD=X", start="2023-01-01", end="2025-09-01")
eurusd[['Close']].to_csv("data/eurusd.csv", index_label='date')
#Use of Ai for the above code has been employed as this strategy is meant to be implemented on an institutional level, in size. 


```bash
python macro_vol_overlay.py
