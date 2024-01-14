from simsnake.core import Block, SinkBlock, SourceBlock, Delay, Variable

class Connect():
    def __init__(self, output_block, output, input_block, input, variable=None) -> None:
        if variable is None:
            variable = Variable(f"{output}->{input}")
        output_block.outputs[output] = variable
        input_block.inputs[input] = variable
        self.output_block = output_block
        self.input_block = input_block


class System():
    
    def __init__(self) -> None:
        self.blocks = []
        self.connections = []
        self.execution_order = []

    def add(self, *args):
        """Add blocks and connections to a system
        """
        for t in args:
            if isinstance(t, Block):
                self.blocks.append(t)
            elif isinstance(t, Connect):
                self.connections.append(t)
    
    def run(self):
        pass

    def build_execution_order(self):
        self.execution_order = [0]*len(self.blocks)
        for i, b in enumerate(self.blocks):
            if isinstance(b, SourceBlock) or isinstance(b, Delay):
                self.execution_order[i] = 0
            else:
                b.inputs = 
                self.execution_order
