import binascii
from typing import List

def get_key():

    # gegeben:
    print("gegeben:")
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
    # -> behalten IV, darf ja mehrmals vorkommen:
    # Ek(IV) XOR m_1 = c_1
    # M_1 XOR C_1 XOR m_1 = c_1

    print("a)")
    c_1 = M_1 ^ C_1 ^ m_1 
    print("c_1 = {:04x}".format(c_1))

    # da m_2 == M_2 und wir IV unverändert lassen, ist c_2 == C_2
    # IV = 0xdabe785fb5a688a61cc77c3035d754fa
    # c1 = 0x5973ecca8de35f99172bd28ba0ede12b
    # c2 = 0x42f2dc27a8a676d69e1825d323016d38

    # überprüfen:
    mes_1 = c_1 ^ M_1 ^ C_1
    print("mes_1 = {:04x}".format(mes_1))
    #Ergebnis von mes_1 aus terminal kopieren und einsetzen: (geht bestimmt auch eleganter, weiß gerad nicht wie^^)
    mes_1 = binascii.unhexlify('5a61686c652045766520353030455552')
    print("Neue Nachricht Teil 1:", mes_1)




# b) CBC Mode:
    # C1 = Ek(IV XOR M1)
    # C2 = Ek(C1 XOR M2)
    # M = (m1, M2)
    # hier muss iv geändert werden:
    # c1 = Ek(iv XOR m1)
    # c2 = Ek(c1 XOR M2)
    # gut wäre, wenn Ek(IV XOR M1) == Ek(iv XOR m1), damit c1 == C1 - anders kommt man da nicht dran. 
    # also: iv XOR m1 == IV XOR M1
    # Es gilt m2 == M2 und wenn c1 == C1, dann gilt wegen c2 = Ek(c1 XOR m1) = Ek(C1 XOR M1) = C2

    print("b)")
    res = I_V ^ M_1
    iv = m_1 ^ res

    print("iv = {:04x}".format(iv))

    #überprüfen: (eigl reduntant, ist ja nur umstellen und beweist nix ... aber funktioniert :D)
    message_1 = I_V ^ iv ^ M_1
    print("message_1 = {:04x}".format(message_1))
    message_1 = binascii.unhexlify('5a61686c652045766520353030455552')
    print("Neue Nachricht Teil 1:", message_1)

    # iv = 0xdabe785fb5a68fbf1bc7783035d754fa
    # c1 = C1 = 0x5973ecca8de35880102bd68ba0ede12b
    # c2 = C2 = 0x42f2dc27a8a676d69e1825d323016d38

get_key()