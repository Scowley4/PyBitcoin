from PyBitcoin.transaction import tx_to_raw
import json
import os
import testing_utils # utils for testing

DATADIR = 'data'
TXSDIR = os.path.join(DATADIR, 'txs')

def test_genesis_tx_to_raw():
    with open(os.path.join(DATADIR, 'genesis_tx.txt')) as infile:
        tx = json.load(infile)
        h = tx_to_raw(tx)
        assert h == tx['rawtx']

def test_tx_to_raw():
    """Test that all txs are built to their correct rawtx."""
    for tx, filename in testing_utils.gen_alltxs():
        rawtx = tx_to_raw(tx)
        assert rawtx == tx['rawtx'], (f'{filename} error in tx_to_raw')

def test_tx_to_raw_each():
    """Same as test_tx_to_raw, but gives information about which files failed."""
    wrong = []
    error = []
    for tx, filename in testing_utils.gen_alltxs():
        try:
            rawtx = tx_to_raw(tx)
            if rawtx != tx['rawtx']:
                wrong.append(filename)
        except:
            error.append(filename)
    assert (len(wrong)==0) and (len(error)==0), (
        f'wrong {len(wrong)}: {wrong}\nerror {len(error)}: {error}')
