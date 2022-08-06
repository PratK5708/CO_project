class ProgramCounter:
    def __init__(self):
        self.value = 0
        self.temp  = 0
    def dump(self):
        return(str(bin(self.value)).replace("0b","").rjust(8,"0"))
    def update(self,value):
        self.value = int(value,2)
    def updatetemp(self, value ):
        self.temp = int(value,2)    
    def stdUpdate(self):
        self.value = self.value+1

if __name__=="__main__":
    PC = ProgramCounter()
    print(PC.dump())
    PC.update("01010")
    print(PC.dump())
    PC.stdUpdate()
    print(PC.dump())
