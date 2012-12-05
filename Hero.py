# Hero.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame
import Vec
import Weapon

class Hero:
	"""The game contains a single Hero instance, which handles input, rendering, and"""
	""" positioning in worldmap mode.  It also handles inventory functions, hit points,"""
	""" and other features of the character for worldmap and combat modes."""

	def __init__(self):
		Game.game.AddUpdate(self, 20)	# relatively early update
		Game.game.AddRender(self, 90)	# relatively late render (more on top)
		Game.game.AddHandler(self, 20)	# relatively early event handler

		# BB (dave) placeholder surface until we have a reasonable graphic

		self.surf = pygame.Surface((32, 32))
		self.surf.fill(pygame.Color(128, 128, 192))

		# Tracking for key events

		class KeyState:
			def __init__(self):
				self.Clear()

			def Clear(self):
				self.tickUp = 0
				self.tickDown = 0

			def FIsPressed(self):
				return self.tickDown > self.tickUp

			def TicksHeld(self):
				if not FIsPressed():
					return 0

				return pygame.time.get_ticks() - self.tickDown

		self.mpKeyState = {
				pygame.K_UP: KeyState(),
				pygame.K_DOWN: KeyState(),
				pygame.K_LEFT: KeyState(),
				pygame.K_RIGHT: KeyState(),
			}

		# position, velocity, etc.

		self.v = Vec.Vec(0, 0)
		self.pos = Vec.Vec(50, 50)

		# player statistics

		self.hpMax = 100
		self.hpCur = self.hpMax
		self.xp = 0

		# inventory

		self.gold = 0
		self.lItem = []
		self.weapon = Weapon.Sword()	# BB (davidm) placeholder for now

	def OnUpdate(self):
		if Game.game.Mode() == Game.Mode.COMBAT:

			# BB (dave) Handle damge, etc.

			# Give our weapon a chance to update

			if self.weapon:
				self.weapon.OnUpdate()

		elif Game.game.Mode() == Game.Mode.WORLDMAP:

			# Compute new velocity

			# We do a fairly simple "n% of the difference" approach here,
			#  which isn't a realistic acceleration, but lets us make things
			#  fairly rapid to collapse to the target velocity anyway

			# BB (dave) don't use fixed dT

			rdV = 0.6
			dT = 0.03

			vCur = self.v
			vTarget = self.VTargetCompute()
			dV = vTarget - vCur
			self.v = vCur + rdV * dV

			if dV.Len() < 0.5:
				self.v = vTarget

			if "DEBUG" == 0:
				print "vCur: %s vTarget: %s dV: %s vNext %s" % \
					(vCur, vTarget, dV, self.v)

			# Compute new position

			self.pos += dT * self.v

			# Check for collisions with the world

			rectHero = pygame.Rect(int(self.pos.x), int(self.pos.y), 32, 32)	# BB (davidm) don't hardcode size!
			colinfo = Game.game.World().ColinfoFromRect(rectHero)

			if colinfo:
				# BB (davidm) collision/velocity stuff should probably move to Colinfo class

				dX = 0.0
				dY = 0.0
				for rectWall in colinfo.lRect:
					rectIntersect = rectWall.clip(rectHero)

					if rectIntersect.width > rectIntersect.height:
						# collision in y direction

						if rectWall.centery > rectHero.centery:
							dY = min(-rectIntersect.height, dY)
						else:
							dY = max(rectIntersect.height, dY)
					else:
						# collision in x direction (left or right)

						if rectWall.centerx > rectHero.centerx:
							dX = min(-rectIntersect.width, dX)
						else:
							dX = max(rectIntersect.width, dX)

				# Resolve collision -- adjust position and velocity

				dPos = Vec.Vec(dX, dY)
				self.pos += dPos
				dV = (1.0 / dT) * dPos
				self.v += dV

			# Interact with an NPC if we should

			# BB (davidm) No ordering here; we'll interact with whatever NPC we happen to be
			#  in range of, and if multiple, whichever happens to be first in the game's NPC
			#  list.  Might consider doing something that involves priority here as well...

			for npc in Game.game.LNpc():
				if npc.FShouldInteract(self.pos):
					npc.OnInteract()
					break

	def FHandleEvent(self, event):
		if Game.game.Mode() == Game.Mode.COMBAT:

			# Clear key state map so that when we re-enter worlmap mode
			#  everything is cleaned up

			# BB (davidm) suggests we want to be notified when the mode changes instead
			#  so that we could do this just once on a boundary instead of every frame
			#  during combat mode...

			for ks in self.mpKeyState.values():
				ks.Clear()

			# Give current weapon a chance to handle the event

			if self.weapon:
				return self.weapon.FHandleEvent(event)

			return False

		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return False

		# BB (dave) handle 'i' key to go to inventory

		if event.type == pygame.KEYDOWN:
			keystate = self.mpKeyState.get(event.key)
			if keystate:
				keystate.tickDown = pygame.time.get_ticks()
				return True
		if event.type == pygame.KEYUP:
			keystate = self.mpKeyState.get(event.key)
			if keystate:
				keystate.tickUp = pygame.time.get_ticks()
				return True

		return False

	def OnRender(self, surfScreen):
		if Game.game.Mode() == Game.Mode.WORLDMAP:
			# BB (dave) very basic positioning here -- can flow off sides, no collision, etc.
			surfScreen.blit(self.surf, (int(self.pos.x), int(self.pos.y)))

		elif Game.game.Mode() == Game.Mode.COMBAT:
			# BB (davidm) draw the hero

			# draw current hp

			surfHp = Game.Font.FONT20.render("HP: %d/%d" % (self.hpCur, self.hpMax), False, pygame.Color(255, 255, 255))
			surfScreen.blit(surfHp, (20, 20))

			# Give our weapon a chance to render

			if self.weapon:
				self.weapon.OnRender(surfScreen)
		
	def OnDamage(self, damage):
		self.hpCur += damage

	def AddItem(self, item):
		self.lItem.append(item)

	def AddGold(self, dGold):
		self.gold += dGold

	def AddXp(self, dXp):
		self.xp += dXp

	def VTargetCompute(self):
		"""Uses current keyboard input to determine target velocity."""

		vMax = 180.0

		vY = 0.0

		ksUp = self.mpKeyState.get(pygame.K_UP)
		ksDown = self.mpKeyState.get(pygame.K_DOWN)

		if ksUp.FIsPressed() and not ksDown.FIsPressed():
			vY = -vMax
		elif ksDown.FIsPressed() and not ksUp.FIsPressed():
			vY = vMax

		vX = 0.0

		ksLeft = self.mpKeyState.get(pygame.K_LEFT)
		ksRight = self.mpKeyState.get(pygame.K_RIGHT)

		if ksLeft.FIsPressed() and not ksRight.FIsPressed():
			vX = -vMax
		elif ksRight.FIsPressed() and not ksLeft.FIsPressed():
			vX = vMax

		return Vec.Vec(vX, vY)
