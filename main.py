from classes.user import User
import random
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64
from classes.utils import generate_private_key, sign_message
from keyboard import is_pressed
import sys
import json



users =[] 
lastTransaction = None
scrooge_private = None



def initialize_users():
    # Need to create a datastructure that stores the user
    users = []
    transactions = []

    for i in range(10):
        coinsList= []
        newUser = User(i)
        for j in range(10):
            cID = str(i*10+j)
            signature = sign_message(scrooge_private, str(cID))
            newUser.add_coin([cID, signature])
            transaction = {}
            transaction['previous_transaction'] = None
            transaction['sender'] = 'scrooge'
            transaction['receiver'] = newUser.user_id
            transaction['coin_id'] = cID
            transactions.append(transaction)

        print("User "+str(i)+"\n"+str(newUser.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))) 
        print("10 coins")
        users.append(newUser)
    return users, transactions

# def create_transaction(lastTransaction):
#     a_b = random.sample(users, 2)
#     a = a_b[0]
#     b = a_b[1]
#     while(len(a.coins)<1):
#         a_b = random.sample(users, 2)
#         a = a_b[0]
#         b = a_b[1]
#     amount = random.randint(1,len(a.coins))
#     coins = a.coins[:amount]
#     transaction = {}
#     transaction['previous_transaction'] = lastTransaction
#     transaction['sender'] = a.user_id
#     transaction['receiver'] = b.user_id
#     transaction['coins'] = coins
#     signature = a.sign_message(transaction.__str__())
#     transaction_hash = hash(str(transaction))
#     return transaction, signature, transaction_hash
    
def find_user(id):
    for user in users:
        if(user.user_id==id):
            return user
    return False

def verify_signature(j, signature):
    t = json.loads(j)
    with_bytes= signature.encode('utf-8')    
    b = base64.b64decode(with_bytes)
    sender_id = t['sender']
    public_key = scrooge_private.public_key()
    if(sender_id != 'scrooge'):
        sender = find_user(sender_id)
        public_key = sender.private_key.public_key() # TODO: Getter method for public key
    try:
        verify =  public_key.verify(
            signature = b,
            data= j.encode('utf-8'),
            padding = padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            algorithm= hashes.SHA256()
        )
        return verify
    except InvalidSignature:
        return False


# def complete_transaction(transaction):
#     sender_id = transaction['sender']
#     sender = find_user(sender_id)
#     receiver_id = transaction['receiver']
#     receiver = find_user(receiver_id)
#     coins = transaction['coins']
#     for coin in coins:
#         if(not sender.has_coin(coin)):
#             return False

#     for coin in coins:
#         sender.remove_coin(coin)
#         receiver.add_coin(coin)
    
#     return True


def sign_and_hash(message_type, message):
    dict_with_sig = {}
    if(message_type == "transaction"):
        dict_with_sig['transaction'] = message
    elif(message_type == "block"):
        dict_with_sig['block'] = message
    message_json = json.dumps(message)
    signature = sign_message(scrooge_private, message_json)
    encoded = base64.b64encode(signature)
    no_bytes = encoded.decode('utf-8')
    dict_with_sig['signature'] = no_bytes
    dict_json = json.dumps(dict_with_sig)
    dict_json_bytes = dict_json.encode('utf-8')
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(dict_json_bytes)
    hashed = digest.finalize()
    b64_hash = base64.b64encode(hashed).decode('utf-8')
    dictionary = {b64_hash : dict_with_sig}
    return dictionary

def verify_transaction(transaction, public_key):
    signature = transaction['signature']
    message = transaction['transaction']
    message_json = json.dumps(message)
    verification = verify_signature(message_json, signature)
    return verification

def create_block(queue):
    block = {}
    for item in queue:
        for key in item:
            verification = verify_transaction(item[key], scrooge_private.public_key())
            if(verification is None):
                block[key] = item[key]
    return block



if __name__ == "__main__":
    # orig_stdout = sys.stdout
    # f = open('out.txt', 'w')
    # sys.stdout = f
    scrooge_private = generate_private_key()
    users, init_transactions = initialize_users()
    queue = []
    # for transaction in init_transactions:
    for transaction in init_transactions:
        dictionary = sign_and_hash("transaction", transaction)
        queue.append(dictionary)
        if(len(queue)==10):
            block = create_block(queue)
            queue = []
            signed_block = sign_and_hash("block", block)
            print(signed_block)

    
    # l = {}
    # j = json.dumps(transaction)
    # l['transaction'] = transaction
    # s = sign_message(scrooge_private, j)
    # encoded = base64.b64encode(s)
    # print(encoded)
    # no_bytes = encoded.decode('utf-8')
    # l['signature'] = no_bytes
    # with_bytes= no_bytes.encode('utf-8')
    
    # print(hash(json.dumps(l)))
    # b = base64.b64decode(encoded)
    # print("=====")
    # print(s)
    # print("-----")
    # print(b)
    # # print(b)
    # print(verify_signature(j,b))
    # j2 = json.dumps(l)
    # print(j2)

    # blocks = []
    # j = 0
    # last_block = -1
    # try: 
    #     while True:
    #         if keyboard.press_and_release('space'):
    #             break
    #         print("============================")
    #         print("Initializing block number ",j)
    #         block = []
    #         for i in range(10):
    #             completed = False
    #             t, s, h = create_transaction(lastTransaction)
    #             # print(t, base64.b64encode(s))
    #             b = verify_signature(t,s)
    #             if (b is None):
    #                 completed = complete_transaction(t)
    #             if(completed):
    #                 lastTransaction = h
    #                 block.append([t, s ,h])
    #                 print("Transaction number ", j*10+i , " are completed")
    #                 print("Sender is "+str(t['sender']))
    #                 print("Receiver is "+str(t['receiver']))
    #                 print("Amount is "+str(len(t['coins']))) 
    #             else:
    #                 i-=1
    #         block_details = {'block':block, 'hash':hash(str(block)), 'id':j, 'previous_block':last_block}
    #         blocks.append(block_details)
    #         last_block = hash(str(block_details))
    #         sign_message(scrooge_private, str(last_block))
    #         j+=1
    #         print(block_details['hash'])
    #         print("Block appended ",j) 
    # except KeyboardInterrupt:
    #     SystemExit(0)
    #     # sys.stdout = orig_stdout
    #     # f.close()

    




