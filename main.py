from classes.user import User
import random
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64
from classes.utils import generate_private_key, sign_message, sign_and_hash
import classes.utils as utils
from keyboard import is_pressed
import sys
import json
from collections import OrderedDict



users =[] 
scrooge_private = None
queue = []



def initialize_users():
    # Need to create a datastructure that stores the user
    users = []
    transactions = []

    for i in range(utils.number_of_users):
        coinsList= []
        newUser = User(i)
        for j in range(10):
            cID = str(i*10+j)
            signature = sign_message(scrooge_private, str(cID))
            encoded = base64.b64encode(signature)
            no_bytes = encoded.decode('utf-8')
            coin_dict = {}
            coin_dict[cID] = no_bytes
            newUser.add_coin(coin_dict)
            transaction = {}
            transaction['previous_transaction'] = None
            transaction['sender'] = 'scrooge'
            transaction['receiver'] = newUser.user_id
            transaction['coin_id'] = json.dumps(coin_dict)
            transactions.append(transaction)

        utils.printLog("User "+str(i)+"\n"+str(newUser.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))) 
        utils.printLog("10 coins")
        users.append(newUser)
    return users, transactions

def verify_signature(j, signature):
    t = json.loads(j)
    with_bytes= signature.encode('utf-8')    
    b = base64.b64decode(with_bytes)
    sender_id = t['sender']
    public_key = scrooge_private.public_key()
    if(sender_id != 'scrooge'):
        sender = find_user(sender_id)
        public_key = sender.get_public_key()
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

def verify_transaction(transaction):
    signature = transaction['signature']
    message = transaction['transaction']
    message_json = json.dumps(message)
    verification = verify_signature(message_json, signature)
    return verification

def check_double(transaction, index):
    get_cID = transaction['coin_id']
    get_sender = transaction['sender']
    for index2, signed_transaction in enumerate(queue):
        for key in signed_transaction:
            q_transaction = signed_transaction[key]['transaction']
            if(get_cID==q_transaction['coin_id'] and get_sender==q_transaction['sender'] and index > index2):
                utils.printLog("Double Spending, User ",get_sender," Tried to pay coin ID",get_cID, "to Users ", transaction['receiver'], " and ", q_transaction['receiver'])
                queue.remove(queue[index])
                index-=1
                return True    
    return False

def doChecks(check_double_spending=False):
    for index, item in enumerate(queue):
        for key in item:
            verification = verify_transaction(item[key])
            if(verification is None):
                if(check_double_spending):
                    ds = check_double(item[key]['transaction'], index)
            else:
                queue.remove(queue[index])
                index-=1

def create_block(print_transactions=False):
    block = OrderedDict()
    for index in range(10):
        item = queue[index]
        for key in item:
            if(print_transactions):
                utils.printLog("Adding to block Transaction ID: ",key)
            block[key] = item[key]

    block['previous_block'] = utils.previous_block
    return block

def find_user(id):
    for user in users:
        if(user.user_id==id):
            return user
    return False

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
def complete_transaction(block):
    for key in block:
        if(key!="previous_block"):
            signed_t = block[key]
            transaction = signed_t['transaction']
            sender = find_user(transaction['sender'])
            cID = transaction['coin_id']
            sender.remove_coin(cID)
            receiver = find_user(transaction['receiver'])
            receiver.add_coin(cID)


if __name__ == "__main__":
    # orig_stdout = sys.stdout
    # f = open('out.txt', 'w')
    # sys.stdout = f
    scrooge_private = generate_private_key()
    users, init_transactions = initialize_users()

    
    # for transaction in init_transactions:
    for transaction in init_transactions:
        dictionary, _ = sign_and_hash("transaction", transaction, scrooge_private)
        queue.append(dictionary)
        if(len(queue)==10):
            doChecks(check_double_spending=False)
            block = create_block()
            queue = []
            signed_block, _  = sign_and_hash("block", block, scrooge_private)
            for key in signed_block:
                utils.blockchain[key] = signed_block[key]
    while True:
        if is_pressed(' '):
            utils.printLog("Created ", len(utils.blockchain), " blocks")
            SystemExit(0)
            break
        random_user_id = random.randint(0,utils.number_of_users-1)
        transaction = users[random_user_id].create_transaction()
        if(transaction is not None):
            queue.append(transaction)
        if(len(queue)>=10):
            doChecks(check_double_spending=True)
        if(len(queue)>=10):
            utils.printLog("Creating a block")
            block = create_block(print_transactions=True)
            queue = queue[10:]
            signed_block, _ = sign_and_hash("block", block, scrooge_private)
            for key in signed_block:
                utils.blockchain[key] = signed_block[key]
                utils.printLog("Block ID: ",key," Previous block ID ", block['previous_block'], " Block has pointer is signed. ")
            complete_transaction(block)
        # sys.stdout = orig_stdout
        # f.close()
    
    
    
    
    # l = {}
    # j = json.dumps(transaction)
    # l['transaction'] = transaction
    # s = sign_message(scrooge_private, j)
    # encoded = base64.b64encode(s)
    # utils.printLog(encoded)
    # no_bytes = encoded.decode('utf-8')
    # l['signature'] = no_bytes
    # with_bytes= no_bytes.encode('utf-8')
    
    # utils.printLog(hash(json.dumps(l)))
    # b = base64.b64decode(encoded)
    # utils.printLog("=====")
    # utils.printLog(s)
    # utils.printLog("-----")
    # utils.printLog(b)
    # # utils.printLog(b)
    # utils.printLog(verify_signature(j,b))
    # j2 = json.dumps(l)
    # utils.printLog(j2)

    # blocks = []
    # j = 0
    # last_block = -1
    # try: 
    #     while True:
    #         if keyboard.press_and_release('space'):
    #             break
    #         utils.printLog("============================")
    #         utils.printLog("Initializing block number ",j)
    #         block = []
    #         for i in range(10):
    #             completed = False
    #             t, s, h = create_transaction(lastTransaction)
    #             # utils.printLog(t, base64.b64encode(s))
    #             b = verify_signature(t,s)
    #             if (b is None):
    #                 completed = complete_transaction(t)
    #             if(completed):
    #                 lastTransaction = h
    #                 block.append([t, s ,h])
    #                 utils.printLog("Transaction number ", j*10+i , " are completed")
    #                 utils.printLog("Sender is "+str(t['sender']))
    #                 utils.printLog("Receiver is "+str(t['receiver']))
    #                 utils.printLog("Amount is "+str(len(t['coins']))) 
    #             else:
    #                 i-=1
    #         block_details = {'block':block, 'hash':hash(str(block)), 'id':j, 'previous_block':last_block}
    #         blocks.append(block_details)
    #         last_block = hash(str(block_details))
    #         sign_message(scrooge_private, str(last_block))
    #         j+=1
    #         utils.printLog(block_details['hash'])
    #         utils.printLog("Block appended ",j) 
        # sys.stdout = orig_stdout
        # f.close()

    




