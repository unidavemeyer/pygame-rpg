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

Mentor Work Item Backlog
------------------------
 * Investigate why spawning isn't working consistently
 * Do we want to add graphical health bars to hero, NPCs?
 * Consider a "freeze" or "slow" attack/aura for NPCs - reduce hero movement speed
 * Do we have any balance considerations?
 * Should we consider making a boss NPC of some kind?
 * Do we want inventory and inventory management?

Daily Plan 2022-09-28
---------------------
 * Prepare python environment
   * ~Need to have a python3 installation~
     * Link: https://www.python.org/downloads/release/python-3107/
     * Probably want Windows installer 64-bit - marked Recommended on the page
   * ~Need to have the pygame library~
     * Once python is installed, run: pip install pygame
   * Need to have the pyyaml library
     * Once python is installed, run: pip install pyyaml
 * ~Prepare git for code access~
   * ~Need to have a git software installation~
     * Link: https://git-scm.com/download/win
     * Probably want the very first/top-most link for the latest build
     * School did Github Desktop, which also works totally fine
   * ~Once git is installed, get the code!~
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

Daily Plan 2022-10-06
---------------------
 * Video call with Mentor in the morning to start up and again in the afternoon to wrap up
 * Discuss project goals
   * Possibility: Add simple AI behaviors to make interesting enemies (fixed path, heat seeking, random path, etc.)
   * Possibility: Add magic attack to hero to auto target and strike enemies (easier than melee)
   * Possibility: Add melee attack to hero to fight enemies at close range (more math involved)
   * Possibility: Add collectible coins as items
   * Possibility: Add hero inventory slots
   * Possibility: Add hero inventory menu/screen
   * Possibility: Add basic flipbook animation model for hero, enemies
   * Possibility: Add upgrade menu and ability upgrades for hero (stronger attack, more health, etc.)
 * Discuss basic game loop and features
   * ~Python uses "duck typing" - update, render follow this model~
   * ~Game - outer loop, does same thing over and over, handles, updates, then renders. Run is main entry point.~
     * Priority order is used to sort things to happen in the right relative order at each phase
     * Lower numbers go first, higher numbers go last
     * For event handling (responding to keys) lower numbers win over higher numbers
     * For updating (running game logic in response to input, etc.) lower numbers go first
     * For rendering (drawing) can think of "stack" of images, so higher numbers appear over the top of lower ones
     * We probably want to only use MENU and WORLDMAP modes, and ignore/remove COMBAT (it's for turn-based fights, not action ones)
   * Hero - character the player controls, can move around, etc.
     * Existing code structured for turn-based combat (ala a JRPG or what have you), but we can kill that if we want
     * Event handling tracks key down/up times and uses that to see press, hold, release, etc.
       * Could set up similar model to listen for an attack key, or a magic key, or whatever
     * VTargetComputeKeyboard is what determines the direction keyboard input is sending the hero
     * Update needs to gain kill checking (right now hero takes damage, but never dies)
   * Npc - various classes that provide enemies, etc.
     * We could/should make a new subclass for an action-based enemy, vs. Goon which is turn-based
     * OnUpdate would figure out where the enemy goes (if anywhere) and if they attack, etc.
     * Can probably ignore Animal for now, unless we decide to add collection of moving targets or something
       * It is also incomplete, so not a great example to look at
   * World - the background, walls, doors, etc.
     * Picks where hero, npcs, items, etc., are initially placed
     * Each screen full of stuff is its own world (think of them more almost like rooms rather than worlds)
     * Not sure why keys, locks are rendered specially in the World instead of having their own registration
     * .wld files are the worlds, which are text representations of what is to happen, etc.
     * Will need to update NpcSpawn function to support new enemy types, but should just be mpTypeFn and no other surgery (hopefully!)
     * May also consider having a "murder lock" instead of a keyed lock - kill all npcs from a spawner to open door and continue, etc.
   * Menu - provides a menu overlay for various menu purposes (start game, pause menu, etc.)
     * Handles escape key always, to bring up or bring down the menu
     * Can see that not many things are implemented yet (save, options, load)
     * Right now have just one single menu for all purposes, but if we wanted, could subclass and make self.m_lEntry be per subclass or something
   * Weapon - things the hero uses to deal damage
     * These are very turn-based ideas right now
     * Could make a new subclasses that weren't turn-based, and use them to be bound to keys for the hero
     * Should be fairly easy to make radius-based weapons with cooldowns, especially if we ignore walls, etc.
   * Item - stub class, nothing in here yet
 * See if we can get the game to run
   * may cheat and get yaml library ourselves, unpack, and put in there - process may work from prior internship
 * Look at a couple .wld files (start.wld is a good one to start with, for example)
   * consider changing an exit and build your own .wld file to see if you can make it work!
 * If we have goals set up, maybe start working on something in that area

Daily Plan 2022-10-13
---------------------
 * Video call with Mentor in the morning to start up and again in the afternoon to wrap up
 * ~Get the game running~
   * Get PyYaml installed via school installer
   * Get fonts figured out (if necessary)
 * ~Brief introduction to .wld files~
   * yaml format (= text that is readable by humans *and* good for programs to understand)
   * tiles section defines what the "tiles" that make up the level are
   * plan section defines the "picture" or "map" for the level, using the tiles
   * tiles can include instructional information in addition to image/color
     * walls
     * spawners (to make NPCs) - note that you can put settings in here too
     * start locations (for where hero begins when entering the level)
     * gates to go to other worlds
 * Discuss project goals
   * Possibility: Add simple AI behaviors to make interesting enemies (fixed path, heat seeking, random path, etc.)
   * Possibility: Add magic attack to hero to auto target and strike enemies (easier than melee)
   * Possibility: Add melee attack to hero to fight enemies at close range (more math involved)
   * Possibility: Add collectible coins as items
   * Possibility: Add hero inventory slots
   * Possibility: Add hero inventory menu/screen
   * Possibility: Add basic flipbook animation model for hero, enemies
   * Possibility: Add upgrade menu and ability upgrades for hero (stronger attack, more health, etc.)
 * Start working on something
   * Could make/modify a wld file to set up your own thing
   * Could try to adjust how fast the hero runs
   * Could try to add an NPC that moves in a fixed shape
   * Could try to add an NPC that moves toward the hero

Daily Plan 2022-10-13
---------------------
 * Video call with Mentor in the morning to start up and again in the afternoon to wrap up
   * Note funny schedule - may need to cut short morning call
 * Reminder on overall project goals
   * Add hero magic attack(s) to damage NPCs
   * Add two or more types of NPCs which move and damage the hero
   * Replace current "box art" characters with images
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
 * Add initial hero magic attack
   * Add appropriate "cooldowns" so that attack doesn't run back-to-back constantly
   * Find and apply damage to NPCs
   * Determine behavior for long press: allow auto attack or require re-press by player?
   * Bonus: Add some kind of basic graphical display for the attack happening
 * Add a heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Add a "fixed path" NPC
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Add a "rebound" NPC
   * How does impact & bounce calculation work?
   * What about initial setup for motion, how is that specified?
 * Replace hero an NPC(s) with images
 * Consider how flipbook animation would work
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?

