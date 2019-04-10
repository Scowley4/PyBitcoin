from Crypto.Hash import SHA256

# Don't need these right now, but maybe later?
# from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5

def doubleSHA256(bytedata):
    """Returns the byte rep of a double SHA256 hash of the input bytedata."""
    return (SHA256.new((SHA256.new(bytedata)).digest())).digest()

def h_doubleSHA256(h, reverse_in=False, reverse_out=False):
    """Returns the hex rep of a double SHA256 hash of the input hex.
    If reverse_in=True, input hex will be bytewise reversed before hash.
    if reverse_out=True, output hex will be bytewise reversed after hash.
    """
    b = bytes.fromhex(h)
    b = b[::-1] if reverse_in else b
    out_b = doubleSHA256(b)
    return out_b[::-1].hex() if reverse_out else out_b.hex()

# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
def concathex_doubleSHA256(hex1, hex2):
    """Returns the doubleSHA256 concatination of two hexes.

    This function is used in the merkletree for bitcoin. Note that this handles
    the difference in endianness as well.
    """
    # Reverse for big-endian/little-endian conversion
    bytes1 = bytes.fromhex(hex1)[::-1]
    bytes2 = bytes.fromhex(hex2)[::-1]
    return doubleSHA256(bytes1+bytes2)[::-1].hex()
