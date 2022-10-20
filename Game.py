# Outermost game module
#
# Copyright 2012 by David Meyer

import os
import pygame
import sys
import traceback

import Hero
import Menu
import World
import Joystick

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
		# BB (davidm) come up with a better way to locate fonts
        #finds fonts
		s_aPath = [
			'/usr/share/fonts/truetype/freefont/FreeSans.ttf',
			r'c:\windows\boot\fonts\segoe_slboot.ttf',
		]

		pathUse = None
		for pathCheck in s_aPath:
			if os.path.exists(pathCheck):
				pathUse = pathCheck
				break
		
		if not pathUse:
			raise Exception("Ack! No font found, update Game.py with one from your system!")

		Font.FONT20 = pygame.font.Font(pathUse, 20)
		Font.FONT25 = pygame.font.Font(pathUse, 25)



class Game:
	"""Glues together the whole game.  Runs the game loop and provides"""
	""" services to register objects for update, event handling, and"""
	""" rendering."""

	def __init__(self):
		self.mpPriUpdate = {}		# priority based list of update objects
		self.mpPriRender = {}		# priority based list of render objects
		self.mpPriHandler = {}		# priority based list of handler objects
		self.lNpc = []		       		# (unsorted) list of NPCs currently in the world
		self.lHero = []				# current hero objects
		self.menu = None			# current menu object
		self.world = None			# current world object
		self.worldNext = None		# next world object (pending warp)
		self.npcCombatant = None	# current npc the hero is fighting (if any)

		self.fpsClock = None		# rate limiter for performance
		self.surfScreen = None		# area where everything is drawn
		self.lJoy = []				# joysticks we've found

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

	def LHero(self):
		return self.lHero

	def Hero(self, iHero):
		return self.lHero[iHero]

	def SetWorld(self, world):
		self.world = world

	def World(self):
		return self.world

	def SetNextWorld(self, strWorld):
		self.worldNext = World.World('worlds/%s' % strWorld)
        #makes more worlds 

	def AddJoysticks(self):
		"""Make sure that self.lJoy is consistent with the number of"""
		""" joysticks reported by pygame"""

		pygame.joystick.init()
		for id in range(pygame.joystick.get_count()):
			self.lJoy.append(Joystick.Joystick(id))

	def Joy(self, iJoy):
		if iJoy < 0:
			return None

		if iJoy > len(self.lJoy):
			return None

		return self.lJoy[iJoy]

	def LJoy(self):
		return self.lJoy

	def OnNewGame(self):
		"""Clears objects and internal state and makes a new game start at the world map"""
         # calls function on new game. gets rid of all the npc(s) and heros. Resets everything like a refreash button
		# Kill npcs

		for npc in self.lNpc:
			npc.Kill()

		self.lNpc = []
		self.npcCombatant = None

		# Kill heroes

		for hero in self.lHero:
			hero.Kill()

		self.lHero = []

		# Kill worlds

		if self.world:
			self.world.Kill()
			self.world = None

		if self.worldNext:
			self.worldNext.Kill()
			self.worldNext = None

		# Generate one hero for each joystick

		# BB (davidm) probably only want two, and always two...
        # BB = bug
		self.lHero = [ Hero.Hero(j) for j in self.lJoy ]

		if not self.lHero:
			self.lHero = [ Hero.Hero(None) ]

		# BB (davidm) totally placeholder

		world = World.World('worlds/start.wld')
		world.MakeActive()

		self.SetMode(Mode.WORLDMAP)
        # exit out of the menu and set it were the player is in control and can walk around

	def Run(self):

		# Set up pygame

		pygame.init()
		pygame.joystick.init()
		self.fpsClock = pygame.time.Clock()
		self.surfScreen = pygame.display.set_mode((640,480))
		pygame.display.set_caption('Arithmancer')

		self.AddJoysticks()

		if len(self.lJoy) < 2:
			print("Warning:  Should have two joysticks connected")

		# Set up starter objects

		Font.Init()
		self.menu = Menu.Menu()

		# Run the main loop

		while True:

			# Handle any pending warps

			if self.worldNext:
				self.world.MakeInactive()
				self.worldNext.MakeActive()
				self.worldNext = None

			# Give objects a chance to handle input

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
					return

				elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
					fHandled = False
					for pri in sorted(self.mpPriHandler.keys()): #Mp mean map
						for obj in self.mpPriHandler[pri]:
							if obj.FHandleEvent(event):
								fHandled = True # f means flag
								break # a way to get out of a loop(early)
						if fHandled:
							break

				elif event.type in (pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
					iJoy = event.joy
					self.lJoy[iJoy].ConsumeEvent(event)

			# Give objects a chance to update

			# BB (dave) should we copy this list here so that we can
			#  modify the running copy? or is python ok with dynamic
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
