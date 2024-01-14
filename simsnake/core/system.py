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
        layers = self.build_execution_order()
        print(self.execution_order)
        finished = False
        while not finished:
            for i in range(layers+1):
                for block, l in self.execution_order.items():
                    if l == i:
                        if not block.forward() is None:
                            finished = True

    def build_execution_order(self):
        self.execution_order = dict(zip(self.blocks, [0]*len(self.blocks)))
        max_layers = 0
        solved = False
        while solved == False:
            solved = True
            for c in self.connections:
                b = c.input_block
                # c.output_block is a dependency of b
                if not isinstance(b, Delay) and not isinstance(b, SourceBlock):
                    if self.execution_order[c.output_block] > self.execution_order[b]:
                        self.execution_order[b] = self.execution_order[c.output_block]+1
                        if max_layers < self.execution_order[b]:
                            max_layers = self.execution_order[b]
                        solved = False
        self.execution_order
        return max_layers

