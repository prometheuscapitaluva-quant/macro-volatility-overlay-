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

1. Provide CSV files: `eurusd.csv`, `spx.csv`, `kc.csv` with columns: `date,close`.
2. Run the backtest:

```bash
python macro_vol_overlay.py
