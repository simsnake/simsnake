

class Block():
    """The base block class. Defines inputs and outputs
    """
    def ___init__(self) -> None:
        self.inputs = {}
        self.outputs = {}
    
    def forward(self, n=1):
        """Forward n steps of simulation. Update outputs from given inputs. 
        """
        return False

    def check_connection(self):
        """Checks that all outputs and inputs are connected
        """
        for inp, v in self.inputs.items():
            if v is None:
                print(f"WARNING: input {inp} not connected")
        for out, v in self.outputs.items():
            if v is None:
                print(f"WARNING: output {out} not connected")


class SourceBlock(Block):
    """Block with no input
    """
    def __init__(self) -> None:
        super().__init__()


class SinkBlock(Block):
    """Block with no outputs
    """
    def __init__(self) -> None:
        super().__init__()


class Delay(Block):
    """Block that holds a value until the next simulation step
    """
    def __init__(self, delay) -> None:
        super().__init__()
        # Create buffer (queue) of size delay
        self.delay_buffer = [0]*delay
        # Single output and input
        self.inputs = {"input" : None}
        self.outputs = {"output": None}

    def set_buffer(self, buffer):
        """Initialize to non-zero values
        """
        self.delay_buffer = buffer

    def forward(self, n=1):
        for i in range(n):
            self.delay_buffer.append(self.inputs["input"].value)
            self.outputs["output"].value = self.delay_buffer.pop(0)
        super().forward()

