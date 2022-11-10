# Menu.py
#
# Copyright (c) 2012 by David Meyer

import Game
import Joystick
import Npc
import pygame
import Vec
import World

class MenuEntry:
	"""Represents one entry on a menu (title plus callback function)"""

	def __init__(self, strTitle, fnExec):
		colorUnsel = pygame.Color(128, 0, 0)
		colorSel = pygame.Color(255, 128, 128)

		self.m_strTitle = strTitle
		self.m_fnExec = fnExec
		self.m_surfUnsel = Game.Font.FONT20.render(strTitle, False, colorUnsel)
		self.m_surfSel = Game.Font.FONT25.render(strTitle, False, colorSel)

	def Exec(self):
		self.m_fnExec()

class MenuData:
	"""Information about a specific menu."""

	def __init__(self):
		self.m_lEntry = []
		self.m_iEntry = 0

	def AddEntry(self, strText, fnExec):
		self.m_lEntry.append(MenuEntry(strText, fnExec))

	def OnNavUp(self):
		self.m_iEntry = (self.m_iEntry + len(self.m_lEntry) - 1) % len(self.m_lEntry)

	def OnNavDown(self):
		self.m_iEntry = (self.m_iEntry + 1) % len(self.m_lEntry)

	def OnNavOk(self):
		self.m_lEntry[self.m_iEntry].Exec()

def FnStartGame(strWorld):
	"""Create function that will cause a new game to happen in the given world"""

	return lambda: Game.game.OnNewGame(strWorld)

class Menu:
	"""Manages the menu for the game -- used when paused, when starting the"""
	""" game, etc."""

	def __init__(self):
		Game.game.AddUpdate(self, 10)	# relatively early update
		Game.game.AddRender(self, 100)	# relatively late render (more on top)
		Game.game.AddHandler(self, 10)	# relatively early event handler

		self.m_lMd = []

		# Episode menu

		# BB (davidm) would be nice to encapsulate these possiblities somewhere and autogen, maybe?

		mdEpisode = MenuData()
		mdEpisode.AddEntry("Test Episode", FnStartGame("worlds/start.wld"))
		mdEpisode.AddEntry("Other Episode", FnStartGame("worlds/second.wld"))	# BB (davidm) replace with better title & target

		# Main menu

		mdMain = MenuData()
		mdMain.AddEntry("Resume", self.OnPopMenu),
		mdMain.AddEntry("New Game", self.FnPushMenu(mdEpisode)),
		mdMain.AddEntry("Save Game", self.OnSaveGame),
		mdMain.AddEntry("Load Game", self.OnLoadGame),
		mdMain.AddEntry("Options", self.OnOptions),
		mdMain.AddEntry("Quit", self.OnQuit),

		# Track active menu

		self.m_lMd.append(mdMain)

		self.modeResume = None

	def FnPushMenu(self, md):
		"""Provides a function to push the given submenu"""

		return lambda: self.OnPushMenu(md)

	def OnPushMenu(self, md):
		self.m_lMd.append(md)

	def OnUpdate(self):

		# BB (davidm) unfortunate to have some menu actions happen in FHandleEvent
		#  and other actions happen in OnUpdate.  Maybe we should have a keyboard
		#  class that tracks input events there, just like we have for the joystick?

		for joy in Game.game.LJoy():
			if joy.FWasBtnPressed(Joystick.BTN_Menu):
				if Game.game.Mode() == Game.Mode.MENU:
					self.OnPopMenu()
				else:
					self.modeResume = Game.game.Mode()
					Game.game.SetMode(Game.Mode.MENU)
				return

		if Game.game.Mode() != Game.Mode.MENU:
			return
		
		for joy in Game.game.LJoy():
			# handle nav button presses

			if joy.FWasBtnPressed(Joystick.BTN_NavUp):
				self.m_lMd[-1].OnNavUp()
			elif joy.FWasBtnPressed(Joystick.BTN_NavDown):
				self.m_lMd[-1].OnNavDown()
			elif joy.FWasBtnPressed(Joystick.BTN_Ok):
				self.m_lMd[-1].OnNavOk()

		return

	def FHandleEvent(self, event):
		if event.type != pygame.KEYDOWN:
			return False

		if event.key == pygame.K_ESCAPE:
			if Game.game.Mode() == Game.Mode.MENU:
				self.OnPopMenu()
			else:
				self.modeResume = Game.game.Mode()
				Game.game.SetMode(Game.Mode.MENU)
			return True

		if Game.game.Mode() != Game.Mode.MENU:
			return False

		if event.key == pygame.K_UP:
			self.m_lMd[-1].OnNavUp()
		elif event.key == pygame.K_DOWN:
			self.m_lMd[-1].OnNavDown()
		elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
			self.m_lMd[-1].OnNavOk()

		return True

	def OnRender(self, surfScreen):
		if Game.game.Mode() != Game.Mode.MENU:
			return

		# Draw all active menu datas

		iMdActive = len(self.m_lMd) - 1

		s_colorActive = pygame.Color(64, 64, 64)	# color for active menu
		s_colorInactive = pygame.Color(32, 32, 32)	# color for inactive menus

		s_dYEntry = 30		# height per menu entry
		s_dXEntry = 300		# estimated width per menu entry - BB (davidm) compute?
		s_dXStack = 50		# offset per menu level
		s_dYStack = 50		#  ...
		s_dXPad = 25		# padding to outset to menu background from text
		s_dYPad = 25		#  ...

		for iMd, md in enumerate(self.m_lMd):
			xEntry = 100 + s_dXStack * iMd
			yEntry = 50 + s_dYStack * iMd

			# Calculate menu background coordinates and create background rectangle

			dYText = s_dYEntry * len(md.m_lEntry)
			xUR, yUR = (xEntry - s_dXPad, yEntry - s_dYPad)
			xLL, yLL = (xUR + s_dXEntry + 2 * s_dXPad, yUR + dYText + 2 * s_dYPad)

			colorUse = s_colorActive if iMd == iMdActive else s_colorInactive
			surfScreen.fill(colorUse, pygame.Rect(xUR, yUR, xLL, yLL))

			# Fill in text for each entry

			for iEntry, entry in enumerate(md.m_lEntry):
				surfText = entry.m_surfUnsel
				if iEntry == md.m_iEntry:
					surfText = entry.m_surfSel

				surfScreen.blit(surfText, (xEntry, yEntry))
				yEntry += s_dYEntry

	def OnPopMenu(self):

		# Pop child menus if we have them

		# BB (davidm) this doesn't clear sub-menu rendering, unfortunately...

		if len(self.m_lMd) > 1:
			del self.m_lMd[-1]
			return

		# Resume appropriate game mode if we have one

		if self.modeResume:
			Game.game.SetMode(self.modeResume)
			self.modeResume = None

	def OnSaveGame(self):
		print("Save game not yet implemented")

	def OnLoadGame(self):
		print("Load game not yet implemented")

	def OnOptions(self):
		print("Options not yet implemented")

	def OnQuit(self):
		pygame.event.post(pygame.event.Event(pygame.QUIT))
