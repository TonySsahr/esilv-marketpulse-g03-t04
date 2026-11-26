# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- **Source:** `data/sample/bloomberg_reference_sample.json`
- **Reference:** `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md`
- **Live connectivity:** not demonstrated (no physical access to the Bloomberg room during the session)

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

> **Note:** In `APPROVED_SAMPLE` mode, the source keys listed below are **teaching wrapper keys** from the fallback fixture (`teaching wrapper key != Bloomberg LIVE field mnemonic`).

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| `date` | `observation_date` | Formatted as `YYYY-MM-DD` string |
| `ticker` | Application mapping (`canonical_ticker`) | Preserves `AAPL` and `SP500` (never Bloomberg identifiers) |
| `open` | `open_value` | Cast to `float` |
| `high` | `high_value` | Cast to `float` |
| `low` | `low_value` | Cast to `float` |
| `close` | `close_value` | Cast to `float` |
| `volume` | `volume_value` | Cast to `int` (`0` acceptable for index) |

## TD10 handoff

- **Access mode:** `APPROVED_SAMPLE`
- **Instrument identifier:** `AAPL US Equity` -> canonical `AAPL`
- **Benchmark identifier:** `SPX Index` -> canonical `SP500`
- **Date representation:** `YYYY-MM-DD` string from `observation_date`
- **Input structure:** JSON series in `data/sample/bloomberg_reference_sample.json` using teaching wrapper keys (`*_value`, `observation_date`)
- **Missing fields:** None in the approved sample fixture; LIVE Bloomberg field mnemonics are not recorded here because live room access was unavailable
- **Special normalization notes:** Map `AAPL US Equity` to `AAPL` and `SPX Index` to `SP500` at the provider boundary so `src/analytics.py` remains untouched.
- **Expected canonical reference:** `data/sample/bloomberg_reference_expected.json`