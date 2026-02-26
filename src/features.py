import polars as pl

class Features:
    def add_obi(self, df):
        lf = pl.LazyFrame(df)
        ls = []
        for i in range(20):
            ls.append(((pl.col(f"bid_{i}_q") - pl.col(f"ask_{i}_q")) / (pl.col(f"bid_{i}_q") + pl.col(f"ask_{i}_q"))).alias(f"obi_{i}"))

        return lf.with_columns(*ls).collect()

    def add_micro_price(self, df):
        lf = pl.LazyFrame(df)
        ls = []
        for i in range(20):
            ls.append(((pl.col(f"ask_{i}_p") * pl.col(f"bid_{i}_q") + pl.col(f"bid_{i}_p") * pl.col(f"ask_{i}_q"))/(pl.col(f"bid_{i}_q") + pl.col(f"ask_{i}_q"))).alias(f"micro_price_{i}"))

        return lf.with_columns(*ls).collect()

    def add_spread(self, df):
        lf = pl.LazyFrame(df)
        ls = []
        for i in range(20):
            ls.append((pl.col(f"ask_{i}_p") - pl.col(f"bid_{i}_p")).alias(f"spread_{i}"))

        return lf.with_columns(*ls).collect()

    def add_state(self, df):
        lf = pl.LazyFrame(df)

        mid_price = (pl.col("ask_0_p") + pl.col("bid_0_p")) / 2
        future_mean = pl.col("mid_price").rolling_mean(100).shift(-100)
        change = (future_mean - pl.col("mid_price")) / pl.col("mid_price")
        alpha = 0.00005

        return lf.with_columns(mid_price.alias("mid_price")).with_columns(
            pl.when(change > alpha).then(2)
            .when(change < -alpha).then(0)
            .otherwise(1)
            .alias("label")
        ).collect()

    def add_features(self, df):
        lf = pl.LazyFrame(df)
        ls = []
        for i in range(20):
            ls.append(((pl.col(f"bid_{i}_q")-pl.col(f"ask_{i}_q"))/(pl.col(f"bid_{i}_q")+pl.col(f"ask_{i}_q"))).alias(f"obi_{i}"))
            ls.append(((pl.col(f"ask_{i}_p") * pl.col(f"bid_{i}_q") + pl.col(f"bid_{i}_p") * pl.col(f"ask_{i}_q")) / (pl.col(f"bid_{i}_q") + pl.col(f"ask_{i}_q"))).alias(f"micro_price_{i}"))
            ls.append((pl.col(f"ask_{i}_p") - pl.col(f"bid_{i}_p")).alias(f"spread_{i}"))

        temp = lf.with_columns(*ls).collect()
        return self.add_state(temp)