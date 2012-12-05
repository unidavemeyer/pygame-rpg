# World.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame
import re
import yaml

class World:
	"""Provides a world, which is a contiguous set of tiles/spaces"""
	""" where the player can navigate the hero.  Includes the ability"""
	""" to have "doors" that transport the hero/player to another world."""

	def __init__(self, strPath):
		# BB (dave) should also have a list of gates (rectangles and links to places)
		# BB (dave) should also have a list of spawners (areas for NPCs to appear)
		# BB (dave) should also have a start point, maybe?  (where hero appears initially)

		self.surf = None				# surface to render to the screen
		self.lRectWall = []				# rectangles that are impassable

		self.LoadFromFile(strPath)
		
	def MakeActive(self):
		Game.game.SetWorld(self)
		Game.game.AddUpdate(self, 90)	# relatively late update
		Game.game.AddRender(self, 10)	# relatively early render (more on bottom)

	def MakeInactive(self):
		if Game.game.World() == self:
			Game.game.SetWorld(None)
		Game.game.RemoveUpdate(self, 90)
		Game.game.RemoveRender(self, 10)

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		return;

	def ColinfoFromRect(self, rect):
		liRectCollide = rect.collidelistall(self.lRectWall)
		if not liRectCollide:
			return None

		# Generate collision info summing up which rectangles were
		#  hit in the collision

		return Colinfo([rect for iRect, rect in enumerate(self.lRectWall) if iRect in liRectCollide])

	def OnRender(self, surfScreen):
		if Game.game.Mode() == Game.Mode.COMBAT:
			# BB (davidm) placeholder -- probably want to consider having an
			#  Arena class or somesuch instead of having the world draw here

			surfScreen.fill(pygame.Color(64, 64, 64))
			surfCombat = Game.Font.FONT25.render("Combat!", False, pygame.Color(255, 64, 64))
			surfScreen.blit(surfCombat, (50, 100))

		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return;

		# BB (dave) center the view based on where the player is?

		surfScreen.fill(pygame.Color(0, 0, 0))
		surfScreen.blit(self.surf, (0, 0))

	def LoadFromFile(self, strPath):
		"""Loads data from the given path and constructs the surface"""
		""" for the world."""

		# Load the file via YAML into a dictionary

		# Example world file
		#
		# tiles:
		#	a:
		#		color: [127, 127, 127]
		#		wall: true
		#	b:
		#		image: path/to/image.png
		# plan:
		#	- aaaaaa
		#	- abbbba
		#	- aaaaaa

		fileIn = open(strPath, 'r')
		mpSecData = yaml.load(fileIn)
		fileIn.close()

		# Add surfaces for each symbol as appropriate

		dSTile = 32

		for sym, mpSymData in mpSecData['tiles'].items():
			if mpSymData.get('color'):
				mpSymData['surf'] = pygame.Surface((dSTile, dSTile))
				mpSymData['surf'].fill(pygame.Color(*mpSymData['color']))
			elif mpSymData.get('image'):
				mpSymData['surf'] = pygame.image.load(mpSymData['image'])
			else:
				print "Warning:  symbol '%s' had no surface property" % sym

		# Validate floorplan

		llSym = mpSecData['plan']
		cRow = len(llSym)
		cCol = len(llSym[0])

		for iRow, lSym in enumerate(llSym):
			if len(lSym) != cCol:
				print "Warning:  invalid plan; row %d has %d values instead of %d" % (iRow + 1, len(lSym), cCol)

		# Convert dictionary data into a renderable surface and a list of wall rectangles

		# BB (dave) could have the symbols be ordered, and draw each symbol
		#  to its places here rather than just going through each tile...

		rectSize = pygame.Rect(0, 0, dSTile, dSTile)
		self.surf = pygame.Surface((cCol * dSTile, cRow * dSTile))
		for iRow, lSym in enumerate(llSym):
			for iCol, sym in enumerate(lSym):
				self.surf.blit(mpSecData['tiles'][sym]['surf'], (iCol * dSTile, iRow * dSTile), rectSize)

				if mpSecData['tiles'][sym].get('wall', False):
					self.lRectWall.append(pygame.Rect(iCol * dSTile, iRow * dSTile, dSTile, dSTile))

		# BB (davidm) post-process self.lRectWall to combine adjoining rectangles into
		#  larger contiguous chunks -- would speed collision checking, etc., but requires
		#  a clever/careful algorithm to expand things reasonably

		# TODO: Extract spawner tile locations from dictionary

		# TODO: Extract gate tile locations from dictionary



class Colinfo:
	"""Provides data about a collision.  Returned by collision checks"""
	""" against the world object."""

	def __init__(self, lRect):
		self.lRect = lRect
