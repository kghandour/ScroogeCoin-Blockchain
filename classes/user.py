from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class User:
    user_id = None
    private_key = None
    coins = []
    
    def __init__(self, userid, coinsList):
        self.private_key = self.generate_private_key()
        self.user_id = userid
        self.coins = coinsList

    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key
    
    def sign_message(self, message):
        signature = self.private_key.sign(
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def has_coin(self, cid):
        if(self.coins.__contains__(cid)):
            return True
        return False

    def remove_coin(self,cid):
        self.coins.remove(cid)
    
    def add_coin(self, cid):
        self.coins.append(cid)

