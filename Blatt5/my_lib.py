# Valerie Lemuth (117017) & Johanna Sacher (117353)

def mult_inv(_x, Z_n):
    '''
    Multiplikatives Inverses von x in Zn bestimmen
    '''
    if ggT(_x, Z_n) == 1:
        for i in range (0, Z_n +1):
            if ((i * x) % Z_n) == 1:
                #print(i)
                return i
    else:
        print("Es existiert kein multiplikatives Inverses zu %s in Z_%s." %(x, Z_n))
        return(-1)


def ord(g,p):
    '''Ordnung von Generator g aus Zp (für das neutrale Element e=1)'''

    for i in range(1,p):
        if ((g**i)%p)== 1:
            return i


def ggT(a, b):
    '''GGT von a und b'''

    r = a%b
    if r == 0:
        return b
    else:
        return ggT(b,r)


def averageOrdnung(ge,p):
    '''
    average order of elements is the sum of orders of the groups elements divided by the order of the group \n
    av_ord(g^ab) = sum(ord(g))/|G|                                                                          \n
    g = Generator von Z_n                                                                                   \n
    n = Primzahl p                                                                                          \n
    e = neutrales Element                                                                                   \n
    a,b = zufällige Elemente aus Z_n                                                                        \n
    (takes some time! About 20-25 minutes?)
    '''
    add = 0

    for a in range(1,p):
        for b in range(1,p):
            ordnung = ord(ge,p)/ggT(ord(ge,p),a*b)
            add += ordnung
            #print("Ordnung für ", ge, "^", a*b, ": ", ordnung)
    print ("\n\n\n Durchschnittliche Ordnung für ", ge, " aus Z", p, ":", add/((p-1)*(p-1)))



# averageOrdnung(13,883)      # 193.18313357088869

# averageOrdnung(13,863)      # 536.2586939669791