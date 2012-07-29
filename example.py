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

# initialize to red (why not!)

surfScreen.fill(colorRed)

# run an event loop

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)

		elif event.type == pygame.KEYDOWN:
			iColor = (iColor + 1) % len(lColor)
			surfScreen.fill(lColor[iColor])
			
	# refresh the screen -- very important to do at the end of the loop!

	pygame.display.update()
