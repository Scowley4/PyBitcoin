from PyBitcoin import transaction_hash as th
import json
import os
import testing_utils # utils for testing

DATADIR = 'data'
TXSDIR = os.path.join(DATADIR, 'txs')

def test_genesis_tx_to_hex():
    with open(os.path.join(DATADIR, 'genesis_tx.txt')) as infile:
        tx = json.load(infile)
        h = th.tx_to_hex(tx)
        assert h == tx['rawtx']

def test_tx_to_hex():
    """Test that all txs are built to their correct rawtx."""
    for tx, filename in testing_utils.gen_alltxs():
        rawtx = th.tx_to_hex(tx)
        assert rawtx == tx['rawtx'], (f'{filename} error in tx_to_hex')

def test_tx_to_hex_each():
    """Same as above test, but gives information about which files failed."""
    wrong = []
    error = []
    for tx, filename in testing_utils.gen_alltxs():
        try:
            rawtx = th.tx_to_hex(tx)
            if rawtx != tx['rawtx']:
                wrong.append(filename)
        except:
            error.append(filename)
    assert (len(wrong)==0) and (len(error)==0), (
        f'wrong {len(wrong)}: {wrong}\nerror {len(error)}: {error}')
