# Weapon.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame

class Weapon:
	"""Base class for anything the player uses to deal damage in combat."""
	""" Responsible for rendering questions and handling input during"""
	""" combat, and then determining damage to deal to the opponent."""

	# BB (davidm) figure out where to really load this from...

	s_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 20)

	s_colorCur = pygame.Color(128, 128, 192)
	s_colorPass = pygame.Color(128, 255, 128)
	s_colorFail = pygame.Color(255, 128, 128)

	def __init__(self):
		Game.game.AddUpdate(self, 20)	# relatively early update
		Game.game.AddRender(self, 90)	# relatively late render (more on top)
		Game.game.AddHandler(self, 20)	# relatively early event handler

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		print "Base weapon update"

	def FHandleEvent(self, event):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return False

		# BB (davidm) base class doesn't actually handle squat

		return False

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		# Basic rendering to show the weapon is active

		surfScreen.fill(pygame.Color(255, 128, 128), pygame.Rect(400, 400, 50, 25))



class Sword(Weapon):
	"""Weapon that provides addition problems of the one-digit-plus-one-digit"""
	""" variety."""

	def __init__(self):
		Weapon.__init__(self)

		# Keyboard keys we know how to handle

		# BB (davidm) seems like this handling should be moved up to
		#  the Weapon class so that all weapons get that behavior by
		#  default and don't have to do anything special.  Maybe we
		#  should abstract out the problem generation, solution stuff,
		#  and then go from there?  Tough to know for sure before we've
		#  really gotten everything running with a weapon or two, though.

		self.mpKeyFn = {
				pygame.K_0:			lambda: self.OnDigit(0),
				pygame.K_1:			lambda: self.OnDigit(1),
				pygame.K_2:			lambda: self.OnDigit(2),
				pygame.K_3:			lambda: self.OnDigit(3),
				pygame.K_4:			lambda: self.OnDigit(4),
				pygame.K_5:			lambda: self.OnDigit(5),
				pygame.K_6:			lambda: self.OnDigit(6),
				pygame.K_7:			lambda: self.OnDigit(7),
				pygame.K_8:			lambda: self.OnDigit(8),
				pygame.K_9:			lambda: self.OnDigit(9),
				pygame.K_KP0:		lambda: self.OnDigit(0),
				pygame.K_KP1:		lambda: self.OnDigit(1),
				pygame.K_KP2:		lambda: self.OnDigit(2),
				pygame.K_KP3:		lambda: self.OnDigit(3),
				pygame.K_KP4:		lambda: self.OnDigit(4),
				pygame.K_KP5:		lambda: self.OnDigit(5),
				pygame.K_KP6:		lambda: self.OnDigit(6),
				pygame.K_KP7:		lambda: self.OnDigit(7),
				pygame.K_KP9:		lambda: self.OnDigit(8),
				pygame.K_KP9:		lambda: self.OnDigit(9),
				pygame.K_KP_ENTER:	self.OnEnterKey,
				pygame.K_RETURN:	self.OnEnterKey,
				pygame.K_BACKSPACE:	self.OnBackspaceKey,
			}

		# Current user entry

		self.nUser = None
		self.fSubmitAnser = False

		# Current problem and answer

		self.strProblem = None
		self.nAnswer = 0

		# Previous problem/answer/status as a surface (doesn't change)

		self.surfOld = None

		self.dHpAttack = -3		# HP damage deal with each successful attack

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.COMBAT:
			self.strProblem = None
			return

		# if we've answered a question, deal damage to our opponent, etc.

		if self.fSubmitAnswer:
			colorOld = Weapon.s_colorFail

			if self.nUser == self.nAnswer:
				Game.game.NpcCombatant().OnDamage(self.dHpAttack)
				colorOld = Weapon.s_colorPass

			strOld = "%s = %d" % (self.strProblem, self.nUser)
			self.surfOld = Weapon.s_font.render(strOld, False, colorOld)

			self.strProblem = None
			self.fSubmitAnswer = False

		# if we need a problem, generate one

		if not self.strProblem:
			n1 = random.randint(0, 9)
			n2 = random.randint(0, 9)
			self.strProblem = "%d + %d"
			self.nAnswer = n1 + n2

	def FHandleEvent(self, event):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return False

		if event.type != pygame.KEYDOWN:
			return False

		fnHandleKey = self.mpKeyFn.get(event.key)
		if fnHandleKey:
			fnHandleKey()
			return True

		return False

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.COMBAT:
			return

		if self.surfOld:
			surfScreen.blit(self.surfOld, (20, 400))

		strUser = ''
		if self.nUser != None:
			strUser = "%d" % self.nUser

		strDisplay = "%s = %s" % (self.strProblem, strUser)

		surfDisplay = Weapon.s_font.render(strDisplay, False, Weapon.s_colorCur)

		surfScreen.blit(surfDisplay, (20, 425))

	def OnDigit(self, n):
		if not self.nUser:
			self.nUser = n
		else:
			self.nUser = self.nUser * 10 + n

	def OnEnterKey(self):
		self.fSubmitAnswer = True

	def OnBackspaceKey(self):
		if self.nUser > 10:
			self.nUser = int(self.nUser / 10)
		else:
			self.nUser = None

