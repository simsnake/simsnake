

class Variable():
    def __init__(self, name) -> None:
        self._value = 0
        self.name = ""
        self.unit = ""

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, sval):
        self._value = sval
    
