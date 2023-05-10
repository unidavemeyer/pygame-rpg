# Item.py
#
# Copyright (c) 2013 by David Meyer

import Game
import pygame
class Item:
	"""An Item is something that a Hero may keep in its inventory, and"""
	""" which is generally provided out in the world or from an Npc."""

	def __init__(self, world, mpVarValue, pos):
		self.pos = pos
		self.mpVarValue = mpVarValue
		Game.game.AddRender(self)
		Game.game.AddUpdate(self)
		self.surf = pygame.image.load(r"Superkey.png") #Dave BB: it would be cool or better if we took an image from something in this var value?; multiple keys.
	def Renderpri(self):
		return Game.RenderPri.ITEM
	
	def OnRender(self, surfScreen):
		surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))
	
	def FMatches(self, mpVarValue):
		if self.mpVarValue['tag'] == mpVarValue['tag']:
			return True
		else: 
			return False
	
	def FHasTag(self, tag):
		# BB (davidm) consider merging the FHasTag and FMatches concepts -- quite similar

		return self.mpVarValue['tag'] == tag

	def Updatepri(self):
		return Game.UpdatePri.ITEM
	
	def OnUpdate(self):
		hero = Game.game.LHero()[0]
		sHero = (self.pos - hero.pos).Len()
		if sHero < 10.0:
			Game.game.RemoveRender(self)
			Game.game.RemoveUpdate(self)
			hero.lItem.append(self)
