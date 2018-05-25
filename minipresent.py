#!/usr/bin/env python3

"""
Defines a 16-bit simplified variant of the PRESENT.

__author__ = eik list
__last-modified__ = 2018-05
__copyright__ = CC0
"""

# ----------------------------------------------------------

from typing import List


# ----------------------------------------------------------

class MiniPresent:
    """
    A 16-bit simplified variant of PRESENT.
    """

    NUM_ROUNDS = 16
    NUM_STATE_BITS = 16
    NUM_KEY_BITS = 16
    NUM_SBOX_BITS = 4

    WORD_MASK = (1 << NUM_STATE_BITS) - 1
    SBOX = [
        0xe, 0x7, 0x1, 0xa, 0x3, 0x2, 0xb, 0xd,
        0x6, 0x0, 0xf, 0x8, 0x5, 0xc, 0x9, 0x4
    ]
    INVERSE_SBOX = [
        0x9, 0x2, 0x5, 0x4, 0xf, 0xc, 0x8, 0x1,
        0xb, 0xe, 0x3, 0x6, 0xd, 0x7, 0x0, 0xa
    ]
    PERMUTATION = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    INVERSE_PERMUTATION = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    # ----------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------

    @staticmethod
    def _apply_sbox(value: int, sbox: List[int]) -> int:
        """
        Transforms the given state by applying the S-box four times in parallel.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """

        num_sboxes = int(MiniPresent.NUM_STATE_BITS / MiniPresent.NUM_SBOX_BITS)
        sbox_mask = (1 << MiniPresent.NUM_SBOX_BITS) - 1
        result = 0

        for i in range(num_sboxes):
            shift = (num_sboxes - 1 - i) * MiniPresent.NUM_SBOX_BITS
            sbox_output = sbox[(value >> shift) & sbox_mask]
            result |= sbox_output << shift

        return result

    # ----------------------------------------------------------

    @staticmethod
    def _sbox_layer(value: int) -> int:
        """
        Transforms the given state by applying the S-box four times in parallel.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        return MiniPresent._apply_sbox(value, MiniPresent.SBOX)

    # ----------------------------------------------------------

    @staticmethod
    def _invert_sbox_layer(value: int) -> int:
        """
        Transforms the given state by applying the S-box four times in parallel.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        return MiniPresent._apply_sbox(value, MiniPresent.INVERSE_SBOX)

    # ----------------------------------------------------------

    @staticmethod
    def _permute(value: int, permutation: List[int]) -> int:
        """
        Permutes the bits of the given state value by applying the permutation.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        result = 0

        for i in range(MiniPresent.NUM_STATE_BITS):
            bit = (value >> permutation[i]) & 1
            result |= bit << i

        return result

    # ----------------------------------------------------------

    @staticmethod
    def _permutation_layer(value: int) -> int:
        """
        Permutes the bits of the given state value by applying the permutation.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        return MiniPresent._permute(value, MiniPresent.PERMUTATION)

    # ----------------------------------------------------------

    @staticmethod
    def _invert_permutation_layer(value: int) -> int:
        """
        Permutes the bits of the given state value by applying the permutation.
        :param value: 16-bit input state.
        :return: 16-bit output state.
        """
        return MiniPresent._permute(value, MiniPresent.INVERSE_PERMUTATION)

    # ----------------------------------------------------------

    def _encrypt_round(self,
                       round_index: int,
                       round_key: int,
                       state: int) -> int:
        """
        Encrypts the state represented by left || right by one round of
        Mini-PRESENT under the given round_key.
        :param round_index: Integer in [1..16]
        :param round_key: 16-bit integer round-key
        :param state: 16-bit integer
        :return: 16-bit state
        """
        state = ((state ^ round_key) + round_index) & MiniPresent.WORD_MASK
        state = self._sbox_layer(state)
        state = self._permutation_layer(state)
        return state

    # ----------------------------------------------------------

    def _decrypt_round(self,
                       round_index: int,
                       round_key: int,
                       state: int) -> int:
        """
        Decrypts the state represented by left || right by one round of
        Mini-PRESENT under the given round_key.
        :param round_index: Integer in [1..16]
        :param round_key: 16-bit integer round-key
        :param state: 16-bit integer
        :return: 16-bit state
        """
        state = self._invert_permutation_layer(state)
        state = self._invert_sbox_layer(state)
        state = ((state - round_index) ^ round_key) & MiniPresent.WORD_MASK
        return state

    # ----------------------------------------------------------

    def encrypt(self, key: int, state: int) -> int:
        """
        Encrypts the given 32-bit integer under the given 16-bit key with
        full-round Mini-PRESENT.
        :param key: 16-bit integer
        :param state: 32-bit integer plaintext
        :return: 32-bit integer ciphertext
        """
        key = key & MiniPresent.WORD_MASK

        for i in range(MiniPresent.NUM_ROUNDS):
            state = self._encrypt_round(i+1, key, state)

        state ^= key
        return state

    # ----------------------------------------------------------

    def decrypt(self, key: int, state: int) -> int:
        """
        Decrypts the given 32-bit integer under the given 16-bit key with
        full-round Mini-PRESENT.
        :param key: 16-bit integer
        :param state: 32-bit integer ciphertext
        :return: 32-bit integer plaintext
        """
        key = key & MiniPresent.WORD_MASK
        state ^= key

        for i in reversed(range(MiniPresent.NUM_ROUNDS)):
            state = self._decrypt_round(i+1, key, state)

        return state


# ----------------------------------------------------------

def main() -> None:
    """
    Tests MiniPresent.
    """
    cipher = MiniPresent()
    plaintext = 0x1122
    key = 0x4567
    ciphertext = cipher.encrypt(key, plaintext)
    expected_ciphertext = 0x904b

    second_plaintext = cipher.decrypt(key, ciphertext)
    print("{:04x}".format(ciphertext))
    print("{:04x}".format(second_plaintext))

    assert ciphertext == expected_ciphertext
    assert plaintext == second_plaintext

    print("K:  {:04x}".format(key))
    print("P:  {:04x}".format(plaintext))
    print("C:  {:04x}".format(ciphertext))
    print("P': {:04x}".format(second_plaintext))


# ----------------------------------------------------------

if __name__ == "__main__":
    main()
