# TD08 - Yahoo Finance

## Duration

```text
1 hour 30 minutes
```

## Business requirement

```text
"MarketPulse must work on real market data, not only a frozen local file."
```

## Context

TD07 built the analytics layer and proved it on the local CSV. The numbers were
correct, but the data never changed.

TD08 replaces the local file with a real remote source: **Yahoo Finance**,
accessed through the `yfinance` Python package.

The important design idea of this TD is the **canonical contract**. Your Yahoo
adapter must return the exact same row shape the CSV produced, so the analytics
functions from TD07 keep working without a single change:

```text
Yahoo Finance API
        |
        v
src/providers/yahoo_provider.py   (new - converts raw Yahoo data)
        |
        v
canonical observation rows        (SAME shape as prices.csv)
        |
        v
src/analytics.py                  (TD07 - unchanged)
        |
        v
src/main.py                       (prints the comparison)
```

If you have to edit `src/analytics.py` to make Yahoo work, your adapter is wrong.

## MarketPulse feature

```text
Feature       : Feature 2 - Yahoo provider
Branch        : feature/yahoo-provider
New module     : src/providers/yahoo_provider.py
Integrated in  : src/main.py (provider switch)
Companion      : notebooks/02_yahoo_provider.ipynb (exploration only, optional)
```

## The canonical contract (reminder)

Every provider must return a list of these dictionaries, one per session:

```python
{
    "date": "YYYY-MM-DD",  # str
    "ticker": "AAPL",      # str  (canonical application ticker)
    "open": 249.20,        # float
    "high": 251.50,        # float
    "low": 248.00,         # float
    "close": 250.00,       # float
    "volume": 38000000     # int  (0 is acceptable for an index)
}
```

Canonical tickers stay `AAPL` and `SP500` inside MarketPulse. Yahoo uses its own
symbols, so the adapter must translate:

```text
MarketPulse ticker : Yahoo symbol
AAPL               : AAPL
SP500              : ^GSPC
```

## Team organization (teams of 3 to 4)

TD08 reuses the TD07 collaboration pattern but rotates the roles so a different
student leads.

### Team of 4

```text
Student 3 (Lead Yahoo)  : implements src/providers/yahoo_provider.py, opens PR
Student 4               : official code reviewer
Student 1               : wires the provider switch into src/main.py
Student 2               : validates the canonical rows and the live retrieval
```

### Team of 3

```text
Student 3 (Lead Yahoo)  : implements the provider, wires main.py, opens PR
Student 1               : official code reviewer
Student 2               : validates canonical rows and the live retrieval
```

Rotating the lead is deliberate: Checkpoint B needs an identifiable individual
contribution from each student, and TD07 already gave a PR to the analytics
lead.

## Learning objectives

At the end of TD08, you should be able to:

- add an external dependency to `requirements.txt` and install it;
- call a remote market-data API with `yfinance`;
- translate a provider symbol to a canonical ticker;
- normalize raw provider output into the canonical observation contract;
- reuse the TD07 analytics layer unchanged on remote data;
- switch MarketPulse between the CSV provider and the Yahoo provider;
- reason about what to do when the network or the provider is unavailable.

## CORE definition of done

TD08 is complete when the team can confirm:

```text
[ ] yfinance is listed in requirements.txt and installed
[ ] src/providers/yahoo_provider.py exists with a fetch function
[ ] the adapter returns canonical rows (same shape as prices.csv)
[ ] AAPL and SP500 both come back with the canonical tickers (not ^GSPC)
[ ] src/main.py can run on the Yahoo provider
[ ] the TD07 analytics layer was reused WITHOUT modification
[ ] a successful live retrieval was observed and captured
[ ] a feature/yahoo-provider PR was opened, reviewed and merged
[ ] local main is synchronized after merge
```

## Prerequisites

Before starting:

```text
[ ] TD07 merged: src/analytics.py exists on team main
[ ] python src/main.py prints the TD07 comparison from CSV
[ ] local main synchronized
[ ] internet access available for the live retrieval
[ ] pip works in your environment
```

Sync first:

```bash
git switch main
git pull
```

## Session plan

The CORE is designed for approximately 80 minutes.

| Time | Who | Activity |
|---|---|---|
| 00-10 | All | Read the contract; agree roles; add yfinance to requirements |
| 10-15 | Lead | Create feature branch + provider stub, commit, push |
| 15-20 | All | Pull the branch |
| 20-45 | Lead + reviewer | Implement and test the Yahoo adapter |
| 20-45 | Integrator | Prepare the provider switch in main.py (in parallel) |
| 45-55 | Integrator | Run MarketPulse on Yahoo; capture live retrieval |
| 55-65 | Reviewer | Review the PR |
| 65-75 | All | Merge + sync local main |
| 75-80 | All | CORE validation |
| 80-90 | All | Buffer / OPTIONAL |

# CORE

# Part 1 - Add and install yfinance

Add the dependency to `requirements.txt`:

```text
yfinance
```

Install it:

```bash
python -m pip install -r requirements.txt
```

Confirm the import works:

```bash
python3 -c "import yfinance; print('yfinance', yfinance.__version__)"
```

This is the first external dependency in MarketPulse. Until now the project used
only the Python standard library.

# Part 2 - Understand the yfinance output

`yfinance` returns a pandas DataFrame indexed by date, with columns such as
`Open`, `High`, `Low`, `Close`, `Volume`. That is NOT the canonical shape. Your
adapter's job is to convert each row of that DataFrame into one canonical
dictionary.

Explore it (in the optional notebook or a scratch script):

```python
import yfinance as yf

raw = yf.download("AAPL", period="1mo", interval="1d")
print(raw.head())
print(raw.columns)
```

Observe:

```text
- the index is a timestamp -> you need "YYYY-MM-DD" as a string
- columns are capitalized  -> Close, not close
- values are numpy floats   -> cast to float / int for the canonical row
- the symbol ^GSPC is Yahoo's -> your canonical ticker must stay SP500
```

# Part 3 - Build src/providers/yahoo_provider.py

Create the provider module. Design it as a pure adapter: it fetches and returns
canonical rows, and does not print.

Suggested shape (you implement the body yourself):

```text
Name    : fetch_yahoo_prices
Input   : canonical_ticker (str), lookback (str, e.g. "1mo"), interval (str, e.g. "1d")
Output  : list of canonical observation dicts, sorted by date ascending
Steps   :
    1. translate canonical_ticker -> Yahoo symbol (AAPL->AAPL, SP500->^GSPC)
    2. call yfinance to download the raw series
    3. for each row, build a canonical dict:
         date   : index formatted as "YYYY-MM-DD"
         ticker : the CANONICAL ticker (AAPL or SP500), never ^GSPC
         open/high/low/close : float(...)
         volume : int(...)
    4. return the rows sorted by date
```

Requirements:

- the returned `ticker` must be the canonical one, not the Yahoo symbol;
- `date` must be the string `YYYY-MM-DD`, not a timestamp object;
- `open/high/low/close` must be `float`, `volume` must be `int`;
- the module must not print and must not hard-code a single instrument only.

Keep a small mapping so adding a future instrument is a one-line change:

```python
CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}
```

# Part 4 - Switch main.py to the Yahoo provider

MarketPulse should be able to run on either provider. In `src/main.py`, replace
the direct CSV load for price data with a provider choice, for example a simple
constant or an argument:

```text
PROVIDER = "yahoo"   # or "csv"
```

When the provider is `yahoo`, build the instrument and benchmark series by
calling `fetch_yahoo_prices` for each canonical ticker instead of reading the
CSV. Everything after that - alignment, returns, base-100, relative performance,
printing - is the TD07 code and must stay the same.

Run it:

```bash
python src/main.py
```

You should see the same comparison block as TD07, now computed from live Yahoo
data. The exact numbers will differ from the frozen CSV because they are real
current prices.

## What a correct run shows

```text
- both AAPL and SP500 series returned with canonical tickers
- a non-zero number of aligned sessions over the lookback
- period returns, relative performance and base-100 printed
- analytics.py untouched since TD07
```

Capture this successful live run for Checkpoint B (see Checkpoint relation).

# Part 5 - Open the Pull Request

The Lead opens the PR for `feature/yahoo-provider`.

```bash
git add requirements.txt src/providers/yahoo_provider.py src/main.py
git commit -m "feat(yahoo): add yfinance provider and provider switch"
git push -u origin feature/yahoo-provider
```

On GitHub:

```text
Base branch    : main
Compare branch : feature/yahoo-provider
Title          : feat: add Yahoo Finance market data provider
Assignee       : Lead (Student 3)
Reviewer       : Student 4 (or Student 1 in a team of 3)
```

# Part 6 - Review and merge

### Review

Open `Files changed` and verify:

```text
[ ] yfinance added to requirements.txt
[ ] fetch_yahoo_prices returns canonical rows (date str, floats, int volume)
[ ] canonical ticker is used in output, not ^GSPC
[ ] src/analytics.py is NOT modified in this PR
[ ] main.py reuses the TD07 analytics unchanged
[ ] the provider module does not print
```

The single most important review check: `src/analytics.py` must not appear in
the diff. If it does, the adapter is not respecting the canonical contract.

Leave meaningful feedback, then approve. Request a change only for a real issue.

### Merge and synchronize

```bash
git switch main
git pull
python src/main.py
```

# Part 7 - CORE validation

Each student should be able to show or explain:

```text
yfinance installed from requirements.txt
the fetch function and the canonical rows it returns
the AAPL / ^GSPC -> SP500 ticker translation
MarketPulse running on live Yahoo data
why analytics.py did not change
the reviewed and merged Pull Request
synchronized local main
```

# Checkpoint relation

Checkpoint B is performed and completed after TD08. The single source of truth
for evidence, filenames and rules is:

```text
docs/04_CHECKPOINTS_AND_EVIDENCE.md
```

This lab does not redefine that contract. It only tells you which evidence TD08
adds.

## Evidence to capture now

TD08 produces the last two of the four required Checkpoint B screenshots. Store
them under your own GitHub username in `evidence/checkpoint-b/<github-user>/`,
alongside the two you captured in TD07.

```text
03_yahoo_market_data.png    -> MarketPulse retrieving/displaying LIVE Yahoo data
04_instrument_benchmark.png -> both instrument AND benchmark over the same
                               lookback (1 month) and interval (daily)
```

So the complete Checkpoint B package in your directory is:

```text
evidence/checkpoint-b/<github-user>/
├── README.md
├── 01_pull_request.png      (from TD07)
├── 02_code_review.png       (from TD07)
├── 03_yahoo_market_data.png (from TD08)
└── 04_instrument_benchmark.png (from TD08)
```

`03_yahoo_market_data.png` requires a REAL successful remote retrieval. If Yahoo
is unavailable during the session, that single item is marked `PENDING_EXTERNAL`
and completed in an instructor-approved recovery window. Do not substitute local
CSV output, a provider double, or fabricated values for it.

Each student's `README.md` must list their name, GitHub handle, branch, main
commits, their PR, the PR they reviewed, and the four filenames exactly as above.
A copy-ready folder and README template are provided at
`evidence/checkpoint-b/TEMPLATE/`; `docs/04_CHECKPOINTS_AND_EVIDENCE.md` section 8
is the canonical reference.

This is the point where your Checkpoint B package must be complete: all four
screenshots present (or any blocked item clearly marked `PENDING_EXTERNAL`), and
your README filled in.

# OPTIONAL

Complete optional work only after the CORE definition of done is satisfied.

## Optional 1 - Config-driven provider

Read the provider from `config/settings.yml` (`market.provider`) instead of a
constant in `main.py`. Parsing YAML is optional in the CORE; do this only if time
allows.

## Optional 2 - Graceful offline fallback

If the Yahoo call fails (no network), fall back to the CSV provider and print a
clear notice. Keep the canonical rows identical so analytics still works.

## Optional 3 - A second instrument

Add one more canonical-to-Yahoo mapping (for example `MSFT`) and confirm the
adapter returns canonical rows for it without any change to analytics.

# ADVANCED

No `READY_TO_TEACH` advanced activity is attached to TD08 at this time.

Complete the CORE and OPTIONAL work only.

# TROUBLESHOOTING

## pip install fails

Check your internet connection and that `python -m pip` points at the same
interpreter you run the app with. Re-run `python -m pip install -r requirements.txt`.

## yfinance returns an empty DataFrame

Usually a wrong symbol or a weekend/holiday window. Confirm `^GSPC` for SP500 and
a `period` like `"1mo"`. Print the raw DataFrame to inspect it.

## Ticker shows as ^GSPC in the output

Your adapter returned the Yahoo symbol instead of the canonical one. Set
`ticker` to the canonical input, not the Yahoo symbol.

## analytics.py had to change

It should not. If alignment or returns break on Yahoo data, the row shape is
wrong: check that `date` is a `YYYY-MM-DD` string and prices are `float`.

## Network blocked during the session

Mark `03_yahoo_market_data.png` as `PENDING_EXTERNAL` and complete the other
Checkpoint B evidence. Capture the live retrieval later in an approved recovery
window.

# What comes next?

Checkpoint B is performed after this TD. Prepare your evidence directory per
`docs/04_CHECKPOINTS_AND_EVIDENCE.md`.

Wave 4 then moves to professional market data:

```text
TD09 - Bloomberg Introduction
TD10 - Bloomberg Provider
TD11 - Dash Dashboard
TD12 - Integration + Release
```

Because every provider returns the same canonical rows, TD10 adds Bloomberg as a
third source behind the exact same analytics layer you have been reusing since
TD07.
