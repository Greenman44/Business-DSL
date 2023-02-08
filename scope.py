from typing import Any, Dict, Optional
from __future__ import annotations

class Scope:
    def __init__(self, parent: Scope = None):
        self.parent : Scope = parent
        self.symbols : Dict[str, Any] ={}
        self.var_count : int = 0

    def newNode(self) ->Scope:
        return Scope(self)

    def setNew(self, name : str, value :Any):
        self.symbols[name] = value

    def Find(self, name : str) -> Optional[Any]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent
            return self.parent.Find(name)
        return None