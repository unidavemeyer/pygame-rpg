# World.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame
import re

class World:
	"""Provides a world, which is a contiguous set of tiles/spaces"""
	""" where the player can navigate the hero.  Includes the ability"""
	""" to have "doors" that transport the hero/player to another world."""

	def __init__(self, strPath):
		Game.game.AddUpdate(self, 90)	# relatively late update
		Game.game.AddRender(self, 10)	# relatively early render (more on bottom)

		self.surf = None

		self.LoadFromFile(strPath)
		
	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		# BB (dave) check if the player has hit one of the doors; if so,
		#  warp them to the associated world

		return;

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		# BB (davidm) center the view based on where the player is?

		surfScreen.blit(self.surf, (10, 10))

	def LoadFromFile(self, strPath):
		"""Loads data from the given path and constructs the surface"""
		""" for the world."""

		class STATE:
			Table = 0
			Plan = 1

		reColorSym = re.compile(r'^\s*(\S+):\s*color:\s*(\d+)\s*(\d+)\s*(\d+)')

		state = STATE.Table
		mpSymSurf = {}
		llSym = []

		fileIn = open(strPath, 'r')
		for line in fileIn:
			if state == STATE.Table:
				match = reColorSym.search(line)
				if match:
					sym = match.group(1)
					mpSymSurf[sym] = pygame.Surface((16, 16))
					mpSymSurf[sym].fill(pygame.Color(
												int(match.group(2)),
												int(match.group(3)),
												int(match.group(4))))
				elif line.strip().lower() == 'plan:':
					state = STATE.Plan
				else:
					print "invalid input '%s' found reading symbol table from '%s'" % (line.strip(), strPath)
			else:
				llSym.append(line.strip())
		fileIn.close()
			
		cRow = len(llSym)
		cCol = len(llSym[0])

		self.surf = pygame.Surface((cCol * 16, cRow * 16))
		for iRow, lSym in enumerate(llSym):
			for iCol, sym in enumerate(lSym):
				self.surf.blit(mpSymSurf[sym], (iCol * 16, iRow * 16))
