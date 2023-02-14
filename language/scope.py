from __future__ import annotations

class Scope:
    def __init__(self, parent : Scope = None):
        self.parent  = parent
        self.locals = {}
        self.var_count = 0

    def new_child(self) -> Scope:
        return Scope(self)

    def set(self, name : str, value):
        self.locals[name] = value

    def find(self, name : str):
        if name in self.locals:
            return self.locals[name]
        if self.parent:
            return self.parent.find(name)
        return None