
def split_next_varint(raw):
    """Splits input string into the next varint and the rest."""
    prefix = int(raw[:2], 16)
    if prefix < 0xfc:
        split = 2
    elif prefix == 0xfd:
        split = 4
    elif prefix == 0xfe:
        split = 8
    elif prefix == 0xff:
        split = 16
    return raw[:split], raw[split:]

def split_n_bytes(raw, n):
    n *= 2
    return raw[:n], raw[n:]
