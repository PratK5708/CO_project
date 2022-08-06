import matplotlib.pyplot as plt

class plot:
    def __init__(self,x,y, cycle):
        self.x = x
        self.y = y
        self.cycle = cycle
    def updatecycle(self):
        self.cycle += 1    
    def appendx(self,val):
        self.x.append(val)
    def appendy(self,val):
        self.y.append(val)
    def plotting(self):
        plt.scatter(self.x,self.y)
        plt.title("Mem Add / cycle number")
        plt.xlabel("Cycles")
        plt.ylabel("Memory address")
        plt.savefig("graph.png", dpi = 200, bbox_inches  = "tight")


