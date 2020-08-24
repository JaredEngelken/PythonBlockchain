import hashlib
import time

class Transaction():
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount

class Block():        
    def __init__(self, timestamp, transactions, previousHash = ''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()
        
    def calculateHash(self):
        return(hashlib.sha256(str.encode(str(self.previousHash)+
                                         str(self.timestamp)+str(self.transactions)+
                                         str(self.nonce))).hexdigest())

    def __repr__(self):
        return "<\nBlock \ntimestamp:%s \ntransactions:%s \npreviousHash:%s \nhash:%s\n>" % (self.timestamp, self.transactions, self.previousHash, self.hash)
    
    def __str__(self):
        return str(self.__class__)+": "+str(self.__dict__)

    def mineBlock(self, difficulty):
        while(self.hash[0:difficulty] != ''.join(['0']*difficulty)):
              self.nonce += 1
              self.hash = self.calculateHash()

        print('Block mined: ',self.hash)

class Blockchain():
    def __init__(self):
        self.chain = [self.createGenisisBlock()]
        self.difficulty = 2
        self.pendingTransactions = []
        self.miningReward = 100

    def __str__(self):
        return str(self.__class__)+": "+str(self.__dict__)

    def createGenisisBlock(self):
        return(Block('01/01/2017', 'Genisis block', '0'))

    def getLatestBlock(self):
        return(self.chain[-1])

    def minePendingTransaction(self, miningRewardAddress):
        block = Block(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.pendingTransactions)
        block.mineBlock(self.difficulty)

        print('Block successfully mined.')
        self.chain.append(block)

        self.pendingTransactions = [Transaction(None, miningRewardAddress, self.miningReward)]

    def createTransaction(self,transaction):
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0

        for block in self.chain[1:]:
            for trans in block.transactions:
                if(trans.fromAddress == address):
                    balance -= trans.amount
                if(trans.toAddress == address):
                    balance += trans.amount

        return balance

    def isChainValid(self):
        for i in range(1,len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]

            if(currentBlock.hash != currentBlock.calculateHash()):
                return False
            if(currentBlock.previousHash != previousBlock.hash):
                return False
            
        return True

batCoin = Blockchain()

batCoin.createTransaction(Transaction('address1','address2',100))
batCoin.createTransaction(Transaction('address2','address1',50))

print('Starting the miner...')
batCoin.minePendingTransaction('jareds-address')

print('\nBalance of jared is', batCoin.getBalanceOfAddress('jareds-address'))

print('Starting the miner...')
batCoin.minePendingTransaction('jareds-address')

print('\nBalance of jared is', batCoin.getBalanceOfAddress('jareds-address'))
