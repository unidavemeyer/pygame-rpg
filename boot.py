# bootstrap script
#
# We need this in cases where command line python isn't available, but we'd still
#  like to be able to see problems when they occur

import os
import subprocess
import sys

if __name__ == '__main__':
	# set up to run Game.py with the same python that ran this script

	lArg = [sys.executable, 'Game.py']

	# run Game.py and capture any resulting stdout/stderr stuff so we can see exceptions

	# NOTE (davidm) setting this should help the child python process not buffer (since it'll think that it
	#  should buffer output since it's not in an interactive terminal, etc.)

	os.environ['PYTHONUNBUFFERED'] = '1'

	# BB (davidm) The Popen docs say that trying to directly read from stdout/stderr/whatever is unsafe and
	#  can block, and thus we should use communicate(). However, communicate() also blocks until the child
	#  process is done...which means we only get output printed after the process is complete, which is
	#  specifically what I'm attempting to avoid.

	po = subprocess.Popen(lArg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

	for strOut in po.stdout:
		print(strOut, end='')
		if po.poll() != None:
			break

	# show what happened and pause so we can examine things

	x = input('Press enter to continue...')
