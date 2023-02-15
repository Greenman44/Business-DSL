import pandas as pd
from language import Business, Collection, Employed, Product


class Business_Data:
    """Class for excel communication"""

    def __init__(self, business: Business):
        self.employed_table = business.staff.df
        self.product_table = business.catalogue.df
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