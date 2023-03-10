from __future__ import annotations
import pandas as pd
import warnings
from dataclasses import dataclass
from datetime import date
from os import getcwd

class Business_Data:
    """Class for excel communication"""

    def __init__(
        self,
        business_name: str,
        employed_data = None,
        product_data = None,
        sales_data = None,
        invests_data = None,
        bill_data = None,
    ):
        self.employed_table = (
            pd.DataFrame(columns = ["name", "salary"])
            if employed_data is None
            else employed_data
        )
        self.product_table = (
            pd.DataFrame(columns = ["name", "amount"])
            if product_data is None
            else product_data
        )
        self.sales_table = (
            pd.DataFrame(columns = ["product", "price", "amount", "date"])
            if sales_data is None
            else sales_data
        )
        self.invests_table = (
            pd.DataFrame(columns = ["product", "cost", "amount", "date"])
            if invests_data is None
            else invests_data
        )
        self.bill_table = (
            pd.DataFrame(columns = ["type", "cost", "date"])
            if bill_data is None
            else bill_data
        )
        self.name = business_name

    def add_bill(self, bill : Bill):
        self.bill_table = self.bill_table.append(
            {"type": bill.bill_type, "cost": bill.cost, "date" : date.today()}, ignore_index=True
        )

    def get_product(self, name: str) -> Product:
        for i in self.product_table.index:
            if self.product_table.at[i, "name"] == name:
                return i, Product(name, amount = Number(self.product_table.at[i, "amount"]))
        raise Exception("Product not found")

    def get_employed(self, name: str) -> Employed:
        """Get employed from employed table"""
        for i in self.employed_table.index:
            if self.employed_table.at[i, "name"] == name:
                return i, Employed(name, Number(self.employed_table.at[i, "salary"]))
        raise Exception("Employed not found")

    def get_catalogue(self) -> Collection:
        """return collection of products"""
        catalog = []
        for i in self.product_table.index:
            current_product = Product(self.product_table.at[i, "name"], amount=Number(self.product_table.at[i, "amount"]))
            catalog.append(current_product)
        return Collection(catalog)

    def get_staff(self) -> Collection:
        staff = []
        for i in self.employed_table.index:
            current_employed = Employed(self.employed_table.at[i, "name"], Number(self.employed_table.at[i, "salary"]))
            staff.append(current_employed)
        return Collection(staff)

    def add_product(self, product: Product):
        """add product to product table"""
        self.product_table = self.product_table.append(
            {"name": product.name, "amount": product.amount.number}, ignore_index=True
        )

    def add_employed(self, employed: Employed):
        """add employed to employed table"""
        self.employed_table = self.employed_table.append(
            {"name": employed.name, "salary": employed.salary.number}, ignore_index=True
        )

    def add_productCollection(self, collection: Collection):
        data_names = [product.name for product in collection]
        data_amounts = [product.amount.number for product in collection]
        new_products = pd.DataFrame()
        new_products["name"] = data_names
        new_products["amount"] = data_amounts
        self.product_table = pd.concat(
            [self.product_table, new_products], ignore_index=True
        )

    def add_employedCollection(self, collection: Collection):
        data_names = [employed.name for employed in collection]
        data_salaries = [employed.salary.number for employed in collection]
        new_employees = pd.DataFrame()
        new_employees["name"] = data_names
        new_employees["salary"] = data_salaries
        self.employed_table = pd.concat(
            [self.employed_table, new_employees], ignore_index=True
        )

    def fill_catalog(self, coll_products: Collection):
        data_name = [product.name for product in coll_products]
        data_amount = [product.amount.number for product in coll_products]
        self.product_table["name"] = data_name
        self.product_table["amount"] = data_amount

    def fill_staff(self, coll_employees: Collection):
        data_name = [employed.name for employed in coll_employees]
        data_salary = [employed.salary.number for employed in coll_employees]
        self.employed_table["name"] = data_name
        self.employed_table["salary"] = data_salary

    def delete_employed(self, name: str):
        """delete employed"""
        for i in self.employed_table.index:
            if self.employed_table.at[i, "name"] == name:
                self.employed_table.drop([i], inplace=True)
                break

    def delete_employedCollection(self, collection: Collection):
        data_names = [e.name for e in collection]
        data_salary = [e.salary.number for e in collection]
        df_toDrop = pd.DataFrame()
        df_toDrop["name"] = data_names
        df_toDrop["salary"] = data_salary
        self.employed_table = self.employed_table[
            ~self.employed_table.apply(tuple, 1).isin(df_toDrop.apply(tuple, 1))
        ]

    def delete_product(self, name: str):
        """delete product from product table"""
        for i in self.product_table.index:
            if self.product_table.at[i, "name"] == name:
                self.product_table.drop([i], inplace=True)
                break

    def delete_productCollection(self, collection: Collection):
        data_names = [e.name for e in collection]
        data_amounts = [e.amount.number for e in collection]
        df_toDrop = pd.DataFrame()
        df_toDrop["name"] = data_names
        df_toDrop["amount"] = data_amounts
        self.product_table = self.product_table[
            ~self.product_table.apply(tuple, 1).isin(df_toDrop.apply(tuple, 1))
        ]
        self.product_table = self.product_table.drop_duplicates(
            subset=["name"], keep=False
        )


    def Save_DatatoExcel(self, path=getcwd() + "/business_data/excel_data"):
        with pd.ExcelWriter(path=path + f"/{self.name}.xlsx", date_format="yyyy/m/d", engine="openpyxl") as writer:
            self.product_table.to_excel(writer, sheet_name="catalog")
            self.employed_table.to_excel(writer, sheet_name="staff")
            self.sales_table.to_excel(writer, sheet_name="sales")
            self.invests_table.to_excel(writer, sheet_name="invests")
            self.bill_table.to_excel(writer, sheet_name="bills")


    @staticmethod
    def LoadBusiness(business_name: str, path=getcwd() + "/business_data/excel_data") -> Business:
        try:
            excel = pd.ExcelFile(path + f"/{business_name}.xlsx")
        except:
            raise Exception(f"{business_name} not found")

        product_data = excel.parse("catalog", index_col=0)
        employed_data = excel.parse("staff", index_col=0)
        sales_data = excel.parse("sales", index_col=0)
        invests_data = excel.parse("invests",index_col=0)
        bill_data = excel.parse("bills", index_col=0)
        data = Business_Data(
            business_name=business_name,
            employed_data=employed_data,
            product_data=product_data,
            sales_data=sales_data,
            invests_data=invests_data,
            bill_data=bill_data
        )
        #data.drop_unnamedColumns()
        catalog = data.get_catalogue()
        staff = data.get_staff()
        return Business(business_name, staff, catalog, data)

    def make_sale(self, sale : Sale):
        index, current_product = self.get_product(sale.product.name)
        self.product_table.at[index, "amount"] = current_product.amount.number - sale.amount
        self.sales_table = self.sales_table.append({"product" : sale.product.name,"price" : sale.price , "amount" : sale.amount, "date" : date.today()}, ignore_index=True)
    

    def make_invest(self, invest: Invest):
        try:
            index, current_product = self.get_product(invest.product.name)
            self.product_table.at[index, "amount"] = current_product.amount.number + invest.amount
        except:
            self.add_product(invest.product)
        self.invests_table = self.invests_table.append({"product" : invest.product.name,"cost" : invest.cost , "amount" : invest.amount, "date" : date.today()}, ignore_index=True)
        
    def get_net_sales(self, date : date):
        net_sales = 0
        for i in self.sales_table.index:
            if self.sales_table.at[i,"date"] >= date:
                net_sales += self.sales_table.at[i,"price"]
        return net_sales
    def get_investments(self, date : date):
        investments = 0
        for i in self.invests_table.index:
            
            if self.invests_table.at[i,"date"] >= date:
                investments += self.invests_table.at[i,"cost"]
        return investments
    def get_gross_profit(self, date : date):
        investments = self.get_investments(date)
        net_sales = self.get_net_sales(date)
        return net_sales - investments
    
    def get_gross_margin(self, date : date):
        net_sales = self.get_net_sales(date)
        gross_profit = self.get_gross_profit(date)
        return (gross_profit/net_sales) * 100
    
    def get_expenses(self, date : date):
        investments = self.get_investments(date)
        bills = 0
        for i in self.bill_table.index:
            if self.bill_table.at[i,"date"] >= date:
                bills += self.bill_table.at[i,"cost"]
        return investments + bills
    
    def get_earnings(self, date : date):
        expenses = self.get_expenses(date)
        net_sales = self.get_net_sales(date)
        return net_sales - expenses



    
    def get_metric(self, current_metric : str, date: date):
        metrics = {
            "net_sales" : self.get_net_sales,
            "gross_profit" : self.get_gross_profit,
            "gross_margin" :  self.get_gross_margin,
            "expenses" : self.get_expenses,
            "earnings" : self.get_earnings,
        }
        return metrics[current_metric](date)
            
        
class Business:
    def __init__(self, name: str, staff: Collection, catalog: Collection, data=None):
        self.name = name
        self.staff = staff
        self.catalogue = catalog
        if data is None:
            self.data = Business_Data(business_name=name)
            self.data.fill_catalog(catalog)
            self.data.fill_staff(staff)
        else:
            self.data = data

    def add_Bill(self, cost:Number, description:str):
        self.data.add_bill(Bill(bill_type=description, cost=cost.number, date=date.today()))

    def save(self):
        self.data.Save_DatatoExcel()

    def make_sale(self, product_name:str, price:Number, amount: Number):
        p = self.get(product_name)
        p.amount -= amount
        self.data.make_sale(Sale(product=Product(product_name), price=price.number, amount=int(amount.number)))

    def make_invest(self, product_name:str, cost:Number, amount:Number):
        try:
            p1 = self.get(product_name)
            p1.amount += amount
        except:
            self.catalogue.add(Product(product_name,amount))    
        self.data.make_invest(Invest(product=Product(product_name, amount=amount), cost=cost.number, amount=int(amount.number)))

    def calculate_metrics(self, metric : str, date):
        return self.data.get_metric(metric, date)

    def get_staff(self):
        return self.staff

    def get_catalogue(self):
        return self.catalogue

    def get(self, name):
        try:
            return self.catalogue.get(name)
        except:
            return self.staff.get(name)

    def add(self, item):
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

    def any_product(self, product: Product):
        return any(p == product for p in self.catalogue)

    def delete(self, item):
        if isinstance(item, Product):
            self.catalogue._delete_instance(item)
        elif isinstance(item, Collection):
            self.catalogue._delete_coll(item)
        else:
            self.catalogue._delete_instanceByName(item)
        try:
            self.data.delete_product(item.name)
        except:
            self.data.delete_product(item)

    def dismiss(self, item):
        if isinstance(item, Employed):
            self.staff._delete_instance(item)
        elif isinstance(item, Collection):
            self.staff._delete_coll(item)
        else:
            self.staff._delete_instanceByName(item)
        
        try:
            self.data.delete_employed(item.name)
        except:
            self.data.delete_employed(item)

    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def __str__(self) -> str:
        ret = "BUSSINESS: " + self.name + "\n" + "STAFF: \n"
        
        for emp in self.staff:
            ret += "name:"+ " " + emp.name + " " + "salary:"+ " " + str(emp.salary) + "\n" 
        ret += "CATALOG: \n"
        for prod in self.catalogue: 
            ret += "name:"+ " " + prod.name + " " + "amount:"+ " " + str(prod.amount) + "\n" 
        return ret

    def __repr__(self) -> str:
        return str(self)
    
    def __contains__(self, item) -> bool:
        if isinstance(item, Product):
            return item in self.catalogue
        elif isinstance(item,Employed):
            return item in self.staff
        raise Exception(f"business not compatible with {item}")            

class Collection:
    def __init__(self, items: list[Employed | Product | Business]):
        self.items = set(items)

    def __str__(self) -> str:
        return str(self.items)

    def __repr__(self) -> str:
        return str(self)

    def get(self, name: str):
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
            self._delete_instance(item)

    def _delete_instance(self, item):
        try:
            self.items.remove(item)
        except KeyError:
            warnings.warn_explicit(
                f"You try remove an item: '{str(item)}' that does not exist",
                RuntimeWarning,
                "Collection class",
                262,
            )

    def _delete_instanceByName(self, name: str):
        current_item = None
        for item in self.items:
            if name == item.name:
                current_item = item
                break
        
        self._delete_instance(current_item if current_item is not None else name )

    def get_type(self):
        return self.peek().__class__.__name__.lower()

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
    

    def __contains__(self,item):
        return item in self.items



class Employed:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

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
    
    def __add__(self, other):
        new_salary = self.salary + other.salary
        return new_salary
    
    def __sub__(self, other):
        new_salary = self.salary - other.salary
        return new_salary
    
    def __mul__(self, other):
        new_salary = self.salary * other.salary
        return new_salary
    
    def __truediv__(self, other):
        new_salary = self.salary / other.salary
        return new_salary


class Number:
    def __init__(self, number):
        self.number = number
    
    def __str__(self) -> str:
        return str(self.number)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __lt__(self, other) -> bool:
        return self.number < other.number

    def __gt__(self, other) -> bool:
        return self.number > other.number

    def __le__(self, other) -> bool:
        return self.number <= other.number

    def __ge__(self, other) -> bool:
        return self.number >= other.number


    def __eq__(self, other):
        return self.number == other.number
    
    def __hash__(self) -> int:
        return self.number.__hash__()
    
    def __add__(self, other):
        return Number(self.number + other.number)
    
    def __sub__(self, other):
        return Number(self.number - other.number)
    
    def __mul__(self, other):
        return Number(self.number * other.number)
    
    def __truediv__(self, other):
        if other.number == 0:
            raise ValueError("You cannot divide by zero")
        return Number(self.number / other.number)
    
    def __mod__(self, other):
        return self.number % other.number


class Product:
    def __init__(self, name, amount=Number(0)):
        self.name = name
        self.amount = amount

    def __str__(self) -> str:
        return f"(name : {self.name}, amount : {str(self.amount)})"

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
    
    def __add__(self, other):
        new_salary = self.amount + other.amount
        return new_salary
    
    def __sub__(self, other):
        new_salary = self.amount - other.amount
        return new_salary
    
    def __mul__(self, other):
        new_salary = self.amount * other.amount
        return new_salary
    
    def __truediv__(self, other):
        new_salary = self.amount / other.amount
        return new_salary
    
    def get_amount(self):
        return self.amount

@dataclass
class Sale:
    product : Product
    price : float
    amount : int

@dataclass
class Invest:
    product : Product
    cost : float
    amount : int

@dataclass
class Bill:
    bill_type : str
    cost : float
    date : date

@dataclass
class Function:
    parameters : list 
    body : list

