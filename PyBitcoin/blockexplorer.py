import requests
import random

BASE = 'https://blockexplorer.com'

def get_random_block(a=0, b=269400):
    """Returns the JSON rep of a random block."""
    height = random.randint(a, b)
    return get_block(get_block_hash(height))

def get_random_tx():
    block = get_random_block()
    return get_tx(random.choice(block['tx']))

def get_block_hash(height):
    """Returns the string blockhash for a given blockheight."""
    return requests.get(BASE+f'/api/block-index/{height}').json()['blockHash']

def get_block(blockhash):
    """Returns the JSON rep of the block from a blockhash."""
    return requests.get(BASE+f'/api/block/{blockhash}').json()

def get_rawblock(blockhash):
    """Returns the byte rep of the block with the given blockhash."""
    return requests.get(BASE+f'/api/block/{blockhash}').json()['rawblock']

def get_tx(txid):
    """Returns the JSON rep of the TX with the given txid."""
    return requests.get(BASE+f'/api/tx/{txid}').json()

def get_rawtx(txid):
    """Returns the byte rep of the TX with the given txid."""
    return requests.get(BASE+f'/api/rawtx/{txid}').json()['rawtx']

def get_block_txs(blockhash):
    return requests.get(BASE+f'/api/txs/?block={blockhash}').json()
