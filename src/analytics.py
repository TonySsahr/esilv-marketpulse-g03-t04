def index_by_date(prices):
    return {observation["date"]: observation for observation in prices}


def align_series(instrument_prices, benchmark_prices):
    return instrument_return - benchmark_return


def calculate_period_return(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_base_100(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError  # Owner: see team table

