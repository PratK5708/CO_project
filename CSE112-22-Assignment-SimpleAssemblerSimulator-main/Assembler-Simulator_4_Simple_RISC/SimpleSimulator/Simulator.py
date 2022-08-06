from ExecutionEngine import ExecutionEngine
from Memory import Memory
from ProgramCounter import ProgramCounter
from Register import Register
from Plot import plot
import sys, time

data = []
for line in sys.stdin:
    data.append(line)

Mem = Memory(data)
PCs = ProgramCounter()
Reg = Register()
plts = plot([],[], 0)
EEs = ExecutionEngine(Mem, Reg, PCs, plts)

while not(EEs.halted):
    EEs.execute(Mem.load(PCs.value))
    print(PCs.dump()+" "+Reg.dump())
    plts.appendx(plts.cycle)
    plts.appendy(PCs.value)
    if EEs.updatePC:
        PCs.stdUpdate()
    else:
        PCs.update(str(bin(PCs.temp)).replace("0b", ""))
    plts.updatecycle()
Mem.dump()
plts.plotting()