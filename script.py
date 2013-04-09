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
    for (i, coeff) in enumerate(c) :
        if not coeff == 0.0 and not i == 0:
            if coeff > 0.0 :
                z += "+"
            if coeff != 1.0 :
                z += " %s" % coeff
            else :
                    z += "-"
            z += xOrw(x,i) 
    print z

    # print constraints 
    for (j, constraint) in enumerate(A) :
        r = xOrw(x,b[j])
        r += "= %s " % constraint[0]
        for (i, element) in enumerate(constraint) :
            if not element == 0.0 : 
                if i > 0 :
                    if element >= 0.0 :
                        r += "+"
                    r += "%s" % element 
                    r += xOrw(x,i)
        print r 

def calculateMainConstraint(a,pivotIndex,baseVariable) :
    # Calculating the optimal constraint
    pivotValue = a[pivotIndex]
    for (i, element) in enumerate(a): 
        if i == baseVariable: 
            a[i] = 1.0/pivotValue
        else :
            if i == pivotIndex : 
                a[i] = 0.0
            else :
                a[i] = element/-pivotValue
    return pivotIndex

def calculateConstraints(mainCon, pivotIndex, fragIndex, A, c) :
    # Calculating the rest of the constraints
    for (i, constraint) in enumerate(A):
        if i == fragIndex:
            continue 
       
        pivotValue = constraint[pivotIndex]
        for (j, element) in enumerate(constraint) :
            if j is pivotIndex : 
                A[i][j] = 0.0
            else :
                A[i][j] = element + pivotValue * mainCon[j]
    
    pivotValue = c[pivotIndex]
    for (j, element) in enumerate(c) :
        if j is pivotIndex : 
            c[j] = 0.0
        else :
            c[j] = element + pivotValue * mainCon[j]


def findLowersFrag(pivotIndex,A,b,x):

    # Finds lowest constraint fragment
    bestFrag = None
    for (i, constraint) in enumerate(A):
        if constraint[pivotIndex] == 0.0:
            continue
        curFrag =  constraint[pivotIndex] /constraint[0] 
        if not bestFrag or curFrag < bestFrag:
            bestFrag = curFrag
            fragIndex = i

    s = xOrw(x,b[fragIndex])
    print "Used constraint %s (%s leaves)" % (s,s)

    return fragIndex

def pivot(A, b, c, x) :
   
    while 1 : 
        # Finding pivot element
        # print A
        pivot = -1
        pivotIndex = 0
        for (i, coefficient) in enumerate(c) :
            if not i == 0 :
                if coefficient > pivot:
                    pivot = coefficient
                    pivotIndex = i 
        
        if pivot <= 0:
            break # break as optimal point found

        s = xOrw(x,pivotIndex)
        print "Used pivot element %s (%s enters)" % (s,s)

        fragIndex = findLowersFrag(pivotIndex,A,b,x)
        
        b[fragIndex] = calculateMainConstraint(A[fragIndex],pivotIndex,b[fragIndex])

        calculateConstraints(A[fragIndex], pivotIndex, fragIndex, A, c)
        
        printModel(A,b,c,x)

    return (A, b, c, x)


def simplexMethod(A, b, c, x) :
    
    # Adding slack values
    c.insert(0,0.0)
    for (i, constraint) in enumerate(A) :
        for (j, element) in enumerate(constraint) :
            A[i][j] = element * -1
        constraint.insert(0,b[i])
        b[i] = len(constraint)
        c.append(0.0)
        
        for restraint in A :
            restraint.append(0.0)
        print "Added slack element w%d" % (i + 1)
    print b
    printModel(A,b,c,x)
    (A,b,c,x) = pivot(A,b,c,x)

def main():
    
    c = [2.0,3.0,1.0]
    b = [1.0,-2.0,1.0]
    A = [[1.0,1.0,1.0],
         [1.0,-2.0,1.0],
         [0.0,1.0,1.0]]
    x = len(c)    
    simplexMethod(A, b, c, x)

if __name__ == "__main__":
   main()
