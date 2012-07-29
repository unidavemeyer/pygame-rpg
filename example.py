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
iColor = 0

# load up an image

surfStars = pygame.image.load('stars.png')
posStars = (320, 240)

# initialize to first color

surfScreen.fill(lColor[0])

# run an event loop

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				posStars = ((posStars[0] + 637) % 640, posStars[1])
			elif event.key == pygame.K_RIGHT:
				posStars = ((posStars[0] + 643) % 640, posStars[1])
			elif event.key == pygame.K_UP:
				posStars = (posStars[0], (posStars[1] + 477) % 480)
			elif event.key == pygame.K_DOWN:
				posStars = (posStars[0], (posStars[1] + 483) % 480)
			else:
				iColor = (iColor + 1) % len(lColor)

	# redraw the things we want drawn

	surfScreen.fill(lColor[iColor])
	surfScreen.blit(surfStars, posStars)
			
	# refresh the screen -- very important to do at the end of the loop!

	pygame.display.update()

	# make sure we don't redraw more than 30 times a second

	# NOTE (dave) this is actually extremely important -- without this,
	#  the update loop will happily consume all of the available CPU
	#  resources, and end up feeling *worse* response-wise than what
	#  we get this way.  absolutely amazing...

	fpsClock.tick(30)
