# Door.py
# Copyright (c) 2023 David J. Meyer

import Game
import pygame
import Vec



class Door:
	"""Provides a blocking but unlockable door in the world. Unlocked when the hero owns
	an Item with the required tag."""

	def __init__(self, mpVarValue, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)
		self.pos = Vec.Vec(x, y)

		self.fIsClosed = mpVarValue.get('door-closed', True)
		self.tagKey = mpVarValue.get('door-keytag', None)
		self.surfOpen = pygame.image.load(mpVarValue.get('door-img-open', 'door-open.png'))
		self.surfClosed = pygame.image.load(mpVarValue.get('door-img-closed', 'door-closed.png'))

		if self.fIsClosed:
			self.surf = self.surfClosed
		else:
			self.surf = self.surfOpen

		Game.game.AddUpdate(self)
		Game.game.AddRender(self)

	def Updatepri(self):
		return Game.UpdatePri.DOOR

	def OnUpdate(self):

		# Nothing to do if we're not closed

		if not self.fIsClosed:
			return

		# Check if the appropriate key is held

		for hero in Game.game.LHero():
			for item in hero.lItem:
				if item.FHasTag(self.tagKey):   # BB (davidm) need to use correct function here
					self.fIsClosed = False
					self.surf = self.surfOpen

	def Renderpri(self):
		return Game.RenderPri.DOOR

	def OnRender(self, surfScreen):
		surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))

	def Rect(self):
		return self.rect

	def FIsClosed(self):
		return self.fIsClosed

