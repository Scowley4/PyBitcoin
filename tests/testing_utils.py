import json
import os
import sys

DATADIR = 'data'
BLOCKSDIR = os.path.join(DATADIR, 'blocks')
TXSDIR = os.path.join(DATADIR, 'txs')

os.makedirs(BLOCKSDIR, exist_ok=True)
os.makedirs(TXSDIR, exist_ok=True)

def reset_imports():
    keys = [k for k in sys.modules if 'PyBitcoin' in k]
    for k in keys:
        try:
            del sys.modules[k]
        except KeyError:
            pass


def is_consistent(obj1, obj2, verbose=False):
    """Basically checks for equality on two objects (recursively if needed).
    The main benefit of this is that the any dict objects don't need to match
    exactly; they only need to not contradict.

    For dicts
        (k1 in d1) and (k1 not in d2) -> fine
        (k2 in d2) and (k2 not in d1) -> fine

        d1[k] != d2[k] -> return False

    """

    # Make sure they are the same type
    if verbose:
        print('\t', end='')
    if not isinstance(obj1, type(obj2)):
        if verbose:
            print(f'TYPE ERROR {obj1} {obj2}')
        return False

    # If they are dicts, check that they don't contradict
    elif isinstance(obj1, dict):
        return dicts_contradict(obj1, obj2)

    # If they are lists, check each element
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            if verbose:
                print(f'LEN ERROR {obj1} {obj2}')
            return False
        for o1, o2 in zip(obj1, obj2):
            return is_consistent(o1, o2, verbose)

    # Otherwise check that they are equal
    elif type(obj1) in [int, float, str]:
        return obj1 == obj2
    else:
        print(type(obj1))
        raise ValueError

def dicts_contradict(d1, d2, verbose=False):
    """Only counts as contradicting if the same keys have contradicting values.
    Additional keys in either dictionary don't count as contradicting."""
    for k in d1:
        if k in d2:
            return is_consistent(d1[k], d2[k])


def pull_random_blocks(n=10, path=BLOCKSDIR):
    """Makes block data files to test block/merkle hashing."""
    from PyBitcoin import blockexplorer as be
    blocks = []
    for _ in range(n):
        block = be.get_random_block()
        rawblock = be.get_rawblock(block['hash'])
        block['rawblock'] = rawblock

        blocks.append(block)
        print(f'{len(blocks)} block data collected', end='\r')
    print()

    for i, block in enumerate(blocks):
        height = str(block['height']).zfill(6)
        filename = os.path.join(BLOCKSDIR, f'block{height}.txt')
        with open(filename, 'w') as outfile:
            json.dump(block, outfile)
        print(filename)
        print()

def pull_random_txs(n=10, path=TXSDIR):
    """Makes TX data files to test tx hashing."""
    from PyBitcoin import blockexplorer as be
    txs = []
    for i in range(n):
        tx = be.get_random_tx()
        rawtx = be.get_rawtx(tx['txid'])
        tx['rawtx'] = rawtx
        txs.append(tx)
        print(f'{i+1} tx data collected', end='\r')
    print()

    for i, tx in enumerate(txs):
        ind = str(i).zfill(3)
        filename = os.path.join(path, f'random_tx{ind}.txt')
        with open(filename, 'w') as outfile:
            json.dump(tx, outfile)

def pull_random_cb_txs(n=10, path=TXSDIR):
    """Makes TX data files to test tx hashing."""
    from PyBitcoin import blockexplorer as be
    txs = []
    for i in range(n):
        block = be.get_random_block()
        tx = None
        while tx is None:
            try:
                tx = be.get_tx(block['tx'][0]) # First TX is coinbase
            except:
                continue
        rawtx = be.get_rawtx(tx['txid'])
        tx['rawtx'] = rawtx
        txs.append(tx)
        print(f'{i+1} tx data collected', end='\r')
    print()

    for i, tx in enumerate(txs):
        block_num = str(tx['blockheight']).zfill(6)
        filename = os.path.join(path, f'coinbase_tx{block_num}.txt')
        with open(filename, 'w') as outfile:
            json.dump(tx, outfile)

def gen_allblocks():
    for filename in os.listdir(BLOCKSDIR):
        filename = os.path.join(BLOCKSDIR, filename)
        with open(filename) as infile:
            block = json.load(infile)
        yield (block, filename)

def gen_randomtxs():
    files = [f for f in os.listdir(TXSDIR) if 'random' in f]
    for filename in files:
        filename = os.path.join(TXSDIR, filename)
        with open(filename) as infile:
            tx = json.load(infile)
        yield (tx, filename)

def gen_coinbasetxs():
    files = [f for f in os.listdir(TXSDIR) if 'coinbase' in f]
    for filename in files:
        filename = os.path.join(TXSDIR, filename)
        with open(filename) as infile:
            tx = json.load(infile)
        yield (tx, filename)

def gen_alltxs():
    for filename in os.listdir(TXSDIR):
        filename = os.path.join(TXSDIR, filename)
        with open(filename) as infile:
            tx = json.load(infile)
        yield (tx, filename)

