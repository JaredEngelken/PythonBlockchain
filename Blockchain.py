import hashlib

class Block():        
    def __init__(self, index, timestamp, data, previousHash = ''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()
        
    def calculateHash(self):
        return(hashlib.sha256(str.encode(str(self.index)+str(self.previousHash)+
                                         self.timestamp+str(self.data)+
                                         str(self.nonce))).hexdigest())

    def __repr__(self):
        return "<\nBlock index:%s \ntimestamp:%s \ndata:%s \npreviousHash:%s \nhash:%s\n>" % (self.index, self.timestamp, self.data, self.previousHash, self.hash)
    
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
        self.difficulty = 5

    def __str__(self):
        return str(self.__class__)+": "+str(self.__dict__)

    def createGenisisBlock(self):
        return(Block(0, '01/01/2017', 'Genisis block', '0'))

    def getLatestBlock(self):
        return(self.chain[-1])

    def addBlock(self,newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

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
print('Mining block 1...')
batCoin.addBlock(Block(1,'01/05/2017',4))
print(batCoin)
print('Mining block 2...')
batCoin.addBlock(Block(2,'01/07/2017',10))

##print('Is blockchain valid? ',batCoin.isChainValid())
##
##batCoin.chain[1].data = 1000
##
##print('Is blockchain valid? ',batCoin.isChainValid())

print(batCoin)
