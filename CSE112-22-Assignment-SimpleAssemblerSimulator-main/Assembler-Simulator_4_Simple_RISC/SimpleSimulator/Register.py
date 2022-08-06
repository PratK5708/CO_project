class Register:
    
    def __init__(self):
        self.R0 = "0000000000000000"
        self.R1 = "0000000000000000"
        self.R2 = "0000000000000000"
        self.R3 = "0000000000000000"
        self.R4 = "0000000000000000"
        self.R5 = "0000000000000000"
        self.R6 = "0000000000000000"
        self.Flags="0000000000000000"

    def read(self,i):
        if i==0:
            return(int(self.R0,2))
        elif i==1:
            return(int(self.R1,2))
        elif i==2:
            return(int(self.R2,2))
        elif i==3:
            return(int(self.R3,2))
        elif i==4:
            return(int(self.R4,2))
        elif i==5:
            return(int(self.R5,2))
        elif i==6:
            return(int(self.R6,2))
        elif i==7:
            return(int(self.Flags,2))

    def store(self,i,value):
        if i==0:
            self.R0 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==1:
            self.R1 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==2:
            self.R2 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==3:
            self.R3 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==4:
            self.R4 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==5:
            self.R5 = str(bin(value)).replace("0b","").rjust(16,"0")
        elif i==6:
            self.R6 = str(bin(value)).replace("0b","").rjust(16,"0")

    def reset(self):
        self.Flags = "0000000000000000"
    def overflow(self):
        self.Flags = "0000000000001000"
    
    def lessThan(self):
        self.Flags = "0000000000000100"
    
    def greaterThan(self):
        self.Flags = "0000000000000010"
    
    def equal(self):
        self.Flags = "0000000000000001"

    def dump(self):
        return(self.R0+" "+self.R1+" "+self.R2+" "+self.R3+" "+self.R4+" "+self.R5+" "+self.R6+" "+self.Flags)