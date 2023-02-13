from abc import ABCMeta, abstractmethod


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
        

