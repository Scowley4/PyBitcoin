from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Hash import SHA256

def doubleSHA256(bytedata):
    """Returns the byte rep of a double SHA256 hash of the input bytedata."""
    return (SHA256.new((SHA256.new(bytedata)).digest())).digest()

# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
def concathex_doubleSHA256(hex1, hex2):
    """Returns the doubleSHA256 concatination of two hexes.

    This function is used in the merkletree for bitcoin. Note that this handles
    the difference in endianness as well.
    """
    # Reverse for big-endian/little-endian conversion
    hash1 = bytes.fromhex(hash1)[::-1]
    hash2 = bytes.fromhex(hash2)[::-1]
    return double_SHA256(hash1+hash2)[::-1].hex()
