import numpy as np

def calculate_return_and_volatility(data, timescale=252):
    # Calculates the return and standard deviation (volatility) of a dataset
    returns = np.log(data / data.shift(1))
    return returns.mean() * timescale, returns.std() * np.sqrt(timescale)