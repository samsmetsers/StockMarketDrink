import numpy as np
import pandas as pd
import datetime
import json
from .drink import Drink

class Pricer():
    def __init__(self):

        self.drinks = {"Bier": Drink(name="Bier", start_quantity=480, cost_price=0.3125, start_price=0.3125),
        "Rode Wijn": Drink(name="Rode Wijn", start_quantity=60, cost_price=0.88, start_price=0.88),
        "Witte Wijn": Drink(name="Witte Wijn", start_quantity=60, cost_price=0.70, start_price=0.70),
        "Jenever":  Drink(name="Jenever", start_quantity=130, cost_price=0.50, start_price=0.50),
        "Salmari": Drink(name="Salmari", start_quantity=90, cost_price=0.70, start_price=0.70),
        "RocketShot": Drink(name="RocketShot", start_quantity=90, cost_price=0.63, start_price=0.63),
        "Fris":  Drink(name="Fris", start_quantity=144, cost_price=0.50, start_price=0.50)}

        self.total_cost = 0
        self.duration = 3*60*60
        self.start_time = datetime.datetime.now().timestamp()
        self.current_time = self.start_time

        self.revenue = 0

        for name, drink in self.drinks.items():
            self.total_cost += drink.cost_price * drink.start_quantity
            drink.price_array.append(drink.price)
            drink.time_array.append(0)
        

    def update_prices(self, names: list, quantities: list):
        self.current_time = datetime.datetime.now().timestamp()
        difference = 0
        

        for i in range(len(names)):
            name = names[i]
            quantity = quantities[i]
            current_drink = self.drinks[name]
            
            self.revenue = current_drink.price * quantity
            # verkocht
            delta = 0.01*quantity + 1
            # fractie over
            delta += quantity/current_drink.quantity 

            temporary_new_price = delta*current_drink.price

            # update quantity of bought product
            current_drink.quantity -= quantity

            potential_profit = current_drink.quantity*current_drink.price
            expected_profit = current_drink.quantity*temporary_new_price

            difference += expected_profit - potential_profit
            
            current_drink.price = temporary_new_price
            current_drink.price_array.append(current_drink.price)
            current_drink.time_array.append((self.current_time - self.start_time))

        total_fraction = 0
        for curname, drink in self.drinks.items():
            if curname not in names:
                drink.compute_quantity_fraction()
                total_fraction += drink.fraction

        for curname, drink in self.drinks.items():
            if curname not in names:
                individual_fraction = drink.fraction / total_fraction
                amount_down = individual_fraction*difference

                pot_profit = drink.price * drink.quantity
                exp_profit = pot_profit - amount_down

                drink.price = exp_profit/drink.quantity
                drink.price_array.append(drink.price)
                drink.time_array.append((self.current_time - self.start_time))

        
    
    def to_json(self):
        total_dict = {}
        for name, drink in self.drinks.items():
            total_dict.update({name+"1": drink.name})
            total_dict.update({name+"2": drink.cost_price})
            total_dict.update({name+"3": drink.start_quantity})
            total_dict.update({name+"4": drink.price})
            total_dict.update({name+"5": drink.price_array})
            total_dict.update({name+"6": drink.time_array})
            total_dict.update({name+"7": drink.fraction})
            total_dict.update({name+"8": drink.quantity})

        total_dict.update({"total_cost": self.total_cost})
        total_dict.update({"current_time": self.current_time})
        total_dict.update({"duration": self.duration})
        total_dict.update({"start_time": self.start_time})
        total_dict.update({"revenue": self.revenue})

        return total_dict

    def from_json(self, json: dict):
        new_drinks = {}
        for name, drink in self.drinks.items():
            drink.price = json[name+"4"]
            drink.price_array = json[name+"5"]
            drink.time_array = json[name+"6"]
            drink.fraction = json[name+"7"]
            drink.quantity = json[name+"8"]
            new_drinks.update({name:drink})
        self.drinks=new_drinks
        
        self.total_cost = json["total_cost"]
        self.current_time = json["current_time"]
        self.duration = json["duration"]
        self.start_time = json["start_time"]
        self.revenue = json["revenue"]






        

        



        
    

