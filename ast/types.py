class Business:
    def __init__(self, name, staff:Staff, catalog):
        self.name = name
        self.staff = staff
        self.catalogue = catalogue

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Product:
    def __init__(self, name, price, amount):
        self.name = name
        self.price = price
        self.amount = amount

class Staff:    
    def __init__(self,employees: list[Employee]):
        self.employees = employees

class Catalog:
    def __init__(self,products: list[Product]):
        self.products = products