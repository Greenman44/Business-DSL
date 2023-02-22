from abc import ABCMeta, abstractmethod

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

class VariableDeclaration(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id
class VariableAssignment(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

class VariableCall(Node):
    def __init__(self, id):
        self.id = id
class Bus_Node(Node):
    def __init__(self, name, collection_1, collection_2):
        self.name = name
        self.staff_collection = collection_1
        self.catalog_collection = collection_2

class Emp_Node(Node):
    def __init__(self, name, number):
        self.name = name
        self.number = number

class Bill_Node(Node):
    def __init__(self, business, cost, description):
        self.business = business
        self.cost = cost
        self.description = description

class Number_Node(Node):
    def __init__(self,number):
        self.number = number
class Prod_Node(Node):
    def __init__(self, name, amount = Number_Node(0)):
        self.name = name
        self.amount = amount
class Collection_Node(Node):
    def __init__(self, collection):
        self.collection = collection

class GetStaff_node(Node):
    def __init__(self, business):
        self.business = business

class GetCatalog_node(Node):
    def __init__(self, business):
        self.business = business
class GetElementFrom_Statement(Node):
    def __init__(self, name, collection):
        self.name = name
        self.collection = collection

class GetAmount_node(Node):
    def __init__(self, product) -> None:
        self.product = product

class Foreach_node(Node):
    def __init__(self, loop_var, collection, body):
        self.loop_var = loop_var
        self.collection = collection
        self.body = body

class While_node(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IfStatement(Node):
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body = body

class ElseStatement(Node):
    def __init__(self, if_statement, body) -> None:
        self.if_statement = if_statement
        self.body = body

class NotStatement(Node):
    def __init__(self, stam) -> None:
        self.stam = stam
    # def evaluate(self, context: Context):
    #     pass

class Bool_Expression_Node(Node):
    def __init__(self, left, right, comparer)-> None:
        self.left = left
        self.right = right
        self.comparer = comparer

class Oper_Node(Node):
    def __init__(self, left, right, oper) -> None:
        self.left = left
        self.right = right
        self.oper = oper

class Load(Node):
    def __init__(self, name) -> None:
        self.name = name

class Save(Node):
    def __init__(self, business) -> None:
        self.business = business

class Print_Node(Node):
    def __init__(self, id_1) -> None:
        self.id_1 = id_1

class Funct_Call_Node(Node):
    def __init__(self, params) -> None:
        self.params = params
class Params_Node(Node):
    def __init__(self, params_type, id) -> None:
        self.params_type = params_type
        self.id = id

class Function_Node(Node):
    def __init__(self, type_ret, id, params, list_inst) -> None:
        self.parmas = params
        self.type_ret = type_ret
        self.id = id
        self.list_inst = list_inst

class InStatement(Node):
    def __init__(self, id_1, id_2) -> None:
        self.id_1 = id_1
        self.id_2 = id_2
    
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
    def __init__(self, business, product, cost_price, amount):
        self.business = business
        self.product = product
        self.sale_price = cost_price
        self.amount = amount

class ActionADD(Node):
    def __init__(self, collection_items, item):
        self.collection_items = collection_items
        self.item = item

class ActionDEL(Node):
    def __init__(self, collection_items, item):
        self.collection_items = collection_items
        self.item = item

class ActionDISMISS(Node):
    def __init__(self, business, employed):
        self.business = business
        self.employed = employed
        

class Metrics(Node):
    def __init__(self,business,metric, date):
        self.business = business
        self.metric = metric
        self.date = date