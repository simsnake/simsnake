import math
import torch
from core import Block, SourceBlock, SinkBlock


class Abs(Block):
    """Calculates absolute value of input
    Inputs:
        input (:obj:`Tensor`) : input tensor
    Outputs:
        output (:obj:`Tensor`) : torch.abs(input)
    """
    def __init__(self) -> None:
        super().__init__()
        self.inputs = {"input" : None}
        self.outputs = {"output" : None}

    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = torch.abs(self.inputs["input"].value)


class Add(Block):
    """Calculates sum of two inputs
    Inputs:
        addend1 (:obj:`Tensor`) : first addend
        addend2 (:obj:`Tensor`) : second addend
    Outputs:
        output (:obj:`Tensor`) : torch.add(addend1, addend2)
    """
    def __init__(self) -> None:
        super().__init__()
        self.inputs = {"addend1" : None, "addend2" : None}
        self.outputs = {"output" : None}

    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = torch.add(self.inputs["addend1"].value, self.inputs["addend2"].value)


class Bias(Block):
    """Add bias, or offset to input
    Inputs:
        input (:obj:`Tensor`) : input tensor
    Outputs:
        output (:obj:`Tensor`) : torch.add(input, offset)
    """
    def __init__(self, offset) -> None:
        super().__init__()
        self.gain = offset
        self.inputs = {"input" : None}
        self.outputs = {"output" : None}
    
    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = torch.add(self.inputs["input"].value, self.offset)


class Gain(Block):
    """Multiply input by a constant
    Inputs:
        input (:obj:`Tensor`) : input tensor
    Outputs:
        output (:obj:`Tensor`) : torch.mul(input, gain)
    """
    def __init__(self, gain) -> None:
        super().__init__()
        self.gain = gain
        self.inputs = {"input" : None}
        self.outputs = {"output" : None}
    
    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = torch.mul(self.inputs["input"].value, self.gain)


class RunningSum(Block):
    """Adds input to total (outputs priori output + input)
    Inputs:
        input (:obj:`Tensor`) : input tensor
    Outputs:
        output (:obj:`Tensor`) : torch.add(output, input)
    """
    def __init__(self) -> None:
        super().__init__()
        self.inputs = {"input" : None}
        self.outputs = {"output" : None}

    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = torch.add(self.inputs["output"].value, self.inputs["input"].value)


class Constant(SourceBlock):
    """Outputs a constant
    Inputs:
    Outputs:
        output (:obj:`Tensor`) : constant
    """
    def __init__(self, constant) -> None:
        super().__init__()
        self.constant = constant
        self.outputs = {"output" : None}

    def forward(self, n=1):
        self.outputs["output"].value = self.constant


class IntegralApprox(Block):
    """Trapezoidal integral approximation
    """
    def __init__(self) -> None:
        super().__init__()
        self.priori_input = None
        self.priori_time = None
        self.inputs = {"value" : None, "time" : None}
        self.outputs = {"integral" : None}

    def forward(self, n=1):
        for i in range(n):
            if self.priori_input is None:
                self.outputs["integral"].value = 0
            else:
                dt = self.inputs["time"].value - self.priori_time
                self.outputs["integral"].value = torch.mul(dt/2, torch.add(self.inputs["value"].value, self.priori_input))
                self.priori_input = self.inputs["value"].value
                self.priori_time = self.inputs["time"].value


class DerivativeApprox(Block):
    """Derivative approximation
    """
    def __init__(self) -> None:
        super().__init__()
        self.priori_input = None
        self.priori_time = None
        self.inputs = {"value" : None, "time" : None}
        self.outputs = {"derivative" : None}

    def forward(self, n=1):
        for i in range(n):
            if self.priori_input is None:
                self.outputs["derivative"].value = 0
            else:
                dt = self.inputs["time"].value - self.priori_time
                self.outputs["derivative"].value = torch.div(torch.sub(self.inputs["value"].value, self.priori_input), dt)
                self.priori_input = self.inputs["value"].value
                self.priori_time = self.inputs["time"].value


class LinStep(SourceBlock):
    pass


class Sum(Block):
    """Calculates sum of any number of inputs
    """
    def __init__(self) -> None:
        super().__init__()
        self.inputs = {}
        self.outputs = {"output" : None}

    def add_input(self, var):
        self.inputs[str(len(self.inputs))] = var

    def forward(self, n=1):
        for i in range(n):
            self.outputs["output"].value = 0
            for k, v in self.inputs.items():
                self.outputs["output"].value = torch.add(self.outputs["output"].value, v.value)

