'''
Sammlung von nützlichen Funktionen; einfach in der Python shell "import ds_lib" eingeben und Funktionen benutzen :)
'''

def ggT(s,e):
    '''
    ggT von s und e mit dem euklidschen Algorithmus bestimmen
    '''
    tmp = 0
    if s < e:
        tmp = e
        e = s
        s = tmp

    while True:
        r = s % e
        if r == 0:
            break
        s = e
        e = r
    #print (e)
    return e


def mult_inv(x, Z_n):
    '''
    Multiplikatives Inverses von x in Zn bestimmen
    '''
    if ggT(x, Z_n) == 1:
        for i in range (0, Z_n +1):
            if ((i * x) % Z_n) == 1:
                #print(i)
                return i
    else:
        return(-1)


def ordnung(a, p, e):
    '''
    Ordnung des Elements a in Z_p mit neutralem Element e \n
    ord(a) = {min(n € N | a**n = e), falls existent, sonst unendlich}
    '''
    for n in range(1, p):
        if ((a ** n) % p) == e :
            #print(n)
            return n
    
    print("infinitive")
    return(-1)




def generator(n):
    '''
    Generatoren der Gruppe Z_n bestimmen - 
    wenn in mod n {a, a^2, a^3, ..., a^n} = Z_n, dann ist a Generator von Z_n
    '''

    Z_n = [i for i in range(1,n)]
    A = []
    generators = []

    for a in range(0, n):
        for z in Z_n:
            x = (a**z) % n
            if not A or x not in A:
                A.append(x)
        A.sort()
        
        if A == Z_n:
            generators.append(a)
        A = []
    
    if generators:
        print("Z_%s ist zyklisch und hat folgende(n) Generator(en):")
        # print(generators)
    return generators

def order_of_gi(g, i, p, e):
    '''
    Ordnung von g^i in Z_p mit neutralem Element e
    ord(g^i) = (ord(g))/ ggT((ord(g)), i)
    '''

    ord_g = ordnung(g, p, e)
    ord_gi = ord_g / ggT(ord_g, i)

    return ord_gi




def aver_ord(g, n, e):
    '''
    average order of elements is the sum of orders of the groups elements divided by the order of the group \n
    av_ord(g^ab) = sum(ord(g))/|G|                                                                          \n
    g = Generator von Z_n                                                                                   \n
    n = Primzahl p                                                                                          \n
    e = neutrales Element                                                                                   \n
    a,b = zufällige Elemente aus Z_n
    '''
    sum_ = 0
    counter = 0

    for a in range (1, n):
        counter += 1
        for b in range(1, n):
            counter +=1
            sum_ += order_of_gi(g, (a*b), n, e)
            #print(sum_)
    print("Counter:") 
    print(counter)
    
    average_order = sum_ / ((n-1)*(n-1))
    return average_order
        