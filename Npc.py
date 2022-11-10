# Npc.py
#
# Copyright (c) 2012 by David Meyer
import random 
import Game
import Item
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
		self.surf = None				# surface to render onto the screen

	def Kill(self):
		Game.game.RemoveNpc(self)
		Game.game.RemoveUpdate(self, 30)
		Game.game.RemoveRender(self, 80)

	def OnUpdate(self):
		# NOTE (davidm) no default behavior here

		pass

	def OnRender(self, surfScreen):
		if Game.game.Mode() == Game.Mode.WORLDMAP:
			surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))

	def OnDamage(self, damage):
		# NOTE (davidm) no default behavior here

		pass

	def OnLeaveWorld(self, world):
		"""Gives NPCs the option to handle world changes. Default behavior is for NPCs to kill themselves
		on world change, since that's typically what we want."""

		self.Kill()

	def Rect(self):
		"""Returns the rectangle that the NPC occupies in the world"""

		return pygame.Rect(int(self.pos.x), int(self.pos.y), 32, 32)

	def FShouldInteract(self, rectOther):
		"""Return true if this NPC should interact with something at the"""
		""" given rectangle (generally the Hero)."""

		return self.Rect().colliderect(rectOther)

	def OnInteract(self, hero):
		"""Begin interaction with the given hero."""

		# NOTE (davidm) no default behavior here

		pass

	def SetPos(self, pos):
		self.pos = pos

class Goon(Npc):
	"""Basic goon opponent.  Attacks on a regular schedule doing minor damage"""
	""" that never misses."""

	def __init__(self, world, mpVarValue):
		Npc.__init__(self)

		self.hpCur = 20			# current hitpoints
		self.hpMax = 20			# max hitpoints
		self.dTAttack = 5		# seconds between attacks
		self.dHpAttack = -1		# hp damage dealt by each attack

		# override the default surface

		# BB (davidm) load goon-specific settings from mpVarValue

		self.surf = pygame.Surface((32, 32))
		self.surf.fill(pygame.Color(255, 0, 0))

		self.ticks_last_attack = 0	# time of last attack

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		# Don't update if we're not in combat

		if Game.game.NpcCombatant() != self:
			return

		# Leave combat if we've been killed

		# BB (davidm) reward experience?  gold?  other?  use an end-of-combat mode?

		if self.hpCur <= 0:
			Game.game.SetNpcCombatant(None)
			self.Kill() # BB (davidm) may be fragile coupling here (old comment?)
			Game.game.SetMode(Game.Mode.WORLDMAP)
			return

		# early exit if it's not time to attack again

		ticksCur = pygame.time.get_ticks()
		if ticksCur - self.ticks_last_attack < self.dTAttack * 1000:
			return

		# do the attack

		# BB (davidm) not particularly suited to a multi-hero setup; should have
		#  a target hero instead, or should drop this notion entirely

		self.ticks_last_attack = ticksCur
		for hero in Game.game.LHero():
			hero.OnDamage(self.dHpAttack)

		# BB (davidm) animate?  notify to screen?

	def OnRender(self, surfScreen):
		Npc.OnRender(self, surfScreen)

		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		if Game.game.NpcCombatant() != self:
			return

		# BB (davidm) draw goon to screen

		# draw HP

		surfHp = Game.Font.FONT20.render("Goon HP: %d/%d" % (self.hpCur, self.hpMax), False, pygame.Color(255, 255, 255))
		surfScreen.blit(surfHp, (200, 20))

	def OnDamage(self, damage):
		self.hpCur += damage

	def OnInteract(self, hero):
		Game.game.SetNpcCombatant(self)
		Game.game.SetMode(Game.Mode.COMBAT)
		self.ticks_last_attack = pygame.time.get_ticks()



class Animal(Npc): 
	"""Animals are the rescuable characters that are out in carcar.  They get"""
	""" their configuration data from the spawner that makes them, can be"""
	""" rescued by a hero, have happy and sad states, etc."""

	def __init__(self, world, mpVarValue):
		Npc.__init__(self)

		self.surfHappy = None
		pathHappy = mpVarValue.get('happy_image')
		if pathHappy:
			self.surfHappy = pygame.image.load(pathHappy)

		self.surfSad = None
		pathSad = mpVarValue.get('sad_image')
		if pathSad:
			self.surfSad = pygame.image.load(pathSad)

		self.strGroup = mpVarValue.get('group', None)

		if self.strGroup:
			world.AddGroupMember(self.strGroup, self)

		fShouldBeActive = mpVarValue.get('active', False)
		self.fIsActive = 'uninit'
		self.SetIsActive(fShouldBeActive)

		# TODO: make a little move pattern list: (vx, vy, dt), ... to allow the animals to wander
		#  around a little bit to make them seem more alive

		self.lPatMove = mpVarValue.get('move_pattern', [])

	def OnUpdate(self):
		# TODO: move around, if we're configured to do so

		pass

	def OnInteract(self, hero):
		"""Causes the interacting hero to collect this animal."""

		# TODO: mark that the given hero collected us, and then Kill ourselves so we're
		#  out of the running lists of objects

		hero.AddItem(self.ItemStamp())

		# Done updating, etc., so go away

		self.Kill()

	def StrGroup(self):
		return self.strGroup

	def FIsActive(self):
		return self.fIsActive

	def SetIsActive(self, fIsActive):
		if self.fIsActive == fIsActive:
			return

		self.fIsActive = fIsActive

		if fIsActive:
			self.surf = self.surfHappy
		else:
			self.surf = self.surfSad

	def ItemStamp(self):
		"""Returns a "stamp" object that represents the collectible"""
		""" form of this animal."""

		return None



class HeroFinder(Npc):
	def __init__(self, world, hero):
		Npc.__init__(self)
		self.dHpAttack = 5
		self.hpCur = 50
		self.surf = pygame.image.load(r"Amazoncrime.png")

	def OnUpdate(self):
		self.UpdateMove()
		if self.GhpCur <= 0:
			self.Kill()

	def UpdateMove(self):
		# BB what do we want to do with multiple heros bros? - ZAC
		hero = Game.game.LHero()[0]
		dPos = hero.pos - self.pos
		dPosMove = Vec.VecLimitLen(dPos, random.randrange(1,6))
		self.SetPos(self.pos + dPosMove)
