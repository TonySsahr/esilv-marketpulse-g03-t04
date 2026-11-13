from pathlib import Path
import csv
import json
from providers.yahoo_provider import fetch_yahoo_prices 



DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
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
    return [row for row in prices if row["ticker"] == ticker]

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


def main():
    prices = load_prices()
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # --- NOUVEAU : Choix du fournisseur ---
    PROVIDER = "yahoo"   # Remplace par "csv" pour revenir à l'ancien comportement

    if PROVIDER == "yahoo":
        # On utilise le nouvel adaptateur pour récupérer les données en direct
        # Les arguments attendus par la fonction sont (ticker, lookback, intervalle)
        instrument_prices = fetch_yahoo_prices(instrument["ticker"], "1mo", "1d")
        benchmark_prices = fetch_yahoo_prices(benchmark["ticker"], "1mo", "1d")
        
        # On recrée une variable "prices" globale pour éviter de faire planter tes "print" plus bas
        prices = instrument_prices + benchmark_prices 
    else:
        # L'ancien système de chargement CSV
        prices = load_prices()
        instrument_prices = filter_prices(prices, instrument["ticker"])
        benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print(f"Provider: {PROVIDER}")
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
    aligned = align_series(instrument_prices,benchmark_prices)
    print(f"Aligned sessions     : {len(aligned[0])}")
    instrument_return=calculate_period_return(instrument_prices)
    benchmark_return=calculate_period_return(benchmark_prices)
    print(f"{instrument['ticker']} period return    : {'+' if instrument_return > 0 else ''}{instrument_return}%")
    print(f"{benchmark['ticker']} period return    : {'+' if benchmark_return > 0 else ''}{benchmark_return}%")
    print(f"Relative Performance    : {calculate_relative_performance(instrument_return,benchmark_return)}")
    print()
    print("Base 100")
    print(f"{instrument["ticker"]}   : 100.00 -> {100+instrument_return}")
    print(f"{benchmark["ticker"]}   : 100.00 -> {100+benchmark_return}")


if __name__ == "__main__":
    main()
