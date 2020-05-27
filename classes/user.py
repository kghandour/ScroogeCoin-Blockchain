import classes.utils as utils

class User:
    user_id = None
    private_key = None
    coins = []
    
    def __init__(self, userid):
        self.private_key = utils.generate_private_key()
        self.user_id = userid

    def sign_message(self, message):
        return utils.sign_message(self.private_key, message)

    def has_coin(self, cid):
        if(self.coins.__contains__(cid)):
            return True
        return False

    def remove_coin(self,cid):
        self.coins.remove(cid)
    
    def add_coin(self, cid):
        self.coins.append(cid)

