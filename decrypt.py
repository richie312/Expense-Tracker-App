# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

def decrypt(ciphered_text,key):
    key = key
    cipher_suite = Fernet(key)
    ciphered_text = ciphered_text
    unciphered_text = (cipher_suite.decrypt(ciphered_text))
    return unciphered_text


    