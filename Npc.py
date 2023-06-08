# Npc.py
#
# Copyright (c) 2012 by David Meyer

import Game
import Lib
import Item
import pygame
import random 
import Vec
 

class Npc:
	"""An Npc is an entity in the world that interacts with the Hero in some"""
	""" way.  Presumably the most common of these is an opponent with whom"""
	""" the Hero fights, but Npc also covers interactives like shopkeepers"""
	""" and quest givers, etc."""

	def __init__(self):
		Game.game.AddUpdate(self)
		Game.game.AddRender(self)

		self.pos = Vec.Vec(0,0)			# location in the world
		self.surf = None				# surface to render onto the screen

		self.hpMax = 100				# default max hp
		self.hpCur = self.hpMax			# default current hp

	def Kill(self):
		Game.game.RemoveNpc(self)
		Game.game.RemoveUpdate(self)
		Game.game.RemoveRender(self)

	def Updatepri(self):
		return Game.UpdatePri.NPC

	def OnUpdate(self):

		# Kill ourselves if hp has been exhausted

		if self.hpCur <= 0:
			self.Kill()

	def Renderpri(self):
		return Game.RenderPri.NPC

	def OnRender(self, surfScreen):
		if Game.game.Mode() == Game.Mode.WORLDMAP:
			surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))
			Lib.RenderHpBar(surfScreen, self.pos, self.hpCur, self.hpMax, False)

	def OnDamage(self, dHp):
		self.hpCur += dHp

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

	# BB (davidm) this is for the turn-based or time-based combat model, and is pretty much
	#  vestigial at this point -- consider removing

	def __init__(self, world, mpVarValue):
		Npc.__init__(self)

		self.hpMax = 20			# goons have few hitpoints
		self.hpCur = self.hpMax	#  ...
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
		self.dHpAttack = -5	# BB (davidm) currently unused
		self.hpMax = 50
		self.hpCur = self.hpMax
		self.surf = pygame.image.load(r"Amazoncrime.png")
	def OnRender(self, surfScreen):
		Npc.OnRender(self, surfScreen)

	def OnUpdate(self):
		self.Restart()
		Npc.OnUpdate(self)
		self.UpdateMove()

	def UpdateMove(self):
		# BB what do we want to do with multiple heros bros? - ZAC
		hero = Game.game.LHero()[0]
		dPos = hero.pos - self.pos
		dPosMove = Vec.VecLimitLen(dPos, random.randrange(1,6))
		self.SetPos(self.pos + dPosMove)
	def Restart(self):
		hero = Game.game.LHero()[0]
		if hero.hpCur <= 0:
			self.Kill()

class Fireball():
	
	def __init__(self, posStart, posEnd):
		self.pos = posStart
		self.posEnd = posEnd
		self.surf = pygame.image.load(r"Fiyaball.png")
		Game.game.AddUpdate(self)
		Game.game.AddRender(self)
	
	def Renderpri(self):
		return Game.RenderPri.FIREBALL

	def OnRender(self, surfScreen):
		surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))
	
	def Updatepri(self):
		return Game.UpdatePri.FIREBALL

	def OnUpdate(self):
		self.UpdateMove()
	
	def Kill(self):
		Game.game.RemoveUpdate(self)
		Game.game.RemoveRender(self)
	
	def	UpdateMove(self):
		hero = Game.game.LHero()[0]
		dPos = self.posEnd - self.pos
		sEnd = dPos.Len()
		sHero = (self.pos - hero.pos).Len()
		dPosdelay = Vec.VecLimitLen(dPos, 10)
		self.pos = self.pos + dPosdelay
		if sHero < 10.0:
			hero.OnDamage(-15)	# BB (davidm) unify damage numbers somewhere?
			self.Kill()
		elif sEnd < 1.0:
			self.Kill()

class Pattroler(Npc):
	def __init__(self, world, hero):
		Npc.__init__(self)

		self.hpMax = 800
		self.hpCur = self.hpMax
		self.posGoal = Vec.Vec(300,160)
		self.surf = pygame.image.load(r"broaintnoway.png")

	def OnUpdate(self):
		self.Restart()
		Npc.OnUpdate(self)
		self.UpdatePos()
	def Restart(self):
		hero = Game.game.LHero()[0]
		if hero.hpCur <= 0:
			self.Kill()

	def UpdatePos(self):
		dPosgoal = self.posGoal - self.pos
		dPosmove = Vec.VecLimitLen(dPosgoal, 2)
		self.SetPos(self.pos + dPosmove)
		if dPosgoal.Len() < 0.001:
			if self.pos.y >= 160:
				self.posGoal = Vec.Vec(300,60)# BB (Z) "should not be hard coded"
			elif self.pos.y == 60:
				self.posGoal = Vec.Vec(300, random.randrange(160,170))

class Boss(Pattroler):
	def __init__(self, world, hero):
		Pattroler.__init__(self, world, hero)#BB(Z) why include hero?
		self.hpMax = 999
		self.hpCur = self.hpMax
		self.tickAttack = 0
		self.tickAnimate = 0
		self.fIsStage2 = False
		self.fIsPrimed = False
		self.surf1 = pygame.image.load(r"Worker1.png")
		self.surf2 = pygame.image.load(r"Worker2.png")
		self.surf3 = pygame.image.load(r"Worker3.png")
		self.surf4 = pygame.image.load(r"Worker4.png")
		self.surf5 = pygame.image.load(r"Worker5.png")
		self.surf6 = pygame.image.load(r"Worker6.png")
		self.surfDef = pygame.image.load(r"Workerdef.png")
		self.surf = self.surfDef
	
	def OnUpdate(self):
		Pattroler.OnUpdate(self)
		if self.hpCur > 0.5 * self.hpMax:
			self.BossAttack()
		else:
			self.fIsStage2 = True
			self.BossAttack2()
		self.AnimationUpdate()
	
	def AnimationUpdate(self):
		tickCur = pygame.time.get_ticks()
		tickInAnim = tickCur - self.tickAnimate 
		if self.fIsStage2 == True:
			self.surf = self.surf6
		else:
			if tickInAnim <= 100:
				self.surf = self.surf1
			elif tickInAnim <= 210:	
				self.surf = self.surf2
			elif tickInAnim <= 270:	
				self.surf = self.surf3
			elif tickInAnim <= 300:
				self.surf = self.surf5
			elif tickInAnim <= 350:
				self.surf = self.surf6
				self.fIsPrimed = True
			elif tickInAnim <= 375:	
				self.surf = self.surf6
				if self.fIsPrimed:
					hero = Game.game.LHero()[0]
					fire = Fireball(self.pos, hero.pos)
					self.fIsPrimed = False
			elif tickInAnim <= 420:	
				self.surf = self.surf5
			elif tickInAnim <= 475:
				self.surf = self.surf4
			elif tickInAnim <= 520:	
				self.surf = self.surf3
			elif tickInAnim <= 560:	
				self.surf = self.surf2
			elif tickInAnim <= 595:
				self.surf = self.surf1
			else:
				self.surf = self.surfDef
	
	def BossAttack (self):
		tickCur = pygame.time.get_ticks()
		if tickCur - self.tickAttack < 2000:
			return
		self.tickAnimate = tickCur
		
		self.tickAttack = tickCur
	
	def BossAttack2 (self):
		tickCur = pygame.time.get_ticks()
		if tickCur - self.tickAttack < 400:
			return
		hero = Game.game.LHero()[0]
		fire = Fireball(self.pos, hero.pos)
		self.tickAttack = tickCur
		
	def Kill(self):
		"""Add a boss key item to the hero's inventory upon death"""

		# Add item to hero inventory; position at hero so we can update for auto-collect

		hero = Game.game.LHero()[0]
		itemKey = Item.Item(Game.game.World(), { 'tag': 'boss-key' }, hero.pos)
		itemKey.OnUpdate()

		# Run superclass behavior

		super().Kill()
