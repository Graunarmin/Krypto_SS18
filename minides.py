#!/usr/bin/env python3

"""
Defines a 32-bit minified variant of the DES.

__author__ = eik list
__last-modified__ = 2018-05
__copyright__ = CC0
"""

# ----------------------------------------------------------

from typing import Tuple


# ----------------------------------------------------------

class MiniDES:
    """
    A 32-bit minified variant of DES.
    """

    NUM_ROUNDS = 16
    NUM_STATE_BITS = 32
    NUM_BITS_IN_WORD = int(NUM_STATE_BITS / 2)
    NUM_KEY_BITS = 16
    NUM_SBOX_BITS = 4

    WORD_MASK = (1 << NUM_BITS_IN_WORD) - 1

    SBOX = [
        0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
    ]
    INVERSE_SBOX = [
        0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD,\
        0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA
    ]
    PERMUTATION = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    INVERSE_PERMUTATION = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    # ----------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------

    @staticmethod
    def _sbox_layer(value: int) -> int:
        """
        Transforms the given state by applying the S-box four times in parallel.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """

        num_sboxes = int(MiniDES.NUM_BITS_IN_WORD / MiniDES.NUM_SBOX_BITS)
        sbox_mask = (1 << MiniDES.NUM_SBOX_BITS) - 1
        result = 0

        for i in range(num_sboxes):
            shift = (num_sboxes - 1 - i) * MiniDES.NUM_SBOX_BITS
            sbox_output = MiniDES.SBOX[(value >> shift) & sbox_mask]
            result |= sbox_output << shift

        return result

    # ----------------------------------------------------------

    @staticmethod
    def _permutation_layer(value: int) -> int:
        """
        Permutes the bits of the given state value by applying the permutation.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        result = 0

        for i in range(MiniDES.NUM_BITS_IN_WORD):
            bit = (value >> MiniDES.PERMUTATION[i]) & 1
            result |= bit << i

        return result

    # ----------------------------------------------------------

    @staticmethod
    def _swap_words(left: int, right: int) -> Tuple[int, int]:
        return right, left

    # ----------------------------------------------------------

    @staticmethod
    def _to_words(state: int) -> Tuple[int, int]:
        """
        Given an 32-bit integer state, outputs it as tuple of two
        16-bit words. Left = the higher 16 bits, right = the lower 16 bits.
        :param state: 32-bit integer state
        :return: 16-bit output words (left, right).
        """
        left = (state >> MiniDES.NUM_BITS_IN_WORD) & MiniDES.WORD_MASK
        right = state & MiniDES.WORD_MASK
        return left, right

    # ----------------------------------------------------------

    @staticmethod
    def _to_state(left: int, right: int) -> int:
        """
        Given two 16-bit integers, outputs it as 32-bit integer.
        :param left: 16-bit integer
        :param right: 16-bit integer
        :return: (left || right) 32-bit integer state
        """
        return (left << MiniDES.NUM_BITS_IN_WORD) | right

    # ----------------------------------------------------------

    def _decrypt_round(self,
                       round_index: int,
                       round_key: int,
                       left: int,
                       right: int) -> int:
        """
        Decrypts the state represented by left || right by one round of
        Mini-DES under the given round_key.
        :param round_index: Integer in [1..16]
        :param round_key: 16-bit integer round-key
        :param left: 16-bit integer
        :param right: 16-bit integer
        :return: Tuple of (left, right) state
        """
        (left, right) = self._swap_words(left, right)
        round_output = ((right ^ round_key) + round_index) & MiniDES.WORD_MASK
        round_output = self._sbox_layer(round_output)
        round_output = self._permutation_layer(round_output)
        left ^= round_output
        return left, right

    # ----------------------------------------------------------

    def _encrypt_round(self,
                       round_index: int,
                       round_key: int,
                       left: int,
                       right: int) -> Tuple[int, int]:
        """
        Encrypts the state represented by left || right by one round of
        Mini-DES under the given round_key.
        :param round_index: Integer in [1..16]
        :param round_key: 16-bit integer round-key
        :param left: 16-bit integer
        :param right: 16-bit integer
        :return: Tuple of (left, right) state
        """
        round_output = ((right ^ round_key) + round_index) & MiniDES.WORD_MASK
        round_output = self._sbox_layer(round_output)
        round_output = self._permutation_layer(round_output)
        left ^= round_output
        return self._swap_words(left, right)

    # ----------------------------------------------------------

    def encrypt(self, key: int, state: int) -> int:
        """
        Encrypts the given 32-bit integer under the given 16-bit key with
        full-round Mini-DES.
        :param key: 16-bit integer
        :param state: 32-bit integer plaintext
        :return: 32-bit integer ciphertext
        """
        (left, right) = self._to_words(state)

        for i in range(MiniDES.NUM_ROUNDS):
            (left, right) = self._encrypt_round(i+1, key, left, right)

        return self._to_state(left, right)

    # ----------------------------------------------------------

    def decrypt(self, key: int, state: int) -> int:
        """
        Decrypts the given 32-bit integer under the given 16-bit key with
        full-round Mini-DES.
        :param key: 16-bit integer
        :param state: 32-bit integer ciphertext
        :return: 32-bit integer plaintext
        """
        (left, right) = self._to_words(state)

        for i in reversed(range(MiniDES.NUM_ROUNDS)):
            (left, right) = self._decrypt_round(i+1, key, left, right)

        return self._to_state(left, right)

def to_hex(number):
    '''
    dachte, die hilft vielleicht dabei, die Schlüssel richtig in der Form
    0x11223344 (z.B) darzustellen, so dass es trotzdem als int erkannt wird,
    klappt aber nicht so richtig.
    '''
        
    key = ""
    length = 4

    base = ['0', '1', '2', '3', '4', '5', '6', '7', 
            '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    
    while length > 0:
        i = number % 16
        key += base[i]
        number //= 16
        length -= 1
    
    return key[::-1]
        

# ----------------------------------------------------------

def main() -> None:
    """
    Tests MiniDES.
    """
    cipher = MiniDES()
    plaintext = 0x11223344
    key = 0x01234567
    ciphertext = cipher.encrypt(key, plaintext)
    expected_ciphertext = 0xcae11b78

    second_plaintext = cipher.decrypt(key, ciphertext)
    assert ciphertext == expected_ciphertext
    assert plaintext == second_plaintext

    print("K:  {:08x}".format(key))
    print("P:  {:08x}".format(plaintext))
    print("C:  {:08x}".format(ciphertext))
    print("P': {:08x}".format(second_plaintext))

    #--------------- unser Teil!--------------------------------------------
    
    # läuft zwar durch, findet aber keinen Schlüssel -.-
    # denke das liegt daran, dass die keys momentan als ganz normale ints 
    # übergeben werden und nicht in der Form 0xabcdef01. Bekomme das nicht hin.

    p_1 = 0xabcdef01
    c_1 = 0xd18c096d

    p_2 = 0x11223344
    c_2 = 0x31f0989e

    table = {}
    possible_keys = {}
    
    found = False

    keylength = 16
    
    for i in range(0, 2**keylength):
        '''
        create dictionary with "key:encrypt(p_1)"
        zuerst p_1 mit allen mögl. keys verschlüsseln (= value_1)
        und Paare speichern
        '''

        key_1 = i #so wird der Schlüssel als "ganz normaler" int übergeben
        print(key_1)
        table[key_1] = cipher.encrypt(key_1, p_1)

    '''
    Dann c_1 mit allen möglichen Keys entschlüsseln (= value_2)
    '''    

    print("checking for matches ..\n")
    for key_2 in table:
        print(key_2)
        value_2 = cipher.decrypt(key_2, c_1)

        '''
        wenn value_1 == irgendein value_2: den key, mit dem v_1 
        erzeugt wurde und den, mit dem v_2 erzeugt wurde 
        gemeinsam als Schlüsselkandidaten abspeichern
        '''
        for k_1 in table:
            if value_2 == table[k_1]:
                print("Match!")
                possible_keys[k_1] = key_2

    print("Testing possible keys .. \n")
    for k_1 in possible_keys:
        '''
        Test all possible keys with the second known pair (p_2, c_2)
        '''
        k_2 = possible_keys[k_1]

        k = str(k_1)+str(k_2)
        key = int(k)

        print("Testing key ",key,"\n")
        print("Plaintext: ",p_2)
        print("Ciphertext: ",c_2)

        encrypt = cipher.encrypt(key, p_2)

        print("Encrypted text from k %s and p %s: %s" %(key, p_2, encrypt))

        if encrypt == c_2:
            print("The Key is: ", key_1,", ",key_2)
            found = True
            break
    
    if found == False:
        print("Key was not found.")

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
