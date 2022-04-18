from hashlib import sha256

class BlockService:

    def mine(self, leading_zeros, poolId):
        prefix = '0' * leading_zeros
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