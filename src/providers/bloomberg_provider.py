import json

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier, start_date, end_date):
    with open("data/sample/bloomberg_reference_sample.json") as file:
        data = json.load(file)

    for series in data["series"]:
        if series["provider_identifier"] == identifier:
            return series


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for observation in raw_data["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def get_bloomberg_rows(canonical_ticker, start_date, end_date):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier, start_date, end_date)
    return normalize_bloomberg_history(raw_data, canonical_ticker)
