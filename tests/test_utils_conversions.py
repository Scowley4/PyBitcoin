from PyBitcoin.utils.conversions import (hex_byte_swap, int_to_nbyte_hex,
                                         int_to_varint, varint_to_int)

def test_hex_byte_swap():
    pairs = [
             ('6a',       '6a'),
             ('2602',     '0226'),
             ('703a0f00', '000f3a70')
            ]
    for h1, h2 in pairs:
        h3 = hex_byte_swap(h1)
        assert h3 == h2, f'Swap {h3} != {h2}'
        h4 = hex_byte_swap(h3)
        assert h4 == h1, f'Double swap {h4} != original {h1}'

def test_int_to_nbyte_hex():
    cases = [
            # int, n, lendian
             ((  0, 4,  True), '00000000'),
             ((  0, 4, False), '00000000'),
             ((  1, 4,  True), '01000000'),
             ((  1, 4, False), '00000001'),
             (( 10, 2,  True),     '0a00'),
             (( 10, 2, False),     '000a'),
            ]

    for args, h in cases:
        h2 = int_to_nbyte_hex(*args)
        assert h2 == h, f'nbyte {h2} != {h}'

def test_int_to_varint():
    pairs = [
                ('6a',         106),
                ('fd2602',     550),
                ('fe703a0f00', 998000),
                ('ff149af3458edb6200', 27825951823075860)
            ]
    for h, i in pairs:
        h1 = int_to_varint(i)
        assert h1 == h, f'int({i})->varint({h1}) != {h}'

def test_varint_to_int():
    pairs = [
                ('6a',         106),
                ('fd2602',     550),
                ('fe703a0f00', 998000),
                ('ff149af3458edb6200', 27825951823075860)
            ]
    for h, i in pairs:
        i1 = varint_to_int(h)
        assert i1 == i, f'varint({h})->int({i1}) != {i}'


