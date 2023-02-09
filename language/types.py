import pandas as pd
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Product:
    def __init__(self, name, cost, price):
        self.name = name
        self.cost = cost
        self.price = price

class Staff:    
    def __init__(self, employees: list[Employee]):
        self.employees = employees
        self.df = pd.DataFrame.from_dict(employees[0].__dict__)
        for i in range(len(employees) - 1):
            self.df = self.df.append(employees[i+1].__dict__)

class Catalog:
    def __init__(self, products: list[Product]):
        self.products = products
        self.df = pd.DataFrame.from_dict(products[0].__dict__)
        for i in range(len(products) - 1):
            self.df = self.df.append(products[i+1].__dict__)
        
class Business:
    def __init__(self, name, staff: Staff, catalog : Catalog):
        self.name = name
        self.staff = staff
        self.catalogue = catalog


