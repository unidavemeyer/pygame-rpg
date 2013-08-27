# Menu.py
#
# Copyright (c) 2012 by David Meyer

import Game
import Joystick
import Npc
import pygame
import Vec
import World

class Menu:
	"""Manages the menu for the game -- used when paused, when starting the"""
	""" game, etc."""

	def __init__(self):
		Game.game.AddUpdate(self, 10)	# relatively early update
		Game.game.AddRender(self, 100)	# relatively late render (more on top)
		Game.game.AddHandler(self, 10)	# relatively early event handler

		colorUnsel = pygame.Color(128, 0, 0)
		colorSel = pygame.Color(255, 128, 128)

		class MenuEntry:
			def __init__(self, strTitle, fnExec):
				self.m_strTitle = strTitle
				self.m_fnExec = fnExec
				self.m_surfUnsel = Game.Font.FONT20.render(strTitle, False, colorUnsel)
				self.m_surfSel = Game.Font.FONT25.render(strTitle, False, colorSel)

			def Exec(self):
				self.m_fnExec()

		self.m_lEntry = [
			MenuEntry("Resume", self.OnResume),
			MenuEntry("New Game", Game.game.OnNewGame),
			MenuEntry("Save Game", self.OnSaveGame),
			MenuEntry("Load Game", self.OnLoadGame),
			MenuEntry("Options", self.OnOptions),
			MenuEntry("Quit", self.OnQuit),
		]

		self.m_iEntry = 0

	def OnUpdate(self):

		# BB (davidm) unfortunate to have some menu actions happen in FHandleEvent
		#  and other actions happen in OnUpdate.  Maybe we should have a keyboard
		#  class that tracks input events there, just like we have for the joystick?

		for joy in Game.game.LJoy():
			if joy.FWasBtnPressed(Joystick.BTN_Menu):
				Game.game.SetMode(Game.Mode.MENU)
				return

		if Game.game.Mode() != Game.Mode.MENU:
			return
		
		for joy in Game.game.LJoy():
			# handle nav button presses

			if joy.FWasBtnPressed(Joystick.BTN_NavUp):
				self.OnNavUp()
			elif joy.FWasBtnPressed(Joystick.BTN_NavDown):
				self.OnNavDown()
			elif joy.FWasBtnPressed(Joystick.BTN_Ok):
				self.OnNavOk()

		return

	def FHandleEvent(self, event):
		if event.type != pygame.KEYDOWN:
			return False

		if event.key == pygame.K_ESCAPE:
			Game.game.SetMode(Game.Mode.MENU)
			return True

		if Game.game.Mode() != Game.Mode.MENU:
			return False

		if event.key == pygame.K_UP:
			self.OnNavUp()
		elif event.key == pygame.K_DOWN:
			self.OnNavDown()
		elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
			self.OnNavOk()

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

	def OnNavUp(self):
		self.m_iEntry = (self.m_iEntry + len(self.m_lEntry) - 1) % len(self.m_lEntry)

	def OnNavDown(self):
		self.m_iEntry = (self.m_iEntry + 1) % len(self.m_lEntry)

	def OnNavOk(self):
		self.m_lEntry[self.m_iEntry].Exec()

	def OnResume(self):
		print "Resume not yet implemented"

	def OnSaveGame(self):
		print "Save game not yet implemented"

	def OnLoadGame(self):
		print "Load game not yet implemented"

	def OnOptions(self):
		print "Options not yet implemented"

	def OnQuit(self):
		pygame.event.post(pygame.event.Event(pygame.QUIT))
