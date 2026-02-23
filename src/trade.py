class Trade:
    trade_id = 0

    def __init__(self, order, fill_price, fill_quantity, timestamp):
        self.FEE = 0.0004
        self.trade_id = Trade.trade_id
        Trade.trade_id += 1
        self.order = order
        self.timestamp  = timestamp
        self.price = fill_price
        self.quantity = fill_quantity
