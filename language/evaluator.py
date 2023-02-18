from .ast_nodes import *
from .scope import Scope
from business_data import Business, Collection, Employed, Product, Business_Data
from .types_checker import  Instance
from .visitor import on, when


class Evaluator:
    def __init__(self, scope : Scope):
        self.scope = scope
    
    @on("node")
    def visit(self, node):
        pass

    @when(Program)
    def visit(self, program_node : Program):
        for inst in program_node.instructions:
            self.visit(inst)

    @when(VariableDeclaration)
    def visit(self, varDeclaration_node : VariableDeclaration):
        self.scope.set(varDeclaration_node.id, Instance(varDeclaration_node.type,None))

    @when(TypeDeclaration)
    def visit(self, typeDec_node : TypeDeclaration):
        self.scope.set(typeDec_node.id, Instance(typeDec_node.type, self.visit(typeDec_node.value)))

    @when(VariableAssignment)
    def visit(self, varAssign_node : VariableAssignment):
        var : Instance = self.scope.find(varAssign_node.id)
        new_value = self.visit(varAssign_node.value) 
        var.value = new_value
    
    @when(Oper_Assign)
    def visit(self, opAssign_node : Oper_Assign):
        var : Instance = self.scope.find(opAssign_node.id_oper)
        new_value = self.visit(opAssign_node.value)
        # TODO: Is necesary not change the all value, only the value of salary or amount
    
    @when(VariableCall)
    def visit(self, varCall_node : VariableCall):
        return self.scope.find(varCall_node.id)

    @when(Bus_Node)
    def visit(self, bus_node : Bus_Node):
        staff = self.visit(bus_node.staff_collection).value
        catalog = self.visit(bus_node.catalog_collection).value
        return Business(bus_node.name, staff, catalog)
    
    @when(Collection_Node)
    def visit(self, coll_node : Collection_Node):
        collection = []
        for item in coll_node.collection:
            collection.append(self.visit(item).value)
        return Collection(collection)

    @when(Emp_Node)
    def visit(self, emp_node : Emp_Node):
        return Employed(emp_node.name, emp_node.number)
    
    @when(Prod_Node)
    def visit(self, prod_node : Prod_Node):
        return Product(prod_node.name)

    @when(Bill_Node)
    def visit(self, bill_node : Bill_Node):
        var_bus : Business = self.visit(bill_node.business).value
        var_bus.add_bill(bill_node.cost, bill_node.description)
    
    @when(ActionSALE)
    def visit(self, sale_node : ActionSALE):
        var_bus : Business = self.visit(sale_node.business).value
        var_prod : Product = self.visit(sale_node.product).value
        #TODO: add this method to Business_Data 
        var_bus.make_sale(var_bus.name, var_prod.name, sale_node.sale_price, sale_node.amount)
    
    @when(ActionINVESTS)
    def visit(self, inv_node : ActionINVESTS):
        var_bus : Business = self.visit(inv_node.business).value
        var_prod : Product = self.visit(inv_node.product).value
        if not var_bus.any_product(var_prod):
            var_bus.add(var_prod)
        var_bus.make_invest(var_bus.name, var_prod.name, inv_node.cost_price, inv_node.amount)
    
    @when(ActionADD)
    def visit(self, add_node : ActionADD):
        var_coll = self.visit(add_node.collection_items)
        var_item = self.visit(add_node.item)
        var_coll.add(var_item)
    
    @when(ActionDEL)
    def visit(self, del_node : ActionDEL):
        var_coll = self.visit(del_node.collection_items).value
        var_item = self.visit(del_node.item).value
        var_coll.delete(var_item)
    
    @when(ActionDISMISS)
    def visit(self, dis_node : ActionDISMISS):
        var_bus : Business = self.visit(dis_node.business).value
        var_emp = self.visit(dis_node.employed).value
        var_bus.dismiss(var_emp)
    
    @when(Oper_Node)
    def visit(self, op_node : Oper_Node):
        var_left = self.visit(op_node.left).value
        var_right = self.visit(op_node.right).value
        operators = {
                "+" : var_left + var_right,
                "-" : var_left - var_right,
                "/" : var_left / var_right,
                "*" : var_left * var_right,
        }
        return operators[op_node.oper](var_right)

    @when(Load)
    def visit(self, load_node : Load):
        var_bus = self.visit(load_node.business)

        var_bus.value = Business_Data.LoadBusiness(load_node.name)

    
    @when(Save)
    def visit(self, save_node : Save):
        var_bus : Business = self.visit(save_node.business).value

        # TODO: add this method to Business_Data
        var_bus.save()

    @when(Metrics)
    def visit(self, metrics : Metrics):
        var_bus : Business = self.visit(metrics.business).value

        var_bus.calculate_metrics(metrics.metric , metrics.date)

    @when(GetElementFrom_Statement)
    def visit(self, getElement : GetElementFrom_Statement):
        var_bus : Business|Collection = self.visit(getElement.collection)
        return var_bus.get(getElement.name)
    
    @when(GetCatalog_node)
    def visit(self, getCatalog : GetCatalog_node):
        var_bus : Business = self.visit(getCatalog.business)
        return var_bus.get_catalogue()
    
    @when(GetStaff_node)
    def visit(self, getStaff : GetStaff_node):
        var_bus : Business = self.visit(getStaff.business)
        return var_bus.get_staff()
    
    @when(Foreach_node)
    def visit(self, foreach : Foreach_node):
        coll : Collection = self.visit(foreach.collection)
        

    @when(IfStatement)
    def visit(self, if_statement: IfStatement):
        var_condition = self.visit(if_statement.condition)
        
        if var_condition:
            if_scope = self.scope.new_child(self.scope)
            if_eva = Evaluator(if_scope)
            for node in if_statement.body:
                if_eva.visit(node)
        return var_condition
            

    @when(NotStatement)
    def visit(self, not_statement: NotStatement):
        var = self.visit(not_statement.stam)

        return not var

    @when(InStatement)
    def visit(self, in_statement: InStatement):
        var_id1 = self.visit(in_statement.id_1).value
        var_id2 = self.visit(in_statement.id_2).value

        return var_id1 in var_id2

    @when(Bool_Expression_Node)
    def visit(self, comparer : Bool_Expression_Node):
        var_left = self.visit(comparer.left)
        var_right = self.visit(comparer.right)
        try:
            operators = {
                "<" : var_left.value < var_right.value,
                ">" : var_left.value > var_right.value,
                "<=" : var_left.value <= var_right.value,
                ">=" : var_left.value >= var_right.value,
                "==" : var_left.value == var_right.value,
            }
            return operators[comparer.comparer]
        except AttributeError:
            if comparer.comparer == "and":
                return var_left and var_right
            else:
                return var_left or var_right


    