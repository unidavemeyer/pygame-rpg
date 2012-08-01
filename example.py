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

# run an event loop

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
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
