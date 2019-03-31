import sys
for k in ['PyBitcoin', 'PyBitcoin.MerkleTree', 'PyBitcoin.crypto_utils']:
    try:
        del sys.modules[k]
    except KeyError:
        pass
from PyBitcoin.MerkleTree import compute_merkle, MerkleTree
from PyBitcoin.crypto_utils import concathex_doubleSHA256


import json
import os

BLOCKSDIR = os.path.join('data', 'blocks')


def pull_random_blocks(n=20, path=BLOCKSDIR):
    """Makes data files to test in test_fixed_merkle."""
    from PyBitcoin import blockexplorer as be
    blocks = []
    # To provide variety for tests
    nums = set()
    while len(nums) < n:
        block = be.get_random_block()
        if len(block['tx']) in nums:
            continue
        blocks.append(block)
        nums.add(len(block['tx']))
        i = len(block['tx'])
        print(f'{len(blocks)} block data collected', end='\r')
    print()
    blocks = sorted(blocks, key=lambda b: len(b['tx']))

    for i, block in enumerate(blocks):
        ind = str(i).zfill(3)
        filename = os.path.join(path, f'random_block{ind}.txt')
        with open(filename, 'w') as outfile:
            json.dump(block, outfile)
        print(filename)
        print()

def gen_testblocks():
    for i in range(20):
        ind = str(i).zfill(3)
        filename = os.path.join(BLOCKSDIR, f'random_block{ind}.txt')
        with open(filename) as infile:
            block = json.load(infile)
        yield (block, filename)

def test_compute_merkle():
    """Test to make sure merkle root computation matches known root."""
    for block, filename in gen_testblocks():
        assert compute_merkle(block['tx'], concathex_doubleSHA256) == block['merkleroot'], (
        f'Merkle root computed in {filename} not equal to known root')

def test_merkletree_init():
    for block, filename in gen_testblocks():
        merk = MerkleTree(hashes=block['tx'], hash_func=concathex_doubleSHA256)
        roothex = merk.root.get_hexdigest()
        trueroothex = block['merkleroot']
        assert roothex == trueroothex, (
        f'{filename} : {roothex} == {trueroothex}')

def nonhash(hash1, hash2):
    return f'({hash1}+{hash2})'

def test_merkletree_init_one_nonhash():
    # If just one TX, the merkleroot is just the TX hash
    hashes = ['a']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    roothex = merk.root.get_hexdigest()
    print(hashes, '->', roothex)
    print('Depth:', merk.depth)
    assert roothex == 'a'
    assert merk.depth == 0

def test_merkletree_init_even_nonhashes():
    hashes = ['a', 'b']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    roothex = merk.root.get_hexdigest()
    print(hashes, '->', roothex)
    print('Depth:', merk.depth)
    assert roothex == '(a+b)'
    assert merk.depth == 1

def test_merkletree_init_widow_nonhashes():
    hashes = ['a', 'b', 'c', 'd', 'e']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    roothex = merk.root.get_hexdigest()
    print(hashes, '->', roothex)
    print('Depth:', merk.depth)
    assert roothex == '(((a+b)+(c+d))+((e+e)+(e+e)))'
    assert merk.depth == 3

def test_merkletree_regularadd_singlelayer_nonhashes():
    hashes = ['a', 'b', 'c']
    to_add = ['d']
    merk = MerkleTree(hashes=hashes, hash_func=nonhash)
    print('Before add:', merk.root.get_hexdigest())
    merk.add_hash('d')
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


