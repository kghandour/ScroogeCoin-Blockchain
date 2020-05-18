from classes.user import User
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64

users =[] 

def initialize_users():
    # Need to create a datastructure that stores the user
    users = []
    for i in range(10):
        newUser = User(i)
        users.append(newUser)
    return users

def create_transaction():
    a_b = random.sample(users, 2)
    a = a_b[0]
    b = a_b[1]
    amount = random.random()*a.coins
    transaction = {}
    transaction['sender'] = a.user_id
    transaction['receiver'] = b.user_id
    transaction['amount'] = amount
    signature = a.sign_message(transaction.__str__())
    return transaction, signature, b
    
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


if __name__ == "__main__":
    users = initialize_users()
    t, s, wrong = create_transaction()
    print(t, base64.b64encode(s))
    b = verify_signature(t,s)
    print(b)

