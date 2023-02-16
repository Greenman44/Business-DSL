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
        self.fill_catalog(business.catalogue)
        self.fill_staff(business.staff)
        self.name = business.name
    

    def get_product(self, name : str) -> Product:
        match = self.product_table["name"] == name
        if match.any():
            return Product(name)
        raise Exception("Product not found")
        
    
    def get_employed(self, name : str) -> Employed:
        """Get employed from employed table"""
        for i in self.employed_table.index:
            if self.employed_table.at[i, "name"] == name:
                return Employed(name, self.employed_table.at[i,"salary"])
        raise Exception("Employed not found")
    
    def get_catalogue(self) -> list[Product]:
        """return list of products"""
        return self.bus.catalogue.df

    def get_staff(self) -> list[Employed]:
        """return list of products"""
        return self.bus.staff.items

    def add_product(self, product : Product):
        """add product to product table"""
        self.product_table = self.product_table.append({"name" : product.name, "amount" : 0}, ignore_index=True)
    
    def add_employed(self, employed : Employed):
        """add employed to employed table"""
        self.employed_table = self.employed_table.append({"name" : employed.name, "salary" : employed.salary}, ignore_index=True)

    def add_productCollection(self, collection : Collection):
        data_names = [product.name for product in collection]
        data_amounts = [0 for product in collection]
        new_products = pd.DataFrame()
        new_products["name"] = data_names
        new_products["amount"] = data_amounts
        self.product_table = pd.concat([self.product_table, new_products], ignore_index=True)
    
    def add_employedCollection(self, collection : Collection):
        data_names = [employed.name for employed in collection] 
        data_salaries = [employed.salary for employed in collection]
        new_employees = pd.DataFrame()
        new_employees["name"] = data_names
        new_employees["salary"] = data_salaries
        self.employed_table = pd.concat([self.employed_table, new_employees], ignore_index=True)


    def fill_catalog(self, coll_products : Collection):
        data_name = [product.name for product in coll_products] 
        data_amount = [0 for i in range(len(coll_products))]
        self.product_table["name"] = data_name
        self.product_table["amount"] = data_amount
    
    def fill_staff(self, coll_employees : Collection):
        data_name = [employed.name for employed in coll_employees]
        data_salary = [employed.salary for employed in coll_employees]
        self.employed_table["name"] = data_name
        self.employed_table["salary"] = data_salary

    
    def delete_employed(self, name:str):
        """delete employed"""
        for i in self.employed_table.index:
            if self.employed_table.at[i, "name"] == name:
                self.employed_table.drop([i], inplace=True)
                break
    
    def delete_employedCollection(self, collection : Collection):
        data_names = [e.name for e in collection]
        data_salary = [e.salary for e in collection]
        df_toDrop = pd.DataFrame()
        df_toDrop["name"] = data_names
        df_toDrop["salary"] = data_salary
        self.employed_table = self.employed_table[~self.employed_table.apply(tuple,1).isin(df_toDrop.apply(tuple,1))]

    def delete_product(self, name:str):
        """delete product from product table"""
        for i in self.product_table.index:
            if self.product_table.at[i, "name"] == name:
                self.product_table.drop([i], inplace=True)
                break
    
    def delete_productCollection(self, collection : Collection):
        data_names = [e.name for e in collection]
        data_amounts = [0 for e in collection]
        df_toDrop = pd.DataFrame()
        df_toDrop["name"] = data_names
        df_toDrop["amount"] = data_amounts
        self.product_table = self.product_table[~self.product_table.apply(tuple,1).isin(df_toDrop.apply(tuple,1))]
        self.product_table = self.product_table.drop_duplicates(subset=["name"],keep=False)
        

    #TODO: CRUD for all tables

    #TODO: Save Data on excel
    def Save_DatatoExcel(self, path = "./excel_sheets"):
        with pd.ExcelWriter(path=path + f"/{self.name}.xlsx") as writer:
            self.product_table.to_excel(writer, sheet_name="catalog")
            self.employed_table.to_excel(writer, sheet_name="staff")
            self.sales_table.to_excel(writer, sheet_name="sales")
            self.invests_table.to_excel(writer, sheet_name="expenses")

    #TODO: Load data from excel
    def ExceltoData(self,excel_sheet_name:str, path = "./excel_sheets")->pd.DataFrame:
        return pd.read_excel(path,excel_sheet_name) 

class Business:
    def __init__(self, name : str, staff: Collection, catalog : Collection, data = None):
        self.name = name
        self.staff = staff
        self.catalogue = catalog
        self.data = Business_Data(self) if data is None else data
    
    def get_staff(self):
        return self.staff

    def get_catalogue(self):
        return  self.catalogue

    def add(self,item):
        if isinstance(item, Collection):
            if isinstance(item.peek(), Product):
                self.catalogue.add(item)
                self.data.add_productCollection(item)
            else:
                self.staff.add(item)
                self.data.add_employedCollection(item)
        
        elif isinstance(item, Product):
            self.catalogue.add(item)
            self.data.add_product(item)
        else:
            self.staff.add(item)
            self.data.add_employed(item)

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

    def get(self, name : str):
        for item in self.items:
            if item.name == name:
                return item
        raise Exception("Item not found")

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

    def peek(self):
        return self.items.copy().pop()

    def delete(self, item):
        if isinstance(item, Collection):
            self._delete_coll(item)
        elif isinstance(item, str):
            self._delete_instanceByName(item)
        else:
            self._delete_instance(item)
    
    def __lt__(self, other) -> bool:
        return len(self.items) < len(other.items)
    
    def __gt__(self, other) -> bool:
        return len(self.items) > len(other.items)
    
    def __le__(self, other) -> bool:
        return len(self.items) <= len(other.items)

    def __ge__(self, other) -> bool:
        return len(self.items) >= len(other.items) 
    
    def __eq__(self, other) -> bool:
        if len(self.items) != len(other.items):
            return False

        aux = self.items.intersection(other)
        return len(aux) == len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)
class Employed:
    def __init__(self, name, salary):
        self.name = name
        self.salary : float = salary
    
    def __str__(self) -> str:
        return f"(name : {self.name}, salary : {str(self.salary)})"
    
    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, other) -> bool:
        return self.salary < other.salary
    
    def __gt__(self, other) -> bool:
        return self.salary > other.salary
    
    def __le__(self, other) -> bool:
        return self.salary <= other.salary

    def __ge__(self, other) -> bool:
        return self.salary >= other.salary 
    
    def __eq__(self, other) -> bool:
        return self.name == other.name and self.salary == other.salary
    
    def __hash__(self) -> int:
        return self.name.__hash__()

class Product:
    def __init__(self, name, amount = 0):
        self.name = name
        self.amount = amount

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, other) -> bool:
        return self.amount < other.amount
    
    def __gt__(self, other) -> bool:
        return self.amount > other.amount
    
    def __le__(self, other) -> bool:
        return self.amount <= other.amount

    def __ge__(self, other) -> bool:
        return self.amount >= other.amount 

    def __eq__(self, other) -> bool:
        return self.name == other.name
    
    def __hash__(self) -> int:
        return self.name.__hash__()