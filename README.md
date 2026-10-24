# The Elephant Index Verifier

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
     0.00003 (drawdown)**;
   - *parameter fishing* → Deflated Sharpe (Bailey–López de Prado) clears the haircut on Bitcoin
     (≈0.99) and credit (≈0.90);
   - *one lucky crisis* → leave-one-crisis-out: drop 1973-74 / 2008 / 2020 / 2022 — result
     essentially unchanged;
   - *no mechanism* → the drawdown reduction is largest exactly where liquidity-driven crashes are deepest.
4. **Honest weak spot** — on calm large-caps the *risk-adjusted* edge is not significant. The proven
   edge is **drawdown** and **liquidity-sensitive assets**. A seatbelt, not an alpha machine.

## What stays locked (and why that's fine)

You verify the signal isn't luck or curve-fitting **without** seeing *which* series, the curve/exit
parameters, the stress-gate definition, the thresholds, or the consensus logic. A crude public rebuild of the
logic caps far below the real signal — so the recipe stays a recipe, and you still didn't have to
trust it.

## Data & provenance (`data/`)

Everything here is an **output or public market data** — never an input to the recipe.

| file | contents | source |
|---|---|---|
| `regime_NQ1.csv`, `regime_BTC.csv` | the research regime's ON/OFF dates (the rule this audit was built and reviewed on) + **price return** | Nasdaq-100 & Bitcoin closes (FRED) |
| `regime_SPX_proxy.csv` | regime dates + **price return**, back to 1962 | S&P 500 price series (public, re-derivable) |
| `regime_HYG.csv` | regime dates + **total return** | HYG ETF dividend-adjusted close (Yahoo) |
| `net_liquidity.csv` | net liquidity = WALCL − RRP − TGA, monthly | FRED |

Don't want to trust the shipped CSVs? Re-pull the inputs yourself — net liquidity and the index/BTC
prices from **FRED**, the ETF total return from **Yahoo** — and re-run. That is the whole point.

## The live feed & the 5-month embargo (`live/`)

| file | contents |
|---|---|
| `live/signal_current.json` | the latest **published** state, as of the cutoff month: per asset `position`, `since`, and `regime` (`"ON"` = any exposure; kept for older readers) |
| `live/signal_history.csv` | monthly **position** history through the published cutoff (`nq_position`, `btc_position`, with prices) |
| `live/nq_history.csv`, `live/btc_history.csv` | the same history, one file per asset: `date,price,position` |
| `live/inputs_monthly.csv` | the sampled monthly inputs behind every published position (Rulebook §2), in FRED units, through the month before the embargo cutoff. Rebuild the Index from this file alone and you reproduce every published position. |
| `live/decision_hashes.csv` | **commit-reveal ledger** — every month-end decision's salted SHA-256, published immediately; nonce + plaintext revealed once the month clears the embargo |

**What a position means.** The share of the asset the Index holds **during** that month, decided at
the previous month-end close. Nasdaq-100: **0, 50 or 100** (the two votes; one vote = 50). Bitcoin:
**0 or 100** (consensus — on a split vote it keeps its previous position). The history starts when all
inputs exist: Nasdaq February 2003, Bitcoin January 2015. It is computed by the same engine and FRED
data as the live Index (Nasdaq-100 cash index); the fund research series use Nasdaq futures prices and
differ from it in the 2003 warm-up and in two months (Dec 2012, Jan 2013), where the index closed 0.01%
below its 10-month average and the futures just above.

**Correction (2026-10-23).** Until this date the `live/` history published the predecessor rule, and
before 2014 a data bug froze it: months with no reverse-repo operations were dropped from net
liquidity instead of counted as $0 (see the reproducibility note below), so the rule held its previous
state — for example ON through the 2008 crash. The bug is fixed and the `live/` files now carry the
live Index's own positions. The live signal and every sealed hash were unaffected (all inputs exist
from 2014 on).

**The regime plaintext is published with a 5-month delay.** Subscribers receive each decision at
month-end; the public record trails it. Two things keep this honest:

1. **Every call is timestamped when made.** The decision hash publishes the day of the decision —
   `SHA-256("<ASSET>:<REGIME>:<since>|...|as_of:<YYYY-MM>|nonce:<hex>")` — and the nonce + plaintext
   are revealed when the month ages out. You can verify every reveal against its pre-published hash.
2. **Free-riding the delayed feed is worthless — verify that yourself:** `python freerider.py`
   computes, on this repo's own data, what copying the published regime N months late gets you.
   Answer: on the Nasdaq-100, the 5-month-late copier takes buy-and-hold's full drawdown with *less*
   return than buy-and-hold; on Bitcoin the copy is dead by ~3 months (buy-and-hold results with
   extra steps, forgoing 20pp+/yr vs acting on time). The delayed feed is a **track record**, not a
   trading signal — by construction, not by promise.

## Reproducibility note (for anyone rebuilding net liquidity)

`RRPONTSYD` has prints in only a minority of months before 2013 — ON-RRP operations were sporadic
then, so **no print means $0 outstanding, not missing data**. If you rebuild net liquidity by
intersecting the three component series, those months become blank and the pre-2013 history breaks.
Reindex RRP and TGA onto WALCL's months: fill a missing RRP month with 0, and carry TGA's last value
over its rare missing month. This reproduces `data/net_liquidity.csv` exactly.

## Notes

- Figures are **hypothetical / backtested** and not indicative of future results; not investment advice.
- `live/` is refreshed monthly through the 5-month cutoff. The audit inputs in `data/` are a fixed
  snapshot through 2026-02, on the research regime (see the table above) — a different rule from the
  live positions in `live/`, so the two are not expected to match month for month.
