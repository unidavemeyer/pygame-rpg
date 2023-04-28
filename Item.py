# Item.py
#
# Copyright (c) 2013 by David Meyer

import Game
import pygame

class Item:
	"""An Item is something that a Hero may keep in its inventory, and"""
	""" which is generally provided out in the world or from an Npc."""

	def __init__(self, world, mpVarValue, pos):
		print(world)
		print(mpVarValue)
		self.pos = pos
		self.mpVarValue = mpVarValue
		self.hero = Game.game.LHero()[0]
		#self.dPos = self.pos - hero.pos
		i = mpVarValue.get('happy_image')
		Game.game.AddRender(self)
		Game.game.AddUpdate(self)
		self.surf = pygame.image.load(r"Superkey.png")
	def Renderpri(self):
		return Game.RenderPri.ITEM
	def OnRender(self, surfScreen):
		surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))
	def	FMatches(self, mpVarValue):
		print(mpVarValue)
		if self.mpVarValue['tag'] == mpVarValue['tag']:
			print("checked item")
			return True
		else: 
			return False
	
	def Updatepri(self):
		return Game.UpdatePri.ITEM
	def OnUpdate(self):
		self.sHero = (self.pos - self.hero.pos).Len()
		print(self.sHero)
		if self.sHero < 10.0:
			Game.game.RemoveRender(self)
			Game.game.RemoveUpdate(self)
			self.hero.lItem.append(self)