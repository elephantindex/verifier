# The Elephant Verifier

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elephantindex/verifier/blob/main/audit.ipynb)

> **Don't trust. Verify.** This is the canonical, reproducible audit behind the Elephant
> Index "How It Works" page. It proves the signal is real and not data-mined — using only
> public data and the signal's published ON/OFF dates — **without revealing the recipe.**

## Run it

**In your browser (no setup):** click the *Open in Colab* badge above and run all cells.

**Locally:**

```bash
pip install -r requirements.txt   # numpy, pandas, scipy
python audit.py
```

## What it checks

1. **The tide is real but lagged** — net liquidity leads markets ~6 months; Bitcoin responds first.
2. **The naive public version underperforms** — a crude "liquidity-up AND price-up" rule trails
   buy-and-hold. Raw liquidity is a trap; timing it is the engineering.
3. **Five refutations of "you data-mined it"**, all run on the published ON/OFF dates + public returns:
   - *cherry-picking* → holds out-of-sample across the S&P-500 proxy (1962+), high-yield credit,
     and Bitcoin — none of them used to build it;
   - *luck* → matched-random permutation (10,000 shuffles), Fisher-combined **p ≈ 0.0001 (return) /
     0.00004 (drawdown)**;
   - *parameter fishing* → Deflated Sharpe (Bailey–López de Prado) clears the haircut on Bitcoin
     (≈0.99) and credit (≈0.90);
   - *one lucky crisis* → leave-one-crisis-out: drop 1973-74 / 2008 / 2020 / 2022 — result
     essentially unchanged;
   - *no mechanism* → the drawdown reduction is largest exactly where liquidity-driven crashes are deepest.
4. **Honest weak spot** — on calm large-caps the *risk-adjusted* edge is not significant. The proven
   edge is **drawdown** and **liquidity-sensitive assets**. A seatbelt, not an alpha machine.

## What stays locked (and why that's fine)

You verify the signal isn't luck or curve-fitting **without** seeing *which* series, the curve/exit
mechanics, the stress gate, the thresholds, or the consensus logic. A crude public rebuild of the
logic caps far below the real signal — so the recipe stays a recipe, and you still didn't have to
trust it.

## Data & provenance (`data/`)

Everything here is an **output or public market data** — never an input to the recipe.

| file | contents | source |
|---|---|---|
| `regime_NQ1.csv`, `regime_BTC.csv` | published regime ON/OFF dates + **price return** | Nasdaq-100 & Bitcoin closes (FRED) |
| `regime_SPX_proxy.csv` | regime dates + **price return**, back to 1962 | S&P 500 price series (public, re-derivable) |
| `regime_HYG.csv` | regime dates + **total return** | HYG ETF dividend-adjusted close (Yahoo) |
| `net_liquidity.csv` | net liquidity = WALCL − RRP − TGA, monthly | FRED |

Don't want to trust the shipped CSVs? Re-pull the inputs yourself — net liquidity and the index/BTC
prices from **FRED**, the ETF total return from **Yahoo** — and re-run. That is the whole point.

## Reproducibility note (for anyone rebuilding net liquidity)

`RRPONTSYD` has prints in only a minority of months before 2013 — ON-RRP operations were sporadic
then, so **no print means $0 outstanding, not missing data**. If you rebuild net liquidity by
intersecting the three component series, those months become blank and the pre-2013 history breaks.
Reindex RRP and TGA onto WALCL's dates and fill missing values with 0.

## Notes

- Figures are **hypothetical / backtested** and not indicative of future results; not investment advice.
- The full history through the latest complete month is published; the current in-progress month's
  state comes from the live signal feed.
