from __future__ import annotations
import pandas as pd
import warnings
class Business_Data:
    """Class for excel communication"""

    def __init__(self, business: Business):
        self.employed_table = pd.DataFrame(columns=["name", "salary"])
        self.product_table = pd.DataFrame(columns=["name", "amount"])
        self.sales_table = pd.DataFrame(columns=["product", "price", "amount"])
        self.invests_table = pd.DataFrame(columns=["product", "cost", "amount"])
    
    def get_product(self, name : str) -> Product:
        """Get product from product table"""
        pass
    
    def get_employed(self, name : str) -> Employed:
        """Get employed from employed table"""
        pass
    
    def get_catalogue(self) -> list[Product]:
        """return list of products"""
        pass

    def get_staff(self) -> list[Employed]:
        """return list of products"""
        pass

    def add_product(self, product : Product):
        """add product to product table"""
        pass

    def add_employed(self, employed : Employed):
        """add employed to employed table"""
        pass

    #TODO: CRUD for all tables

    #TODO: Save Data on excel
    #TODO: Load data from excel

class Business:
    def __init__(self, name : str, staff: Collection, catalog : Collection, data = None):
        self.name = name
        self.staff = staff
        self.catalogue = catalog
        self.data = Business_Data(self) if data is None else data
    
    def add(self,item):
        if isinstance(item, Collection):
            if isinstance(item[0], Product):
                self.catalogue.add(item)
            else:
                self.staff.add(item)    
        
        elif isinstance(item, Product):
            self.catalogue.add(item)
        else:
            self.staff.add(item)

    def any_product(self, product : Product):
        return any(p == product for p in self.catalogue)

    def delete(self, item):
        if isinstance(item, Product):
            self.catalogue._delete_instance(item)
        elif isinstance(item, Collection):
            self.catalogue._delete_coll(item)
        else:
            self.catalogue._delete_instanceByName(item)
        self.data.delete_product(item)
    
    def dismiss(self,item):
        if isinstance(item, Employed):
            self.staff._delete_instance(item)
        elif isinstance(item, Collection):
            self.staff._delete_coll(item)
        else:
            self.staff._delete_instanceByName(item)
    
    def __hash__(self) -> int:
        return self.name.__hash__()



class Collection:
    def __init__(self, items : list[Employed|Product|Business]):
        self.items = set(items)


    def add(self, item):
        if isinstance(item, Collection):
            self.items.update(item)
        else:
            self.items.add(item)
    
    def _delete_coll(self, collection):
        for item in collection:
            self.delete_instance(item)
            
    def _delete_instance(self, item):
        try:
            self.items.remove(item)
        except KeyError:
            warnings.warn_explicit(f"You try remove an item: '{item.name}' that does not exist", RuntimeWarning, "Collection class", 104)

    def _delete_instanceByName(self, name : str):
        current_item = None
        for item in self.items:
            if name == item.name:
                current_item = item
                break
        self.delete_instance(current_item)

    def delete(self, item):
        if isinstance(item, Collection):
            self._delete_coll(item)
        elif isinstance(item, str):
            self._delete_instanceByName(item)
        else:
            self._delete_instance(item)

    def __iter__(self):
        return iter(self.items)
    
    def __getitem__(self, index):
        return self.items[index]

class Employed:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def __str__(self) -> str:
        return f"name : {self.name}, salary : {str(self.salary)}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other) -> bool:
        return self.name == other.name and self.salary == other.salary
    
    def __hash__(self) -> int:
        return self.name.__hash__()

class Product:
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return self.name == other.name
    
    def __hash__(self) -> int:
        return self.name.__hash__()