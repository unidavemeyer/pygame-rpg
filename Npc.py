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

	def __init__(self):
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

	def SetPos(self, pos):
		self.pos = pos


class Goon(Npc):
	"""Basic goon opponent.  Attacks on a regular schedule doing minor damage"""
	""" that never misses."""

	def __init__(self):
		Npc.__init__(self)

		self.hpCur = 20			# current hitpoints
		self.hpMax = 20			# max hitpoints
		self.dTAttack = 5		# seconds between attacks
		self.dHpAttack = -1		# hp damage dealt by each attack

		# override the default surface

		self.surf = pygame.Surface((32, 32))
		self.surf.fill(pygame.Color(255, 0, 0))

		self.ticks_last_attack = 0	# time of last attack

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		# Leave combat if we've been killed

		# BB (davidm) reward experience?  gold?  other?  use an end-of-combat mode?

		if self.hpCur <= 0:
			Game.game.RemoveNpc(self)
			Game.game.SetNpcCombatant(None)
			Game.game.RemoveUpdate(self, 30)	# BB (davidm) fragile coupling
			Game.game.RemoveRender(self, 80)	#  ...
			Game.game.SetMode(Game.Mode.WORLDMAP)
			return

		# early exit if it's not time to attack again

		ticksCur = pygame.time.get_ticks()
		if ticksCur - self.ticks_last_attack < self.dTAttack * 1000:
			return

		# do the attack

		self.ticks_last_attack = ticksCur
		Game.game.Hero().OnDamage(self.dTAttack)

		# BB (davidm) animate?  notify to screen?

	def OnDamage(self, damage):
		self.hpCur += damage

	def OnInteract(self):
		Game.game.SetNpcCombatant(self)
		Game.game.SetMode(Game.Mode.COMBAT)
		self.ticks_last_attack = pygame.time.get_ticks()
