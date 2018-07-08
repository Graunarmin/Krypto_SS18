#!/usr/bin/env python3

"""
Implements a CBC padding oracle for AES-128-CBC.
__author__ = Eik List
__date__   = 2018-04
__copyright__ = Creative Commons CC0
"""

# ---------------------------------------------------------

from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr
#from Crypto import Random
#import binascii


# ---------------------------------------------------------

class CBCPaddingOracle:
    """
    Implements a CBC padding oracle for AES-128-CBC.
    """

    def __init__(self, key: bytes):
        """
        Sets the key.
        :param key:
        """
        self.key = key

    # ---------------------------- a) -----------------------------

    def encrypt(self, initial_value: bytes, message: bytes): # -> bytes:
        """
        Pads the given message to a multiple of the block length,
        computes, and returns its encryption with AES-128-CBC-XMLPad.

        :param initial_value: 16-byte initial value.
        :param message: Plaintext of arbitrary length
        :return: Ciphertext whose length is a multiple of 16 bytes, but
        always at least the length of the message.
        """

        BLOCK_LENGTH = 16

        padded_msg = self.pad(message, BLOCK_LENGTH)
        enc_msg = self.aes_enc(initial_value, padded_msg)

        return enc_msg


    def pad(self, message: bytes, BLOCK_LENGTH: int): #-> bytes
        '''
        pads the message to a length that is a multiple of 16
        '''

        too_short = ((len(message) % BLOCK_LENGTH) != 0)

        if not too_short:
            # Wenn der letzte Block "voll" ist: noch einen Block anhängen (16 x die 16)
            for i in range(0, 16):
                padding = bchr(16)
                message += padding

        else:
            # wenn dem letzten Block Bytes fehlen: die entsprechende Anzahl hinzufügen
            to_add = (BLOCK_LENGTH - len(message)) % BLOCK_LENGTH

            while too_short:
                padding = bchr(to_add)
                message += padding
                if (len(message) % BLOCK_LENGTH) == 0:
                    too_short = False

        return message


    def aes_enc(self, initial_value: bytes, message: bytes): #-> bytes
        '''
        AES Encryption of a given message with a given IV
        '''

        cipher = AES.new(self.key, AES.MODE_CBC, initial_value)
        enc_msg = cipher.encrypt(message)

        return enc_msg

    #-------------------------------- b) -----------------------------------

    def verify_padding(self, initial_value: bytes, ciphertext: bytes): # -> bool:
        """
        Given a ciphertext, evaluates if the padding is correct.
        :param initial_value: 16-byte initial value.
        :param ciphertext: Ciphertext. Length must be multiple of 16 bytes.
        :return: True if padding is correct or there was no padding, and False otherwise 
        AND the decrypted message (for now)
        """

        dec_msg = self.aes_dec(initial_value, ciphertext)
        BLOCK_LENGTH = len(initial_value)
        pad_val = dec_msg[-1]
        padding_correct = False

        if pad_val > BLOCK_LENGTH:
            print("Input is not padded or padding is wrong")

        else:
            for i in range(1, pad_val+1):
                if dec_msg[-i] == pad_val:
                    padding_correct = True
                else:
                    padding_correct = False
                    break;

            if padding_correct == False:
                print("Input is not padded or padding is wrong")
 
        return padding_correct, dec_msg


    def aes_dec(self, initial_value: bytes, ciphertext: bytes): #->bytes
        '''
        AES Decryption of a given ciphertext with a given IV
        '''

        msg = AES.new(self.key, AES.MODE_CBC, initial_value)
        dec_msg = msg.decrypt(ciphertext)

        return dec_msg
  
        #remove padding from ciphertext (not really necassary though^^)
        # l = len(ciphertext) - pad_val
        # without_padding = ciphertext[:l]
    
        # return dec_msg, without_padding
