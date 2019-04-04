from PyBitcoin import transaction_hash as th
import json
import os

DATADIR = 'data'
TXSDIR = os.path.join(DATADIR, 'txs')

os.makedirs(TXSDIR, exist_ok=True)

def pull_random_txs(n=20, path=TXSDIR):
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

def pull_random_cb_txs(n=20, path=TXSDIR):
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
        ind = str(i).zfill(3)
        block_num = str(tx['blockheight']).zfill(6)
        filename = os.path.join(path, f'coinbase_tx{block_num}.txt')
        with open(filename, 'w') as outfile:
            json.dump(tx, outfile)

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
        filename = os.path.join(TXSDIR, f'coinbase_tx{ind}.txt')
        with open(filename) as infile:
            tx = json.load(infile)
        yield (tx, filename)

def gen_alltxs():
    for filename in os.listdir(TXSDIR):
        filename = os.path.join(TXSDIR, filename)
        with open(filename) as infile:
            tx = json.load(infile)
        yield (tx, filename)

def test_hex_byte_swap():
    pairs = [
             ('6a',       '6a'),
             ('2602',     '0226'),
             ('703a0f00', '000f3a70')
            ]
    for h1, h2 in pairs:
        h3 = th.hex_byte_swap(h1)
        assert h3 == h2, f'Swap {h3} != {h2}'
        h4 = th.hex_byte_swap(h3)
        assert h4 == h1, f'Double swap {h4} != original {h1}'

def test_int_to_varint():
    pairs = [
                ('6a',         106),
                ('fd2602',     550),
                ('fe703a0f00', 998000),
                ('ff149af3458edb6200', 27825951823075860)
            ]
    for h, i in pairs:
        h1 = th.int_to_varint(i)
        assert h1 == h, f'int({i})->varint({h1}) != {h}'

def test_varint_to_int():
    pairs = [
                ('6a',         106),
                ('fd2602',     550),
                ('fe703a0f00', 998000),
                ('ff149af3458edb6200', 27825951823075860)
            ]
    for h, i in pairs:
        i1 = th.varint_to_int(h)
        assert i1 == i, f'varint({h})->int({i1}) != {i}'

def test_genesis_tx_to_hex():
    with open(os.path.join(DATADIR, 'genesis_tx.txt')) as infile:
        tx = json.load(infile)
        h = th.tx_to_hex(tx)
        assert h == tx['rawtx']

def test_tx_to_hex():
    """Test that all txs are built to their correct rawtx."""
    for tx, filename in gen_alltxs():
        rawtx = th.tx_to_hex(tx)
        assert rawtx == tx['rawtx'], (f'{filename} error in tx_to_hex')

def test_tx_to_hex_each():
    """Same as above test, but gives information about which files failed."""
    wrong = []
    error = []
    for tx, filename in gen_alltxs():
        try:
            rawtx = th.tx_to_hex(tx)
            if rawtx != tx['rawtx']:
                wrong.append(filename)
        except:
            error.append(filename)
    assert (len(wrong)==0) and (len(error)==0), (
        f'wrong {len(wrong)}: {wrong}\nerror {len(error)}: {error}')
