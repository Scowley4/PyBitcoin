from PyBitcoin.crypto_utils import doubleSHA256, concathex_doubleSHA256

class MerkleTree:
    """"""
    def __init__(self, hashes=None, hash_func=concathex_doubleSHA256):
        if hashes is None:
            hashes = []

        self.hashes = [h for h in hashes]
        self.leafs = [LeafNode(None, h, 0) for h in self.hashes]
        self.hash_func = hash_func

        self.root = HashNode(None, None, None, self.hash_func, 0)

        self.height = self.find_num_layers(len(self.hashes))

        self._init_from_hashes()

    def _init_from_hashes(self):

        # If no hashes:
        if len(self.leafs) == 0:
            return
        # If only one hash, the root is just that hash
        if len(self.leafs) == 1:
            self.root = self.leafs[0]
            return
        self.root = self._r_build(self.leafs, 0)

    def _r_build(self, nodes, layer):
        if layer == self.height:
            return nodes[0]
        new_nodes = []
        for i in range(0, len(nodes)-1, 2):
            new_node = HashNode(None, nodes[i], nodes[i+1],
                                self.hash_func, layer+1)
            new_node.left.parent = new_node
            new_node.right.parent = new_node
            new_nodes.append(new_node)

        if len(nodes) % 2 == 1:
            new_node = HashNode(None, nodes[-1], None,
                            self.hash_func, layer+1)
            new_node.left.parent = new_node
            new_nodes.append(new_node)
        return self._r_build(new_nodes, layer+1)

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
        if len(self.leafs) == 0:
            self.__init__([hexhash], self.hash_func)
        elif len(self.leafs) == 2**self.height:
            self._change_root_add(hexhash)
        else:
            self._regular_add(hexhash)

    def _regular_add(self, hexhash):
        # Find the node above the last leaf
        cur = self.leafs[-1].parent
        # Search for place that node doesn't have a right node
        while cur.right is not None:
            cur = cur.parent
        self._extend_tree(hexhash, cur)

    def _change_root_add(self, hexhash):
        # Increment height
        self.height += 1

        # Add the new root
        new_root = HashNode(None, self.root, None,
                            self.hash_func, self.height)
        self.root.parent = new_root
        self.root = new_root

        self._extend_tree(hexhash, new_root)


    def _extend_tree(self, hexhash, cur):
        """Fill in the tree to add hexhash to the tree."""

        # Just one layer above new node location
        if cur.layer == 1:
            new_node = LeafNode(cur, hexhash, 0)
            cur.right = new_node
        else:
            # First step is always right, since the tree fills in left to right
            cur.right = HashNode(cur, None, None, self.hash_func, cur.layer-1)
            cur = cur.right
            while cur.layer != 1:
                cur.left = HashNode(cur, None, None, self.hash_func, cur.layer-1)
                cur = cur.left
            new_node = LeafNode(cur, hexhash, 0)
            cur.left = new_node

        self.leafs.append(new_node)

        # Rehash cur and all nodes above it
        self._rehash(cur)


    def _rehash(self, cur):
        """Rehash this and all nodes above."""
        while cur is not None:
            cur.get_hexdigest(fresh=True)
            cur = cur.parent

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

class LeafNode(Node):
    """"""
    def __init__(self, parent, hexhash, layer):
        super().__init__(parent, None, None)
        self.hexhash = hexhash
        self.layer = layer

    def get_hexdigest(self):
        return self.hexhash
