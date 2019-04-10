from ..utils.conversions import (hex_byte_swap, int_to_nbyte_hex,
                                 int_to_varint, varint_to_int)
from ..utils.parse import split_next_varint, split_n_bytes


def blockheader_to_raw(block):
    # Version number - 4 bytes
    result = int_to_nbyte_hex(block['version'], 4, lendian=True)

    # Previous Block Hash - 32 bytes BE
    result += hex_byte_swap(block['previousblockhash'])

    # Merkle Root - 32 bytes BE
    result += hex_byte_swap(block['merkleroot'])

    # Time - 4 bytes LE
    # a6c8cb4d
    result += int_to_nbyte_hex(block['time'], 4, lendian=True)

    # Bits - 4 bytes LE
    # b3936a1a
    result += hex_byte_swap(block['bits'])

    # Nonce - 4 bytes LE
    # e3143991
    result += int_to_nbyte_hex(block['nonce'], 4, lendian=True)

    return result


def raw_to_blockheader(raw):
    pass
