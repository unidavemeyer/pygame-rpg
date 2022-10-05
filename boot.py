# bootstrap script
#
# We need this in cases where command line python isn't available, but we'd still
#  like to be able to see problems when they occur

import subprocess
import sys

if __name__ == '__main__':
    # set up to run Game.py with the same python that ran this script

    lArg = [sys.executable, 'Game.py']

    # run Game.py and capture any resulting stdout/stderr stuff so we can see exceptions

    res = subprocess.run(lArg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # show what happened and pause so we can examine things

    print(res.stdout)
    x = input('Press enter to continue...')
