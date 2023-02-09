from abc import ABCMeta, abstractmethod
import pandas as pd

class Node(metaclass = ABCMeta):
    
    @abstractmethod
    def __init__(self):
        pass

class Program(Node):
    def __init__(self, instructions :  list[Node]):
        self.instructions = instructions


class TypeDeclaration(Node):
    def __init__(self, type, id, value):
        self.type = type
        self.id = id
        self.value = value

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
        
class ActionSell(Node):
    def __init__(self, business, product, date, sell_price):
        self.business = business
        self.product = product
        self.date = date
        self.sell_price = sell_price
        #if(business.sells == None):
        #   business.sells == pd.DataFrame(data = [product.name,sell_price,date], columns = ["product", "price", "date"])
        #else:
        #   business.sells.append({"product" : product.name, "price": sell_price, "date" : date})

class ActionBuy()