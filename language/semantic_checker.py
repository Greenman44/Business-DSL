import visitor
from .types import Bus_Types
from .ast_nodes import *
from .scope import Scope

class SemanticChecker:
    def __init__(self, scope : Scope):
        self.scope = scope
    
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, node : Program):
        for inst in node.instructions:
            self.visit(inst)
    
    @visitor.when(TypeDeclaration)
    def visit(self, node : TypeDeclaration):
        try:
            current_type = Bus_Types.find(node.type)
        except:
            raise TypeError("Undefined type")
        var = self.scope.find(node.id)
        if var != None:
            raise Exception("You can not declare two variables with the same name")
        try:
            instance = current_type(*node.value)    
        except:
            raise TypeError("Bad Type declaration")
        self.scope.set(node.id, instance)
    
    @visitor.when(VariableAssignment)
    def visit(self, node : VariableAssignment):
        self.visit(node.value)
        processed_type = node.processed_type
        var_type = self.scope.find(node.id)
        if var_type is None:
            raise Exception(f"Variable '{node.name}' is not defined")
        if var_type != processed_type:
            raise Exception(f" Impossible assign value {node.value} to variable '{node.name}'. Type '{var_type}' different to '{processed_type}'")
        node.processed_type = var_type

    @visitor.when(VariableCall)
    def visit(self, node : VariableCall):
        var_type = self.scope.find(node.id)
        if var_type is None:
            raise Exception(f"Variable '{node.id}' is not defined")
        node.processed_type = var_type
        
    


