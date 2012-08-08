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

		# BB (dave) should also have a list of doors (rectangles and links to places)
		# BB (dave) should also have a list of walls (impassible rectangles)

		self.surf = None
		self.LoadFromFile(strPath)
		
	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		# BB (dave) check if the player has hit one of the doors; if so,
		#  warp them to the associated world

		# BB (dave) if the player has hit a wall, push them back

		return;

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		# BB (dave) center the view based on where the player is?

		surfScreen.blit(self.surf, (10, 10))

	def LoadFromFile(self, strPath):
		"""Loads data from the given path and constructs the surface"""
		""" for the world."""

		class STATE:
			Table = 0
			Plan = 1

		# BB (dave) do more dictionary-style parsing instead -- allow arbitrary keys, etc.

		reColorSym = re.compile(r'^\s*(\S+):\s*color:\s*(\d+)\s*(\d+)\s*(\d+)')

		dSTile = 32
		state = STATE.Table
		mpSymSurf = {}
		llSym = []

		# Load symbol table and 2d array of symbols from the file

		fileIn = open(strPath, 'r')
		for line in fileIn:
			if state == STATE.Table:
				match = reColorSym.search(line)
				if match:
					sym = match.group(1)
					mpSymSurf[sym] = pygame.Surface((dSTile, dSTile))
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

		# Construct world surface from contained symbols

		# BB (dave) could have the symbols be ordered, and draw each symbol
		#  to its places here rather than just going through each tile...

		self.surf = pygame.Surface((cCol * dSTile, cRow * dSTile))
		for iRow, lSym in enumerate(llSym):
			for iCol, sym in enumerate(lSym):
				self.surf.blit(mpSymSurf[sym], (iCol * dSTile, iRow * dSTile))
