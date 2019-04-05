def compute_merkle(hashes, hash_func):
    # If there is one hash left, it is the root
    if len(hashes) == 1:
        return hashes[0]

    new_hashes = [hash_func(hashes[i], hashes[i+1])
                  for i in range(0, len(hashes)-1, 2)]
    # Odd number of hashes, hash the last with itself
    if len(hashes) % 2 == 1:
        new_hashes.append(hash_func(hashes[-1], hashes[-1]))
    return compute_merkle(new_hashes, hash_func)
