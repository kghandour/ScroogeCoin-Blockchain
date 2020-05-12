from classes.user import User
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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
    return transaction, signature
    
def find_user(id):
    for user in users:
        if(user.user_id==id):
            return user
    return False

def verify_signature(transaction, signature):
    sender_id = transaction['sender']
    sender = find_user(sender_id)
    public_key = sender.private_key.public_key() # TODO: Getter method for public key
    verify =  public_key.verify(
        signature,
        transaction.__str__().encode(),
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return verify


if __name__ == "__main__":
    users = initialize_users()
    t, s = create_transaction()
    print(t, s)
    b = verify_signature(t,s)
    print(b)

