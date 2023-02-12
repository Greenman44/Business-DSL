
        
class Type:
    def __init__(self, name:str):
        self.name = name

    
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
        


    def find_type(self, name:str):
        try:
            return self._types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')
        


