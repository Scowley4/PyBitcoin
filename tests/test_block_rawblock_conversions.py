import testing_utils # utils for testing

# Useful for debugging with ipython
testing_utils.reset_imports()

from PyBitcoin.block import blockheader_to_raw, raw_to_blockheader

def test_blockheader_to_raw():
    """Test that all blocks are built to their correct rawblockheader."""
    for block, filename in testing_utils.gen_allblocks():
        rawblockheader = blockheader_to_raw(block)
        assert rawblockheader == block['rawblockheader'], (
            f'{filename} error in blockheader_to_raw')

def test_blockheader_to_raw_each():
    """Same as test_blockheader_to_raw, but gives information about which files failed."""
    wrong = []
    error = []
    for block, filename in testing_utils.gen_allblocks():
        try:
            rawblockheader = blockheader_to_raw(block)
            if rawblockheader != block['rawblockheader']:
                wrong.append(filename)
        except:
            error.append(filename)
    assert (len(wrong)==0) and (len(error)==0), (
        f'wrong {len(wrong)}: {wrong}\nerror {len(error)}: {error}')


def test_raw_to_blockheader():
    """Test that all rawblockheaders are consistent with converted dict rep."""
    pass
