# Joystick abstraction
#
# Copyright 2012 by David Meyer

import pygame

class Joystick:
	"""Represents a single joystick device connected to the system; provies an"""
	""" abstract and cooked representation of the underlying pygame joystick data."""

	def __init__(self, id):
		self.joy = pygame.joystick.Joystick(id)
		self.joy.init()

		# cache data from the controller

		self.id = self.joy.get_id()
		self.name = self.joy.get_name()
		self.lAxis = [0 for x in range(self.joy.get_numaxes())]
		self.lBtn = [0 for x in range(self.joy.get_numbuttons())]

		# BB (davidm) assumes ps3 controller

		# axis 0 = left stick, side-to-side, -1 = left, 1.0 = right
		# axis 1 = left stick, up-and-down, -1 = up, 1.0 = down
		# axis 2 = right stick, side-to-side, -1 = left, 1.0 = right
		# axis 3 = right stick, up-and-down, -1 = up, 1.0 = down
		# axis 4 = no data
		# axis 5 = no data
		# axis 6 = no data
		# axis 7 = no data
		# axis 8 = dpad up, analog pressure, -1 = up, 1 = down
		# axis 9 = dpad left, analog pressure, -1 = up, 1 = down
		# axis 10 = dpad down, analog pressure, -1 = up, 1 = down
		# axis 11 = no data
		# axis 12 = l2, analog pressure, -1 = up, 1 = down
		# axis 13 = r2, analog pressure, -1 = up, 1 = down
		# axis 14 = l1, analog pressure, -1 = up, 1 = down
		# axis 15 = r1, analog pressure, -1 = up, 1 = down
		# axis 16 = triangle, analog pressure, -1 = up, 1 = down
		# axis 17 = circle, analog pressure, -1 = up, 1 = down
		# axis 18 = x, analog pressure, -1 = up, 1 = down
		# axis 19 = square, analog pressure, -1 = up, 1 = down
		# axis 20 = no data
		# axis 21 = no data
		# axis 22 = no data
		# axis 23 = left/right accel, neg = right down, pos = left down
		# axis 24 = fore/back accel, neg = fore down, pos = back down
		# axis 25 = up/down accel, neg = down down, pos = up down
		# axis 26 = no data

		# 0 = select
		# 1 = left stick
		# 2 = right stick
		# 3 = start
		# 4 = dpad up
		# 5 = dpad right
		# 6 = dpad down
		# 7 = dpad left
		# 8 = l2 (?)
		# 9 = r2 (?)
		# 10 = l1 (?)
		# 11 = r1 (?)
		# 12 = triangle
		# 13 = circle
		# 14 = x
		# 15 = square
		# 16 = ps

	def ThumbLeftLR(self):
		"""-1.0 to 1.0 value for the left/right setting of the left stick"""
		pass

	def ThumbLeftUD(self):
		"""-1.0 to 1.0 value for the up/down setting of the left stick"""
		pass

	def ThumbRightLR(self):
		"""-1.0 to 1.0 value for the left/right setting of the right stick"""
		pass

	def ThumbRightUD(self):
		"""-1.0 to 1.0 value for the up/down setting of the right stick"""
		pass
