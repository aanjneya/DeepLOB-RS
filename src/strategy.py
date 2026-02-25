from order import Order

class Strategy:
    def __init__(self):
        self.open_buy = False

    def on_tick(self, cur_ask, cur_bid, cur_time):
        ls  = []
        if not self.open_buy:
            ls.append(Order(cur_time, "BUY", cur_bid-10, 0.1 ))
            self.open_buy = True

        return ls

    def on_execution(self):
        self.open_buy = False