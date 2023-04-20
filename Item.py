# Item.py
#
# Copyright (c) 2013 by David Meyer

import Game

class Item:
	"""An Item is something that a Hero may keep in its inventory, and"""
	""" which is generally provided out in the world or from an Npc."""

	def __init__(self, world, mpVarValue, pos):
		print(world)
		print(mpVarValue)
		self.pos = pos
		self.mpVarValue = mpVarValue
		self.hero = Game.game.LHero()[0]
		i = mpVarValue.get('happy_image')
	def Renderpri(self):
		return Game.RenderPri.Item
	def OnRender(self, surfScreen):
		surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))
	
	def Updatepri(self):
		return Game.UpdatePri.Item
	def OnUpdate(self):
		self.sHero = (self.pos - hero.pos).Len()
		if self.sHero < 10.0:
			Game.game.RemoveRender()
			Game.game.RemoveUpdate()
			hero.lItem.append(self)