import Memory, Register, ProgramCounter, Plot

class ExecutionEngine:
    def __init__(self, Mem, Reg, PC, plts):
        self.halted = False
        self.Mem = Mem
        self.Reg = Reg
        self.PC = PC
        self.plts = plts
        self.updatePC = True

    def execute(self, instruction):
        opcode = instruction[:5]
        if opcode=="10000":
            self.add(instruction)
        elif opcode=="10001":
            self.sub(instruction)
        elif opcode=="10010":
            self.movImm(instruction)
        elif opcode=="10011":
            self.movReg(instruction)
        elif opcode=="10100":
            self.load(instruction)
        elif opcode=="10101":
            self.store(instruction)
        elif opcode=="10110":
            self.mul(instruction)
        elif opcode=="10111":
            self.div(instruction)
        elif opcode=="11000":
            self.rs(instruction)
        elif opcode=="11001":
            self.ls(instruction)
        elif opcode=="11010":
            self.xor(instruction)
        elif opcode=="11011":
            self.bor(instruction)
        elif opcode=="11100":
            self.band(instruction)
        elif opcode=="11101":
            self.bnot(instruction)
        elif opcode=="11110":
            self.cmp(instruction)
        elif opcode=="11111":
            self.jmp(instruction)
        elif opcode=="01100":
            self.jlt(instruction)
        elif opcode=="01101":
            self.jgt(instruction)
        elif opcode=="01111":
            self.je(instruction)
        elif opcode=="01010":
            self.halted=True
            self.Reg.reset()
            self.updatePC = True


   
    def add(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)+self.Reg.read(reg3)
        if (value>65535):
            self.Reg.overflow()
            value = int(str(bin(value)).replace("0b","")[-16:], 2)
        else:
            self.Reg.reset()
        self.Reg.store(reg1,value)
        self.updatePC = True

    ## Function for subtract
    def sub(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)-self.Reg.read(reg3)
        if value<0:
            value=0
            self.Reg.overflow()
        else:
            self.Reg.reset()
        self.Reg.store(reg1,value)
        self.updatePC = True

    def movImm(self,instruction):
        reg1 = int(instruction[5:8],2)
        imm = int(instruction[8:16],2)
        self.Reg.store(reg1,imm)
        self.Reg.reset()
        self.updatePC = True

    def movReg(self,instruction):
        reg1 = int(instruction[10:13],2)
        reg2 = int(instruction[13:16],2)
        self.Reg.store(reg1,self.Reg.read(reg2))
        self.Reg.reset()
        self.updatePC = True

    def load(self,instruction):
        reg1 = int(instruction[5:8],2)
        imm = int(instruction[8:16],2)
        self.plts.appendx(self.plts.cycle)
        self.plts.appendy(imm)
        self.Reg.store(reg1,int(self.Mem.load(imm),2))
        self.Reg.reset()
        self.updatePC = True


    def store(self,instruction):
        reg1 = int(instruction[5:8],2)
        imm = int(instruction[8:16],2)
        self.plts.appendx(self.plts.cycle)
        self.plts.appendy(imm)
        self.Mem.store(imm,self.Reg.read(reg1))
        self.Reg.reset()
        self.updatePC = True


    def mul(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)*self.Reg.read(reg3)
        if (value>65535):
            self.Reg.overflow()
            value = int(str(bin(value)).replace("0b","")[-16:], 2)
        else:
            self.Reg.reset()
        self.Reg.store(reg1,value)
        self.updatePC = True

    def div(self,instruction):
        reg1 = int(instruction[10:13],2)
        reg2 = int(instruction[13:16],2)
        self.Reg.store(0,self.Reg.read(reg1)//self.Reg.read(reg2))
        self.Reg.store(1,self.Reg.read(reg1)%self.Reg.read(reg2))
        self.Reg.reset()
        self.updatePC = True

    def rs(self,instruction):
        reg1 = int(instruction[5:8],2)
        imm = int(instruction[8:16],2)
        value = self.Reg.read(reg1)>>imm
        self.Reg.store(reg1,value)
        self.Reg.reset()
        self.updatePC = True

    def ls(self,instruction):
        reg1 = int(instruction[5:8],2)
        imm = int(instruction[8:16],2)
        value = self.Reg.read(reg1)<<imm
        self.Reg.store(reg1,value)
        self.Reg.reset()
        self.updatePC = True

    def xor(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)^self.Reg.read(reg3)
        self.Reg.store(reg1,value)
        self.Reg.reset()
        self.updatePC = True

    def bor(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)|self.Reg.read(reg3)
        self.Reg.store(reg1,value)
        self.updatePC = True

    def band(self,instruction):
        reg1 = int(instruction[7:10],2)
        reg2 = int(instruction[10:13],2)
        reg3 = int(instruction[13:16],2)
        value = self.Reg.read(reg2)&self.Reg.read(reg3)
        self.Reg.store(reg1,value)
        self.Reg.reset()
        self.updatePC = True

    def bnot(self,instruction):
        reg1 = int(instruction[10:13],2)
        reg2 = int(instruction[13:16],2)
        self.Reg.store(reg1,~self.Reg.read(reg2))
        self.updatePC = True

    def cmp(self,instruction):
        val1 = self.Reg.read(int(instruction[10:13],2))
        val2 = self.Reg.read(int(instruction[13:16],2))
        if val1<val2:
            self.Reg.lessThan()
        elif val1>val2:
            self.Reg.greaterThan()
        else:
            self.Reg.equal()
        self.updatePC = True

    def jmp(self,instruction):
        addr = instruction[8:16]
        self.PC.updatetemp(addr)
        self.Reg.reset()
        self.updatePC = False

    def jlt(self,instruction):
        addr = instruction[8:16]
        if self.Reg.Flags[13]=="1":
            self.PC.updatetemp(addr)
            self.updatePC = False

        else:
            self.updatePC = True
        self.Reg.reset()

    def jgt(self,instruction):
        addr = instruction[8:16]
        if self.Reg.Flags[14]=="1":
            self.PC.updatetemp(addr)
            self.updatePC = False
        else:
            self.updatePC = True
        self.Reg.reset()

    def je(self,instruction):
        addr = instruction[8:16]
        if self.Reg.Flags[15]=="1":
            self.PC.updatetemp(addr)
            self.updatePC = False
        else:
            self.updatePC = True
        self.Reg.reset()


if __name__=="__main__":
    Mem = Memory.Memory([])
    Reg = Register.Register()
    PCs = ProgramCounter.ProgramCounter()
    EEs = ExecutionEngine(Mem,Reg)