import context
from PyBitcoin.MerkleTree import compute_merkle, bitcoin_hash

import json
import os

def pull_random_blocks(n=20, path='data'):
    """Makes data files to test in test_fixed_merkle."""
    from PyBitcoin import blockexplorer as be
    for i in range(n):
        block = be.get_random_block()
        ind = str(i).zfill(3)
        filename = os.path.join(path, f'random_block{ind}.txt')
        with open(filename, 'w') as outfile:
            json.dump(block, outfile)
        print(f'{i+1} block data collected', end='\r')

def test_compute_merkle():
    """Test to make sure merkle root computation matches known root."""
    for i in range(20):
        ind = str(i).zfill(3)
        filename = f'data/random_block{ind}.txt'
        with open(filename) as infile:
            block = json.load(infile)
        assert compute_merkle(block['tx'], bitcoin_hash) == block['merkleroot'], (
        f'Merkle root computed in {filename} not equal to known root')


