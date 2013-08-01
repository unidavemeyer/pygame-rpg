# Joystick abstraction
#
# Copyright 2012 by David Meyer

import pygame

# Names for various button types

# BB (davidm) could do this on class definitions instead, theoretically,
#  and that would be immutable

BTN_NavUp = 0
BTN_NavDown = 1
BTN_NavLeft = 2
BTN_NavRight = 3
BTN_Ok = 4
BTN_Cancel = 5

class Joystick:
	"""Represents a single joystick device connected to the system; provies an"""
	""" abstract and cooked representation of the underlying pygame joystick data."""

	# NOTE (davidm) here is experimentally-derived data from using a
	#  ps3 controller and examining what happened with various input
	#  channels:

	# PIA = PS3 Index for Axis

	PIA_L_LR	= 0		# axis 0 = left stick, side-to-side, -1 = left, 1.0 = right
	PIA_L_UD	= 1		# axis 1 = left stick, up-and-down, -1 = up, 1.0 = down
	PIA_R_LR	= 2		# axis 2 = right stick, side-to-side, -1 = left, 1.0 = right
	PIA_R_UD	= 3		# axis 3 = right stick, up-and-down, -1 = up, 1.0 = down
	PIA_PAD_U	= 8		# axis 8 = dpad up, analog pressure, -1 = up, 1 = down
	PIA_PAD_L	= 9		# axis 9 = dpad left, analog pressure, -1 = up, 1 = down
	PIA_PAD_D	= 10	# axis 10 = dpad down, analog pressure, -1 = up, 1 = down
	PIA_L2		= 12	# axis 12 = l2, analog pressure, -1 = up, 1 = down
	PIA_R2		= 13	# axis 13 = r2, analog pressure, -1 = up, 1 = down
	PIA_L1		= 14	# axis 14 = l1, analog pressure, -1 = up, 1 = down
	PIA_R1		= 15	# axis 15 = r1, analog pressure, -1 = up, 1 = down
	PIA_TRI		= 16	# axis 16 = triangle, analog pressure, -1 = up, 1 = down
	PIA_CIR		= 17	# axis 17 = circle, analog pressure, -1 = up, 1 = down
	PIA_X		= 18	# axis 18 = x, analog pressure, -1 = up, 1 = down
	PIA_SQR		= 19	# axis 19 = square, analog pressure, -1 = up, 1 = down
	PIA_ACL_LR	= 23	# axis 23 = left/right accel, neg = right down, pos = left down
	PIA_ACL_FB	= 24	# axis 24 = fore/back accel, neg = fore down, pos = back down
	PIA_ACL_UD	= 25	# axis 25 = up/down accel, neg = down down, pos = up down

	# PIB = PS3 Index for Button

	PIB_SEL		= 0		# 0 = select
	PIB_L3		= 1		# 1 = left stick
	PIB_R3		= 2		# 2 = right stick
	PIB_STR		= 3		# 3 = start
	PIB_PAD_U	= 4		# 4 = dpad up
	PIB_PAD_R	= 5		# 5 = dpad right
	PIB_PAD_D	= 6		# 6 = dpad down
	PIB_PAD_L	= 7		# 7 = dpad left
	PIB_L2		= 8		# 8 = l2 (?)
	PIB_R2		= 9		# 9 = r2 (?)
	PIB_L1		= 10	# 10 = l1 (?)
	PIB_R1		= 11	# 11 = r1 (?)
	PIB_TRI		= 12	# 12 = triangle
	PIB_CIR		= 13	# 13 = circle
	PIB_X		= 14	# 14 = x
	PIB_SQR		= 15	# 15 = square
	PIB_PS		= 16	# 16 = ps

	def __init__(self, id):
		self.joy = pygame.joystick.Joystick(id)
		self.joy.init()

		# cache data from the controller

		self.id = self.joy.get_id()
		self.name = self.joy.get_name()
		self.lAxis = [0 for x in range(self.joy.get_numaxes())]
		self.lBtn = [0 for x in range(self.joy.get_numbuttons())]
		self.lBtnRead = [0 for x in range(self.joy.get_numbuttons())]

		# BB (davidm) pick a different set of mappings for non-ps3 controllers

		self.mpBtnIbtn = [
				Joystick.PIB_PAD_U,	# BTN_NavUp (= pad up)
				Joystick.PIB_PAD_D,	# BTN_NavDown (= pad down)
				Joystick.PIB_PAD_L,	# BTN_NavLeft (= pad left)
				Joystick.PIB_PAD_R,	# BTN_NavRight (= pad right)
				Joystick.PIB_X,		# BTN_Ok (= x)
				Joystick.PIB_CIR,	# BTN_Cancel = 5
			]


	def ConsumeEvent(self, event):
		assert(event.joy == self.id)

		if event.type == pygame.JOYAXISMOTION:
			self.lAxis[event.axis] = event.value
		elif event.type == pygame.JOYBUTTONDOWN:
			# BB (davidm) add some notion of repeat delay?
			if self.lBtn[event.button] == 0:
				self.lBtn[event.button] = 1
				self.lBtnRead[event.button] = 0
		elif event.type == pygame.JOYBUTTONUP:
			self.lBtn[event.button] = 0

	def ThumbLeftLR(self):
		"""-1.0 (left) to 1.0 (right) value for the position of the left stick"""

		return self.lAxis[Joystick.PIA_L_LR]

	def ThumbLeftUD(self):
		"""-1.0 (up) to 1.0 (down) value for the position of the left stick"""

		return self.lAxis[Joystick.PIA_L_UD]

	def ThumbRightLR(self):
		"""-1.0 (left) to 1.0 (right) value for the position of the right stick"""

		return self.lAxis[Joystick.PIA_R_LR]

	def ThumbRightUD(self):
		"""-1.0 (up) to 1.0 (down) value for the position of the right stick"""

		return self.lAxis[Joystick.PIA_R_UD]

	def FIsBtnDown(self, btn):
		return self.lBtn[self.mpBtnIbtn[btn]]

	def FWasBtnPressed(self, btn):
		"""Return true if this is the first time this joy has been queried"""
		""" about the button being pressed since it became pressed."""

		fIsDown = self.FIsBtnDown(btn)
		fWasRead = self.lBtnRead[self.mpBtnIbtn[btn]]
		self.lBtnRead[self.mpBtnIbtn[btn]] = 1

		return fIsDown and not fWasRead
