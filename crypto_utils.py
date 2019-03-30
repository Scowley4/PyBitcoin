from Crypto.Hash import SHA256

def double_SHA256(data):
    return (SHA256.new((SHA256.new(data)).digest())).digest()
