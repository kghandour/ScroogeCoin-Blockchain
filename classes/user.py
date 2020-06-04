import classes.utils as utils
import random
import json


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
                number = random.randint(0, utils.number_of_users-1)
            transaction = {}
            coin_entry = random.randint(0, len(self.coins)-1)
            cID = self.coins[coin_entry]
            transaction['previous_transaction'] = utils.find_previous_transaction(cID)
            transaction['sender'] = self.user_id
            transaction['receiver'] = number
            transaction['coin_id'] = cID
            dictionary, t_hash = utils.sign_and_hash('transaction', transaction, self.private_key)
            utils.printLog("Creating Transaction ID: ",t_hash, " User ",transaction['sender'], " Sending CoinID ",next(iter(transaction['coin_id']))," to User ",transaction['receiver'], " Previous transaction ID ",transaction['previous_transaction'])
            return dictionary
        return None

    def check_blockchain(self,block):
        for key in block:
            if(key!="previous_block"):
                signed_t = block[key]
                transaction = signed_t['transaction']
                sender = transaction['sender']
                receiver = transaction['receiver']
                cID = transaction['coin_id']
                if(self.user_id==sender):
                    print("User ",self.user_id," contains ",cID,"?",self.coins.__contains__(cID))
                    if(not self.coins.__contains__(cID)):
                        print(self.coins)
                        print(block)
                    self.coins.remove(cID)

                elif(self.user_id==receiver):
                    print("Receiving ",cID)
                    self.coins.append(cID)




