import classes.utils as utils
import random


class User:
    user_id = None
    private_key = None
    coins = []
    
    def __init__(self, userid):
        self.private_key = utils.generate_private_key()
        self.user_id = userid
        self.coins = []

    def sign_message(self, message):
        return utils.sign_message(self.private_key, message)

    def has_coin(self, cid):
        if(self.coins.__contains__(cid)):
            return True
        return False

    def get_public_key(self):
        return self.private_key.public_key()

    def remove_coin(self,cid):
        self.coins.remove(cid)
    
    def add_coin(self, cid):
        self.coins.append(cid)


    def create_transaction(self):
        number = self.user_id
        if(len(self.coins)>0):
            while(number==self.user_id):
                number = random.randint(0, 9)
            transaction = {}
            cID = self.coins[0][0]
            print(cID)
            transaction['previous_transaction'] = utils.find_previous_transaction(cID)
            transaction['sender'] = self.user_id
            transaction['receiver'] = number
            transaction['coin_id'] = cID
            dictionary = utils.sign_and_hash('transaction', transaction, self.private_key)
            return dictionary



