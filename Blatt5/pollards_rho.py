# Valerie Lemuth (117017) & Johanna Sacher (117353)
'''
Berechnen des diskreten Logaritmus von y zur Basis g in Z_p, d.h. es gilt y = g^x (mod p)
(Variablenbenennung pylintkonform ist ein bisschen unübersichtlich, sorry dafür
)
Terminal: python3 pollards_rho.py p g y
    e.g.: python3 pollards_rho.py 1019 2 5
          python3 pollards_rho.py 1018 2 5

with help from https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm_for_logarithms
and http://cacr.uwaterloo.ca/hac/about/chap3.pdf and https://gist.github.com/brunoro/5894145
'''
import sys
import my_lib

X_DICT = {0:1}
A_DICT = {0:0}
B_DICT = {0:0}

def get_xab(i, _g, _y, _p):
    '''get x_i, a_i and b_i'''

    if i not in X_DICT:
        x_i, a_i, b_i = get_xab(i-1, _g, _y, _p)
        X_DICT[i], A_DICT[i], B_DICT[i] = comp_xab(x_i, a_i, b_i, _g, _y, _p)

    return X_DICT[i], A_DICT[i], B_DICT[i]

def comp_xab(_x, _a, _b, _g, _y, _p):
    '''compute x_i, a_i and b_i by dividing Z_p into 3 subsets of about the same size'''

    _n = _p - 1
    _c = _x % 3

    if _c == 0:
        _x = pow(_x, 2, _p)
        _a = (2 * _a) % _n
        _b = (2 * _b) % _n

    elif _c == 1:
        _x = (_g * _x) % _p
        _a = (_a + 1) % _n
        _b = _b

    elif _c == 2:
        _x = (_y * _x) % _p
        _a = _a
        _b = (_b + 1) % _n

    return _x, _a, _b

def pollards_rho(_p, _g, _y):
    '''compute discrete logarithm of g to the base of y in the cyclic group Z_p with order n'''

    _n = _p - 1

    #print("i\tx_i\ta_i\tb_i\tx_2i\ta_2i\tb_2i")
    for i in range(1, _p):
        x_i, a_i, b_i = get_xab(i, _g, _y, _p) #Schildkröte
        x_2i, a_2i, b_2i = get_xab(2*i, _g, _y, _p) #Hase

        #print ("%d\t%d\t%d\t%d\t%d\t%d\t%d" % (i, x_i, a_i, b_i, x_2i, a_2i, b_2i))
        if x_i == x_2i:
            _r = (b_2i - b_i) % _n

            if _r == 0:
                return False

            r_inv = my_lib.mult_inv(_r, _p)
            if r_inv == -1:
                return False

            ergebnis = (r_inv * (a_i - a_2i)) % _p
            print("Der diskrete Logarithmus von %s zur Basis %s mod %s ist %s."
                  %(_y, _g, _p, ergebnis))
            return ergebnis

    print("Something went wrong ... ")
    return 0

def main():
    '''main function docstring'''

    _p = int(sys.argv[1])
    _g = int(sys.argv[2])
    _y = int(sys.argv[3])

    if (_p % _g) == 0:
        print("ERROR: g divides p.")
        sys.exit(1)

    pollards_rho(_p, _g, _y)

if __name__ == '__main__':
    main()
