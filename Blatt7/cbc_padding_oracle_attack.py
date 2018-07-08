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
        messed_msg = [0 for i in range(16)]
        interm_state = [0 for i in range(16)]
        decrypted_msg = [0 for i in range(16)]
        i_v = list(initial_value) #creates a list of the integer-representations of the bytes
        cipher = list(ciphertext)
        rounds = 

        for i in range(15, -1, -1):
            sneaky = []
            sneaky = i_v[:i]

            counter = (16 - i)
            for j in range(-1, -counter-1, -1):
                messed_msg[j] = counter

            sneaky_value = 0
            sneaky.append(sneaky_value)
            for j in range((i+1), 16):
                sneaky.append(messed_msg[j] ^ interm_state[j])
            
            #print("Sneaky: ", sneaky)
            padding_correct, dec = oracle.verify_padding(bytes(sneaky), ciphertext)
                
            while not padding_correct:
                sneaky_value += 1
                if sneaky_value > 255:
                    break
                sneaky[i] = sneaky_value
                padding_correct, dec = oracle.verify_padding(bytes(sneaky), ciphertext)
                #print("Sneaky: ", sneaky)
            

            if padding_correct:
                # Wenn Padding stimmt, dann weiß man, was in der gefälschten Nachricht an der Stelle stand 
                # (wg. Padding)und man kann berechnen, was im vorherigen Cipherblock an der Stelle steht

                for j in range(i, 16):
                    messed_msg[j] = (16 - i)
                    counter = (16 - i)
                
                interm_state[i] = sneaky[i] ^ messed_msg[i]
                decrypted_msg[i] = i_v[i] ^ interm_state[i]
            
            elif sneaky_value > 255:
                print("Something went terribly wrong")
                break

        dec_msg = decrypted_msg
        
        # # catch empty message:
        # print(dec_msg)
        # if dec_msg.count(0) == len(dec_msg):
        #     dec_msg = []

        # Padding entfernen:
        for i in range(1, 17):
            if (decrypted_msg[-1] == i)and(decrypted_msg[-i] == i):
                dec_msg = decrypted_msg[:-i]
            else:
                pass

        return bytes(dec_msg)



        
            

        
        