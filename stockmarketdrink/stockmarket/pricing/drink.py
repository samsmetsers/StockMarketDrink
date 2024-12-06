import numpy as np

class Drink():
    def __init__(self, name: str, start_quantity: int, cost_price: float, start_price: float):
        self.name = name
        self.start_quantity = start_quantity
        self.quantity = start_quantity
        self.cost_price = cost_price
        self.price_array = []
        self.time_array = []
        self.price = start_price
        self.fraction = 1

    def compute_quantity_fraction(self):
        self.fraction = self.quantity/self.start_quantity



