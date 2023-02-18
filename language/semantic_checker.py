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
        if not float.is_integer(node.amount):
            raise Exception("The amount must be an integer")
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

    @when(GetStaff_node)
    def visit(self, node: GetStaff_node):
        self.visit(node.business)
        if node.business.processed_type != "business":
            raise Exception("Only can get staff from a business")
        node.processed_type = "collection_employed"

    @when(GetCatalog_node)
    def visit(self, node: GetCatalog_node):
        self.visit(node.business)
        if node.business.processed_type != "business":
            raise Exception("Only can get catalog from a business")
        node.processed_type = "collection_product"


    @when(GetElementFrom_Statement)
    def visit(self, node : GetElementFrom_Statement):
        self.visit(node.collection)
        current_type = node.processed_type
        if current_type == "business":
            node.processed_type = "employed_product"
        elif "collection" in node.collection.processed_type:  
            coll_type = node.collection.processed_type.split("_")[1]
            node.processed_type = coll_type
        else:
            raise Exception("Only can make get action from a collection or a business")

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
    

    @when(Load)
    def visit(self, node : Load):
        node.processed_type = "business"
    
    @when(Save)
    def visit(self, node : Save):
        self.visit(node.business)
        current_type = node.business.processed_type
        if current_type != "business":
            raise Exception("Only can make Save over a business")
        
        node.processed_type = "save"

    @when(Foreach_node)
    def visit(self, node : Foreach_node):
        self.visit(node.collection)
        if "collection" not in node.collection.processed_type:
            raise Exception("Only can make Foreach over a collection")
        var = self.scope.find(node.loop_var)
        if var != None:
            raise Exception("You can not declare two variables with the same name")
        coll_type = node.collection.processed_type.split("_")[1]
        foreach_scope = self.scope.new_child()
        foreach_scope.set(node.loop_var, coll_type)
        foreach_sem_check = SemanticChecker(foreach_scope)
        for instruction in node.body:
            foreach_sem_check.visit(instruction)
        node.processed_type = "foreach"

    @when(While_node)
    def visit(self, node : While_node):
        self.visit(node.condition)
        if node.condition.processed_type != "bool_expression":
            raise Exception("While expression needs a conditional expression")
        while_scope = self.scope.new_child()
        while_sem_check = SemanticChecker(while_scope)
        for instruction in node.body:
            while_sem_check.visit(instruction)
        node.processed_type = "while"

    @when(Oper_Node)
    def visit(self, node: Oper_Node):
        self.visit(node.left)
        self.visit(node.right)
        type_id_1 = node.left.processed_type
        type_id_2 = node.right.processed_type

        if type_id_1 != type_id_2:
            raise Exception("The type of each of the variables must be the same")
        
        if type_id_1 != "num":
            raise Exception(f"Can not make operations in variable with type {type_id_1}")

        node.processed_type = "num"
    

    @when(IfStatement)
    def visit(self, node : IfStatement):
        self.visit(node.condition)
        type_node_cond = node.condition.processed_type
        if type_node_cond != "bool_expression":
            raise Exception("The condition has to be a bool expression")
        
        if_scope = Scope.new_child(self.scope)
        if_sem_che = SemanticChecker(if_scope)
        for item in node.body:
            if_sem_che.visit(item)
        node.processed_type = "ifStatement"

    @when(ElseStatement)
    def visit(self, node : ElseStatement):
        self.visit(node.if_statement)
        if node.if_statement.processed_type != "ifStatement":
            raise Exception("Else statement needs to be after If statement")
        else_scope = Scope.new_child(self.scope)
        else_sem_check = SemanticChecker(else_scope)
        for instruction in node.body:
            else_sem_check.visit(instruction)
        node.processed_type = "elseStatement"


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
    


