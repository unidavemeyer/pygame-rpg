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
