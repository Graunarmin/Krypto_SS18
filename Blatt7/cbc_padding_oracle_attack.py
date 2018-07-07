#!/usr/bin/env python3

"""
Implements the CBC padding oracle attack and returns (if possible)
the plaintext that corresponded to the given ciphertext.
"""

from cbc_padding_oracle import CBCPaddingOracle


# ---------------------------------------------------------

class CBCPaddingOracleAttack:
    """
    Implements the CBC padding oracle attack.
    """

    # ---------------------------------------------------------

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def recover_message(self, 
                        oracle: CBCPaddingOracle,
                        initial_value: bytes,
                        ciphertext: bytes):# -> bytes:
        """
        Implements the CBC padding-oracle attack.
        :param initial_value: 16-byte initial value.
        :param ciphertext: Ciphertext. Length must be multiple of 16 bytes.
        :return: Returns the plaintext that corresponded to the given
                 ciphertext.
        """

        
        