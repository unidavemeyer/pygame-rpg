# Hero.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame
import Vec

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
		self.pos = Vec.Vec(0, 0)

		# player statistics

		self.hpMax = 100
		self.hpCur = self.hpMax
		self.xp = 0

		# inventory

		self.gold = 0
		self.lItem = []
		self.weapon = None

	def OnUpdate(self):
		if Game.game.Mode() == Game.Mode.COMBAT:
			# BB (dave) Handle damge, etc.
			pass

		elif Game.game.Mode() == Game.Mode.WORLDMAP:

			# BB (dave) Time step shouldn't be hard coded...

			dT = 0.03
			sdVMax = 600.0
			rsdV = 10.0

			# Compute new velocity

			# NOTE (dave) this treatment means we smooth in (via acceleration)
			#  and also smooth out (since accel decreases as we approach target)

			vTarget = self.VTargetCompute()
			dV = vTarget - self.v
			dVScaled = rsdV * dV
			dVLim = Vec.VecLimitLen(dVScaled, sdVMax)

			vOld = self.v
			self.v += dT * dVLim

			if "DEBUG" == 0:
				print "vTarget: %s dV: %s dVScaled %s dVLim %s v %s vNext %s" % \
					(vTarget, dV, dVScaled, dVLim, vOld, self.v)

			# Compute new position

			self.pos += dT * self.v

	def FHandleEvent(self, event):
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
		
	def OnDamage(self, damage):
		# BB (davidm) enqueue damage to be dealt with at update time
		pass

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
