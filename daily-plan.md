BP Internship Spring 2023
=========================

Daily Plan 2023-01-19
---------------------
 * Video call with Mentor in the morning to start up and again in the afternoon to wrap up
   * Can do additional checks in the day if necessary
   * Note that mentor will be out 1:30 - 2:30 for exhibition (may need to adjust call schedule)
 * Discussion on overall project goals for this semester
   * Finish off fireball & boss classes
   * Create end-to-end world as example to show entirely own work
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
   * Other things of interest? Also there is hardening that needs to happen.
 * Fireball class (boss and maybe later hero projectile weapon)
   * Game object (single, for whole game) runs everything in phases: handle input, update, render
   * Fireball won't need input, so just needs update and render to be connected up to game (see Npc's __init__ for AddRender, AddUpdate calls)
     * Game will call update on everyone that needs to update, in priority order (fireball: use probably 10 as priority, to go early)
     * Game will call render on everyone that needs to render, in priority order (fireball: use probably 95 as priority, to go late/top)
   * Fireball will need to have an OnUpdate function taking self as arg (see Run function in Game.py)
     * this is where the fireball should decide how and where to move
   * Fireball will need to have an OnRender function taking self and surf as args (see Run function in Game.py)
     * this is where the fireball will need to draw itself to the input surface - see Npc's OnRender as an example
   * When the boss wants to shoot, its OnUpdate function (or a function called by it) should create a Fireball object
     * This suggests that __init__ on class Fireball will want to take a starting and a target position as arguments as well
     * Recall to create an object with a class, you just pretend the class name is a function, e.g., Fireball(posStart, posTarget)
     * The boss probably doesn't need to remember the fireball as a variable, but you may feel differently
 * Continue work on miniboss NPC
   * Discuss class inheritance plan with mentor - should derive from Patroller
   * Discuss plans for projectiles with mentor - will follow NPC model, but not be an NPC
   * Note that damage should wait -- don't worry about setting up health/hitpoints on the boss -- will be generic
 * Start setting up separate episode to demonstrate full end-to-end behaviors
   * Remember to do this as its own branch off of the main branch
   * See Menu.py for where to hook this up
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Make "facing you" statue
   * Remember to do this as its own branch off of the main branch
   * Fun flavor element to add to world
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Add "heat seeking" version of projectiles used by miniboss
   * Consider if this will adjust timing of damage -- probably should?
   * Experiment with "held key" behavior -- repeated attack with cooldown?
 * Can/should we introduce a physics-aware NPC model?
   * How crazy/simple/whatever should we make the pathing model? Full up A-star?
   * Are we OK with keeping "ghosts" that can just go through walls arbitrarily for heat seekers?

BP Internship Fall 2022
=======================

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
 * ~Discuss project goals~
   * Possibility: Add simple AI behaviors to make interesting enemies (fixed path, heat seeking, random path, etc.)
   * Possibility: Add magic attack to hero to auto target and strike enemies (easier than melee)
   * Possibility: Add melee attack to hero to fight enemies at close range (more math involved)
   * Possibility: Add collectible coins as items
   * Possibility: Add hero inventory slots
   * Possibility: Add hero inventory menu/screen
   * Possibility: Add basic flipbook animation model for hero, enemies
   * Possibility: Add upgrade menu and ability upgrades for hero (stronger attack, more health, etc.)
 * Start working on something
   * ~Could make/modify a wld file to set up your own thing~
   * Could try to adjust how fast the hero runs
   * Could try to add an NPC that moves in a fixed shape
   * Could try to add an NPC that moves toward the hero

Daily Plan 2022-10-20
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
 * ~Add a heat seeking NPC~
   * NOTE: most considerations below here haven't happened - good to discuss, etc.
   * NOTE: should see about getting current state reviewed and updated and such
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Add a "fixed path" NPC
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Add a "rebound" NPC
   * How does impact & bounce calculation work?
   * What about initial setup for motion, how is that specified?
 * ~Replace hero and NPC(s) with images~
 * Consider how flipbook animation would work
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?

Daily Plan 2022-10-27
---------------------
 * ~Video call with Mentor in the morning to start up and again in the afternoon to wrap up~
   * Note funny schedule - may need to cut short morning call
 * Reminder on overall project goals
   * Add hero magic attack(s) to damage NPCs
   * Add two or more types of NPCs which move and damage the hero
   * Replace current "box art" characters with images
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
 * ~Discuss review & commit plans~
   * Should effectively "wrap up" current work to get it ready for review
   * Should do review, make adjustments, then see about getting committed to public repo
 * ~Discuss image size constraints~
   * Code operates expecting 32x32
   * Could scale images maybe
   * Could adjust assumptions - but that would imply rebuilding doors, other grid cells, etc.
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * ~Add initial hero magic attack~
   * Add appropriate "cooldowns" so that attack doesn't run back-to-back constantly
   * Find and apply damage to NPCs
   * Determine behavior for long press: allow auto attack or require re-press by player?
   * Bonus: Add some kind of basic graphical display for the attack happening
 * Add a "fixed path" NPC
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Add a "rebound" NPC
   * How does impact & bounce calculation work?
   * What about initial setup for motion, how is that specified?
 * Consider how flipbook animation would work
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?

Daily Plan 2022-11-03
---------------------
 * ~Video call with Mentor in the morning to start up and again in the afternoon to wrap up~
   * Can do additional checks in the day if necessary
   * Morning call may be a bit longer today - want to get review process going (if possible!)
 * Reminder on overall project goals
   * Add hero magic attack(s) to damage NPCs
   * Add two or more types of NPCs which move and damage the hero
   * Replace current "box art" characters with images
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
   * Create end-to-end world as example to show entirely own work
 * ~Start on review process for current work~
   * ~Create a new branch~
   * ~Push the branch to the public repository~
   * ~Compare that branch to the main branch via /compare URL (and links therein on the github website)~
   * Iterate on changes to the new branch until review work is satisfied
     * Remember to test changes as you go, and commit working pieces to the branch!
   * Finally, merge branch into main branch, and then can remove old branch (if desired -- may leave in place)
 * Add a "fixed path" NPC
   * Continue learning more about Vector math from Khan Academy as needed to improve knowledge/skills here
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Consider how to create whole different world
   * Possible: Mentor to set up "New Game" to allow selection of "episode"
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Add some kind of "mini boss" NPC
   * Need to discuss appropriate AI goals here
 * Consider how flipbook animation would work
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Experiment with "held key" behavior -- repeated attack with cooldown?
   * Possibility: Add some kind of basic graphical display for the attack happening

Daily Plan 2022-11-10
---------------------
 * ~Video call with Mentor in the morning to start up and again in the afternoon to wrap up~
   * Can do additional checks in the day if necessary
   * Do we have updates on dates for work on the project for planning?
 * Reminder on overall project goals
   * Add hero magic attack(s) to damage NPCs
   * Add two or more types of NPCs which move and damage the hero
   * Replace current "box art" characters with images
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
   * Create end-to-end world as example to show entirely own work
 * ~Continue review process~
   * Npc.py, World.py, and fifth.wld still need to be reviewed (probably not much on the last)
   * Will want a re-review after all changes are made to the branch and pushed
   * Should also do a review the "other way" for the episode work (good experience!)
 * Add a "fixed path" NPC
   * Continue learning more about Vector math from Khan Academy as needed to improve knowledge/skills here
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Start setting up separate episode to demonstrate full end-to-end behaviors
   * See Menu.py for where to hook this up
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Add some kind of "mini boss" NPC
   * Need to discuss appropriate AI goals here
 * Consider how flipbook animation would work
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Experiment with "held key" behavior -- repeated attack with cooldown?
   * Possibility: Add some kind of basic graphical display for the attack happening

Daily Plan 2022-11-17
---------------------
 * ~Video call with Mentor in the morning to start up and again in the afternoon to wrap up~
   * Can do additional checks in the day if necessary
   * Mentor has meeting in the morning so there will be a specific period of unavailability
 * Reminder on overall project goals
   * Add two or more types of NPCs which move and damage the hero
   * Create end-to-end world as example to show entirely own work
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
 * ~Do a merge to pull changes from the main branch in to the Patroller branch~
   * Mentor to assist in this process to explain how things work as necessary
   * That will get said feature up and running with latest tech
 * ~Continue developing a "fixed path" NPC~
   * Continue learning more about Vector math from Khan Academy as needed to improve knowledge/skills here
   * How is the path to follow defined?
   * Does NPC ever deviate, say for close range hero?
 * Start setting up separate episode to demonstrate full end-to-end behaviors
   * See Menu.py for where to hook this up
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Add some kind of "mini boss" NPC
   * Need to discuss appropriate AI goals here
 * Consider how flipbook animation would work
   * Do we wish to pursue this? Seems like world setup and AI work is more of interest...
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Experiment with "held key" behavior -- repeated attack with cooldown?
   * Possibility: Add some kind of basic graphical display for the attack happening

Daily Plan 2022-12-08
---------------------
 * ~Video call with Mentor in the morning to start up and again in the afternoon to wrap up~
   * Can do additional checks in the day if necessary
 * Reminder on overall project goals
   * Add two or more types of NPCs which move and damage the hero
   * Create end-to-end world as example to show entirely own work
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
 * ~Continue work on miniboss NPC~
   * Discuss class inheritance plan with mentor - should derive from Patroller
   * Discuss plans for projectiles with mentor - will follow NPC model, but not be an NPC
   * Do not do further work in the Patroller branch once the patroller and mini boss + projectile are working!
   * Will want to review that branch, do fixes, and merge to main before continuing
 * Start setting up separate episode to demonstrate full end-to-end behaviors
   * See Menu.py for where to hook this up
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Make "facing you" statue
   * Fun flavor element to add to world
 * Consider how flipbook animation would work
   * Do we wish to pursue this? Seems like world setup and AI work is more of interest...
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Add "heat seeking" version of projectiles used by miniboss
   * Consider if this will adjust timing of damage -- probably should?
   * Experiment with "held key" behavior -- repeated attack with cooldown?
 * Can/should we introduce a physics-aware NPC model?
   * How crazy/simple/whatever should we make the pathing model? Full up A-star?
   * Are we OK with keeping "ghosts" that can just go through walls arbitrarily for heat seekers?

Daily Plan 2022-12-15
---------------------
 * Video call with Mentor in the morning to start up and again in the afternoon to wrap up
   * Can do additional checks in the day if necessary
 * Reminder on overall project goals
   * Add two or more types of NPCs which move and damage the hero
   * Create end-to-end world as example to show entirely own work
   * Add flipbook animations for moving and maybe attacking characters (hero, npc)
 * Discuss document that intern needs mentor to look over and/or sign off on
 * Discuss some additional vector math primer stuff
   * Mentor to provide information on this topic
 * Discuss how flipbook animation would work
   * Do we wish to pursue this? Seems like world setup and AI work is more of interest...
   * Interested, but not current semester
   * Effectively back-to-back images, pick which to show at any given time
   * Could change based on motion, could change based on time, or a mix of the two
   * Bonus: image interpolation to get "smooth frame" behavior?
 * ~Get patroller branch fixes tested and pushed~
   * Mentor will then do the branch merge
 * Continue work on miniboss NPC
   * Discuss class inheritance plan with mentor - should derive from Patroller
   * Discuss plans for projectiles with mentor - will follow NPC model, but not be an NPC
   * Note that damage should wait -- don't worry about setting up health/hitpoints on the boss -- will be generic
 * Fireball class (boss and maybe later hero projectile weapon)
   * Game object (single, for whole game) runs everything in phases: handle input, update, render
   * Fireball won't need input, so just needs update and render to be connected up to game (see Npc's __init__ for AddRender, AddUpdate calls)
     * Game will call update on everyone that needs to update, in priority order (fireball: use probably 10 as priority, to go early)
     * Game will call render on everyone that needs to render, in priority order (fireball: use probably 95 as priority, to go late/top)
   * Fireball will need to have an OnUpdate function taking self as arg (see Run function in Game.py)
     * this is where the fireball should decide how and where to move
   * Fireball will need to have an OnRender function taking self and surf as args (see Run function in Game.py)
     * this is where the fireball will need to draw itself to the input surface - see Npc's OnRender as an example
   * When the boss wants to shoot, its OnUpdate function (or a function called by it) should create a Fireball object
     * This suggests that __init__ on class Fireball will want to take a starting and a target position as arguments as well
     * Recall to create an object with a class, you just pretend the class name is a function, e.g., Fireball(posStart, posTarget)
     * The boss probably doesn't need to remember the fireball as a variable, but you may feel differently
 * Start setting up separate episode to demonstrate full end-to-end behaviors
   * Remember to do this as its own branch off of the main branch
   * See Menu.py for where to hook this up
   * Consider some kind of interesting layout -- multiple rooms (Worlds) with different enemy types?
   * Could make own art for walls, floors, etc., to go with characters - remember 32x32 image size
 * Make "facing you" statue
   * Remember to do this as its own branch off of the main branch
   * Fun flavor element to add to world
 * Discuss further work on heat seeking NPC
   * Consider range - how close is the hero before this activates?
   * Consider velocity target based approach - discuss with mentor to get the basic idea there
   * Consider how NPC attacking works - contact? short range "stomp"? other?
 * Consider improvements to hero magic attack
   * Add "heat seeking" version of projectiles used by miniboss
   * Consider if this will adjust timing of damage -- probably should?
   * Experiment with "held key" behavior -- repeated attack with cooldown?
 * Can/should we introduce a physics-aware NPC model?
   * How crazy/simple/whatever should we make the pathing model? Full up A-star?
   * Are we OK with keeping "ghosts" that can just go through walls arbitrarily for heat seekers?

