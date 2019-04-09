from .utils.conversions import hex_byte_swap, int_to_nbyte_hex, int_to_varint

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
        if 'txid' in txin:
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
#asm https://bitcoin.stackexchange.com/questions/24651/whats-asm-in-transaction-inputs-scriptsig/24659

