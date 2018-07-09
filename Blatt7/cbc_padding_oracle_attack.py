#!/usr/bin/env python3
# Valerie Lemuth (117017) & Johanna Sacher (117353)

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
        ANMERKUNGEN:
        with great help from: https://robertheaton.com/2013/07/29/padding-oracle-attack/
        Alle Fehler, die Pylint noch anmeckert, sind von Eik, nicht von mir!
        c) funktioniert für die einkommentierten Tests in der Test-Datei.
        Den Rest habe ich nicht hinbekommen, ein gepaddeter Block funktioniert, bei allem drüber
        kommt man beim Hochzählen an die 255 Grenze und ich weiß nicht genau,
        was ich da falsch mache -.- Habe mich an der Seite oben orientiert,
        das war die beste Erklärung, die ich finden konnte.
        """

        interm_state = [0 for i in range(16)]
        i_v = list(initial_value) #creates a list of the integer-representations of the bytes
        whole_cipher = i_v + list(ciphertext)
        dec_msg = []

        for k in range(len(whole_cipher), 31, -16):
            cipher = whole_cipher[(k-16):k]
            sneaky = whole_cipher[(k-32):(k-16)]
            dec_block = [0 for k in range(16)]

            for i in range(15, -1, -1):
                counter = (16 - i)
                sneaky_value = 0
                sneaky[i] = sneaky_value
                for j in range((i+1), 16):
                    sneaky[j] = counter ^ interm_state[j]

                padding_correct = oracle.verify_padding(bytes(sneaky), bytes(cipher))

                while not padding_correct:
                    sneaky_value += 1
                    if sneaky_value > 255:
                        break
                    sneaky[i] = sneaky_value
                    padding_correct = oracle.verify_padding(bytes(sneaky), bytes(cipher))

                if padding_correct:
                    # Wenn Padding stimmt, dann weiß man, was in der gefälschten Nachricht
                    # an der Stelle stand (wg. Padding)und man kann berechnen,
                    # was im vorherigen Cipherblock an der Stelle steht
                    interm_state[i] = sneaky[i] ^ counter
                    dec_block[i] = i_v[i] ^ interm_state[i]

                elif sneaky_value > 255:
                    print("Something went terribly wrong")
                    break

                else:
                    pass

            # Padding entfernen:
            padding = dec_block[-1]
            dec_block = dec_block[:-padding]

            dec_msg = dec_block + dec_msg

        return bytes(dec_msg)
