# example using pygame
#
# This file contains various examples of how to use parts of
#  the pygame library to do things.  It's a starting point for
#  understanding the basics of things, in a way that doesn't clutter
#  up the actual game that we're attempting to make.

import pygame
import sys

# must be called to start all pygame stuff

pygame.init()

# generate a frame-rate managing clock

fpsClock = pygame.time.Clock()

# generate a screen-visible service

surfScreen = pygame.display.set_mode((640, 480))

# set the caption to something interesting

pygame.display.set_caption('Example Pygame Fun')

# create a couple of colors

colorRed = pygame.Color(255, 0, 0)
colorGreen = pygame.Color(0, 255, 0)
colorBlue = pygame.Color(0, 0, 255)
colorPurple = pygame.Color(255, 0, 255)
colorBlack = pygame.Color(0, 0, 0)
colorWhite = pygame.Color(255, 255, 255)
lColor = [colorRed, colorGreen, colorBlue, colorPurple, colorBlack, colorWhite]
lColorStr = ['Red', 'Green', 'Blue', 'Purple', 'Black', 'White']
iColor = 0

# load up an image

surfStars = pygame.image.load('stars.png')
surfGuy = pygame.image.load('guy.png')
posStars = (320, 240)
posGuy = posStars

# set up a couple of fonts so we can render text

font32 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 32)
font16 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 16)

# initialize to first color

surfScreen.fill(lColor[0])

# Do some joystick handling

pygame.joystick.init()		# required to start joystick support

print("%d joysticks found" % pygame.joystick.get_count())

lJoy = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]	# joystick(x) makes a joystick
for joy in lJoy:
	print("Joy %d: <%s>" % (joy.get_id(), joy.get_name()))
	joy.init()		# required to start *using* the joystick
	print("  num axes: %d" % joy.get_numaxes())
	print("  num btns: %d" % joy.get_numbuttons())
	# print "  num hats: %d" % joy.get_numhats()

class CJoy:
	def __init__(self, joy):
		self.joy = joy
		self.lAxis = [0 for x in range(joy.get_numaxes())]
		self.lBtn = [0 for x in range(joy.get_numbuttons())]

joyMem = CJoy(lJoy[0])

# run an event loop

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.joystick.quit()
			pygame.quit()
			sys.exit(0)

		# NOTE (dave) could do something clever here where all
		#  interested parties for handling keyboard input could
		#  register themselves on a list, or in a priority queue,
		#  and then a "try handle event" function could be called
		#  on each in turn until someone handled the event...

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				posGuy = ((posGuy[0] + 637) % 640, posGuy[1])
			elif event.key == pygame.K_RIGHT:
				posGuy = ((posGuy[0] + 643) % 640, posGuy[1])
			elif event.key == pygame.K_UP:
				posGuy = (posGuy[0], (posGuy[1] + 477) % 480)
			elif event.key == pygame.K_DOWN:
				posGuy = (posGuy[0], (posGuy[1] + 483) % 480)
			elif event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			else:
				iColor = (iColor + 1) % len(lColor)

		elif event.type == pygame.MOUSEMOTION:
			posStars = event.pos

		elif event.type == pygame.JOYAXISMOTION:
			joyid = event.joy
			joyaxis = event.axis
			joyvalue = event.value

			joyMem.lAxis[joyaxis] = joyvalue

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

		elif event.type == pygame.JOYBUTTONDOWN:
			joyid = event.joy
			joybutton = event.button

			joyMem.lBtn[joybutton] = 1

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

		elif event.type == pygame.JOYBUTTONUP:
			joyid = event.joy
			joybutton = event.button
			joyMem.lBtn[joybutton] = 0

		lStrJoy = ["%2d: %10f" % (x, joyMem.lAxis[x]) for x in [0, 1, 2, 3]]
		lStrJoy.extend(["%1d" % joyMem.lBtn[x] for x in [12, 13, 14, 15, 16]])
		print(" ".join(lStrJoy))

	# redraw the things we want drawn

	# NOTE (davidm) may make sense to have a prioritized list
	#  of things to draw here, and give each one a chance to
	#  add something to surfScreen, which should probably be an
	#  option

	surfScreen.fill(lColor[iColor])
	surfScreen.blit(surfStars, posStars)
	surfScreen.blit(surfGuy, posGuy)

	# generate some text

	surfColor32 = font32.render(lColorStr[iColor], False, lColor[(iColor+1) % len(lColor)]);
	surfColor16 = font16.render(lColorStr[iColor], False, lColor[(iColor+1) % len(lColor)]);

	surfScreen.blit(surfColor32, (10, 10))
	surfScreen.blit(surfColor16, (10, 50))
			
	# refresh the screen -- very important to do at the end of the loop!

	pygame.display.update()

	# make sure we don't redraw more than 30 times a second

	# NOTE (dave) this is actually extremely important -- without this,
	#  the update loop will happily consume all of the available CPU
	#  resources, and end up feeling *worse* response-wise than what
	#  we get this way.  absolutely amazing...

	fpsClock.tick(30)
