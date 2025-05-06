#This file will be containing all the encryption functions we are gonna use to encrypt user data

import base64
import hashlib
import asyncio
import random
import json
import sys
import onetimepad
import string
import zlib
#from functions.blowfish import *
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

with open('config.json', 'r') as f:
    config = json.load(f)

password = config['password']

abc = string.ascii_lowercase
one_time_pad = list(abc)
__key__ = hashlib.sha256(b'16-character key').digest()

async def encrypt_aes(raw):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key= __key__, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

async def decrypt_aes(enc):
    unpad = lambda s: s[:-ord(s[-1:])]

    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(__key__, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))

async def encrypt_one_time_pad(msg, key = password):
    cipher = onetimepad.encrypt(msg, key)
    return cipher

async def decrypt_one_time_pad(cipher, key = password):
    msg = onetimepad.decrypt(cipher, key)
    return msg

'''
async def base64_encode(msg):
    msg_bytes = msg.encode("ascii")
    base64_bytes = base64.b64decode(msg_bytes)
    str = base64_bytes.decode("ascii")
    return str


async def base64_decode(msg):
    msg_bytes = msg.encode("ascii")
    base64_bytes = base64.b64encode(msg_bytes)
    str = base64_bytes.decode("ascii")
    return str
'''

async def encrypt(email, password):
    enc_aes = await encrypt_aes(f"{email}:{password}")
    enc = enc_aes.decode('UTF-8')
    enc = await encrypt_one_time_pad(enc)
    #enc = await base64_encode(enc)
    return enc

async def decrypt(enc):
    #enc = await base64_decode(enc)
    enc = await decrypt_one_time_pad(enc)
    data = await decrypt_aes(enc)
    return data

async def split_email_password(enc):
    value = await decrypt(enc)
    value = value.split(':')
    email = value[0]
    password = value[1]
    return email, password

email = "me@lonelyguyy.me"
password = "i wonder..."
#enc = asyncio.run(encrypt(email, password))
#print(asyncio.run(decrypt(enc)))