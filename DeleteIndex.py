import shutil
import os
import PARAMETER


def deleteblocks(path):
    for root, directories, files in os.walk("./" + path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for directory in directories:
            shutil.rmtree(os.path.join(root, directory))

if __name__ == '__main__':
    deleteblocks(PARAMETER.BLOCK_PATH)
    deleteblocks(PARAMETER.MERGE_BLOCK_PATH)
    deleteblocks(PARAMETER.NO_NUMBER_BLOCK_PATH)
    deleteblocks(PARAMETER.NO_NUMBER_MERGE_BLOCK_PATH)
    deleteblocks(PARAMETER.CASE_FOLDING_BLOCK_PATH)
    deleteblocks(PARAMETER.CASE_FOLDING_MERGE_BLOCK_PATH)
    deleteblocks(PARAMETER.STOP_WORDS_30_BLOCK_PATH)
    deleteblocks(PARAMETER.STOP_WORDS_30_MERGE_BLOCK_PATH)
    deleteblocks(PARAMETER.STOP_WORDS_150_BLOCK_PATH)
    deleteblocks(PARAMETER.STOP_WORDS_150_MERGE_BLOCK_PATH)
