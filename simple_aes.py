#!/usr/bin/env python3

"""
A simplified variant of the AES

__author__ = eik list
__last-modified__ = 2018-05
__copyright__ = CC0
"""

# ----------------------------------------------------------

from typing import List


# ----------------------------------------------------------

def _double(value: int) -> int:
    """
    Computes 2 * x in GF(2^8) modulo the irreducible polynomial
    p(z) = (z^8 + z^4 + z^3 + z + 1) = 0x11b. Note that x is interpreted
    as polynomial in GF(2^8) and "2" is the polynomial z^1 in GF(2^8).

    So, doubling in GF(2^8) is equivalent to
    2 * x = (x << 1) if x < 2^7,
            (x << 1) xor 0x11b if x >= 2^7.

    :param value: x
    :return: Result of 2 * x.
    """
    return (value << 1) ^ (((value >> 7) & 1) * 0x11b)


# ----------------------------------------------------------

def gf2_8_multiply(value: int, constant: int) -> int:
    """
    Multiplies x * y in GF(2^8) modulo the irreducible polynomial
    p(z) = (z^8 + z^4 + z^3 + z + 1) = 0x11b. This function only works if
    y is at most 15. Though, this is no problem with the AES mix-columns
    and inverse mix-columns matrix.

    This is a constant implementation that takes y as bit string.
    For example, y = 11 is taken apart into
    y = (y_3 y_2 y_1 y_0) = (1011).
    Then, the result is composed of the sum of
    2^3 * x + 2^1 * x + x. Note that in GF, addition is XOR.
    :param value: x
    :param constant: y
    :return: Result of x * y.
    """
    # if y_i = 1 => add 2^i * x to the result
    return ((constant & 1) * value)\
        ^ (((constant >> 1) & 1) * _double(value))\
        ^ (((constant >> 2) & 1) * _double(_double(value)))\
        ^ (((constant >> 3) & 1) * _double(_double(_double(value))))


# ----------------------------------------------------------

def print_state(state: List[int]) -> None:
    """
    Prints a given list of 8-bit hex strings.
    :param state:
    :return:
    """
    for i in state:
        print("{:02x}".format(i), end=" ")

    print()


# ----------------------------------------------------------

def xor_state(left: List[int], right: List[int]) -> List[int]:
    """
    XORs two lists and returns a list c, where c[i] = left[i] ^ right[i],
    i.e., the element-wise XOR.
    :param left:
    :param right:
    :return: Element-wise XORed list or AssertionError if the lengths of
    left and right do not match.
    """
    assert len(left) == len(right)
    return [left[i] ^ right[i] for i in range(len(left))]


# ----------------------------------------------------------

class SimpleAES:
    """
    A simplified variant of the AES. The simplification consists of the fact
    that it does not employ the key schedule.
    """

    NUM_ROUNDS = 10
    NUM_KEY_BITS = 128
    NUM_STATE_BITS = 128

    NUM_STATE_BYTES = int(NUM_STATE_BITS / 8)
    NUM_KEY_BYTES = int(NUM_ROUNDS / 8)
    NUM_COLUMNS = 4
    NUM_ROWS = 4

    ROUND_CONSTANTS = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
    ]

    '''für a) und b) SBOX_o wieder in SBOX umbennenen und SBOX unten auskommentieren'''
    SBOX_o = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    #print(SBOX_o)

    #c): alle SBox-Einträge mit 85 XOR
    SBOX = []
    for x in SBOX_o:
        SBOX.append(x ^ 85)

    #print(SBOX)


    INVERSE_SBOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38,
        0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
        0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d,
        0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2,
        0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
        0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
        0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a,
        0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
        0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea,
        0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85,
        0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
        0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20,
        0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31,
        0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
        0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0,
        0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26,
        0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]

    PERMUTATION = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    #PERMUTATION = [0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14] #für a)
    #PERMUTATION = [0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 5, 14, 7] #für b)

    '''zum Decrypten die inverse'''
    INVERSE_PERMUTATION = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]

    MIX_COLUMNS_MATRIX = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]
    INVERSE_MIX_COLUMNS_MATRIX = [
        [0xe, 0xb, 0xd, 0x9],
        [0x9, 0xe, 0xb, 0xd],
        [0xd, 0x9, 0xe, 0xb],
        [0xb, 0xd, 0x9, 0xe]
    ]

    # ----------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------

    @staticmethod
    def _substitute(state: List[int], sbox: List[int]) -> List[int]:
        """
        Transforms the given state by applying the S-box 16x in parallel.
        :param state: 16-byte state.
        :param sbox: 8-bit- times 8-bit S-box.
        :return: 16-byte updated state.
        """
        assert len(state) == SimpleAES.NUM_STATE_BYTES

        for i in range(SimpleAES.NUM_STATE_BYTES):
            state[i] = sbox[state[i]]

        return state

    # ----------------------------------------------------------

    @staticmethod
    def _sub_bytes(state: List[int]) -> List[int]:
        """
        Transforms the given state by applying the S-box 16x in parallel.
        :param state: 16-byte input state.
        :return: 16-byte output state.
        """
        return SimpleAES._substitute(state, SimpleAES.SBOX)

    # ----------------------------------------------------------

    @staticmethod
    def _invert_sub_bytes(state: List[int]) -> List[int]:
        """
        Transforms the given state by applying the S-box 16x in parallel.
        :param state: 16-byte input state.
        :return: 16-byte output state.
        """
        return SimpleAES._substitute(state, SimpleAES.INVERSE_SBOX)

    # ----------------------------------------------------------

    @staticmethod
    def _permute(state: List[int], permutation: List[int]) -> List[int]:
        """
        Permutes the state byte by the given permutation.
        :param state:
        :param permutation:
        :return: Updated state
        """
        assert len(state) == SimpleAES.NUM_STATE_BYTES
        assert len(permutation) == SimpleAES.NUM_STATE_BYTES
        return [state[permutation[i]] for i in range(SimpleAES.NUM_STATE_BYTES)]

    # ----------------------------------------------------------

    @staticmethod
    def _shift_rows(state: List[int]) -> List[int]:
        """
        Permutes the bytes of the given state value by applying the permutation.
        :param state: 16-bytes input state.
        :return: 16-bytes output state.
        """
        return SimpleAES._permute(state, SimpleAES.PERMUTATION)

    # ----------------------------------------------------------

    @staticmethod
    def _invert_shift_rows(state: List[int]) -> List[int]:
        """
        Permutes the bits of the given state value by applying the permutation.
        :param state: 16-bytes input state.
        :return: 16-bytes output state.
        """
        return SimpleAES._permute(state, SimpleAES.INVERSE_PERMUTATION)

    # ----------------------------------------------------------

    @staticmethod
    def _multiply_state(state: List[int], matrix: List[List[int]]) -> List[int]:
        """
        Multiplies the given state S by the given matrix A
        :param state:
        :param matrix:
        :return: Returns A * S.
        """
        result = [0 for _ in state]

        for column in range(SimpleAES.NUM_COLUMNS):
            for row in range(SimpleAES.NUM_ROWS):
                matrix_row = matrix[row]
                entry = 0

                for i in range(SimpleAES.NUM_COLUMNS):
                    entry ^= gf2_8_multiply(
                        state[SimpleAES.NUM_ROWS * column + i],
                        matrix_row[i]
                    )

                result[SimpleAES.NUM_ROWS * column + row] = entry

        return result

    # ----------------------------------------------------------

    @staticmethod
    def _mix_columns(state: List[int]) -> List[int]:
        """
        Applies the AES mixcolumns matrix to the given state.
        :param state: 16-byte input state.
        :return: 16-byte output state.
        """
        return SimpleAES._multiply_state(state, SimpleAES.MIX_COLUMNS_MATRIX)

    # ----------------------------------------------------------

    @staticmethod
    def _invert_mix_columns(state: List[int]) -> List[int]:
        """
        Applies the inverse AES mixcolumns matrix to the given state.
        :param state: 16-byte input state.
        :return: 16-byte output state.
        """
        return SimpleAES._multiply_state(
            state,
            SimpleAES.INVERSE_MIX_COLUMNS_MATRIX
        )

    # ----------------------------------------------------------

    @staticmethod
    def add_round_key(key: List[int], state: List[int]) -> List[int]:
        """
        XORs the given round key to the given state.
        :param key: 16-byte round key K.
        :param state: 16-byte input state X.
        :return: 16-byte output state K ^ X.
        """
        return [key[i] ^ state[i] for i in range(SimpleAES.NUM_STATE_BYTES)]

    # ----------------------------------------------------------

    def decrypt_round(self,
                      round_index: int,
                      round_key: List[int],
                      state: List[int]) -> List[int]:
        """
        Applies an AES round decryption to the given state.
        :param round_index:
        :param round_key: 16-byte list
        :param state: 16-byte list
        :return: Updated 16-byte state.
        """
        state = self.add_round_key(round_key, state)

        if round_index < SimpleAES.NUM_ROUNDS:
            state = self._invert_mix_columns(state)

        state = self._invert_shift_rows(state)
        state = self._invert_sub_bytes(state)
        return state

    # ----------------------------------------------------------

    def encrypt_round(self,
                      round_index: int,
                      round_key: List[int],
                      state: List[int]) -> List[int]:
        """
        Applies an AES round encryption to the given state.
        :param round_index:
        :param round_key: 16-byte list
        :param state: 16-byte list
        :return: Updated 16-byte state.
        """
        state = self._sub_bytes(state)
        state = self._shift_rows(state)

        if round_index < SimpleAES.NUM_ROUNDS:
            state = self._mix_columns(state)

        return self.add_round_key(round_key, state)

    # ----------------------------------------------------------

    def encrypt_rounds(self,
                       key: List[int],
                       state: List[int],
                       from_round: int,
                       to_round: int) -> List[int]:
        """
        Applies an AES encryption to the given plaintext state.
        :param key: 16-byte list
        :param state: 16-byte plaintext
        :param from_round: [1..10].
        :param to_round: [1..10].
        :return: 16-byte ciphertext.
        """
        assert from_round >= 1 and to_round <= SimpleAES.NUM_ROUNDS

        if from_round == 1:
            state = self.add_round_key(key, state)

        for i in range(from_round, to_round+1):
            state = self.encrypt_round(i, key, state)

        return state

    # ----------------------------------------------------------

    def encrypt(self, key: List[int], state: List[int]) -> List[int]:
        """
        Applies an AES encryption to the given plaintext state.
        :param key: 16-byte list
        :param state: 16-byte plaintext
        :return: 16-byte ciphertext.
        """
        state = self.add_round_key(key, state)

        for i in range(SimpleAES.NUM_ROUNDS):
            state = self.encrypt_round(i+1, key, state)

        return state

    # ----------------------------------------------------------

    def decrypt(self, key: List[int], state: List[int]) -> List[int]:
        """
        Applies an AES encryption to the given plaintext state.
        :param key: 16-byte list
        :param state: 16-byte ciphertext
        :return: 16-byte plaintext.
        """
        for i in reversed(range(SimpleAES.NUM_ROUNDS)):
            state = self.decrypt_round(i+1, key, state)

        state = self.add_round_key(key, state)
        return state


# ----------------------------------------------------------

def main() -> None:
    """
    Tests SimpleAES.
    """
    cipher = SimpleAES()
    plaintext = [
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
    ]

    # plaintext = [
    #     0x01, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    #     0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
    # ]

    key = [
        0x9b, 0x35, 0xb2, 0xce, 0xca, 0x9c, 0x69, 0x0c,
        0x3a, 0x50, 0x65, 0xee, 0xab, 0x4e, 0x60, 0x9b
    ]
    ciphertext = cipher.encrypt(key, plaintext)
    expected_ciphertext = [
        0x9b, 0x1d, 0x72, 0x0c, 0x89, 0x0a, 0x84, 0xd7,
        0x73, 0x77, 0x42, 0x4e, 0xf6, 0x65, 0xbf, 0x0d
    ]

    second_plaintext = cipher.decrypt(key, ciphertext)

    print("Key:")
    print(key) # key in dec
    print("Plain:")
    print(plaintext)
    print("Cipher:")
    print(ciphertext)
    print("Second Plaintext:")
    print(second_plaintext)
    print("\n\n")

    # print_state(key) # key in hex
    # print_state(plaintext)
    # print_state(ciphertext)
    # print_state(second_plaintext)

    #assert ciphertext == expected_ciphertext
    # assert plaintext == second_plaintext


# ----------------------------------------------------------

if __name__ == "__main__":
    main()
