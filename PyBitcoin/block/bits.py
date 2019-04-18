
def bits_to_hex(bits):
    """Converts compact bits rep to the hex target.
    """
    n_bytes = int(bits[:2], 16)
    prefix = bits[2:]
    target = prefix + '0'*((n_bytes-3)*2)
    return target

def hex_to_bits(h):
    n_bytes = len(h)//2
    return '{:x}'.format(n_bytes) + h[:6]

def bits_to_int(bits):
    return int(bits_to_hex(bits), 16)

def int_to_bits(i):
    return hex_to_bits('{:x}'.format(i))

