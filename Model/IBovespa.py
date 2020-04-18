class Investing:
    """Data extracted from https://www.investing.com/equities/StocksFilter?index_id={}}"""

    def __init__(self, name, last, high, low, chg, chg_percent, vol, time):
        self.name = name
        self.last = last
        self.high = high
        self.low = low
        self.chg = chg
        self.chg_percent = chg_percent
        self.vol = vol
        self.time = time

