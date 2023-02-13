from __future__ import annotations

class Scope:
    def __init__(self, parent : Scope = None):
        self.parent  = parent
        self.symbols = {}
        self.var_count = 0

    def new_child(self) -> Scope:
        return Scope(self)

    def set(self, name : str, value):
        self.symbols[name] = value

    def find(self, name : str):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.Find(name)
        return None