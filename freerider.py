"""What does trading this feed N months late actually get you? Run it and see.

The regime plaintext in this repo is published with a 5-month embargo (subscribers get
each decision at month-end; the salted decision hash publishes immediately). A natural
question: "why not just trade the public feed late, for free?" This script computes the
answer on the repo's own data — a free-rider copies each published regime N months after
the decision, vs the real signal and vs plain buy-and-hold.

Spoiler (and the reason the embargo is 5 months):
  - Nasdaq-100: the 5-month-late copier takes buy-and-hold's full drawdown with LESS
    return than buy-and-hold. Free-riding is strictly worse than doing nothing.
  - Bitcoin: dead even sooner — by ~3 months the copier's return equals buy-and-hold at
    nearly buy-and-hold's drawdown, forgoing 20pp+/yr vs acting on time. The first months
    of each recovery, which the late copier always misses, carry the compounding.

Run:  python freerider.py     (needs: numpy, pandas)
"""
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "data")
ANN = np.sqrt(12)


def stats(ret, rf):
    ret, rf = np.asarray(ret, float), np.asarray(rf, float)
    eq = np.cumprod(1 + ret)
    cagr = eq[-1] ** (12 / len(eq)) - 1
    ex = ret - rf
    sh = ex.mean() / ex.std() * ANN if ex.std() > 0 else np.nan
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    return cagr, sh, dd


def main():
    line = "=" * 92
    print(line + "\nFREE-RIDER CHECK — copying the published regime N months late (this repo's data)\n" + line)
    for key in ["NQ1", "BTC"]:
        p = pd.read_csv(f"{DATA}/regime_{key}.csv").dropna(subset=["fwd_ret_tr"])
        fwd, rf = p["fwd_ret_tr"].to_numpy(), p["rf_fwd_1m"].to_numpy()
        on = p["regime_on"].astype(int)
        bh = stats(fwd, rf)
        print(f"\n[{key}] {p['period'].iloc[0]}..{p['period'].iloc[-1]} ({len(p)} mo)   "
              f"buy&hold: CAGR {bh[0]*100:5.1f}%  Sharpe {bh[1]:.2f}  MaxDD {bh[2]*100:4.0f}%")
        print(f"    {'lag':>3s} | {'CAGR':>6s} {'Sharpe':>6s} {'MaxDD':>6s} |")
        for N in range(0, 7):
            lag_on = on.shift(N).fillna(on.iloc[0]).to_numpy()
            r = np.where(lag_on == 1, fwd, rf)
            c, s, d = stats(r, rf)
            tag = "  <- acting on time (subscriber)" if N == 0 else ""
            print(f"    {N:3d} | {c*100:5.1f}% {s:6.2f} {d*100:5.0f}% |{tag}")
    print("\n" + line)
    print("The late copier rides every bear N months longer AND misses the first N months of")
    print("every recovery. Both legs of the seatbelt degrade together. That is the embargo.")
    print(line)


if __name__ == "__main__":
    main()
