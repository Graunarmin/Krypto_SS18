from math import gcd

def mult_inv(x, Z_n):
    '''
    Multiplikatives Inverses von x in Zn bestimmen
    '''
    if gcd(x, Z_n) == 1:
        for i in range (0, Z_n +1):
            if ((i * x) % Z_n) == 1:
                #print(i)
                return i
    else:
        print("Es existiert kein multiplikatives Inverses zu %s in Z_%s." %(x, Z_n))
        return(-1)