# World.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame

class World:
	"""Provides a world, which is a contiguous set of tiles/spaces"""
	""" where the player can navigate the hero.  Includes the ability"""
	""" to have "doors" that transport the hero/player to another world."""

	def __init__(self, strPath):
		Game.game.AddUpdate(self, 90)	# relatively late update
		Game.game.AddRender(self, 10)	# relatively early render (more on bottom)

		self.surf = pygame.Surface()	# BB (dave) right plan?

		# BB (dave) read strPath and fill in self.surf based on its contents
		
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

		surfScreen.blit(self.surf)
