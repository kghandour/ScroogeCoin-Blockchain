from classes.user import User
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64
from classes.utils import generate_private_key, sign_message
import keyboard


users =[] 
lastTransaction = -1
scrooge_private = None



def initialize_users():
    # Need to create a datastructure that stores the user
    users = []
    for i in range(10):
        coinsList= []
        for j in range(10):
            cID = str(i*10+j)
            signature = sign_message(scrooge_private, cID)
            coinsList.append([cID, signature])
        newUser = User(i, coinsList)
        users.append(newUser)
    return users

def create_transaction(lastTransaction):
    a_b = random.sample(users, 2)
    a = a_b[0]
    b = a_b[1]
    while(len(a.coins)<1):
        a_b = random.sample(users, 2)
        a = a_b[0]
        b = a_b[1]
    amount = random.randint(1,len(a.coins))
    coins = a.coins[:amount]
    transaction = {}
    transaction['previous_transaction'] = lastTransaction
    transaction['sender'] = a.user_id
    transaction['receiver'] = b.user_id
    transaction['coins'] = coins
    signature = a.sign_message(transaction.__str__())
    transaction_hash = hash(str(transaction))
    return transaction, signature, transaction_hash
    
def find_user(id):
    for user in users:
        if(user.user_id==id):
            return user
    return False

def verify_signature(transaction, signature):
    sender_id = transaction['sender']
    sender = find_user(sender_id)
    public_key = sender.private_key.public_key() # TODO: Getter method for public key
    try:
        verify =  public_key.verify(
            signature = signature,
            data= transaction.__str__().encode('utf-8'),
            padding = padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            algorithm= hashes.SHA256()
        )
        return verify
    except InvalidSignature:
        return False


def complete_transaction(transaction):
    sender_id = transaction['sender']
    sender = find_user(sender_id)
    receiver_id = transaction['receiver']
    receiver = find_user(receiver_id)
    coins = transaction['coins']
    owns_it = True
    for coin in coins:
        if(not sender.has_coin(coin)):
            return False

    for coin in coins:
        sender.remove_coin(coin)
        receiver.add_coin(coin)
    
    return True

if __name__ == "__main__":
    scrooge_private = generate_private_key()
    users = initialize_users()
    blocks = []
    j = 0
    last_block = -1
    while True:
        if keyboard.press_and_release('space'):
            break
        print("Initializing block number ",j)
        block = []
        for i in range(10):
            completed = False
            t, s, h = create_transaction(lastTransaction)
            # print(t, base64.b64encode(s))
            b = verify_signature(t,s)
            if (b is None):
                completed = complete_transaction(t)
            if(completed):
                lastTransaction = h
                block.append([t, s ,h])
                print("Transaction number ", j*10+i , " are completed")
            else:
                i-=1
        block_details = {'block':block, 'hash':hash(str(block)), 'id':j, 'previous_block':last_block}
        blocks.append(block_details)
        last_block = hash(str(block_details))
        sign_message(scrooge_private, last_block)
        j+=1
        print("Block appended ",j)   


    




