import classes.utils as utils
import json
import base64

def verify_signature(j, signature, public_key):
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
    block['previous_block'] = previous_block
    return block

def find_user(id, users):
    for user in users:
        if(user.user_id==id):
            return user
    return False