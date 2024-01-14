from simsnake.core import System, Connect, Delay
from simsnake.blocks import *

test = System()

time = LinStep(0, 1000, 1)
delay = Delay(1)
sink = Print()

test.add(time, sink, delay)
# time -> delay -> sink
test.add(Connect(time, "output", delay, "input"))
test.add(Connect(delay, "output", sink, "input"))

test.run()
