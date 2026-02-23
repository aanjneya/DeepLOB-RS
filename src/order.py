from datetime import timedelta

class Order:
    order_id = 0
    LATENCY = 20

    def __init__(self, sim_time, side, price, quantity):
        self.order_id = Order.order_id
        self.creation_time = sim_time
        self.arrival_time = self.creation_time+Order.LATENCY
        self.side = side
        self.price = price
        self.quantity = quantity
        Order.order_id+= 1
        self.status = "PENDING"
