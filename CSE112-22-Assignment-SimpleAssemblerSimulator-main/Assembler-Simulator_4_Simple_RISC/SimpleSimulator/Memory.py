class Memory:
    def __init__(self,data):
        self.data = list("0000000000000000" for i in range(256))
        for i in range(len(data)):
            self.data[i]=data[i]

    def load(self,i):
        return(self.data[i])

    def store(self,i,value):
        self.data[i]=str(bin(value)).replace("0b","0").rjust(16,"0")

    def dump(self):
        print("\n".join(self.data))

if __name__=="__main__":
    Mem = Memory(["0","1","2"])
    Mem.dump()