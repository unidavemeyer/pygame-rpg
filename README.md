# pygame-rpg

Purpose
-------

This is a framework/experiment/ongoing project making a basic top-down action
RPG in python using pygame for input/rendering/sound. There are a variety of
ideas that I've had about what to do here in the past, so it is a little bit
on the branchy/messy side since there are lots of different partial bits of
progress that have happened over time.

BP Internship Fall 2022
=======================

Daily Plan 2022-09-28
---------------------
 * Prepare python environment
   * Need to have a python3 installation
     * Link: https://www.python.org/downloads/release/python-3107/
     * Probably want Windows installer 64-bit - marked Recommended on the page
   * Need to have the pygame library
     * Once python is installed, run: pip install pygame
   * Need to have the pyyaml library
     * Once python is installed, run: pip install pyyaml
 * Prepare git for code access
   * Need to have a git software installation
     * Link: https://git-scm.com/download/win
     * Probably want the very first/top-most link for the latest build
   * Once git is installed, get the code!
     * git clone https://github.com/unidavemeyer/pygame-rpg.git
 * Start investigating the codebase to gain familiarity with it
   * To invoke, you'd run, e.g., python3 Game.py
     * If there isn't command-line access, we'd probably just double-click on Game.py
   * We probably need to update some Linux paths to work on Windows
     * example: Game.py loads fonts from /usr/share, which doesn't exist on Win
     * See if you can find other things like that which we'll need to update
     * Bonus: see if you can find reasonable alternatives (particularly for fonts)
   * What are the main functional pieces that make up the primary game loop?
   * What keys on the keyboard actually do anything? And, what do they do? Where is that code found?
 * Come up with a firmer set of goals for the internship
   * Example: Set up a hero character with actual art which can do realtime melee combat
   * Example: Set up NPC characters that can actually move and attack in interesting ways
   * Will want to discuss what we legitimately think can be done and how that aligns with interests
