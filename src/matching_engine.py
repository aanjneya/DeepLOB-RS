from portfolio import Portfolio
from trade import Trade

class Matching_Engine:

    def __init__(self):
        self.active_orders = []

    def execute_order(self, ask, bid, time):
        fulfilled = []
        for order in self.active_orders:
            if time >= order.arrival_time:
                if (order.side=="BUY" and ask<order.price) or (order.side=="SELL" and bid>order.price):
                    order.status = "FULFILLED"
                    trade = Trade(order, order.price, order.quantity, time)
                    fulfilled.append(trade)
        self.active_orders = [x for x in self.active_orders if x.status != "FULFILLED"]
        return fulfilled

    def add_orders(self, orders):
        for order in orders:
            self.active_orders.append(order)


