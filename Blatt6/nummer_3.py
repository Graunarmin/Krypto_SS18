import binascii
from typing import List

def get_key():

    # gegeben:
    I_V = 0xdabe785fb5a688a61cc77c3035d754fa
    C_1 = 0x5973ecca8de35880102bd68ba0ede12b
    C_2 = 0x42f2dc27a8a676d69e1825d323016d38

    # M als 8-bit ASCII in hex:
    M_1 = binascii.hexlify(b'Zahle Bob 100EUR')
    print("M1 =", M_1)
    M_2 = binascii.hexlify(b' von Konto 12345')
    print("M2 =", M_2)
    M_1 = 0x5a61686c6520426f6220313030455552
    M_2 = 0x20766f6e204b6f6e746f203132333435

    # neue Nachricht m in ASCII:
    m_1 = binascii.hexlify(b'Zahle Eve 500EUR')
    print("m1 =", m_1)
    m_1 = 0x5a61686c652045766520353030455552
    m_2 = M_2

# a) CTR Mode:
    # Ek(IV) XOR M_1 = C_1
    # Ek(IV) = M_1 XOR C_1
    # Ek(IV) XOR m_1 = c_1
    # M_1 XOR C_1 XOR m_1 = c_1

    c_1 = M_1 ^ C_1 ^ m_1 
    print("c_1 = {:04x}".format(c_1))

    # da m_2 == M_2 und wir IV unverändert lasse, ist c_2 == C_2
    # IV = 0xdabe785fb5a688a61cc77c3035d754fa
    # c1 = 0x5973ecca8de35f99172bd28ba0ede12b
    # c2 = 0x42f2dc27a8a676d69e1825d323016d38

# b) CBC Mode:




get_key()