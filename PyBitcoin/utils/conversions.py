def hex_byte_swap(h):
    """Swaps endianness of a hex value."""
    return bytes.fromhex(h)[::-1].hex()

def int_to_nbyte_hex(i, n, lendian=False):
    """Converts int to nbyte hex."""
    h = ('{:x}'.format(i)).zfill(n*2)
    if lendian:
        h = hex_byte_swap(h)
    return h

def int_to_varint(i):
    """Converts in to varint."""
    if i <= 0xfc:
        prefix = ''
        n_bytes = 1
    elif i <= 0xffff:
        prefix = 'fd'
        n_bytes = 2
    elif i <= 0xffffffff:
        prefix = 'fe'
        n_bytes = 4
    elif i <= 0xffffffffffffffff:
        prefix = 'ff'
        n_bytes = 8
    return prefix + int_to_nbyte_hex(i, n_bytes, lendian=True)

def varint_to_int(varint):
    """Converts a varint to int."""
    h = varint[2:] if len(varint)>2 else varint
    return int(hex_byte_swap(h), 16)


