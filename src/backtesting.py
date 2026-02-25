import polars as pl
from matching_engine import Matching_Engine
from portfolio import Portfolio
import glob
from strategy import Strategy


class Backtesting:
    def __init__(self):
        self.match = Matching_Engine()
        self.portfolio = Portfolio(10000)
        self.data = glob.glob("src/data/raw/*.parquet")
        print("Found", len(self.data), "files!")
        self.data.sort()
        self.strategy = Strategy()

    def run(self):
        for filename in self.data:
            df = pl.read_parquet(filename)
            asks = df["ask_0_p"].to_list()
            bids = df["bid_0_p"].to_list()
            times = df["event_time"].to_list()

            for cur_ask, cur_bid, cur_time in zip(asks, bids, times):
                trades = self.match.execute_order(cur_ask, cur_bid, cur_time)
                ls = self.strategy.on_tick(cur_ask, cur_bid, cur_time)
                self.match.add_orders(ls)

                for j in trades:
                    self.portfolio.get_trade(j)
                    self.strategy.on_execution()

                self.portfolio.update((cur_ask + cur_bid)/2)