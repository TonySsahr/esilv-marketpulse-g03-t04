def index_by_date(prices):
    return {observation["date"]: observation for observation in prices}


def align_series(instrument_prices, benchmark_prices):
    raise NotImplementedError  # Owner: Lead


def calculate_period_return(prices):
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])
    return ((last_close / first_close) - 1.0) * 100.0



def calculate_base_100(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return
