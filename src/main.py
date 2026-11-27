from pathlib import Path
import csv
import json
from providers.yahoo_provider import fetch_yahoo_prices
from providers.bloomberg_provider import get_bloomberg_rows



DATA_DIR = Path("data/sample")

PROVIDER = "bloomberg"
LOOKBACK = "1mo"
INTERVAL = "1d"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)

def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def load_provider_label():
    with open(DATA_DIR / "bloomberg_reference_sample.json", encoding="utf-8") as file:
        return json.load(file)["provider_stage"]

def filter_prices(prices, ticker):
    return [row for row in prices if row['ticker'] == ticker]

def get_first_close(prices):
    return prices[0]["close"]

def get_last_close(prices):
    return prices[-1]["close"]

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]

def get_market(asset):
    return asset["market"]

def display_market_summary(asset, prices, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"{asset['ticker']}: {len(prices)}")
    print(f"Market : {get_market(asset)}")
    print(f"First date: {get_first_date(prices)}", (asset['currency'] if show_currency else ''))
    print(f"Last date: {get_last_date(prices)}", (asset['currency'] if show_currency else ''))
    print(f"First close: {get_first_close(prices)}", (asset['currency'] if show_currency else ''))
    print(f"Last close: {get_last_close(prices)}", (asset['currency'] if show_currency else ''))


def build_market_snapshot(provider, lookback, interval):
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    if provider == "bloomberg":
        provider_label = "Bloomberg stage"
        access_mode = "APPROVED_SAMPLE"
        instrument_prices = get_bloomberg_rows(instrument['ticker'], "2026-09-01", "2026-09-30")
        benchmark_prices = get_bloomberg_rows(benchmark['ticker'], "2026-09-01", "2026-09-30")
    elif provider == "yahoo":
        provider_label = "yahoo"
        access_mode = "N/A"
        instrument_prices = fetch_yahoo_prices(instrument['ticker'], lookback, interval)
        benchmark_prices = fetch_yahoo_prices(benchmark['ticker'], lookback, interval)
    else:
        provider_label = "csv"
        access_mode = "N/A"
        prices = load_prices()
        instrument_prices = filter_prices(prices, instrument['ticker'])
        benchmark_prices = filter_prices(prices, benchmark['ticker'])

    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)
    aligned_instrument = list(aligned_instrument.values())
    aligned_benchmark = list(aligned_benchmark.values())

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": provider_label,
        "access_mode": access_mode,
        "lookback": lookback,
        "interval": interval,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "aligned_sessions": len(aligned_instrument),
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(instrument_return, benchmark_return),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    snapshot = build_market_snapshot(PROVIDER, LOOKBACK, INTERVAL)

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_prices = snapshot["instrument_prices"]
    benchmark_prices = snapshot["benchmark_prices"]
    prices = instrument_prices + benchmark_prices
    instrument_return = snapshot["instrument_return"]
    benchmark_return = snapshot["benchmark_return"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print(f"Provider: {snapshot['provider']}")
    print(f"Access mode: {snapshot['access_mode']}")
    print()
    print("Instrument")
    display_market_summary(instrument, instrument_prices)
    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)
    print()
    print()
    print(f"Start Date: {get_first_date(prices)}")
    print(f"End Date:   {get_last_date(prices)}")
    print()
    print("Comparison (aligned)")
    print(f"Aligned sessions     : {snapshot['aligned_sessions']}")
    print(f"{instrument['ticker']} period return    : {'+' if instrument_return > 0 else ''}{instrument_return}%")
    print(f"{benchmark['ticker']} period return    : {'+' if benchmark_return > 0 else ''}{benchmark_return}%")
    print(f"Relative Performance    : {snapshot['relative_performance']}")
    print()
    print("Base 100")
    print(f"{instrument['ticker']}   : {snapshot['instrument_base_100'][0]['value']:.2f} -> {snapshot['instrument_base_100'][-1]['value']:.2f}")
    print(f"{benchmark['ticker']}   : {snapshot['benchmark_base_100'][0]['value']:.2f} -> {snapshot['benchmark_base_100'][-1]['value']:.2f}")

if __name__ == "__main__":
    main()
