from ..utils.conversions import (hex_byte_swap, int_to_nbyte_hex,
                                 int_to_varint, varint_to_int)
from ..utils.parse import split_next_varint, split_n_bytes

# http://learnmeabitcoin.com/glossary/transaction-data

def tx_to_raw(tx):
    """Sends the tx (dict) to raw hex value to be hashed."""
    # Version number - 4 bytes
    result = int_to_nbyte_hex(tx['version'], 4, lendian=True)

    # Number of inputs - Varint
    n_in = len(tx['vin'])
    result += int_to_varint(n_in)

    for i in range(n_in):
        txin = tx['vin'][i]

        # If it is a regular tx
        if 'scriptSig' in txin:
            # TXID - 32 bytes (Reversed)
            result += hex_byte_swap(txin['txid'])

            # Index of prev output - 4 bytes
            result += int_to_nbyte_hex(txin['vout'], 4, lendian=True)

            # sig on the scriptSig
            sig = txin['scriptSig']['hex']
        elif 'coinbase' in txin:
            result += int_to_nbyte_hex(0, 32, lendian=True)

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
        result += int_to_nbyte_hex((txin['sequence']), 4, lendian=True)

    # Number of outputs - Varint
    n_out = len(tx['vout'])
    result += int_to_varint(n_out)

    for i in range(n_out):
        txout = tx['vout'][i]

        # Hex value in satoshis - 8 bytes
        value = txout['value']
        s_value = int(value.replace('.', '')) # convert to satoshis
        result += int_to_nbyte_hex(s_value, 8, lendian=True)

        # scriptPubKey size - Varint
        sig = txout['scriptPubKey']['hex']
        # Size of scriptPubKey in bytes - Varint
        result += int_to_varint(len(sig)//2)

        # scriptPubKey
        result += sig

    # Locktime - 4 bytes
    result += int_to_nbyte_hex(tx['locktime'], 4, lendian=True)

    return result

def raw_to_tx(raw):
    """Converts the raw hex tx to a tx dict."""
    tx = dict()

    # Version - 4 bytes
    version, raw = split_n_bytes(raw, 4)
    tx['version'] = int(hex_byte_swap(version), 16)

    n_in, raw = split_next_varint(raw)
    n_in = varint_to_int(n_in)

    vin = []
    for _ in range(n_in):
        txin = {}

        # txid - 32 bytes
        txid, raw = split_n_bytes(raw, 32)
        txin['txid'] = hex_byte_swap(txid)

        # vout - 4 bytes
        vout, raw = split_n_bytes(raw, 4)
        txin['vout'] = int(hex_byte_swap(vout), 16)

        # Size of the scriptsig
        size, raw = split_next_varint(raw)

        # scriptsig - 'size' bytes
        sig, raw = split_n_bytes(raw, varint_to_int(size))

        # Check if coinbase
        if (txid == '0'*64) and (vout == 'f'*8):
            tx['isCoinbase'] = True
            label = 'coinbase'
        else:
            label = 'scriptSig'
            sig = {'hex': sig}

        txin[label] = sig

        # sequence - 4 bytes
        seq, raw = split_n_bytes(raw, 4)
        txin['sequence'] = int(hex_byte_swap(seq), 16)

        vin.append(txin)

    tx['vin'] = vin

    n_out, raw = split_next_varint(raw)
    n_out = varint_to_int(n_out)

    vout  = []
    for _ in range(n_out):
        txout = {}

        # value in satoshis - 8 bytes
        val, raw = split_n_bytes(raw, 8)
        val = int(hex_byte_swap(val), 16)
        txout['value'] = '{:.8f}'.format(val * 10**-8)

        # Size of the scriptpubkey
        size, raw = split_next_varint(raw)

        # scriptpubkey - 'size' bytes
        pubkey, raw = split_n_bytes(raw, varint_to_int(size))
        txout['scriptPubKey'] = {'hex': pubkey}

        vout.append(txout)

    tx['vout'] = vout

    # locktime = 4 bytes
    locktime, raw = split_n_bytes(raw, 4)

    tx['locktime'] = int(hex_byte_swap(locktime), 16)

    return tx
