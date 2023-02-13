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
    


