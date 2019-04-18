import testing_utils # utils for testing

# Useful for debugging with ipython
testing_utils.reset_imports()
from PyBitcoin.block import bits_to_hex, hex_to_bits, bits_to_int, int_to_bits

BITSHEX = (
    # First block
    ('1d00ffff', '00ffff0000000000000000000000000000000000000000000000000000'),
    # https://bitcoin.stackexchange.com/questions/30467/what-are-the-equations-to-convert-between-bits-and-difficulty
    ('182815ee', '2815ee000000000000000000000000000000000000000000'),
    # https://stackoverflow.com/questions/22059359/trying-to-understand-nbits-value-from-stratum-protocol/22161019#22161019
    ('1b3cc366', '3cc366000000000000000000000000000000000000000000000000'),
)

def test_bits_to_hex():
    for bits, h in BITSHEX:
        assert bits_to_hex(bits) == h, (
            f'Incorrect conversion with bits {bits}')

def test_hex_to_bits():
    for bits, h in BITSHEX:
        assert hex_to_bits(h) == bits, (
            f'Incorrect conversion with bits {bits}')

def test_bits_to_int():
    for bits, h in BITSHEX:
        assert bits_to_int(bits) == int(h, 16), (
            f'Incorrect conversion with bits {bits}')

# Seems to not be unique... SO question open about it
# def test_int_to_bits():
#     for bits, h in BITSHEX:
#         assert int_to_bits(int(h, 16)) == bits, (
#             f'Incorrect conversion with bits {bits}')


