import Crypto.Hash.SHA256 as hash_func, binascii
tx = {
      'nVersion': '01000000',
      'inputs': {
        'count': '01',
        }
     }

def version_to_32bithex_LE(version):
    return bytes.fromhex('{:08X}'.format(version))[::-1].hex()

class Transaction:
    def __init__(self):
        pass



#asm https://bitcoin.stackexchange.com/questions/24651/whats-asm-in-transaction-inputs-scriptsig/24659




tx = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'

tx_bytes = bytes.fromhex(tx)

#hashed = double_SHA256(tx_bytes)
