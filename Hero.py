# Hero.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame

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

	def OnUpdate(self):
		if Game.game.Mode() == Game.Mode.COMBAT:
			# BB (dave) Handle damge, etc.
			pass

		elif Game.game.Mode() == Game.Mode.WORLDMAP:
			# BB (dave) Handle motion, etc.
			pass

	def FHandleEvent(self, event):
		if Game.game.Mode() != Game.Mode.WORLDMAP:
			return False

		# BB (dave) handle 'i' key to go to inventory

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
			elif event.key == pygame.K_DOWN:
			elif event.key == pygame.K_LEFT:
			elif event.key == pygame.K_RIGHT:
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
			elif event.key == pygame.K_DOWN:
			elif event.key == pygame.K_LEFT:
			elif event.key == pygame.K_RIGHT:
