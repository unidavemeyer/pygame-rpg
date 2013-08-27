# World.py
#
# Copyright (c) 2012 by David Meyer

import Npc
import Game
import math
import pygame
import random
import re
import Vec
import yaml

class World:
	"""Provides a world, which is a contiguous set of tiles/spaces"""
	""" where the player can navigate the hero."""

	def __init__(self, strPath):
		self.surf = None				# surface to render to the screen
		self.lRectWall = []				# rectangles that are impassable
		self.lSpawner = []				# spawners
		self.lGate = []					# gates (go to other worlds)
		self.lPosStart = []				# start positions for hero characters
		self.lKey = []					# keys, which interact with locks or other keys
		self.lLock = []					# locks, which act as walls until unlocked

		self.LoadFromFile(strPath)
		
	def Kill(self):
		self.MakeInactive()

	def MakeActive(self):
		Game.game.SetWorld(self)
		Game.game.AddUpdate(self, 90)	# relatively late update
		Game.game.AddRender(self, 10)	# relatively early render (more on bottom)

		# Chose randomized starting locations for the heroes

		liPosStart = range(len(self.lPosStart))
		random.shuffle(liPosStart)

		# Ensure we have enough start indices for everyone

		lHero = Game.game.LHero()
		while len(liPosStart) < len(lHero):
			liPosStart.append(liPosStart[0])

		for iHero, hero in enumerate(Game.game.LHero()):
			posStart = self.lPosStart[liPosStart[iHero]]
			hero.SetPos(posStart)

	def MakeInactive(self):
		if Game.game.World() == self:
			Game.game.SetWorld(None)
		Game.game.RemoveUpdate(self, 90)
		Game.game.RemoveRender(self, 10)

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return

		# Let spawners we control do their things

		for spawner in self.lSpawner:
			spawner.OnUpdate()

		# Check for hero collisions with gates

		# BB (davidm) what do we do if we want multiple linked gates to have collisions
		#  simultaneously?  maybe provide some means by which to link gates together
		#  so they have required collisions on both?

		for hero in Game.game.LHero():
			rectHero = hero.Rect()
			for gate in self.lGate:
				if rectHero.colliderect(gate.rect):
					Game.game.SetNextWorld(gate.worldTarget)

		# Update key states

		for key in self.lKey:
			key.OnUpdate()

	def ColinfoFromRect(self, rectCheck):
		liRectCollide = []
		liRectCollide.extend(rectCheck.collidelistall(self.lRectWall))
		lRectCollide = [rect for iRect, rect in enumerate(self.lRectWall) if iRect in liRectCollide]
		
		for lock in self.lLock:
			if lock.FIsActive():
				continue

			if lock.rect.colliderect(rectCheck):
				lRectCollide.append(lock.rect)

		return Colinfo(lRectCollide)

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

		# Render keys

		for key in self.lKey:
			key.OnRender(surfScreen)

		# Render locks

		for lock in self.lLock:
			lock.OnRender(surfScreen)

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

		# Generate renderable surface, wall rectangles, and spawn locations

		# BB (dave) could have the symbols be ordered, and draw each symbol
		#  to its places here rather than just going through each tile...

		rectSize = pygame.Rect(0, 0, dSTile, dSTile)
		self.surf = pygame.Surface((cCol * dSTile, cRow * dSTile))

		for iRow, lSym in enumerate(llSym):
			for iCol, sym in enumerate(lSym):
				self.surf.blit(mpSecData['tiles'][sym]['surf'], (iCol * dSTile, iRow * dSTile), rectSize)

				if mpSecData['tiles'][sym].get('wall', False):
					self.lRectWall.append(pygame.Rect(iCol * dSTile, iRow * dSTile, dSTile, dSTile))
				
				if mpSecData['tiles'][sym].get('spawner', False):
					self.lSpawner.append(Spawner(
											mpSecData['tiles'][sym],
											iCol * dSTile + 0.5 * dSTile,
											iRow * dSTile + 0.5 * dSTile))

				if mpSecData['tiles'][sym].get('gate', False):
					self.lGate.append(Gate(
										mpSecData['tiles'][sym],
											iCol * dSTile,
											iRow * dSTile,
											dSTile,
											dSTile))

				if mpSecData['tiles'][sym].get('start', False):
					self.lPosStart.append(Vec.Vec(iCol * dSTile, iRow * dSTile))

				if mpSecData['tiles'][sym].get('key', False):
					self.lKey.append(Key(
										mpSecData['tiles'][sym],
										iCol * dSTile,
										iRow * dSTile,
										dSTile,
										dSTile))

				if mpSecData['tiles'][sym].get('lock', False):
					self.lLock.append(Lock(
										mpSecData['tiles'][sym],
										iCol * dSTile,
										iRow * dSTile,
										dSTile,
										dSTile))

		# Ensure we have a reasonable start position list (at least *some* start position)

		if not self.lPosStart:
			self.lPosStart.append(Vec.Vec(50, 50))

		# BB (davidm) post-process self.lRectWall to combine adjoining rectangles into
		#  larger contiguous chunks -- would speed collision checking, etc., but requires
		#  a clever/careful algorithm to expand things reasonably

		# Configure the keys (allow them to resolve their names to objects)

		for key in self.lKey:
			key.Configure(self.lKey, self.lLock)



class Gate:
	"""Gate class represents connection from one world to another.  When the player"""
	""" walks into a gate, they get warped to the start location of the linked world."""

	def __init__(self, mpVarValue, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)
		self.worldTarget = mpVarValue['target']



class Colinfo:
	"""Provides data about a collision.  Returned by collision checks"""
	""" against the world object."""

	def __init__(self, lRect):
		self.lRect = lRect



class Spawner:
	"""Spawns NPCs based on various guidelines when its world is active."""

	def __init__(self, mpVarValue, x, y):
		self.pos = Vec.Vec(x, y)

		self.npcType = mpVarValue['npc_type']
		self.cNpcMaxLifetime = mpVarValue.get('max_npcs', 0)
		self.cNpcMaxSimultaneous = mpVarValue.get('simultaneous_npcs', 0)
		self.sRadius = mpVarValue.get('spawn_radius', 64)

		self.lNpcCur = []
		self.cNpcLifetime = 0

	def FIsWithinLimits(self):
		if self.cNpcMaxLifetime > 0 and self.cNpcLifetime >= self.cNpcMaxLifetime:
			return False

		if self.cNpcMaxSimultaneous > 0 and len(self.lNpcCur) >= self.cNpcMaxSimultaneous:
			return False

		return True

	def OnUpdate(self):

		# Clear dead NPCs from our list of current NPCs

		setNpcGame = set(Game.game.LNpc())
		lNpcNew = [npc for npc in self.lNpcCur if npc in setNpcGame]
		self.lNpcCur = lNpcNew

		# Early exit if we couldn't spawn anything

		if not self.FIsWithinLimits():
			return

		# Early exit if any hero is too close by

		for hero in Game.game.LHero():
			if Vec.SDistPos(hero.Pos(), self.pos) < self.sRadius + 50:
				return

		# Generate NPCs up to our simultaneous & max lifetime limits

		cAttempt = 0

		while self.FIsWithinLimits() and cAttempt < 10:
			cAttempt += 1

			# Generate a location

			dPos = Vec.VecCircle(random.uniform(0, 2 * math.pi), random.uniform(0, self.sRadius))
			posCenter = self.pos + dPos
			posNpc = Vec.Vec(int(posCenter.x) - 16, int(posCenter.y) - 16)

			rectNpc = pygame.Rect(posNpc.x, posNpc.y, 32, 32)

			# Check vs. walls, other npcs

			if Game.game.World().ColinfoFromRect(rectNpc):
				continue

			fHitNpc = False

			for npc in Game.game.LNpc():
				if npc.Rect().colliderect(rectNpc):
					fHitNpc = True
					break

			if fHitNpc:
				continue

			self.NpcSpawn(posNpc)

	def NpcSpawn(self, pos):
		npc = Npc.Goon()	# BB (davidm) use self.npcType
		npc.SetPos(pos)
		Game.game.AddNpc(npc)

		self.lNpcCur.append(npc)
		self.cNpcLifetime += 1



class Key:
	"""Keys are picked up or activated when Heroes touch them.  They can"""
	""" be used to modify the state of Locks or other Keys."""

	def __init__(self, mpVarValue, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)

		# track what groups we activate (required)

		self.setStrGroupActivate = set(mpVarValue['activate_groups'])

		# track images for held/unheld states (required)

		# BB (davidm) for sticky keys, may make sense to not require a held
		#  image -- it could effectively be empty...

		self.surfHeld = pygame.image.load(mpVarValue['held_image'])
		self.surfUnheld = pygame.image.load(mpVarValue['unheld_image'])

		# track what group we are in (other keys, simultaneous activate)

		self.strGroup = mpVarValue.get('group', None)

		# track if we remain active after the player leaves

		self.fIsHoldSticky = mpVarValue.get('sticky', False)

		# track if we're initially active or not

		self.fIsActive = mpVarValue.get('active', True)

		# initialize other state

		self.fIsHeld = False
		self.fIsHeldByHero = False
		self.lObjActivate = []
		self.lKeyGroup = []

	def StrGroup(self):
		return self.strGroup

	def Configure(self, lKey, lLock):
		"""Converts string values into real objects after everything has been properly"""
		""" initialized."""

		# pull keys into activate & key groups

		for key in lKey:
			if key == self:
				continue

			if key.StrGroup() in self.setStrGroupActivate:
				self.lObjActivate.append(key)

			if self.strGroup != None and key.StrGroup() == self.strGroup:
				self.lKeyGroup.append(key)

		# pull locks into activate group

		for lock in lLock:
			if lock.StrGroup() in self.setStrGroupActivate:
				self.lObjActivate.append(lock)

	def FIsActive(self):
		return self.fIsActive

	def SetIsActive(self, fIsActive):
		self.fIsActive = fIsActive

	def SetIsHeld(self, fIsHeld):
		if self.fIsHeld == fIsHeld:
			return

		self.fIsHeld = fIsHeld

		# toggle activation state for anything involved, if all keys in the group
		#  are held

		# BB (davidm) logic here is funky

		fIsGroupHeld = fIsHeld

		for key in self.lKeyGroup:
			if not key.FIsHeld():
				fIsGroupHeld = False
				break

		if fIsGroupHeld:
			for obj in self.lObjActivate:
				obj.SetIsActive(fIsHeld)

	def FIsHeld(self):
		return self.fIsHeld

	def SetHeldByHero(self, fIsHeldByHero):
		if self.fIsHeldByHero == fIsHeldByHero:
			return

		self.fIsHeldByHero = fIsHeldByHero

		if fIsHeldByHero:
			self.SetIsHeld(True)
		elif not self.fIsHoldSticky:
			self.SetIsHeld(False)

	def OnUpdate(self):
		"""Check to see if any hero is currently on our space; adjust our hold state"""
		""" as appropriate."""

		if not self.FIsActive():
			return

		for hero in Game.game.LHero():
			self.SetHeldByHero(hero.Rect().colliderect(self.rect))

	def OnRender(self, surfScreen):
		if self.FIsActive():
			if self.FIsHeld():
				surfScreen.blit(self.surfHeld, (self.rect.x, self.rect.y))
			else:
				surfScreen.blit(self.surfUnheld, (self.rect.x, self.rect.y))



class Lock:
	"""Locks can be in open or closed states.  When open, they are passable"""
	""" and when closed, they act as walls.  Lock states are typically modified"""
	""" by Keys."""

	def __init__(self, mpVarValue, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)

		# track what group we are in (keys activate groups) (required)

		self.strGroup = mpVarValue['group']

		# track active and inactive images (required)

		self.surfActive = pygame.image.load(mpVarValue['active_image'])
		self.surfInactive = pygame.image.load(mpVarValue['inactive_image'])

		# track if we're initially active or not

		self.fIsActive = mpVarValue.get('active', False)

	def StrGroup(self):
		return self.strGroup

	def FIsActive(self):
		return self.fIsActive

	def SetIsActive(self, fIsActive):
		self.fIsActive = fIsActive

	def OnRender(self, surfScreen):
		if self.FIsActive():
			surfScreen.blit(self.surfActive, (self.rect.x, self.rect.y))
		else:
			surfScreen.blit(self.surfInactive, (self.rect.x, self.rect.y))
