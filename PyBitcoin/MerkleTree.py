from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from .crypto_utils import double_SHA256

# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
def bitcoin_hash(hash1, hash2):
    # Reverse for big-endian/little-endian conversion
    hash1 = bytes.fromhex(hash1)[::-1]
    hash2 = bytes.fromhex(hash2)[::-1]
    return double_SHA256(hash1+hash2)[::-1].hex()

def compute_merkle(hashes, hash_func):
    # If there is one hash left, it is the root
    if len(hashes) == 1:
        return hashes[0]

    new_hashes = [hash_func(hashes[i], hashes[i+1])
                  for i in range(0, len(hashes)-1, 2)]
    # Odd number of hashes, hash the last with itself
    if len(hashes) % 2 == 1:
        new_hashes.append(hash_func(hashes[-1], hashes[-1]))
    return compute_merkle(new_hashes, hash_func)

class MerkleTree:
    """"""
    def __init__(self, items=None, hash_func=double_SHA256):
        if items is None:
            items = []

        self.items = items.copy()
        self.root = None
        self.hash_func = hash_func

    def build_from_items(self, items):
        pass

    def add_data(self, data):
        """Adds data to the merkletree.

        Constructs a node from the data and calls the add_node method."""
        self.add_node(LeafNode(None, data))

    def add_node(self, node):
        """Inserts a new node into the tree."""
        pass

    def compute_root(self):
        pass

    def __contains__(self, item):
        pass

class Node:
    """"""
    def __init__(self, parent, left, right):
        self.parent = parent
        self.left = left
        self.right = right

class HashNode(Node):
    """"""
    def __init__(self, parent, left, right, hash_func):
        super().__init__(parent, left, right)
        self.digest = None
        self.hash_func = hash_func

    def get_digest(self, fresh=False, r_fresh=False):
        if self.digest is None or fresh or r_fresh:
            self.digest = self.hash_func(self.left.get_digest(r_fresh, r_fresh) +
                                         self.right.get_digest(r_fresh, r_fresh))
        return self.digest

class LeafNode(Node):
    """"""
    def __init__(self, parent, data, hash_func):
        super().__init__(parent, None, None)
        self.data = data
        self.digest = None
        self.hash_func = hash_func

    def get_digest(self, fresh=False, r_fresh=False):
        if self.digest is None or fresh or r_fresh:
            self.digest = self.hash_func(str(data).encode())
        return self.digest
