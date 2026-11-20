import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}

def fetch_yahoo_prices(canonical_ticker, lookback="1mo", interval="1d"):
    yahoo_symbol = CANONICAL_TO_YAHOO[canonical_ticker]

    raw = yf.download(
        yahoo_symbol,
        period=lookback,
        interval=interval,
        multi_level_index=False,
    )
    rows = []
    for timestamp, row in raw.iterrows():
        rows.append({
            "date": timestamp.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    rows.sort(key=lambda r: r["date"])
    return rows
