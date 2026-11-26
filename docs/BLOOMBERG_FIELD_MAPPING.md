# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- **Source:** `data/sample/bloomberg_reference_sample.json`
- **Reference:** `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md`
- **Live connectivity:** not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| `date` | `observation_date` | Formatted as `YYYY-MM-DD` string (`teaching wrapper key != Bloomberg LIVE field mnemonic`) |
| `ticker` | `canonical_ticker` | Preserves `AAPL` and `SP500` |
| `open` | `open_value` | Cast to `float` |
| `high` | `high_value` | Cast to `float` |
| `low` | `low_value` | Cast to `float` |
| `close` | `close_value` | Cast to `float` |
| `volume` | `volume_value` | Cast to `int` (`0` acceptable for index) |

## TD10 handoff

- **Access mode:** `APPROVED_SAMPLE`
- **Instrument identifier:** `AAPL US Equity` -> `AAPL`
- **Benchmark identifier:** `SPX Index` -> `SP500`
- **Date representation:** `YYYY-MM-DD` string from `observation_date`
- **Input structure:** JSON series in `data/sample/bloomberg_reference_sample.json` using teaching wrapper keys (`*_value`, `observation_date`)
- **Missing fields:** None in sample fixture; LIVE field mnemonics not observed
- **Special normalization notes:** Map `AAPL US Equity` to `AAPL` and `SPX Index` to `SP500` at the provider boundary so `src/analytics.py` remains unchanged
- **Expected canonical reference:** `data/sample/bloomberg_reference_expected.json`