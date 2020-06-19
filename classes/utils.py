from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
import base64
from collections import OrderedDict
import os


blockchain = OrderedDict()
previous_block = None
previous_block_signature = None
number_of_users=10

def printLog(*args, **kwargs): # Stackoverflow: https://stackoverflow.com/questions/11325019/how-to-output-to-the-console-and-file
    print(*args, **kwargs)
    with open('output.txt','a') as file:
        print(*args, **kwargs, file=file)

def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key


def sign_message(pk, message):
    signature = pk.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def sign_and_hash(message_type, message, private_key):
    dict_with_sig = {}
    if(message_type == "transaction"):
        dict_with_sig['transaction'] = message
    elif(message_type == "block"):
        dict_with_sig['block'] = message
    message_json = json.dumps(message)
    signature = sign_message(private_key, message_json)
    encoded = base64.b64encode(signature)
    no_bytes = encoded.decode('utf-8')
    dict_with_sig['signature'] = no_bytes
    dict_json = json.dumps(dict_with_sig)
    dict_json_bytes = dict_json.encode('utf-8')
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(dict_json_bytes)
    hashed = digest.finalize()
    b64_hash = base64.b64encode(hashed).decode('utf-8')
    if(message_type == "block"):
        global previous_block
        previous_block = b64_hash
        global previous_block_signature
        signed_b = sign_message(private_key, b64_hash)
        encoded_b = base64.b64encode(signed_b)
        no_bytes_b = encoded_b.decode('utf-8')
        previous_block_signature = no_bytes_b
    dictionary = {b64_hash : dict_with_sig}
    return dictionary, b64_hash

def find_previous_transaction(cID):
    prev_transaction = None
    for key in blockchain:
        block = blockchain[key]['block']
        for transaction_key in block:
            if(transaction_key!='previous_block'):
                transaction = block[transaction_key]['transaction']
                try:
                    coin_id = json.loads(transaction['coin_id'])
                except:
                    coin_id = transaction['coin_id']
                for key in cID:
                    for key2 in coin_id:
                        if(key==key2):
                            prev_transaction = transaction_key
    return prev_transaction