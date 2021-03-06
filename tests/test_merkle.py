import sys
for k in ['PyBitcoin', 'PyBitcoin.MerkleTree', 'PyBitcoin.utils']:
    try:
        del sys.modules[k]
    except KeyError:
        pass
from PyBitcoin.merkle import compute_merkle, MerkleTree
from PyBitcoin.utils.crypto import concathex_doubleSHA256

import json
import os
import testing_utils # utils for testing

DATADIR = 'data'
BLOCKSDIR = os.path.join(DATADIR, 'blocks')

def test_compute_merkle():
    """Test to make sure merkle root computation matches known root."""
    for block, filename in testing_utils.gen_allblocks():
        assert compute_merkle(block['tx'], concathex_doubleSHA256) == block['merkleroot'], (
        f'Merkle root computed in {filename} not equal to known root')

def test_merkletree_init():
    for block, filename in testing_utils.gen_allblocks():
        merk = MerkleTree(hashes=block['tx'], hash_func=concathex_doubleSHA256)
        roothex = merk.root.get_hexdigest()
        trueroothex = block['merkleroot']
        assert roothex == trueroothex, (
        f'{filename} : {roothex} == {trueroothex}')

def nonhash(hash1, hash2):
    return f'({hash1}+{hash2})'

def test_merkletree_init_one_nonhash():
    """Tests the case that there is just one element."""
    hashes = ['a']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    roothex = merk.root.get_hexdigest()
    print(hashes, '->', roothex)
    print('Height:', merk.height)
    assert roothex == 'a'
    assert merk.height == 0

def test_merkletree_init_even_nonhashes():
    """Tests the case that there is a power of two elements."""
    hashes_list = [('a', 'b'), ('a', 'b', 'c', 'd')]
    answers = [('(a+b)', 1), ('((a+b)+(c+d))', 2)]
    for hashes, (hex_ans, height_ans) in zip(hashes_list, answers):
        merk = MerkleTree(hashes=hashes, hash_func=nonhash)
        roothex = merk.root.get_hexdigest()
        print(hashes, '->', roothex)
        print('Height:', merk.height)
        assert roothex == hex_ans
        assert merk.height == height_ans

def test_merkletree_init_widow_nonhashes():
    hashes = ['a', 'b', 'c', 'd', 'e']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    roothex = merk.root.get_hexdigest()
    print(hashes, '->', roothex)
    print('Height:', merk.height)
    assert roothex == '(((a+b)+(c+d))+((e+e)+(e+e)))'
    assert merk.height == 3

def test_merkletree_regularadd_singlelayer_nonhashes():
    hashes = ['a', 'b', 'c']
    to_add = ['d']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    print('Before add:', merk.root.get_hexdigest())
    for l in to_add:
        merk.add_hash(l)
    roothex = merk.root.get_hexdigest()
    print('After add:', roothex)
    comp_roothex = compute_merkle(hashes+to_add, nonhash)
    assert roothex == comp_roothex, (f'{roothex} != {comp_roothex}')

def test_merkletree_regularadd_multilayer_nonhashes():
    hashes = ['a', 'b', 'c', 'd', 'e', 'f']
    to_add = ['g']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    print('Before add:', merk.root.get_hexdigest())
    for l in to_add:
        merk.add_hash(l)
    roothex = merk.root.get_hexdigest()
    print('After add:', roothex)
    comp_roothex = compute_merkle(hashes+to_add, nonhash)
    assert roothex == comp_roothex, (f'{roothex} != {comp_roothex}')

def test_merkletree_changerootadd_nonhashes():
    """Test the MerkleTree add function for change root add."""
    hashes = ['a', 'b']
    to_add = ['c']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    print('Before add:', merk.root.get_hexdigest())
    for l in to_add:
        merk.add_hash(l)
    roothex = merk.root.get_hexdigest()
    print('After add:', roothex)
    comp_roothex = compute_merkle(hashes+to_add, nonhash)
    assert roothex == comp_roothex, (f'{roothex} != {comp_roothex}')

def test_merkletree_add_fromnone_nonhashes():
    """Test the MerkleTree add function adding one from nothing."""
    hashes = []
    to_add = ['a']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    for l in to_add:
        merk.add_hash(l)
    roothex = merk.root.get_hexdigest()
    print('After add:', roothex)
    comp_roothex = compute_merkle(hashes+to_add, nonhash)
    assert roothex == comp_roothex, (f'{roothex} != {comp_roothex}')

def test_merkletree_add_nonhashes(verbose=False):
    """Test the MerkleTree add function building from nothing."""
    hashes = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    merk = MerkleTree(hash_func=nonhash)
    for i in range(len(hashes)):
        merk.add_hash(hashes[i])
        roothex = merk.root.get_hexdigest()
        if verbose:
            print(f'After add {hashes[i]}:', roothex)
            print()
        comp_roothex = compute_merkle(hashes[:i+1], nonhash)
        assert roothex == comp_roothex, (f'{roothex} != {comp_roothex}')

def test_merkletree_add_blocks():
    """Test the MerkleTree add function with real block data."""
    for block, filename in testing_utils.gen_allblocks():
        merk = MerkleTree(hash_func=concathex_doubleSHA256)
        for hexhash in block['tx']:
            merk.add_hash(hexhash)
        roothex = merk.root.get_hexdigest()
        trueroothex = block['merkleroot']
        assert roothex == trueroothex, (
        f'{filename} : {roothex} == {trueroothex}')


