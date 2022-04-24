from hashlib import sha256

class BlockService:

    def mine(self, poolId):
        prefix = '0' * 4
        if self.previousBlock is not None:
            self.previousHash = self.previousBlock.CurrentHash
        for i in range(1000000):
            self.Nonce = i
            digest = str(self.data) + str(i)
            if self.previousBlock is not None:
                digest += str(self.previousHash)
            digest = sha256(digest)
            if digest.startswith(prefix):
                self.CurrentHash = digest
                return