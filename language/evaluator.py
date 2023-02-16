from .ast_nodes import *
from .scope import Scope
from business_data import Business, Collection, Employed, Product
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
        #TODO:  add this method to Business_Data
        var_bus.data.add_bill(var_bus.name, bill_node.cost)
    
    @when(ActionSALE)
    def visit(self, sale_node : ActionSALE):
        var_bus : Business = self.visit(sale_node.business).value
        var_prod : Product = self.visit(sale_node.product).value
        #TODO: add this method to Business_Data 
        var_bus.data.make_sale(var_bus.name, var_prod.name, sale_node.sale_price, sale_node.amount)
    
    @when(ActionINVESTS)
    def visit(self, inv_node : ActionINVESTS):
        var_bus : Business = self.visit(inv_node.business).value
        var_prod : Product = self.visit(inv_node.product).value
        if not var_bus.any_product(var_prod):
            var_bus.add(var_prod)
        var_bus.data.make_invest(var_bus.name, var_prod.name, inv_node.cost_price, inv_node.amount)
    
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
    
    @when(Metrics)
    def visit(self, metrics : Metrics):
        var_bus : Business = self.visit(metrics.business).value

        #TODO: add this method to Business_Data
        var_bus.calculate_metrics(var_bus.name, metrics.metric , metrics.date)
    
    @when(IfStatement)
    def visit(self, if_statement: IfStatement):
        pass

    @when(NotStatement)
    def visit(self, not_statement: NotStatement):
        var_id1 = self.visit(not_statement.stam.id_1).value
        var_id2 = self.visit(not_statement.stam.id_2).value

        return var_id1 not in var_id2

    @when(InStatement)
    def visit(self, in_statement: InStatement):
        var_id1 = self.visit(in_statement.id_1).value
        var_id2 = self.visit(in_statement.id_2).value

        return var_id1 in var_id2

    @when(Comparer)
    def visit(self, comparer : Comparer):
        var_id1 = self.visit(comparer.id_1).value
        var_id2 = self.visit(comparer.id_2).value
        #TODO: Make a method to do this

    