from .ast_nodes import *
from .scope import Scope
from business_data import Business, Collection, Employed, Product, Business_Data, Number, Function
from .types_checker import  Instance
from .visitor import on, when
from datetime import date, timedelta

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
        try:
            new_value = new_value.value
        except:
            pass
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
        if coll_node.collection is not None:
            for item in coll_node.collection:
                collection.append(self.visit(item).value)
        return Collection(collection)

    @when(Emp_Node)
    def visit(self, emp_node : Emp_Node):
        var_salary = self.visit(emp_node.number)
        try:
            var_salary = var_salary.value
        except:
            pass
        
        return Employed(emp_node.name, var_salary)
    
    @when(Prod_Node)
    def visit(self, prod_node : Prod_Node):
        var_amount = self.visit(prod_node.amount)
        try:
            var_amount = var_amount.value
        except:
            pass
        return Product(prod_node.name, amount=var_amount)

    @when(Bill_Node)
    def visit(self, bill_node : Bill_Node):
        var_bus : Business = self.visit(bill_node.business).value
        var_cost : Number = self.visit(bill_node.cost)
        try:
            var_cost = var_cost.value
        except:
            pass
        var_bus.add_Bill(var_cost, bill_node.description)
    
    @when(Number_Node)
    def visit(self, number_node : Number_Node):
        return Number(number_node.number)


    @when(ActionSALE)
    def visit(self, sale_node : ActionSALE):
        var_bus : Business = self.visit(sale_node.business).value
        var_prod : Product = self.visit(sale_node.product).value
        var_price : Number =  self.visit(sale_node.sale_price)
        var_amount : Number = self.visit(sale_node.amount)
        try:
            var_price = var_price.value
            var_amount = var_amount.value
        except:
            pass
        if not float.is_integer(var_amount.number):
            raise Exception("Amount must be an integer")
        #TODO: add this method to Business_Data 
        var_bus.make_sale(var_prod.name, var_price, var_amount)
    
    @when(ActionINVESTS)
    def visit(self, inv_node : ActionINVESTS):
        var_bus : Business = self.visit(inv_node.business).value
        var_prod : Product = self.visit(inv_node.product).value
        var_price : Number =  self.visit(inv_node.sale_price)
        var_amount : Number = self.visit(inv_node.amount)
        
        try:
            var_price = var_price.value
            var_amount = var_amount.value
        except:
            pass
        if not float.is_integer(var_amount.number):
            raise Exception("Amount must be an integer")
        var_amount += var_prod.amount
        var_bus.make_invest(var_prod.name, var_price, var_amount)
    
    @when(ActionADD)
    def visit(self, add_node : ActionADD):
        var_coll = self.visit(add_node.collection_items).value
        var_item = self.visit(add_node.item)
        try:
            var_item = var_item.value
        except:
            pass
        var_coll.add(var_item)
    
    @when(ActionDEL)
    def visit(self, del_node : ActionDEL):
        var_coll = self.visit(del_node.collection_items).value
        var_item = None
        if isinstance(del_node.item, str):
            var_item = del_node.item
        else:            
            var_item = self.visit(del_node.item)
            try:
                var_item = var_item.value
            except:
                pass
        var_coll.delete(var_item)
    
    @when(ActionDISMISS)
    def visit(self, dis_node : ActionDISMISS):
        var_bus : Business = self.visit(dis_node.business).value
        var_item = None
        if isinstance(dis_node.employed, str):
            var_item = dis_node.employed
        else:            
            var_item = self.visit(dis_node.employed)
            try:
                var_item = var_item.value
            except:
                pass
        var_bus.dismiss(var_item)
    
    @when(Oper_Node)
    def visit(self, op_node : Oper_Node):
        var_left = self.visit(op_node.left)
        var_right = self.visit(op_node.right)
        try:
            var_left = var_left.value
            var_right = var_right.value
        except:
            pass
        

        operators = {
                "+" : var_left.__add__,
                "-" : var_left.__sub__,
                "/" : var_left.__truediv__,
                "*" : var_left.__mul__,
        }
        return operators[op_node.oper](var_right)

    @when(Load)
    def visit(self, load_node : Load):
        

        return Business_Data.LoadBusiness(load_node.name)

    
    @when(Save)
    def visit(self, save_node : Save):
        var_bus : Business = self.visit(save_node.business).value

        # TODO: add this method to Business_Data
        var_bus.save()

    @when(Print_Node)
    def visit(self, print_node : Print_Node):
        var_id = self.visit(print_node.id_1).value

        print(var_id)

    @when(Date_node)
    def visit(self, date_node : Date_node):
        valid_dates = {
            "today" : date.today(),
            "last_week" : date.today() - timedelta(days=7),
            "last_month" : date.today() - timedelta(days=30),
            "last_year" : date.today() + timedelta(days=365)
        }
        try:
            return valid_dates[date_node.date]
        except:
            return date_node.date
            
    @when(Funct_Call_Node)
    def visit(self, call_node : Funct_Call_Node):
        func : Function = self.scope.find(call_node.id)
        func_scope = self.scope.new_child()
        for i in range(len(func.parameters)):
            param = self.visit(call_node.params[i])
            try:
                param = param.value
            except:
                pass
            func_scope.set(func.parameters[i].id, param)
        func_eval = Evaluator(func_scope)
        for inst in func.body:
            var_return = func_eval.visit(inst)
            if isinstance(inst, Return_Node):
                return var_return
        

    
    
    @when(Function_Node)
    def visit(self, function_node : Function_Node):
        self.scope.set(function_node.id, Function(parameters=function_node.params, body=function_node.body))

        

    @when(Metrics)
    def visit(self, metrics : Metrics):
        var_bus : Business = self.visit(metrics.business).value
        var_date : date = self.visit(metrics.date)

        return var_bus.calculate_metrics(metrics.metric , var_date)

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
    
    @when(GetAmount_node)
    def visit(self, getAmount : GetAmount_node):
        var_product : Product = self.visit(getAmount.product).value
        return var_product.get_amount()
    
    @when(Foreach_node)
    def visit(self, foreach : Foreach_node):
        coll : Collection = self.visit(foreach.collection).value
        type_coll = coll.get_type()
        for item in coll:
            foreach_scope = self.scope.new_child()
            foreach_scope.set(foreach.loop_var, Instance(type_coll, item))
            foreach_eval = Evaluator(foreach_scope)
            for instruction in foreach.body:
                foreach_eval.visit(instruction)
    
    @when(While_node)
    def visit(self, while_node: While_node):
        while self.visit(while_node.condition):
            while_scope = self.scope.new_child()
            while_eval = Evaluator(while_scope)
            for instruction in while_node.body:
                while_eval.visit(instruction)

        

    @when(IfStatement)
    def visit(self, if_statement: IfStatement):
        var_condition = self.visit(if_statement.condition)
        
        if var_condition:
            if_scope = self.scope.new_child()
            if_eva = Evaluator(if_scope)
            for node in if_statement.body:
                if_eva.visit(node)
        return var_condition

    @when(ElseStatement)
    def visit(self, else_statement: ElseStatement):
        var_if = self.visit(else_statement.if_statement)
        if not var_if:
            else_scope = self.scope.new_child()
            else_eval = Evaluator(else_scope)
            for node in else_statement.body:
                else_eval.visit(node)
        return not var_if   

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


    