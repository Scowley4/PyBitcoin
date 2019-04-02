from PyBitcoin import transaction_hash as th
import json
import os

DATADIR = 'data'

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





