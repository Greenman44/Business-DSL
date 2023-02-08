from abc import ABCMeta, abstractmethod
class Node(metaclass = ABCMeta):
    
    @abstractmethod
    def __init__(self):
        pass

class InstList(Node):
    def __init__(self, instructions):
        self.instructions = instructions

