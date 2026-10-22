def index_by_date(prices):
    return {observation["date"]: observation for observation in prices}


def align_series(instrument_prices, benchmark_prices):
    raise NotImplementedError  # Owner: Lead


def calculate_period_return(prices):
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])
    return ((last_close / first_close) - 1.0) * 100.0



def calculate_base_100(prices):
    if not prices:
        raise ValueError("Price series cannot be empty.")
    first_close = float(prices[0]["close"])
    if first_close == 0:
        raise ValueError("First close price cannot be zero.")

    base_100_series = []
    for obs in prices:
        val = (float(obs["close"]) / first_close) * 100.0
        base_100_series.append(
            {"date": obs["date"], "ticker": obs["ticker"], "value": val}
        )
    return base_100_series

def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return
