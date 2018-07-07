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

    # ---------------------------------------------------------

    def encrypt(self, initial_value: bytes, message: bytes): # -> bytes:
        """
        Pads the given message to a multiple of the block length,
        computes, and returns its encryption with AES-128-CBC-XMLPad.

        :param initial_value: 16-byte initial value.
        :param message: Plaintext of arbitrary length
        :return: Ciphertext whose length is a multiple of 16 bytes, but
        always at least the length of the message.
        """

        block_length = 16
        padding_necessary = ((len(message) % block_length) != 0)
        a_mess = message

        # if necessary: pad message so its length is a multiple of (or equal to) blocklength
        if padding_necessary:
            to_add = (block_length - len(message)) % block_length

            while padding_necessary:
                padding = bchr(to_add)
                a_mess += padding
                if (len(a_mess) % block_length) == 0:
                    padding_necessary = False
        print("Padded Message: ", a_mess)

        # AES encrypt
        cipher = AES.new(self.key, AES.MODE_CBC, initial_value)
        enc_msg = cipher.encrypt(a_mess)

        return enc_msg

    # ---------------------------------------------------------

    def verify_padding(self, initial_value: bytes, ciphertext: bytes): # -> bool:
        """
        Given a ciphertext, evaluates if the padding is correct.
        :param initial_value: 16-byte initial value.
        :param ciphertext: Ciphertext. Length must be multiple of 16 bytes.
        :return: True if padding is correct or there was no padding, and False otherwise.
        """
        
        msg = AES.new(self.key, AES.MODE_CBC, initial_value)
        dec_msg = msg.decrypt(ciphertext)

        block_length = len(initial_value)
        pad_val = dec_msg[-1]

        padding_correct = False

        if pad_val > block_length:
            print("Input is not padded or padding is wrong")

        else:
            for i in range(1, pad_val+1):
                if dec_msg[-i] == pad_val:
                    padding_correct = True
                else:
                    padding_correct = False
                    break;

            if padding_correct == False:
                # raise ValueError("Input is not padded or padding is wrong")
                print("Input is not padded or padding is wrong")
        
        return padding_correct
        
        #remove padding from ciphertext (not really necassary though^^)
        # l = len(ciphertext) - pad_val
        # without_padding = ciphertext[:l]
    
        # return dec_msg, without_padding
