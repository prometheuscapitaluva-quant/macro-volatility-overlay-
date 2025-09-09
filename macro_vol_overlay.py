
---


```python
import pandas as pd
import numpy as np
from math import log, sqrt
from scipy.stats import norm
import random
import yfinance as yf

# ---------------- CONFIG ----------------
TARGET_NOTIONAL_EUR = 150_000
EUR_USD = 1.07
TARGET_NOTIONAL_USD = TARGET_NOTIONAL_EUR * EUR_USD

CONTRACT_SPECS = {
    "KC": {"contract_size": 37500},
    "SPX": {"contract_size": 100},
    "EURUSD": {"contract_size": 125000}
}

LOOKBACK_RV = 30
IV_RV_LONG = 0.85
IV_RV_SHORT = 1.20
DELAY_MIN = 40  # minutes
DELAY_MAX = 120  # minutes
BID_ASK_SLIPPAGE = 0.001  # 0.1%

# ---------------- BLACK 76 PRICER ----------------
def black76_price(f, k, t, sigma, is_call=True):
    if t <= 0 or sigma <= 0:
        return max(0.0, (f - k) if is_call else (k - f))
    d1 = (log(f / k) + 0.5 * sigma**2 * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)
    if is_call:
        return f * norm.cdf(d1) - k * norm.cdf(d2)
    else:
        return k * norm.cdf(-d2) - f * norm.cdf(-d1)

# ---------------- HELPERS ----------------
def annualized_vol_from_series(series, days=LOOKBACK_RV, trading_days=252):
    returns = np.log(series / series.shift(1)).dropna().iloc[-days:]
    return float(returns.std(ddof=0) * sqrt(trading_days)) if len(returns) > 1 else np.nan

def size_in_contracts(product, spot):
    specs = CONTRACT_SPECS[product]
    notional_per_contract = spot * specs['contract_size']
    return max(1, int(round(TARGET_NOTIONAL_USD / notional_per_contract)))

# ---------------- TRADE SIMULATION ----------------
def simulate_asset(df_spot, product, delay=False):
    df_spot = df_spot.sort_values('date').reset_index(drop=True)
    trades = []

    for idx in range(LOOKBACK_RV, len(df_spot)-30):
        today = df_spot.loc[idx, 'date']
        spot = df_spot.loc[idx, 'close']
        rv = annualized_vol_from_series(df_spot['close'].iloc[:idx+1])
        if np.isnan(rv):
            continue

        # IV signal for trade
        iv = rv * np.random.uniform(0.8, 1.2)
        signal = None
        if iv < rv * IV_RV_LONG:
            signal = 'BUY_CONVEXITY'
            call = black76_price(spot, spot, 30/252, iv, True)
            put  = black76_price(spot, spot, 30/252, iv, False)
            premium = call + put
        elif iv > rv * IV_RV_SHORT:
            signal = 'SELL_PREMIUM'
            width = 0.05 * spot
            sc = black76_price(spot, spot+width, 30/252, iv, True)
            sp = black76_price(spot, spot-width, 30/252, iv, False)
            premium = sc + sp

        if signal:
            contracts = size_in_contracts(product, spot)
            # apply delay and slippage if requested
            if delay:
                # simulate execution delay: pick a future bar within 40-120 min
                idx_fill = min(idx + random.randint(1, 8), len(df_spot)-1)  # approx 40-120 min
                spot_fill = df_spot.loc[idx_fill, 'close']
                premium *= (1 - BID_ASK_SLIPPAGE)  # reduce due to slippage
            else:
                spot_fill = spot

            trades.append({
                'date': today,
                'product': product,
                'signal': signal,
                'spot_entry': spot,
                'spot_fill': spot_fill,
                'iv': iv,
                'rv': rv,
                'premium': premium,
                'contracts': contracts
            })
    return pd.DataFrame(trades)

# ---------------- RUN BACKTEST ----------------
def run_backtest(kc_csv, spx_csv, fx_csv, delay=False):
    kc = pd.read_csv(kc_csv, parse_dates=['date'])[['date','close']]
    spx = pd.read_csv(spx_csv, parse_dates=['date'])[['date','close']]
    fx  = pd.read_csv(fx_csv, parse_dates=['date'])[['date','close']]

    kc_trades = simulate_asset(kc, 'KC', delay=delay)
    spx_trades = simulate_asset(spx, 'SPX', delay=delay)
    fx_trades  = simulate_asset(fx, 'EURUSD', delay=delay)

    all_trades = pd.concat([kc_trades, spx_trades, fx_trades], ignore_index=True)
    all_trades.to_csv("results/trades.csv", index=False)
    print(f"Saved {len(all_trades)} trades to results/trades.csv")
    print(all_trades.head())
    return all_trades

# ---------------- MAIN ----------------
if __name__ == "__main__":
    trades = run_backtest('data/kc.csv', 'data/spx.csv', 'data/eurusd.csv', delay=True)  # realistic delayed fills
