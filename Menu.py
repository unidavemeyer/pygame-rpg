# Menu.py
#
# Copyright (c) 2012 by David Meyer

import Game
import pygame

class Menu:
	def __init__(self):
		print "Menu: game is", Game.game

		Game.game.AddUpdate(self, 10)		# relatively early update
		Game.game.AddRender(self, 100)	# relatively late render (more on top)
		Game.game.AddHandler(self, 10)	# relatively early event handler

		font20 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
		font25 = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 25)
		colorUnsel = pygame.Color(128, 0, 0)
		colorSel = pygame.Color(255, 128, 128)

		class MenuEntry:
			def __init__(self, strTitle, fnExec):
				self.m_strTitle = strTitle
				self.m_fnExec = fnExec
				self.m_surfUnsel = font20.render(strTitle, False, colorUnsel)
				self.m_surfSel = font25.render(strTitle, False, colorSel)

			def Exec(self):
				self.m_fnExec()

		self.m_lEntry = [
			MenuEntry("Resume", self.OnResume),
			MenuEntry("New Game", self.OnNewGame),
			MenuEntry("Save Game", self.OnSaveGame),
			MenuEntry("Load Game", self.OnLoadGame),
			MenuEntry("Options", self.OnOptions),
			MenuEntry("Quit", self.OnQuit),
		]

		self.m_iEntry = 0

	def OnUpdate(self):
		if Game.game.Mode() != Game.Mode.MENU:
			return
		
		# BB (dave) do we even need to be an updater?
		#  maybe if we want to pulse the text or something...

		return

	def FHandleEvent(self, event):
		if event.type != pygame.KEYDOWN:
			return False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			Game.game.SetMode(Game.Mode.MENU)
			return True

		if Game.game.Mode() != Game.Mode.MENU:
			return False

		if event.key == pygame.K_UP:
			self.m_iEntry = (self.m_iEntry + len(self.m_lEntry) - 1) % len(self.m_lEntry)
		elif event.key == pygame.K_DOWN:
			self.m_iEntry = (self.m_iEntry + 1) % len(self.m_lEntry)
		elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
			self.m_lEntry[self.m_iEntry].Exec()

		return True

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.MENU:
			return

		# BB (davidm) make dynamic to match text

		surfScreen.fill(pygame.Color(64, 64, 64), pygame.Rect(50, 25, 300, 250))

		xEntry = 100
		yEntry = 50

		for iEntry, entry in enumerate(self.m_lEntry):
			surfText = entry.m_surfUnsel
			if iEntry == self.m_iEntry:
				surfText = entry.m_surfSel

			surfScreen.blit(surfText, (xEntry, yEntry))
			yEntry += 30

	def OnResume(self):
		print "Resume not yet implemented"

	def OnNewGame(self):
		print "New game not yet implemented"

	def OnSaveGame(self):
		print "Save game not yet implemented"

	def OnLoadGame(self):
		print "Load game not yet implemented"

	def OnOptions(self):
		print "Options not yet implemented"

	def OnQuit(self):
		pygame.event.post(pygame.event.Event(pygame.QUIT))