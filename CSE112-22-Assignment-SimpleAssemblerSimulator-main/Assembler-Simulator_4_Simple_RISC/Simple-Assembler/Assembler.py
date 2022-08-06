#############
## Imports ##
#############
import sys
import Errors


###################
## Main Function ##
###################
def main():
    ## List to store all given instructions
    data=[]
    ## List to store all binaries generated
    binaries=[]
    ## Dictionary to store locations of all labels
    labels={}
    ## Dictionary to store locations of all variables
    vars={}
    varCount=0
    ## Variable to store instruction number
    instNum=0
    ## Variable to check for no error
    isError=False
    ## Taking inputs
    for line in sys.stdin:
        data.append(line.lstrip())
    ## just for custom inputs
    """
    n=int(input())
    for i in range(n):
        data.append(input()) """
    ## Checking for few errors on overall code
    isError=Errors.errorGHI(data)
    if isError:
        return
    ## Traversing to check for errors and collecting data
    if not(isError):
        ## Working on each instruction
        for i in range(0,len(data)):
            ## Checking for empty lines
            if data[i].lstrip()=="":
                continue
            ## Spliting instruction into parts
            instruction=data[i].split()
            ## Checking for variable declaration
            if instruction[0]=="var":
                
                ## checking if instruction follows syntax
                if len(instruction) != 2 :
                    isError = True
                ## Checking if variable is valid or not
                else:
                    isError = Errors.check_var_lab(instruction[1])
                
                if not(isError):
                    vars[instruction[1]]=varCount
                    varCount+=1
                else:
                    printErr(f"Variable name not supported in line {i}")
                    return
                continue
            ## Checking for label
            if instruction[0][-1]==":":
                if len(instruction) < 2:
                    printErr(f"Label name not supported in line {i}")
                    return 
                instType=instructionType(instruction[1:])
                ## Checking if label name is valid 
                isError = Errors.check_var_lab(instruction[0][:-1])
                if not(isError):
                    labels[instruction[0][:-1]]=instNum
                else:
                    printErr(f"Label name not supported in line {i}")
                    return
            else:
                instType=instructionType(instruction)
                instruction=data[i]
            ## Checking if instuction type matches or not
            isError=not(instType in ["A","B","C","D","E","F"])
            if isError:
                printErr(f"Invalid Instruction: Instruction '{instruction}', in line {i} is not supported by the ISA")
                return 
            ## Incrementing instruction number
            instNum+=1
    ## Updating Variables dictionary so that variables are in the end
    for var in vars:
        vars[var]=vars[var]+instNum
    ## Traversing to generate binary
    if not(isError):
        ## Working on each instruction
        for i in range(0,len(data)):
            ## Spliting instruction into parts
            instruction=data[i].split()
            ## Checking for empty lines
            if data[i].lstrip()=="":
                continue
            ## Checking for variable declaration
            if instruction[0]=="var":
                continue
            ## Checking for label
            if instruction[0][-1]==":":
                instType=instructionType(instruction[1:])
                instruc=" ".join(instruction[1:])
                instruction = instruction[1:]
            else:
                instType=instructionType(instruction)
                instruc=data[i]
            ## Retrieving binary for instuction as per their type
            if instType=="Z":
                printErr(f"Typos in instruction name at line {i}")
                return 
            elif instType=="A":
                binary=typeA(instruc,i)
            elif instType=="B":
                binary=typeB(instruc,i)
            elif instType=="C":
                binary= TypeC(instruction,i)
            elif instType=="D":
                binary= TypeD(vars, instruction,labels,i)
            elif instType=="E":
                binary=typeE(instruc,vars,labels,i)
            elif instType=="F":
                binary="0101000000000000"
            ## Checking for syntax error
            if binary==None:
                printErr(f"Invalid syntax for line {i}")
                return
            elif binary==False:
                return
            ## Storing binary
            binaries.append(binary)
    ## Checking if there is no error in program
    if not(isError):
        print("\n".join(binaries))
    #print(vars,labels)



###################################################
## Function To Determine The Type Of Instruction ##
###################################################
def instructionType(instruction):
    TypeA=["add","sub","mul","xor","or","and"]
    TypeB=["rs","ls"]
    TypeC=["div","not","cmp"]
    TypeD=["ld","st"]
    TypeE=["jmp","jlt","jgt","je"]
    ## Checking for move instructions
    if instruction[0]=="mov":
        if len(instruction) < 2:
            return ("Z")
        ## Checking for move intermediate
        if instruction[2][0]=="$":
            return("B")
        ## Checking for move register
        else:
            return("C")
    ## Checking for hlt instruction
    elif instruction[0]=="hlt":
        return("F")
    ## Checking for type A instructions
    elif instruction[0] in TypeA:
        return("A")
    ## Checking for type B instructions
    elif instruction[0] in TypeB:
        return("B")
    ## Checking for type C instructions
    elif instruction[0] in TypeC:
        return("C")
    ## Checking for type D instructions
    elif instruction[0] in TypeD:
        return("D")
    ## Checking for type E instructions
    elif instruction[0] in TypeE:
        return("E")
    ## Returning error value
    else:
        return("Z")


######################################
## Function For Type E Instructions ##
######################################
def typeE(instruction, vars, labels,i):
    instruction=instruction.split()
    try:
        if (Errors.errorC(instruction, vars,labels,i)):
            return(False)
        ## Working for JMP instruction
        if instruction[0]=="jmp":
            return("11111000"+str(bin(labels[instruction[1]])).replace("0b","").rjust(8,"0"))
        ## Working for JLT instruction
        elif instruction[0]=="jlt":
            return("01100000"+str(bin(labels[instruction[1]])).replace("0b","").rjust(8,"0"))
        ## Working for JGT instruction
        elif instruction[0]=="jgt":
            return("01101000"+str(bin(labels[instruction[1]])).replace("0b","").rjust(8,"0"))
        ## Working for JE instruction
        elif instruction[0]=="je":
            return("01111000"+str(bin(labels[instruction[1]])).replace("0b","").rjust(8,"0"))
    except:
        return(None)

opc = {"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
opd = {"ld": "10100","st":"10101"}
regadd = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
unused5 = "00000"

def regbit(i,n,r1,r2=0,):
    if n == 1:
        if r1 not in regadd.keys():
            printErr(f"Typos in register name at line {i}")
            return None
        return regadd.get(r1)
    else:
        if (r1 not in regadd.keys()) or (r2 not in regadd.keys()) :
            printErr(f"Typos in register name at line {i}")
            return None
        return regadd.get(r1)+ regadd.get(r2)
def memadd(n):
        a=n
        q=1
        s=""
        while q !=0:
            q=a//2
            r=a%2
            a=q
            s+=str(r)
        final = "".join(reversed(s))
        return final

######################################
## Function For Type C Instructions ##
######################################
def TypeC(lst,i):
    if lst[1] == "FLAGS":
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    elif lst[1] == "FLAGS":
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    elif lst[0] != 'mov' and lst[2] == 'FLAGS':
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    try:
        if regbit(i,2,lst[1],lst[2]) == None:
            return False
        return opc.get(lst[0])+ unused5 + regbit(i,2,lst[1],lst[2])
    except:
        return(None)

######################################
## Function For Type D Instructions ##
######################################
def TypeD(instNum,lst, labels, i):
    if lst[1] == "FLAGS":
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    try:
        if (Errors.errorB(lst,instNum,labels,i)):
            return False
        
        if regbit(i,1,lst[1]) == None:
            return False
        return opd.get(lst[0]) + regbit(i,1,lst[1]) + str(bin(instNum[lst[2]])).replace("0b","").rjust(8,"0")
    except:
        return(None)


######################################
## Function For Type A Instructions ##
######################################
def typeA(instruction,i):
    
    binval = ''                    # final val
    inst_arr = instruction.split() # array with instructions space seperated
    
    # dictionary with op code vals for each type A instruction
    opcode = {
                'add' : '10000',
                'sub' : '10001',
                'mul' : '10110',
                'xor' : '11010',
                'or'  : '11011',
                'and' : '11100'
                
    }

    # dictionary with register bin vals
    regs = {
                'R0': '000' ,
                'R1': '001' ,
                'R2': '010' ,
                'R3': '011' ,
                'R4': '100' ,
                'R5': '101' ,
                'R6': '110' ,
                'FLAGS': '111' ,
    }
    # ERRORS ----------------------------------------------------------------------------------------------
    
    if inst_arr[0] not in opcode.keys():
        printErr(f"Typos in instruction name at line {i}")
        return False
    
    elif (inst_arr[1] not in regs.keys()) or (inst_arr[2] not in regs.keys()) or (inst_arr[3] not in regs.keys()):
        printErr(f"Typos in register name at line {i}")
        return False

    if inst_arr[1] == 'FLAGS' or inst_arr[2] == 'FLAGS' or inst_arr[3] == 'FLAGS' :
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    #------------------------------------------------------------------------------------------------------
    
    try:# checking for wrong syntax used
        # creating the binary value if no error pops up 
        binval = binval + opcode[inst_arr[0]] + '00' + regs[inst_arr[1]] + regs[inst_arr[2]] + regs[inst_arr[3]]
        return binval
    except:
        printErr(f"Wrong syntax used for instructions at line {i}")
        return False

######################################
## Function For Type B Instructions ##
######################################
def typeB(instruction,i):
    binval = ''                            # final val
    inst_arr = instruction.split()         # array with instructions space seperated
    
    # dictionary with op code vals for each type A instruction
    opcode = {
        'mov' : '10010',
        'rs'  : '11000',
        'ls'  : '11001'
    }
    # dictionary with register bin vals
    regs = {
                'R0': '000' ,
                'R1': '001' ,
                'R2': '010' ,
                'R3': '011' ,
                'R4': '100' ,
                'R5': '101' ,
                'R6': '110' ,
                'FLAGS': '111' ,
    }

    # ERRORS ----------------------------------------------------------------------------------------------
    if inst_arr[0] not in opcode.keys():
        printErr(f"Typos in instruction name at line {i}")
        return False

    elif inst_arr[1] == 'FLAGS':
        printErr(f"Illegal use of FLAGS register at line {i}")
        return False
    
    elif inst_arr[1] not in regs.keys():
        printErr(f"Typos in register name at line {i}")
        return False

    elif int(inst_arr[2][1:]) > 255  or int(inst_arr[2][1:]) < 0 :
        printErr(f"Illegal Immediate values (less than 0 or more than 255) at line {i}")
        return False
    #------------------------------------------------------------------------------------------------------
    
    try:# checking for wrong syntax used
        # creating the binary value if no error pops up    
        binval = binval + opcode[inst_arr[0]] + regs[inst_arr[1]] + bin(int(inst_arr[2][1:])).replace("0b","").rjust(8, "0")
        return binval
    except:
        printErr(f"Wrong syntax used for instructions at line {i}")
        return False

def printErr(data):
    print("\033[91m"+data+"\033[0m")


main()