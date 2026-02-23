import polars as pl
from src.matching_engine import Matching_Engine
from src.portfolio import Portfolio
import glob


class Backtesting:
    def __init__(self):
        self.match = Matching_Engine()
        self.portfolio = Portfolio(10000)
        self.data = glob.glob("data/raw/*.parquet")
        self.data.sort()

    def run(self):
        for filename in self.data:
            df = pl.read_parquet(filename)
            asks = df["ask_0_p"].to_list()
            bids = df["bid_0_p"].to_list()
            times = df["event_time"].to_list()
            for cur_ask, cur_bid, cur_time in zip(asks, bids, times):
                trades = self.match.execute_order(cur_ask, cur_bid, cur_time)
                for j in trades:
                    self.portfolio.get_trade(j)

                self.portfolio.update((cur_ask + cur_bid)/2)