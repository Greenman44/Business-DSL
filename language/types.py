from __future__ import annotations
import pandas as pd

class Bus_Types:
    types = {}
    
    def __init__(self, name : str):
        self.mame = name
        Bus_Types.types[name] = self
    
    @staticmethod
    def find(name : str):
        try:
            return Bus_Types[name]
        except KeyError:
            raise TypeError(f"Undefined Type : {name}")
        



class Business(Bus_Types):
    def __init__(self, name, staff: Collection, catalog : Collection):
        Bus_Types.__init__(self, "business")
        self.name = name
        self.staff = staff
        self.catalogue = catalog
    
class Collection(Bus_Types):
    def __init__(self, items : list[Bus_Types]):
        Bus_Types.__init__(self, "collection")
        self.items = items
        self.df = pd.DataFrame.from_dict(items[0].__dict__)
        for i in range(len(items) - 1):
            self.df = self.df.append(items[i+1].__dict__)
class Employee(Bus_Types):
    def __init__(self, name, salary):
        Bus_Types.__init__(self, name)
        self.name = name
        self.salary = salary

class Product(Bus_Types):
    def __init__(self, name, cost, price):
        Bus_Types.__init__(self, name)
        self.name = name
        self.cost = cost
        self.price = price

        
<<<<<<< Updated upstream
class Business:
    def __init__(self, name, staff: Staff, catalog : Catalog):
        self.name = name
        self.staff = staff
        self.catalogue = catalog
        self.sells = None
        self.adquisitions = None
=======
>>>>>>> Stashed changes


