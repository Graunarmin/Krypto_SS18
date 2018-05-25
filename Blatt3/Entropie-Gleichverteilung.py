import math

def summe():
    m = 0

    for n in range (0,16):
        m += math.log2(95-n)

    print(m)

summe()
    
   