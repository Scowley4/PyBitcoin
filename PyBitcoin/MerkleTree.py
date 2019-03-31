try:
    from .crypto_utils import doubleSHA256, concathex_doubleSHA256
except ModuleNotFoundError:
    from crypto_utils import doubleSHA256, concathex_doubleSHA256

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
    def __init__(self, hashes=None, hash_func=concathex_doubleSHA256):
        if hashes is None:
            hashes = []

        self.hashes = hashes.copy()
        self.leafs = []
        self.hash_func = hash_func

        self.root = HashNode(None, None, None, self.hash_func, 0)

        self.depth = self.find_num_layers(len(self.hashes))

        self._init_from_hashes()

    def _init_from_hashes(self):
        def r_build(nodes, layer):
            if layer == 0:
                return nodes[0]
            new_nodes = []
            for i in range(0, len(nodes)-1, 2):
                new_node = HashNode(None, nodes[i], nodes[i+1],
                                    self.hash_func, layer-1)
                new_node.left.parent = new_node
                new_node.right.parent = new_node
                new_nodes.append(new_node)

            if len(nodes) % 2 == 1:
                new_node = HashNode(None, nodes[-1], None,
                                self.hash_func, layer-1)
                new_node.left.parent = new_node
                new_nodes.append(new_node)
            return r_build(new_nodes, layer-1)

        self.leafs = [LeafNode(None, h, self.depth) for h in self.hashes]

        # If only one hash, the root is just that hash
        if len(self.leafs) == 1:
            self.root = self.leafs[0]
            return
        self.root = r_build(self.leafs, self.depth)

    @staticmethod
    def find_num_layers(n):
        i = 0
        tot = 1
        while tot < n:
            i += 1
            tot *= 2
        return i

    def add_hash(self, hexhash):
        """Adds data to the merkletree.

        Constructs a node from the data and calls the add_node method."""
        if len(self.leafs) == 2**self.depth:
            self._change_root_add(hexhash)
        else:
            self._regular_add(hexhash)

    def _regular_add(self, hexhash):
        cur = self.leafs[-1].parent
        while cur.right is not None:
            cur = cur.parent

        # Just one layer above new node location
        if cur.layer == self.depth-1:
            new_node = LeafNode(cur, hexhash, self.depth)
            cur.right = new_node

        else:
            cur.right = HashNode(cur, None, None, self.hash_func, cur.layer+1)
            cur = cur.right
            while cur.layer != self.depth-1:
                cur.left = HashNode(cur, None, None, self.hash_func, cur.layer+1)

            new_node = LeafNode(cur, hexhash, self.depth)
            cur.left = new_node

        # Send the changes up the tree
        while cur is not None:
            cur.get_hexdigest(fresh=True)
            cur = cur.parent


    def _change_root_add(self, h):
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
    def __init__(self, parent, left, right, hash_func, layer):
        super().__init__(parent, left, right)
        self.hexdigest = None
        self.digest = None
        self.hash_func = hash_func
        self.layer = layer

    def get_hexdigest(self, fresh=False):
        if self.hexdigest is None or fresh:
            lhex = self.left.get_hexdigest()
            rhex = lhex if self.right is None else self.right.get_hexdigest()
            self.hexdigest = self.hash_func(lhex, rhex)
        return self.hexdigest

    def get_digest(self, fresh=False, r_fresh=False):
        if self.digest is None or fresh or r_fresh:
            self.digest = self.hash_func(self.left.get_digest(r_fresh, r_fresh) +
                                         self.right.get_digest(r_fresh, r_fresh))
        return self.digest

class LeafNode(Node):
    """"""
    def __init__(self, parent, hexhash, layer):
        super().__init__(parent, None, None)
        self.hexhash = hexhash
        self.layer = layer

    def get_hexdigest(self):
        return self.hexhash

    def get_digest(self, fresh=False, r_fresh=False):
        if self.digest is None or fresh or r_fresh:
            self.digest = self.hash_func(str(data).encode())
        return self.digest
