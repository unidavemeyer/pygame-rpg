# Lib.py
#
# Copyright (c) 2022 by David Meyer

import pygame
import Vec



def RenderHpBar(surfScreen, pos, hpCur, hpMax, heroset):
	"""Renders a hit point bar to the screen based on the position for an entity and its current/max hitpoint
	values"""
	# Calculate fraction of full health that hpCur represents
	uHp = min(max(hpCur / hpMax, 0.0), 1.0)
	wHp = int(uHp * 32)
	wBack = 32 - wHp

	# Calculate hp and background bar sizes

	s_dYHpOffset = 33
	s_dYHp = 3

	yHpTop = pos.y + s_dYHpOffset

	rectHp = pygame.Rect(pos.x, yHpTop, wHp, s_dYHp)
	rectHpBack = pygame.Rect(pos.x + wHp, yHpTop, wBack, s_dYHp)

	# Calculate color for hp bar
	if heroset:
		s_rgbFull = (64,224,208)
		s_rgbEmpty = (64,224,208)
	elif not heroset:
		s_rgbFull = (124,252,0)
		s_rgbEmpty = (255, 0, 0)

	rgbHp = Vec.Lerp(s_rgbEmpty, s_rgbFull, uHp)
	rgbHpBack = (0, 0, 0)

	# Draw the bar (both parts, as necessary)

	surfScreen.fill(rgbHp, rectHp)

	if wBack > 0:
		surfScreen.fill(rgbHpBack, rectHpBack)

