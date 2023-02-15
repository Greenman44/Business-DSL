from __future__ import annotations
import pandas as pd

        
class Type:
    def __init__(self, name:str):
        self.name = name
        self.attribute = {}

    def def_attribute(self, name , value):
        self.attribute[name] = value
class Instance:
    def __init__(self, type : Type, value) -> None:
        self.type = type
        self.value = value

class Business:
    def __init__(self, name, staff: Collection, catalog : Collection):
        self.name = name
        self.staff = staff
        self.catalogue = catalog
    
class Collection:
    def __init__(self, items : list[Employed|Product|Business]):
        self.items = items
        self.df = pd.DataFrame.from_dict(items[0].__dict__)
        for i in range(len(items) - 1):
            self.df = self.df.append(items[i+1].__dict__)

class Employed:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Product:
    def __init__(self, name, cost, price):
        self.name = name
        self.cost = cost
        self.price = price


class Bus_Context:
    def __init__(self):
        self._types = {}
        self._create_busTypes()

    def _create_busTypes(self):
        self._types["str"] = Type("str")
        self._types["number"] = Type("number")
        self._types["business"] = Type("business")
        self._types["collection"] = Type("collection")
        self._types["employed"] = Type("employed")
        self._types["product"] = Type("product")
        


    def find_type(self, name:str):
        try:
            return self._types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')
        


