# Valerie Lemuth (117017) & Johanna Sacher (117353)
""" Abgabe für die Aufgaben 1 und 4a) """

def mult_inv(_x, z_n):
    '''
    Multiplikatives Inverses von x in Zn bestimmen
    '''
    if ggt(_x, z_n) == 1:
        for i in range(0, z_n +1):
            if ((i * _x) % z_n) == 1:
                #print(i)
                return i
    else:
        print("Es existiert kein multiplikatives Inverses zu %s in Z_%s." %(_x, z_n))
        return -1


def order(_g, _p):
    '''Ordnung von Generator g aus Zp (für das neutrale Element e=1)'''

    for i in range(1, _p):
        if ((_g**i)%_p) == 1:
            return i


def ggt(_a, _b):
    '''GGT von a und b'''

    _r = _a%_b
    if _r == 0:
        return _b
    return ggt(_b, _r)


def average_ordnung(_ge, _p):
    '''
    average order of elements is the sum of orders of the groups elements \n
    divided by the order of the group                                     \n
    av_ord(g^ab) = sum(ord(g))/|G|                                        \n
    g = Generator von Z_n                                                 \n
    n = Primzahl p                                                        \n
    e = neutrales Element                                                 \n
    a,b = zufällige Elemente aus Z_n                                      \n
    (takes some time! About 20-25 minutes?)
    '''
    add = 0

    for _a in range(1, _p):
        for _b in range(1, _p):
            ordnung = order(_ge, _p)/ggt(order(_ge, _p), _a*_b)
            add += ordnung
            #print("Ordnung für ", ge, "^", a*b, ": ", ordnung)
    print("\n\n\n Durchschnittliche Ordnung für ", _ge, " aus Z", _p, ":", add/((_p-1)*(_p-1)))

def main():
    '''main function docstring'''
    #average_ordnung(13,883)       #193.18313357088869 
    #average_ordnung(13,863)       #536.2586939669791
    return 0

if __name__ == '__main__':
    main()
