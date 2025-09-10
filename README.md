# macro-volatility-overlay-
Python Back test for a macro volatility overlay strategy across KC, SPX, and EUR/USD, including realistic execution delay and slippage.
# Macro Volatility Overlay Backtest

This repository contains a **Python backtest for a macro volatility overlay strategy** across Coffee (KC), S&P 500 (SPX), and EUR/USD.

## Strategy Overview

- **Objective:** Harvest volatility risk premia and tail convexity in macro instruments.
- **Trade Type:** Iron Condors and ATM straddles.
- **Time Horizon:** 30-day options.
- **Position Sizing:** €150k notional per product.
- **Execution Model:** Includes realistic broker execution delay. The bid/ask slippage (0.1%).

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

#Use of Ai for the above code has been employed. 
#Please also keep in mind the strtegy implemented above is for institutional trading. 

# 📊 Macro Volatility Overlay Strategies

This repository contains research code and notes for developing **macro derivative strategies**, focusing on volatility structures in commodity and index futures.

We use option pricing models such as **Black 76** (for futures options) to build systematic overlays that hedge risk, monetize volatility, or express macro views.

---

## 🚀 Overview

- **Strategies:** Macro volatility overlays (commodities, indices, FX).  
- **Instruments:** Options on futures (e.g., Coffee, S&P 500 futures, EUR/USD).  
- **Execution Context:** Designed for delayed broker fills (40 min – 2 hours).  
- **Focus:** Simple, interpretable models with real-world execution constraints.

---

## 📐 Intuition Behind Black 76

The **Black 76 model** is a variant of Black-Scholes, designed for **options on futures or forwards** rather than spot assets.  

### Why Not Black-Scholes?  
- In macro trading, we often deal with **futures contracts** (e.g., Coffee, FX, equity index futures).  
- Futures already incorporate carry (interest rates, dividends, storage costs), so there is **no need for discounting** as in Black-Scholes.  
- Black 76 directly uses the **forward/futures price \( f \)** instead of spot \( S \).  

---

### The Core Idea  
Option pricing boils down to **two ingredients**:  
1. **Where the forward is relative to the strike** (\( f \) vs \( k \)).  
2. **How much uncertainty there is until expiry** (volatility \( \sigma \), time \( t \)).  

The model encodes this through two terms, \( d_1 \) and \( d_2 \):  

![d1](https://latex.codecogs.com/svg.latex?d_1%20=%20\frac{\ln\left(\tfrac{f}{k}\right)%20+%20\frac{1}{2}\sigma^2t}{\sigma\sqrt{t}})  

![d2](https://latex.codecogs.com/svg.latex?d_2%20=%20d_1%20-%20\sigma\sqrt{t})  

- **\( d_1 \)**: Measures how many standard deviations the forward price is above the strike, adjusted for volatility and time.  
- **\( d_2 \)**: Shifts \( d_1 \) downward by one “volatility step”, capturing the probability of expiring in-the-money.  

---

### Option Pricing Formulas  

- **Call Option** (right to buy futures at strike \( k \)):  

![call](https://latex.codecogs.com/svg.latex?C%20=%20f%20\cdot%20N(d_1)%20-%20k%20\cdot%20N(d_2))  

- **Put Option** (right to sell futures at strike \( k \)):  

![put](https://latex.codecogs.com/svg.latex?P%20=%20k%20\cdot%20N(-d_2)%20-%20f%20\cdot%20N(-d_1))  

Where:  
- \( N(\cdot) \) = standard normal cumulative distribution.  
- \( f \) = forward price of the future.  
- \( k \) = strike price.  
- \( \sigma \) = volatility.  
- \( t \) = time to expiry (years).  

---

### Intuition in Words  
- \( f \cdot N(d_1) \): **Expected value of being long futures**, adjusted for probability of ending up above strike.  
- \( k \cdot N(d_2) \): **Strike “cost”**, weighted by probability of exercise.  
- The difference is the **fair value** of the option.  

For puts, the roles flip: you’re insuring against downside, so the payoff comes from the probability of finishing **below strike**.  

---

### Why We Use It in the Fund  
- **Macro overlay portfolios** trade heavily in futures (commodities, indices, FX).  
- Black 76 ensures we price these options consistently with how futures already embed carry.  
- It’s the **industry standard** in commodities and rates — so our numbers are directly comparable to brokers, exchanges, and other funds.  

---

## 🧮 Example: Black 76 Option Pricer

```python
from math import log, sqrt
from scipy.stats import norm

def black76_price(f, k, t, sigma, is_call=True):
    """ Price a European option on futures using Black 76 """
    if t <= 0 or sigma <= 0:
        return max(0.0, (f - k) if is_call else (k - f))
    
    d1 = (log(f / k) + 0.5 * sigma**2 * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)
    
    if is_call:
        return f * norm.cdf(d1) - k * norm.cdf(d2)
    else:
        return k * norm.cdf(-d2) - f * norm.cdf(-d1)


```bash
python macro_vol_overlay.py
