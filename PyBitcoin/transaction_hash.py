import Crypto.Hash.SHA256 as hash_func, binascii

def hex_byte_swap(h):
    return bytes.fromhex(h)[::-1].hex()

def int_to_4bytehex_LE(i):
    return hex_byte_swap('{:08x}'.format(i))

def int_to_nbyte_hex(i, n, lendian=True):
    h = ('{:x}'.format(i)).zfill(n*2)
    if lendian:
        h = hex_byte_swap(h)
    return h

def int_to_varint(i):
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
    return prefix + int_to_nbyte_hex(i, n_bytes)


def varint_to_int(varint):
    h = varint[2:] if len(varint)>2 else varint
    return int(hex_byte_swap(h), 16)

def tx_to_hex(tx):
    """Sends the tx (dict) to raw hex value to be hashed."""
    # Version number - 4 bytes
    result = int_to_nbyte_hex(tx['version'], 4)

    # Number of inputs - Varint
    n_in = len(tx['vin'])
    result += int_to_varint(n_in)

    for i in range(n_in):
        txin = tx['vin'][i]

        # If it is a regular tx
        if 'txid' in txin:
            # TXID - 32 bytes (Reversed)
            result += hex_byte_swap(txin['txid'])

            # Index of prev output - 4 bytes
            result += int_to_nbyte_hex(txin['vout'], 4)

            # sig on the scriptSig
            sig = txin['scriptSig']['hex']
        elif 'coinbase' in txin:
            result += int_to_nbyte_hex(0, 32)

            # Index is max - 4 bytes
            result += 'f'*8

            # sig on the coinbase
            sig = txin['coinbase']
        else:
            raise ValueError('txin has no txid or coinbase')

        # Size of scriptSig in bytes - Varint
        result += int_to_varint(len(sig)//2)

        # scriptSig
        result += sig

        # NOTE I'm not sure what the sequence is - 4 bytes
        print(txin)
        result += int_to_nbyte_hex((txin['sequence']), 4)

    # Number of outputs - Varint
    n_out = len(tx['vout'])
    result += int_to_varint(n_out)

    for i in range(n_out):
        txout = tx['vout'][i]

        # Hex value in satoshis - 8 bytes
        value = txout['value']
        s_value = int(value.replace('.', '')) # convert to satoshis
        result += int_to_nbyte_hex(s_value, 8)

        # scriptPubKey size - Varint
        sig = txout['scriptPubKey']['hex']
        # Size of scriptPubKey in bytes - Varint
        result += int_to_varint(len(sig)//2)

        # scriptPubKey
        result += sig

    # Locktime - 4 bytes
    result += int_to_nbyte_hex(tx['locktime'], 4)

    return result


class Transaction:
    def __init__(self):
        pass



#asm https://bitcoin.stackexchange.com/questions/24651/whats-asm-in-transaction-inputs-scriptsig/24659




#tx = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'

#tx_bytes = bytes.fromhex(tx)

#hashed = double_SHA256(tx_bytes)
genesis_tx = {
    'txid': '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
    'version':  1,
    'locktime': 0,
    'vin': [{'txid': '0000000000000000000000000000000000000000000000000000000000000000',
             'vout': 0xffffffff,
             'scriptSig': {'hex': '04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73'}
    }],
    'vout': [{'value': '50.00000000',
              'scriptPubKey': {'hex': '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac'}
     }],
    'rawtx': '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'
}
