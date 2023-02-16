from .visitor import when, on
from .types_checker import Bus_Context, Instance
from .ast_nodes import *
from .scope import Scope
import datetime

class SemanticChecker:
    def __init__(self, scope : Scope):
        self.scope = scope
        self.context = Bus_Context()
        self.today =  datetime.datetime.now()
    
    @on("node")
    def visit(self, node):
        pass

    @when(Program)
    def visit(self, node : Program):
        for inst in node.instructions:
            self.visit(inst)
    
    @when(VariableDeclaration)
    def visit(self, node : VariableDeclaration):
        try:
            current_type = self.context.find_type(node.type)
        except:
            raise TypeError("Undefined type")

        var = self.scope.find(node.id)
        if var != None:
            raise Exception("You can not declare two variables with the same name")
        self.scope.set(node.id, current_type.name)
        node.processed_type = current_type.name

    @when(TypeDeclaration)
    def visit(self, node : TypeDeclaration):
        try:
            current_type = self.context.find_type(node.type)
        except:
            raise TypeError("Undefined type")
        var = self.scope.find(node.id)
        if var != None:
            raise Exception("You can not declare two variables with the same name")

    
        self.visit(node.value)
        if not(current_type.name in node.value.processed_type):
            raise TypeError("Bad Type declaration")

        self.scope.set(node.id, node.value.processed_type)
        node.processed_type = node.value.processed_type
    
    @when(VariableAssignment)
    def visit(self, node : VariableAssignment):
        current_type = self.scope.find(node.id)
        if current_type is None:
            raise Exception(f"Variable '{node.name}' is not defined")
        
        self.visit(node.value)
        if not (current_type in node.value.processed_type):
            raise Exception(f" Impossible assign value {node.value} to variable '{node.id}'. Type '{current_type}' different to '{node.value.processed_type}'")
        self.scope.set(node.id, node.value.processed_type)
        node.processed_type = node.value.processed_type

    @when(VariableCall)
    def visit(self, node : VariableCall):
        current_type = self.scope.find(node.id)
        if current_type is None:
            raise Exception(f"Variable '{node.id}' is not defined")
        
        node.processed_type = current_type
        

    @when(Bus_Node)
    def visit(self, node : Bus_Node):
        self.visit(node.staff_collection)
        self.visit(node.catalog_collection)
        if node.staff_collection.processed_type != "collection_employed":
            raise Exception("The type of the first collection need to be employed")
        if node.catalog_collection.processed_type != "collection_product":
            raise Exception("The type of the second collection need to be product")
        node.processed_type = "business"
    
    @when(Prod_Node)
    def visit(self, node : Prod_Node):
        node.processed_type = "product"
    
    @when(Emp_Node)
    def visit(self, node : Emp_Node):
        node.processed_type = "employed"
    
    @when(Bill_Node)
    def visit(self, node : Bill_Node):
        self.visit(node.business)
        if node.business.processed_type != "business":
            raise Exception("Only can add bills on business")
        node.processed_type = "bill"

    
    @when(Collection_Node)
    def visit(self, node : Collection_Node):
        self.visit(node.collection[0])
        current_type = node.collection[0].processed_type
        for i in range(1, len(node.collection)):
            self.visit(node.collection[i])
            if current_type != node.collection[i].processed_type:
                raise Exception("The type of every item in a collection needs to be the same")

        node.processed_type = f"collection_{current_type}"




    @when(ActionSALE)
    def visit(self, node : ActionSALE):
        self.visit(node.business)
        self.visit(node.product)
        if node.business.processed_type != "business":
            raise Exception("Only can make an action sale from business")
        if node.product.processed_type != "product":
            raise Exception("Only can make an action sale over a product")
        if not float.is_integer(node.amount):
            raise Exception("The amount must be an integer")
        
        node.processed_type = "actionSale"
    
    @when(ActionINVESTS)
    def visit(self, node : ActionINVESTS):
        self.visit(node.business)
        self.visit(node.product)
        if node.business.processed_type != "business":
            raise Exception("Only can make an action invest from business")
        if node.product.processed_type != "product":
            raise Exception("Only can make an action invest over a product")
        if not float.is_integer(node.amount):
            raise Exception("The amount must be an integer")
        
        node.processed_type = "actionInvest"

    @when(ActionADD)
    def visit(self, node : ActionADD):
        self.visit(node.collection_items)
        current_type = node.collection_items.processed_type
        if current_type != "business" and not ("collection" in current_type):
            raise Exception("The type of the first ID has to be business or collection")
        self.visit(node.item)
        current_type_2 = node.item.processed_type
        if current_type == "business" and not("employed" in current_type_2) and not ("product" in current_type_2):
            raise Exception("You only can add to a business employeds and products")
        if "collection" in current_type and current_type_2 not in current_type:
            raise Exception(f"You can not add {current_type_2} to a collection of {current_type}")
        node.processed_type = "actionAdd"

    @when(ActionDEL)
    def visit(self, node : ActionDEL):
        self.visit(node.collection_items)
        current_type = node.collection_items.processed_type
        if current_type != "business" and not ("collection" in current_type):
            raise Exception("The type of the first ID has to be business or collection")
        
        try:
            self.visit(node.item)
            if current_type == "business":
                if not("product" in node.item.processed_type):
                    raise Exception(f"Can not delete {node.item.processed_type} from {current_type}")
            else:
                if not (node.item.processed_type in current_type):
                    raise Exception(f"Can not delete {node.item.processed_type} from {current_type}")
        except:
            pass
        node.processed_type = "actionDel"

    @when(ActionDISMISS)
    def visit(self, node : ActionDISMISS):
        self.visit(node.business)
        if node.business.processed_type != "business":
            raise Exception(f"Can not make action dismiss from {node.business.processed_type}")
        try:
            self.visit(node.employed)
            if not("employed" in node.employed.processed_type):
                raise Exception(f"Can not dismiss {node.employed.processed_type}")
        except:
            pass
        node.processed_type = "actionDismiss"
    

    

    @when(IfStatement)
    def visit(self, node : IfStatement):#TODO: this
        pass

    @when(Bool_Expression_Node)
    def visit(self, node : Bool_Expression_Node):
        self.visit(node.left)
        self.visit(node.right)
        type_id_1 = node.left.processed_type
        type_id_2 = node.right.processed_type
        
        if type_id_1 == "business":
            raise Exception(f"Can not compare type Business")

        if type_id_1 != type_id_2:
            raise Exception(f"Type of {node.id_1} is not equal to the type of {node.id_2}")
        
        node.processed_type = "bool_expression"
    
    @when(InStatement)
    def visit(self, node : InStatement):
        self.visit(node.id_1)
        self.visit(node.id_2)
        type_id_1 = node.id_1.processed_type
        type_id_2 = node.id_2.processed_type

        if type_id_2 != "business" and not("collection" in type_id_2):
            raise Exception("The type of the second item has to be collection or business")
        
        node.processed_type = "bool_expression"
    
    @when(NotStatement)
    def visit(self, node : NotStatement):
        self.visit(node.stam)
        current_type = node.stam.processed_type
        if current_type != "bool_expression":
            raise Exception("Only can make a not syntax to a bool_expression")
        node.processed_type = "bool_expression"


    @when(ForeachStatement)
    def visit(self, node : ForeachStatement):
        pass

    @when(Metrics)
    def visit(self, node : Metrics):
        self.visit(node.business)
        if node.business.processed_type != "business":
            raise Exception("Can only calculate metrics to a business")
        
        self.visit(node.date)
        if node.date > self.today:
            raise Exception("You can only calculate metrics from an old date")
        
        node.processed_type =  "metrics"
    


