import pandas as pd
from language import Business, Collection, Employed, Product


class Business_Data:
    """Class for excel communication"""

    def __init__(self, business: Business):
        self.employed_table = business.staff.df
        self.product_table = business.catalogue.df
        self.sales_table = pd.DataFrame(columns=["product", "price", "amount"])
        self.invests_table = pd.DataFrame(columns=["product", "cost", "amount"])
        self.bus = business
    
    def get_product(self, name : str) -> Product:
        """Get product from product table"""
        for product in self.bus.catalogue.items:
            if product.name == name:
                return product
        raise Exception("Product not found: %s" % name)
        
    
    def get_employed(self, name : str) -> Employed:
        """Get employed from employed table"""
        for employee in self.bus.staff.items:
            if employee.name == name:
                return  employee
        raise Exception("Employed not found: %s" % name)
        pass
    
    def get_catalogue(self) -> list[Product]:
        """return list of products"""
        return self.bus.catalogue.items

    def get_staff(self) -> list[Employed]:
        """return list of products"""
        return self.bus.staff.items

    def add_product(self, product : Product):
        """add product to product table"""
        self.bus.catalogue.items.append(product)
        self.bus.catalogue.df.append(product.__dict__)
        

    def add_employed(self, employed : Employed):
        """add employed to employed table"""
        self.bus.catalogue.items.append(employed)
        self.bus.catalogue.df.append(employed.__dict__)

    #TODO: CRUD for all tables

    #TODO: Save Data on excel
    def DatatoExcel(self, data : pd.DataFrame, excel_sheet:str, path = "./excel_sheets"):
        data.to_excel(path, excel_sheet)

    #TODO: Load data from excel
    def ExceltoData(self,excel_sheet_name:str, path = "./excel_sheets")->pd.DataFrame:
        return pd.read_excel(path,excel_sheet_name) 