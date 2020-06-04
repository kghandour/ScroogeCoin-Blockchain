# Scrooge Coin Emulation
If you are running MacOS, make sure you run the python script as admin. "keyboard" module is used and it requires administrator priveleges on Mac to access the space button to break the while loop.

## Modules used:
- ### cryptography
Used for RSA and hashing and signature validation.
- ### keyboard
Used to detect the space key press
- ### JSON, Base64, Random


## Initialization
``` main.py ```
is considered as scrooge. The first step is to generate the private/public key pair. 
The next step is to initialize users and the initial transactions. 
These transactions are then signed and hashed using scrooge's private key. Each transaction is then added to a queue and once the queue reaches 10 transactions, signature checks are done to ensure validity. 
After 10 transactions are checked, a block is created, signed and hashed using scrooge's private key.


## Transactions 
A ```while True``` loop is created that can be broken using the ```Space key```. 
A user is selected at random and the user object calls a create transaction method. 

### Create Transaction
Found in ```user.py```
A random user ID is selected. A random coin is selected for the transaction. A dictionary is of the transaction is created. 
For the previous transaction ID to be found ```find_previous_transactions``` method is called which loops over the blockchain until the ```coin id``` is found in a transaction and obtains that transaction hash. The last transaction with the coin_id is considered the correct ```previous transaction key```

The transaction is then signed and hashed using the user's private key. The transaction is added to a queue.

Once the queue reaches 10 or more transactions, checks are done to make sure that all transactions are valid.

#### Valid signature
Transaction's signature is checked using the user's public key. 

#### No Double spending
Checks all the entries in the queue to make sure that no two transactions has the same sender and the same coin ID. In which case the last transaction is removed from the queue.

### Block Creation
If the queue after the checks has less than 10 transactions, after additional transactions are done and the checks done, the first 10 transactions in the queue are used to create a block. 

Once the block is created and the previous block ID is found, and the block is signed and hashed using scrooge's private key, the transactions are completed. 

### Transaction completion
Each transaction is obtained, the sender is obtained. The sender user is then "notified" that the transaction is completed in which case the user then removes the coin from it. The receiver user is then "notified" that the transaction is completed in which case the user then removes the coin from it.

## Data Structures:
Coin - Dictionary:

{

    cID: coin signed by scrooge

}

Transactions - Dictionary:

{
 
    'sender': is the userID,
    'receiver': is the userID receiving the money,
    'coin_id': is a dictionary of the coin ID and the signature,
    'previous_transaction': is the hash of the previous transaction where the coin ID was transferred.

}

Block - Dictionary:

{

    [Transaction Hash]:Transaction,
    previous_block: previous block in the blockchain

}

Blockchain - Ordered Dictionary of blocks

{

    [Block Hash]: block

}

## Variables:
```utils.py``` 
- number_of_users=100
- blockchain = OrderedDict()



## Output
Initialization for the number of users and coins
```
User ID
public key
number of coins
```

Creating Transactions
```
Creating Transaction ID:  [Transaction ID]  User  [Sender ID]  Sending CoinID  [Coin ID]  to User  [Receiver ID]  Previous transaction ID  [Previous Transaction ID]
```

Detected Double spending
```
Double Spending, User  [ID]  Tried to pay coin ID {'[Coin ID]': '[Coin signature by scrooge]'} to Users  [First user ID]  and [Second user ID]
```

Block Creation
```
Creating a block
Adding to block Transaction ID:  [First transaction ID]
Adding to block Transaction ID:  [Second transaction ID]
Adding to block Transaction ID:  [Third transaction ID]
Adding to block Transaction ID:  [Fourth transaction ID]
Adding to block Transaction ID:  [Fifth transaction ID]
Adding to block Transaction ID:  [Sixth transaction ID]
Adding to block Transaction ID:  [Seventh transaction ID]
Adding to block Transaction ID:  [Eighth transaction ID]
Adding to block Transaction ID:  [Nineth transaction ID]
Adding to block Transaction ID:  [Tenth transaction ID]
Block ID:  [Block Hash]  Previous block ID  [Previous block hash]
```

