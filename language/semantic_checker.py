import visitor
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
    
    

