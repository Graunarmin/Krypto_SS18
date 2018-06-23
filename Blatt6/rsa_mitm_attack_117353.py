# Valerie Lemuth (117017) & Johanna Sacher (117353)
'''
Geburtstagsangriff auf Textbook RSA mit gegebenem (n, e, c, b).
Es ist c = M^e (mod n) und M = m1 * m2  [mit m1, m2 prim und beide <= b]
Terminal: python3 rsa_mitm_attack_117353.py params.txt
'''

import sys
import gmpy2

def read_parameters(param_root):
    '''read in parameters n, e, c and b from given txt file'''

    keys = ["n", "e", "c", "b"]
    index = 0
    parameters = {}

    with open(param_root, "r") as p_file:
        for line in p_file:
            if line.startswith("#"):
                pass
            else:
                parameters[keys[index]] = int(line)
                index += 1

    _n = parameters["n"]
    _e = parameters["e"]
    _c = parameters["c"]
    _b = parameters["b"]

    return _n, _e, _c, _b

def angriff(param_root):
    '''
    m1, m2 prime and <= b
    First creating dict with c_i = (c/m1^e) mod n as {c_i : m1}
    Then testing if any m2^e matches any c_i.
    If match: Test if (m1*m2)^e == C (mod n) -> yes: (m1*m2) = Message
    '''

    _n, _e, _c, _b = read_parameters(param_root)
    # print("n = ", _n)
    # print("e = ", _e)
    # print("c = ", _c)
    # print("b = ", _b)
    candidates = {}
    prime_m1 = 2
    prime_m2 = 2
    match = False

    print("Calculating C_i ...")
    while prime_m1 <= _b:
        p_m1 = pow(prime_m1, _e, _n)
        c_i = _c * gmpy2.invert(p_m1, _n)
        c_i = c_i % _n
        candidates[c_i] = prime_m1
        prime_m1 = gmpy2.next_prime(prime_m1)

    print("Searching for a match ...")
    while prime_m2 <= _b:
        p_m2 = pow(prime_m2, _e, _n)
        if p_m2 in candidates:
            m_1 = candidates[p_m2]
            m_2 = prime_m2
            print("possible match... ")
            if test(m_1, m_2, _n, _e, _c):
                match = True
                break
            print("was not a match")
        prime_m2 = gmpy2.next_prime(prime_m2)

    if match:
        message = (m_1 * m_2) % _n
        print("The message is", message, "with m1 =", m_1, "and m2 =", m_2, ".")
        return message

    print("No match found")
    return None


def test(m_1, m_2, _n, _e, _c):
    '''test if (m1*m2)^e == c (mod n)'''

    print("testing ...")
    message = pow(m_1, _e, _n) * pow(m_2, _e, _n)
    if (_c % _n) == (message % _n):
        return True
    return False


def main():
    '''main function docstring'''

    param_root = sys.argv[1]
    angriff(param_root)

if __name__ == '__main__':
    main()
      