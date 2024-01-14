from simsnake.core import System, Connect, Delay
from simsnake.blocks import *

pid = System()

time = LinStep(0, 1000, 0.001)
setpoint_src = Constant(10)
invert_reading = Gain(-1)
subtract_err = Add()
integrate_err = IntegralApprox()
diff_err = DerivativeApprox()
sum_corr = Sum()
feedback = Delay(1)
sink = Print()
feedback_gain = Gain(0.1)
feedback_add = IntegralApprox()

p_term = Gain(0.5) # kP
i_term = Gain(0.1) # kI
d_term = Gain(0.3) # kD

pid.add(time, setpoint_src, invert_reading, subtract_err, integrate_err, diff_err, sum_corr, feedback)
pid.add(p_term, i_term, d_term)
pid.add(sink, feedback_gain, feedback_add)
pid.add(Connect(invert_reading, "output", subtract_err, "addend1"))
pid.add(Connect(setpoint_src, "output", subtract_err, "addend2"))
pid.add(Connect(subtract_err, "output", p_term, "input"))
pid.add(Connect(subtract_err, "output", integrate_err, "value"))
pid.add(Connect(time, "output", integrate_err, "time"))
pid.add(Connect(integrate_err, "integral", i_term, "input"))
pid.add(Connect(subtract_err, "output", diff_err, "value"))
pid.add(Connect(time, "output", diff_err, "time"))
pid.add(Connect(diff_err, "derivative", d_term, "input"))
pid.add(Connect(p_term, "output", sum_corr, "input1"))
pid.add(Connect(i_term, "output", sum_corr, "input2"))
pid.add(Connect(d_term, "output", sum_corr, "input3"))
pid.add(Connect(sum_corr, "output", feedback, "input"))
pid.add(Connect(feedback, "output", feedback_gain, "input"))
pid.add(Connect(feedback_gain, "output", feedback_add, "value"))
pid.add(Connect(time, "output", feedback_add, "time"))
pid.add(Connect(feedback_add, "integral", invert_reading, "input"))
pid.add(Connect(subtract_err, "output", sink, "input"))
pid.run()