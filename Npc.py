# Npc.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame
import Vec

class Npc:
	"""An Npc is an entity in the world that interacts with the Hero in some"""
	""" way.  Presumably the most common of these is an opponent with whom"""
	""" the Hero fights, but Npc also covers interactives like shopkeepers"""
	""" and quest givers, etc."""

	def __init__(self)
		Game.game.AddUpdate(self, 30)	# relatively early update
		Game.game.AddRender(self, 80)	# relatively late render (more on top)

		self.pos = Vec.Vec(0,0)			# location in the world
		self.radius = 20				# range at which hero will interact
		self.surf = None				# surface to render onto the screen

	def OnUpdate(self):
		# NOTE (davidm) no default behavior here

		pass

	def OnRender(self, surfScreen):
		if Game.game.Mode() == Game.Mode.WORLDMAP:
			surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))

	def OnDamage(self, damage):
		# NOTE (davidm) no default behavior here

		pass

	def FShouldInteract(self, pos):
		"""Return true if this NPC should interact with something at the"""
		""" given position (generally the Hero)."""

		dPos = self.pos - pos
		dS = dPos.Len()

		return dS <= self.radius

	def OnInteract(self):
		"""Begin interaction.  Assumed that this will change the game mode"""
		""" and presumes that interaction is to be with the Hero."""

		# NOTE (davidm) no default behavior here

		pass
