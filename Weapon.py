# Weapon.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame

class Weapon:
	"""Base class for anything the player uses to deal damage in combat."""
	""" Responsible for rendering questions and handling input during"""
	""" combat, and then determining damage to deal to the opponent."""

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

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.COMBAT:
			self.strProblem = None
			return

		# if we've answered a question, deal damage to our opponent

		if self.fSubmitAnswer:
			if self.nUser == self.nAnswer:
				# TODO: damage opponent
				# TODO: generate surface in "success" form
			else:
				# TODO: generate surface in "failure" form

			self.strProblem = None
			self.fSubmitAnswer = False

		# TODO: if we don't have a problem, generate one

		if not self.strProblem:
			# TODO: generate a problem to answer, along with its answer

		print "Sword update"

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

		# TODO: render old answer, if any
		# TODO: render current problem + user entry

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

