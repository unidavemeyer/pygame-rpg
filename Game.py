# Outermost game module
#
# Copyright 2012 by David Meyer

import pygame
import sys

import Hero
import Menu

class Mode:
	"""Enum-type class tracking various game modes."""

	# BB (dave) should make these read-only attributes

	MENU = 0		# player is using the menu
	WORLDMAP = 1	# player is navigating the world map
	COMBAT = 2		# player is in combat



class Font:
	"""Holder for standard fonts used in the game.  Thin wrapper around"""
	""" the native pygame fonts so that things are at least somewhat"""
	""" consistent across all of the places that we render text."""

	FONT20 = None
	FONT25 = None

	@staticmethod
	def Init():
		Font.FONT20 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
		Font.FONT25 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 25)



class Game:
	"""Glues together the whole game.  Runs the game loop and provides"""
	""" services to register objects for update, event handling, and"""
	""" rendering."""

	def __init__(self):
		self.mpPriUpdate = {}		# priority based list of update objects
		self.mpPriRender = {}		# priority based list of render objects
		self.mpPriHandler = {}		# priority based list of handler objects
		self.lNpc = []				# (unsorted) list of NPCs currently in the world
		self.hero = None			# current hero object
		self.menu = None			# current menu object
		self.npcCombatant = None	# current npc the hero is fighting (if any)

		self.fpsClock = None
		self.surfScreen = None

		self.m_mode = Mode.MENU

	def AddUpdate(self, obj, priority):
		"""Add obj to the priority list of objects to update.  obj is expected"""
		""" to have an OnUpdate() method, which will be called to do the update."""
		""" Priorities are run each frame from least to greatest."""

		self.mpPriUpdate.setdefault(priority, []).append(obj)

	def RemoveUpdate(self, obj, priority):
		"""Remove obj from the priority list of update objects."""

		self.mpPriUpdate[priority].remove(obj)

	def AddRender(self, obj, priority):
		"""Add obj to the priority list of objects to render.  obj is expected"""
		""" to have an OnRender(surf) method, which will be called when the object"""
		""" is to render itself to the display surface.  Priorities are run each"""
		""" frame from least to greatest."""

		self.mpPriRender.setdefault(priority, []).append(obj)

	def RemoveRender(self, obj, priority):
		"""Remove obj from the priority list of render objects."""

		self.mpPriRender[priority].remove(obj)

	def AddHandler(self, obj, priority):
		"""Add obj to the priority list of event handler objects.  obj is expected"""
		""" to have an FHandleEvent(event) function.  If said function returns true,"""
		""" the event is considered consumed and will not be sent to any other objects"""
		""" in the list.  Priorities are run in order from least to greatest."""

		self.mpPriHandler.setdefault(priority, []).append(obj)

	def RemoveHandler(self, obj, priority):
		"""Remove obj from the priority list of event handler objects."""

		self.mpPriHandler[priority].remove(obj)

	def Mode(self):
		"""Queries the current game mode, which will be a value from the Mode enum class"""

		return self.m_mode

	def SetMode(self, mode):
		"""Sets the current mode for the game, which must be from the Mode enum class"""

		self.m_mode = mode

	def AddNpc(self, npc):
		self.lNpc.append(npc)

	def RemoveNpc(self,npc):
		lNpcNew = [x for x in self.lNpc if x != npc]
		self.lNpc = lNpcNew
		
	def LNpc(self):
		return self.lNpc

	def SetNpcCombatant(self, npc):
		self.npcCombatant = npc

	def NpcCombatant(self):
		return self.npcCombatant

	def Menu(self):
		return self.menu

	def Hero(self):
		return self.hero

	def Run(self):

		# Set up pygame

		pygame.init()
		self.fpsClock = pygame.time.Clock()
		self.surfScreen = pygame.display.set_mode((640,480))
		pygame.display.set_caption('Arithmancer')

		# Set up starter objects

		Font.Init()
		self.menu = Menu.Menu()
		self.hero = Hero.Hero()

		# Run the main loop

		while True:

			# Give objects a chance to handle input

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
					return

				fHandled = False
				for pri in sorted(self.mpPriHandler.keys()):
					for obj in self.mpPriHandler[pri]:
						if obj.FHandleEvent(event):
							fHandled = True
							break
					if fHandled:
						break

			# Give objects a chance to update

			# BB (dave) should we copy this list here so that we can
			#  modify the running copy?  or is python ok with dynamic
			#  changes to the list while it's being iterated over?

			for pri in sorted(self.mpPriUpdate.keys()):
				for obj in self.mpPriUpdate[pri]:
					obj.OnUpdate()

			# Give objects a chance to render

			for pri in sorted(self.mpPriRender.keys()):
				for obj in self.mpPriRender[pri]:
					obj.OnRender(self.surfScreen)

			# Update the display

			pygame.display.update()

			# Don't run at more than 30 fps (really helps perf!)

			self.fpsClock.tick(30)

# Global single instance of the Game class

game = Game()

# Command-line driver (how the whole thing operates)

if __name__ == '__main__':
	# BB (dave) funny construction here so that we talk to the
	#  same singleton game instance that all other modules are
	#  using

	import Game
	Game.game.Run()
