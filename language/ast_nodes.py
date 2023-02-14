from abc import ABCMeta, abstractmethod
import pandas as pd

class Node(metaclass = ABCMeta):
    
    @abstractmethod
    def __init__(self):
        self.processed_type = None

class Program(Node):
    def __init__(self, instructions :  list[Node]):
        self.instructions = instructions


class TypeDeclaration(Node):
    def __init__(self, type, id, value):
        self.type = type
        self.id = id
        self.value = value

class Bus_Node(Node):
    def __init__(self, name, collection_1, collection_2):
        self.name = name
        self.staff_collection = collection_1
        self.catalog_collection = collection_2


class Emp_Node(Node):
    def __init__(self, name, number):
        self.name = name
        self.number = number


class Prod_Node(Node):
    def __init__(self, name):
        self.name = name

class Collection_Node(Node):
    def __init__(self, collection):
        self.collection = collection

class VariableAssignment(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

class VariableCall(Node):
    def __init__(self, id):
        self.id = id

class IfStatement(Node):
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body = body
    
    # def evaluate(self, context: Context):
    #     pass

class WhileStatement(Node):
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body = body
    
    # def evaluate(self, context: Context):
    #     pass
        
class ActionSALE(Node):
    def __init__(self, business, product, sale_price, amount):
        self.business = business
        self.product = product
        self.sale_price = sale_price
        self.amount = amount
        #if(business.sells == None):
        #   business.sells == pd.DataFrame(data = [product.name,sell_price,date], columns = ["product", "price", "date"])
        #else:
        #   business.sells.append({"product" : product.name, "price": sell_price, "date" : date})

class ActionINVESTS(Node):
    def __init__(self, business, product, sale_price, amount):
        self.business = business
        self.product = product
        self.sale_price = sale_price
        self.amount = amount

class ActionADD(Node):
    def __init__(self, collection_items, item):
        self.collection_items = collection_items
        self.item = item

class ActionDEL(Node):
    def __init__(self, collection_items, item):
        self.collection_items = collection_items
        self.item = item

class Metrics(Node):
    def __init__(self,business,metric, date):
        self.business = business
        self.metric = metric
        self.date = date