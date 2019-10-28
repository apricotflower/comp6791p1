import os
import PARAMETER
import shutil


def deleteblocks(path):
    for root, directories, files in os.walk("./" + path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for directory in directories:
            shutil.rmtree(os.path.join(root, directory))


if __name__ == '__main__':
    deleteblocks(PARAMETER.INDEX)

