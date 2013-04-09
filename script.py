#!/usr/bin/python

    # xOrw prints w if variableNumber is a slackvariable, otherwise it prints x
    # x is the number of variables given 
def xOrw(x,variableNumber) :
    if variableNumber <= x :
       return "x%d " % (variableNumber)
    else :
       return "w%d " % (variableNumber - x)


def printModel(A,b,c,x) :
    # print objective function
    z = "z = "
    if c[0] != 0.0 :
        z += "%s " % c[0]
    i = 0
    for coeff in c :
        if not coeff == 0.0 and not i == 0:
            if coeff > 0.0 :
                z += "+"
            if coeff != 1.0 :
                z += " %s" % coeff
            else :
                    z += "-"
            z += xOrw(x,i) 
        i += 1
    print z

    # print constraints 
    j = 0 
    for constraint in A :
        i = 0
        r = xOrw(x,b[j])
        r += "= %s " % constraint[0]
        for element in constraint :
            if not element == 0.0 : 
                if i > 0 :
                    if element >= 0.0 :
                        r += "+"
                    r += "%s" % element 
                    r += xOrw(x,i)
            i += 1
        j += 1
        print r 


def removeRedundant(A,b,c,x) :
    # removes redundant restraints from A
    for constraint in A :
       pass 

    
    return (A,b,c,x)

def calculateMainConstraint(a,pivotIndex,baseVariable) :
    # Calculating the optimal constraint
    i = 0
    pivotValue = a[pivotIndex]
    for element in a: 
        if i == baseVariable: 
            a[i] = 1.0/pivotValue
        else :
            if i == pivotIndex : 
                a[i] = 0.0
            else :
                a[i] = element/-pivotValue
        i += 1
    return pivotIndex

def calculateConstraints(mainCon, pivotIndex, fragIndex, A, c) :
    # Calculating the rest of the constraints
    i = 0
    for constraint in A:
        if i == fragIndex:
            i += 1
            continue 
       
        pivotValue = constraint[pivotIndex]
        j = 0
        for element in constraint :
            if j is pivotIndex : 
                A[i][j] = 0.0
            else :
                A[i][j] = element + pivotValue * mainCon[j]
            j = j + 1
        i = i + 1
    
    j = 0
    pivotValue = c[pivotIndex]
    for element in c :
        if j is pivotIndex : 
            c[j] = 0.0
        else :
            c[j] = element + pivotValue * mainCon[j]
        j = j + 1

def pivot(A, b, c, x) :
   
    while 1 : 
        # Finding pivot element
        # print A
        pivot = -1
        pivotIndex = 0
        i = 0
        for coefficient in c :
            if not i == 0 :
                if coefficient > pivot:
                    pivot = coefficient
                    pivotIndex = i 
            i = i + 1
        
        if pivot <= 0 :
            break # break as optimal point found

        s = xOrw(x,pivotIndex)
        print "Used pivot element %s (%s enters)" % (s,s)

        # pivotIndex = pivotIndex + 1 # offsets the constant and variable/constraint

        # Finds lowest constraint fragment

        bestFrag = None
        i = 0
        for constraint in A :
            if constraint[pivotIndex] == 0.0 :
                i += 1
                continue
            curFrag =  constraint[pivotIndex] /constraint[0] 
            if not bestFrag or curFrag < bestFrag :
                bestFrag = curFrag
                fragIndex = i
            i += 1

        s = xOrw(x,b[fragIndex])
        print "Used constraint %s (%s leaves)" % (s,s)

        b[fragIndex] = calculateMainConstraint(A[fragIndex],pivotIndex,b[fragIndex])

        calculateConstraints(A[fragIndex], pivotIndex, fragIndex, A, c)
        
        printModel(A,b,c,x)
    return (A, b, c, x)


def simplexMethod(A, b, c, x) :
    
    # Adding slack values
    i = 0
    c.insert(0,0.0)
    for constraint in A :
        j = 0
        for element in constraint :
            A[i][j] = element * -1
            j = j + 1
        constraint.insert(0,b[i])
        b[i] = len(constraint)
        c.append(0.0)
        
        for restraint in A :
            restraint.append(0.0)
        print "Added slack element w%d" % (i + 1)
        i = i + 1
    printModel(A,b,c,x)
    (A,b,c,x) = pivot(A,b,c,x)

def inputvector() : 
    (l, i) = ([], 1)
    while 1:
        input = raw_input("%s value: " % i)
        if not input.isdigit():
            if input is "n" :
                break
            print "%s is not a digit" % input 
            continue
        l.append(input)
        i = i + 1 
    return l

def main():
    
    # creates vector c
    # print "c values: paste \"n\" when done"
    # c = inputvector()
    # print c

    # creates vector b
    # print "b values: paste \"n\" when done"
    # b = inputvector()

    # creates matrix A
    # print "A values: paste \"n\" when done"
    # i = 1
    # A = [[]]
    # length = None
    # while 1 :
        # print "%s constraint, paste 0 if no use of resource" % i
        # a = inputvector()

        # check constraint length
        # if length is None :
            # length = len(a)
        # if not length == len(a) :
            # print "length of constraint does not match previous"
            # continue

        # appends constraint and asks for more
        # A.append(a) 
        # print "More constraints? \"n\" if no" 
        # input = raw_input("More constraints? \"n\" if no: " % i)
        # if input is "n" :
            # break

        # pass    
    # print A

    c = [0.0,0.0,1.0]
    b = [-1.0,-2.0,1.0]
    A = [[-1.0,1.0,-1.0],
         [-1.0,-2.0,-1.0],
         [0.0,1.0,-1.0]]
    x = len(c)    
    # zip(*A)
    simplexMethod(A, b, c, x)


if __name__ == "__main__":
   main()
