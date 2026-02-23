class Portfolio:
    def __init__(self, start_cash):
        self.cash = start_cash
        self.inventory = 0
        self.realized_pnl = 0
        self.unrealized_pnl = 0
        self.value = self.cash

    def get_trade(self, trade):
        value = trade.price * trade.quantity
        if trade.order.side == 'buy':
            self.cash -= value + value*trade.FEE
            self.inventory += trade.quantity
        elif trade.order.side == 'sell':
            self.cash += value - value*trade.FEE
            self.inventory -= trade.quantity

    def update(self, mid_price):
        self.value = self.cash + self.inventory*mid_price

