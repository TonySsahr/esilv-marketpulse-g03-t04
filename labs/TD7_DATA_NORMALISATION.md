# TD07 - Data Normalization + Comparison

## Duration

```text
1 hour 30 minutes
```

## Business requirement

```text
"An instrument is only meaningful when compared to a benchmark on the same basis."
```

## Context

Wave 2 established the collaborative Git workflow.

TD07 opens Wave 3 and builds the first real analytical layer of MarketPulse.

Until now, MarketPulse could load local instrument and benchmark data and print
the latest price. Open `src/main.py` and confirm this: it loads instruments,
loads prices, filters by ticker, and prints the last observation of each.

It cannot yet answer the only question that matters to an analyst:

```text
Did this instrument outperform or underperform its benchmark,
over the same period, on a comparable scale?
```

TD07 introduces the reusable comparison layer:

```text
canonical local data
        |
        v
alignment
        |
        v
period return
        |
        v
base 100
        |
        v
relative performance
```

This TD is a MarketPulse feature, not only a Git exercise.

You will:

```text
1. build a new Python file  : src/analytics.py  (all analytics functions)
2. import and call it from   : src/main.py       (visual comparison output)
```

There is no notebook and no starter code for the functions. You implement every
function yourself, then wire them into `main.py` so your application prints a
real instrument-vs-benchmark comparison.

## MarketPulse feature

```text
Feature       : Feature 1 - Analytics
Branch        : feature/analytics
New module     : src/analytics.py
Integrated in  : src/main.py
```

## Team organization (teams of 3 to 4)

The five functions are NOT equal in size, and some depend on others. To keep
everyone busy inside 90 minutes, you do not split "one function per person"
blindly. Instead you follow three rules:

```text
1. Stubs first  : all five functions exist (empty) before anyone implements one
2. Own a unit   : each student owns an independent unit of roughly equal effort
3. One integrator: a single student wires main.py (never edited by four people)
```

Relative difficulty of each unit (plan your split around this):

```text
index_by_date                   : easy  (but align_series depends on it)
align_series                    : hard
calculate_period_return         : medium
calculate_base_100              : medium
calculate_relative_performance  : trivial (one line)
```

### Team of 4

```text
Student 1 (Lead / Integrator) : creates the stub file, owns align_series,
                                wires src/main.py, opens the PR
Student 2                     : owns index_by_date + calculate_relative_performance,
                                is the official code reviewer
Student 3                     : owns calculate_period_return
Student 4                     : owns calculate_base_100, runs the expected-values check
```

### Team of 3

```text
Student 1 (Lead / Integrator) : creates the stub file, owns align_series,
                                wires src/main.py, opens the PR
Student 2                     : owns index_by_date + calculate_period_return,
                                is the official code reviewer
Student 3                     : owns calculate_base_100 + calculate_relative_performance,
                                runs the expected-values check
```

The reviewer never reviews their own function: in both layouts the reviewer
(Student 2) checks the work of others in `Files changed`.

Every student must be able to explain all five functions and the `main.py`
integration, not only the function they wrote.

## Learning objectives

At the end of TD07, you should be able to:

- create a new Python module from scratch and import it into another file;
- explain why two market series must be aligned before comparison;
- align an instrument and a benchmark on their common trading dates;
- compute a period return from a price series;
- normalize any price series to a base-100 index;
- compute relative performance in percentage points;
- keep an analytics module pure (no printing, no file reading);
- call pure functions from `main.py` to produce a readable comparison.

## CORE definition of done

TD07 is complete when the team can confirm:

```text
[ ] src/analytics.py exists and contains the five functions
[ ] each student implemented at least one function (traceable in git log)
[ ] src/analytics.py has no print statements and no data-loading code
[ ] src/main.py imports from src/analytics
[ ] python src/main.py prints returns, relative performance and base-100 summary
[ ] the printed numbers match the expected values below
[ ] a feature/analytics Pull Request was opened
[ ] the PR was reviewed by another student and merged into team main
[ ] local main is synchronized after merge
[ ] each student can explain the three formulas and the main.py integration
```

Per-student contribution is checked from history, so each person commits their
own function under their own identity:

```bash
git log --oneline --author="<your name or email>"
```

## Prerequisites

Before starting:

```text
[ ] TD06 completed and local main synchronized
[ ] python src/main.py works and prints the current MarketPulse summary
[ ] data/sample/prices.csv and data/sample/instruments.json are present
[ ] the team can create a feature branch and open a Pull Request
```

If local `main` is behind, fix that first:

```bash
git switch main
git pull
```

## Session plan

The CORE is designed for approximately 80 minutes. The plan is built so that all
students work at the same time instead of waiting for one person.

| Time | Who | Activity |
|---|---|---|
| 00-10 min | All together | Read the contract; agree on who owns which function |
| 10-15 min | Lead | Create src/analytics.py with FIVE empty stubs, commit, push |
| 15-20 min | All | Pull the stub file so everyone has the same starting point |
| 20-45 min | All in parallel | Each student implements ONLY their own function(s) |
| 45-55 min | Integrator | Wire analytics into src/main.py, run, check expected values |
| 55-65 min | Reviewer | Review the PR; author fixes only if a real issue is found |
| 65-75 min | All | Merge into team main, synchronize local main |
| 75-80 min | All | CORE validation |
| 80-90 min | All | Buffer / OPTIONAL |

The two things that protect the 90-minute budget:

```text
stubs exist first  -> nobody is blocked waiting for another function
one integrator     -> main.py is never edited by four people at once
```

# CORE

# Part 1 - Understand the analytical contract

MarketPulse defines three quantitative formulas.

You must implement them exactly as specified.

## Period return

Total arithmetic return over the observed period, expressed as a percentage:

```text
period_return = ((last_close / first_close) - 1.0) * 100.0
```

## Base-100 index

Normalize a price series so that the first observation equals 100.0.

Every later point is expressed relative to that starting value:

```text
base_100_value = (current_close / first_close) * 100.0
```

Base-100 is what lets you compare an instrument and a benchmark on the same
scale even when their raw prices differ by orders of magnitude (AAPL near 250,
S&P 500 near 6600).

## Relative performance

Outperformance or underperformance, expressed in percentage points:

```text
relative_performance = instrument_return - benchmark_return
```

A positive value means the instrument outperformed its benchmark.

# Part 2 - Understand the data and the current main.py

The sample data lives in:

```text
data/sample/prices.csv       (daily OHLCV rows for two tickers)
data/sample/instruments.json (instrument and benchmark metadata)
```

The contract for the CORE pair:

```text
Instrument : AAPL
Benchmark  : SP500
Lookback   : 1 month (2026-09-01 to 2026-09-30)
Interval   : Daily
```

Each price row is a canonical observation with these fields:

```text
date   (YYYY-MM-DD)
ticker
open
high
low
close
volume
```

Analytics only needs `date`, `ticker` and `close`.

`src/main.py` already gives you the data you need. It calls:

```text
load_instruments()                -> instrument and benchmark metadata
load_prices()                     -> all price rows
filter_prices(prices, ticker)     -> rows for a single ticker
```

In Part 4 you will reuse those existing lists (`instrument_prices` and
`benchmark_prices`) and pass them into your new analytics functions.

# Part 3 - Build src/analytics.py

## Step 3.0 - Stub file first (the Lead, ~5 minutes)

Before anyone implements logic, the Lead creates the branch and a stub file so
that all five functions already exist by name. This is what lets the whole team
work in parallel without blocking each other or fighting over the file.

```bash
git switch main
git pull origin main
git switch -c feature/analytics
```

Create `src/analytics.py` with five empty stubs (keep the signatures exactly as
specified below):

```python
"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    raise NotImplementedError  # Owner: see team table


def align_series(instrument_prices, benchmark_prices):
    raise NotImplementedError  # Owner: Lead


def calculate_period_return(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_base_100(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError  # Owner: see team table
```

Commit and push the stubs immediately:

```bash
git add src/analytics.py
git commit -m "chore(analytics): add function stubs for TD07"
git push -u origin feature/analytics
```

Every other student then gets the same starting point:

```bash
git fetch origin
git switch feature/analytics
```

## Step 3.1 - Implement your own function (all students, in parallel)

Everyone now works on the SAME branch but a DIFFERENT function. Because each
person edits a different block of the file, conflicts stay small and local.

Workflow for each student:

```bash
# before you start editing, get the latest version of the branch
git pull

# edit ONLY your function(s) in src/analytics.py

# commit your function
git add src/analytics.py
git commit -m "feat(analytics): implement <your_function_name>"

# share it and pick up teammates' functions
git pull            # integrate others (resolve small conflicts if any)
git push
```

Rule: touch only the function you own. If you edit someone else's function you
create conflicts and break the time budget.

Implement your function as a **pure function**: it takes data in, returns data
out, and does no printing, no file reading, and no global state.

Golden rule for this module:

```text
No print statements.
No CSV / JSON loading.
No sample data.
Pure, reusable functions only.
```

## Function 1 - index_by_date

```text
Name    : index_by_date
Input   : prices (list of observation dicts)
Output  : dict mapping {date: observation_dict}
Purpose : allow fast lookup of an observation by its date
```

## Function 2 - align_series

```text
Name    : align_series
Input   : instrument_prices (list), benchmark_prices (list)
Output  : tuple (aligned_instrument, aligned_benchmark)
Purpose : keep only the dates present in BOTH series, in chronological order
```

Requirements:

- the two returned lists must have the same length;
- both must be sorted by date ascending;
- a date missing from either series must appear in neither output.

Hint: build the sorted intersection of the two sets of dates, then select the
matching observation from each series. Reuse `index_by_date`.

Why this matters: a holiday, a halt, or a missing row in one series would
otherwise shift every later comparison by one day and silently corrupt the
returns.

## Function 3 - calculate_period_return

```text
Name    : calculate_period_return
Input   : prices (chronologically sorted list)
Output  : float (percentage, e.g. 6.48 means +6.48%)
Formula : ((last_close / first_close) - 1.0) * 100.0
```

Edge cases you must handle:

- an empty series must raise an error (there is no return to compute);
- a first close equal to zero must raise an error (division is undefined).

The `close` values read from CSV are strings. Convert them to `float` before
arithmetic.

## Function 4 - calculate_base_100

```text
Name    : calculate_base_100
Input   : prices (list of canonical observations)
Output  : list of dicts [{"date": ..., "ticker": ..., "value": float}, ...]
Formula : (current_close / first_close) * 100.0
```

Requirements:

- the first point's `value` must equal 100.0;
- preserve `date` and `ticker` on every output row;
- apply the same empty-series and zero-first-close guards as the return function.

## Function 5 - calculate_relative_performance

```text
Name    : calculate_relative_performance
Input   : instrument_return (float), benchmark_return (float)
Output  : float (percentage points)
Formula : instrument_return - benchmark_return
```

### Verify the module imports

Before touching `main.py`, from the repository root:

```bash
python3 -c "import src.analytics as a; print('analytics.py imported OK')"
```

If this fails, read the error. The most common cause is a stray print or a data
import that does not belong in a pure module.

# Part 4 - Call analytics from src/main.py (the Integrator)

Once all five functions are implemented and pushed, the Integrator pulls the
complete branch and wires the module into the application. Only one person edits
`main.py` to avoid a four-way conflict.

```bash
git pull
```

Import your functions at the top of `src/main.py`:

```python
from src.analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
```

Then, inside `main()`, after the existing code builds `instrument_prices` and
`benchmark_prices`, add a comparison section that:

```text
1. aligns the instrument and benchmark series
2. computes the period return of each
3. computes the relative performance
4. computes the base-100 series of each
5. prints a readable comparison block
```

You design the exact wording. The goal is a visual, readable result when you run
the application, for example:

```text
=== MarketPulse ===

... existing instrument / benchmark summary ...

Comparison (aligned)
Aligned sessions        : 21
AAPL period return      : +6.48%
SP500 period return     : +2.15%
Relative performance    : +4.33 percentage points

Base 100
AAPL   : 100.00 -> 106.48
SP500  : 100.00 -> 102.15
```

Keep all printing in `main.py`. The analytics module stays silent and reusable.

Run it:

```bash
python src/main.py
```

## Expected results (sample data)

Using the frozen sample data, your comparison must produce values close to:

```text
Aligned sessions        : 21
AAPL period return      : +6.48%
SP500 period return     : +2.15%
Relative performance    : +4.33 percentage points
AAPL  base 100 end      : 106.48
SP500 base 100 end      : 102.15
```

If your numbers do not match, re-check your formulas and your `float`
conversion. A wrong sign on relative performance usually means you subtracted in
the wrong order.

Interpretation: over September 2026, AAPL returned +6.48% while its benchmark
returned +2.15%, so AAPL outperformed by about 4.33 percentage points.

# Part 5 - Open the Pull Request

The `feature/analytics` branch already exists (created in Step 3.0) and holds
everyone's functions. The Integrator just commits the `main.py` integration and
pushes.

```bash
git add src/main.py
git commit -m "feat(analytics): wire comparison output into main"
git push
```

### Open the PR on GitHub

```text
Base branch    : main
Compare branch : feature/analytics
Title          : feat: add core quantitative analytics module
Assignee       : Student 1
Reviewer       : Student 2
```

# Part 6 - Review and merge

### Review (Student 2)

Open `Files changed` and verify:

```text
[ ] src/analytics.py contains exactly the five expected functions
[ ] src/analytics.py has no print statements and no data loading
[ ] the three formulas match the analytical contract
[ ] edge cases (empty series, zero first close) are handled
[ ] src/main.py imports from src/analytics and prints the comparison
[ ] python src/main.py runs and the numbers match the expected values
```

Leave meaningful feedback describing what you actually checked, then approve.

If a real issue exists, request a change; Student 1 fixes it on the same branch
and pushes again. Do not invent a defect just to create a correction cycle
(see TD06).

### Merge and synchronize

After approval, merge into team `main`. Every student then runs:

```bash
git switch main
git pull
git log --oneline -5
python src/main.py
```

Everyone should see the same comparison output locally.

# Part 7 - CORE validation

Each student should be able to show or explain:

```text
the five functions in src/analytics.py
the three formulas
why alignment must happen before comparison
why src/analytics.py stays pure while main.py does the printing
the comparison output of python src/main.py
the reviewed and merged Pull Request
synchronized local main
```

# Checkpoint relation

Checkpoint B is performed after TD08. The single source of truth for evidence,
filenames and rules is:

```text
docs/04_CHECKPOINTS_AND_EVIDENCE.md
```

This lab does not redefine that contract. It only tells you which evidence you
can already capture during TD07.

## Evidence to capture now

TD07 produces the first two of the four required Checkpoint B screenshots. Store
them under your own GitHub username in `evidence/checkpoint-b/<github-user>/`.

```text
01_pull_request.png   -> your feature/analytics Pull Request
                         (title, author, source and target branch visible)
02_code_review.png    -> the review YOU performed on a teammate's PR
                         (a real comment, not just a reaction)
```

A copy-ready folder and README template are provided at
`evidence/checkpoint-b/TEMPLATE/`. Copy it, rename it to your GitHub username,
and fill in the README.

Capture tip: when you take `01_pull_request.png`, also keep a terminal
screenshot of `python src/main.py` showing the comparison block. It is not a
separately named required file, but it is the fastest way to prove your team's
application actually runs, and the instructor may ask for it during validation.

Because this is group work, each student must be the author of at least one
`feat(analytics): ...` commit. Verify your own contribution:

```bash
git log --oneline --author="<your name or email>"
```

Do not submit Checkpoint B yet. It closes after TD08.

# OPTIONAL

Complete optional work only after the CORE definition of done is satisfied.

## Optional 1 - Full base-100 table

In `main.py`, print the complete AAPL and SP500 base-100 series date by date,
not only the first and last values. Identify the date where the gap between the
two is widest.

## Optional 2 - Alignment with a missing date

Remove one AAPL row for a date in a copy of the sample data, re-run the app, and
confirm that the aligned session count drops and both series stay equal length.

## Optional 3 - Guard against non-chronological input

`calculate_period_return` assumes the list is already sorted. Explain what it
would return for reversed input, and how `align_series` protects the normal
flow.

## Optional 4 - Reuse readiness

Explain in one or two sentences why `calculate_base_100` returns a list of dicts
rather than printing a table, and relate it to how TD11 (the Dash dashboard)
will consume it.

# ADVANCED

No `READY_TO_TEACH` advanced activity is attached to TD07 at this time.

Complete the CORE and OPTIONAL work only.

# TROUBLESHOOTING

## import src.analytics fails

Run from the repository root, not from inside `src/`. If it still fails, the
module probably contains a print or a data import that does not belong in a pure
module.

## ModuleNotFoundError: No module named 'src'

Run the app from the repository root as `python src/main.py`. The import
`from src.analytics import ...` resolves relative to the project root.

## Returns look wrong

Check that you converted `close` from string to `float`. CSV values are strings.

## Relative performance has the wrong sign

The formula is `instrument_return - benchmark_return`, in that order.

## Aligned series have different lengths

Your intersection logic is off. Build one set of common dates and select from
both series using that same set, then sort.

## Merge conflict in src/analytics.py

Two students edited near each other. This is expected occasionally and is quick
to fix because each conflict is inside one function:

```bash
git pull
# open src/analytics.py, keep BOTH functions (yours and theirs),
# delete the <<<<<<< ======= >>>>>>> markers
git add src/analytics.py
git commit
git push
```

If conflicts keep happening, you are editing a function you do not own. Stop and
edit only your own function.

## A function still raises NotImplementedError

Its owner has not pushed yet, or you did not `git pull`. Pull the branch and
check that all five stubs have been filled in before running `main.py`.

## Division by zero

A `first_close` of 0.0 must raise an error, not produce `inf`. Add the guard.

# What comes next?

Wave 3 continues with remote data:

```text
Wave 3 - Comparison + Remote Data - 3 hours

TD07 - Data Normalization + Comparison
TD08 - Yahoo Finance
```

TD08 replaces the local CSV with real daily market data from Yahoo Finance, and
feeds it into the exact same analytics layer you built here. Keeping
`src/analytics.py` pure is what makes that swap painless.
