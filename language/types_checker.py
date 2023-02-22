
        
class Type:
    def __init__(self, name:str):
        self.name = name
        self.attr = {}
    
    def set_attr(self, name, value):
        self.attr[name] = value
    
    def get_attr(self, name):
        try:
            return self.attr[name]
        except KeyError:
            raise AttributeError("Attribute not found: %s" % name)    
class Instance:
    def __init__(self, type , value) -> None:
        self.type = type
        self.value = value


class Bus_Context:
    def __init__(self):
        self._types = {}
        self._create_busTypes()

    def _create_busTypes(self):
        self._types["business"] = Type("business")
        self._types["collection"] = Type("collection")
        self._types["employed"] = Type("employed")
        self._types["product"] = Type("product")
        self._types["num"] = Type("num")
        


    def find_type(self, name:str):
        try:
            return self._types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')
        


