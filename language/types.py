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

class Catalog:
    def __init__(self, products: list[Product]):
        self.products = products
        
class Business:
    def __init__(self, name, staff: Staff, catalog : Catalog):
        self.name = name
        self.staff = staff
        self.catalogue = catalog


