def printErr(data):
    print("\033[91m"+data+"\033[0m")

## Error B
def errorB(instruc,vars,labels,i):
    if instruc[2] in labels.keys():
        printErr("Misuse of labels as variables. Error in line:"+str(i))
    
    elif instruc[2] not in vars.keys():
        printErr("Use of undefined variable name.Error in line:"+str(i))
        return True
    else:
        return False

## Error C
# Valid only for typeE
def errorC(instruc,vars,labels,i):
    if instruc[1] in vars.keys():
        printErr("Misuse of variables as labels. Error in line:"+str(i))
    
    elif instruc[1] not in labels.keys():
        printErr("Use of undefined labels. Error in line:"+str(i))
        return True
    else:
        return False

## Error G and H and I
def errorGHI(data):
    err = False  # True if error exists
    other = 0    # counts all instructions except var and ""
    hlt_cnt = 0  # counts hlt instructions
    
    if data[len(data)-1].find("hlt") == -1 :
        printErr("hlt not being used as the last instruction")
        err = True
        return err


    for x in data:
        # checking for more than 1 hlt
        if x.count("  ") > 0:
            printErr("Invalid syntax")
            return True
        elif x.count("hlt") > 1:
            printErr("more than 1 hlt used")
            return True
        elif x.find("hlt") != -1:
            hlt_cnt += 1
            other += 1
            if hlt_cnt > 1 :
                printErr("more than 1 hlt used")
                err = True
                return err
        # skipping for empty lines
        elif x == "":
            continue

        # checking for if var are declared in the start
        elif other > 0:
            if x[0:3] == "var":
                printErr("Variables not declared at the beginning")
                err = True
                return err
            else:
                other += 1
        elif x[0:3] == "var":
            continue
        else:
            other += 1
    
    return err

# checks if variable and label names are valid or not
def check_var_lab(x):
    Types=["add","sub","mul","xor","or","and", "rs","ls", "div","not","cmp", "ld","st", "jmp","jlt","jgt","je", "var"]
    if x == "":
        return True
    if x in Types:
        return True
    for i in x:
        if i.isalpha() or i.isnumeric() or i == "_":
            continue
        else:
            return True
    return False