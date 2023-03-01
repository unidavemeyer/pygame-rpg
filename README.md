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
 * ~Investigate why spawning isn't working consistently~
   * Found a possible issue (hero nearby) which has been adjusted, and added tracing to help track other issues
 * ~Fix bug with NPCs living past world load boundaries~
 * ~Find/prepare a good basic vector math introduction~
   * Maybe compare to single variable operations/expectations to show how the math Just Works (TM)
 * ~Consider how we want to do code reviews in this virtual model~
   * How do we get a git diff against the thing?
     * probably best model I've found: make a new branch, push that, then compare that branch to main
     * workflow then would be to do corrections on the branch until we're satisfied, and then merge it to main
   * ~Investigate how to add contributors to github project, consider doing so for interns~
     * This looks like it's pretty straightforward, and is a reasonable model to make this work
     * Alternative: Have people clone directly to their own github account, and then issue pull requests from said project
     * I *think* for the learning model I want, we'd prefer to be collaborators on the same project
   * ~Consider instruction and use of git branches~
     * Already did a little bit of this, which is great
   * ~What issues (if any!) exist for copyright, contribution, attribution, etc., for minors?~
     * Basic reading on the topic suggests copyright can be held by minors
     * Could be swirl with guardians, so should check on that front
     * E.g., could leave everything copyright by me, or could attribute; both have advantages
     * Current plan: direct/public credit and commits, etc.
 * ~Consider making whole own world chain for new npcs and such~
   * would be a good end-of-project goal, clean out stuff that's not necessary, etc.
   * other opportunity to make own art for the fun of it as well -- walls, floor, doorways (if desired)
   * ~Mentor to provide "episode" support on the menu so that this work can be slotted in~
     * ~May be a good opportunity to allow code review the other direction~
 * ~Do we want to add graphical health bars to hero, NPCs?~
   * Agreed that this was a good thing to add. Mentor to do this feature.
 * ~Open question for Mentor: Is there availability for following session?~
   * Yes, plan to continue for the following semester
 * ~Should we consider making a boss NPC of some kind?~
 * ~Approximate end for current session: January 22, with 3 days removed for holidays~
   * Suggests that current items should be completed and polished, probably boss NPC is last "add"
 * ~Should make update and render numbers into an enum/list type instead -- easier to see/maintain~
 * ~Will need to come up with a concrete plan to unify/solidify the damage model~
   * should have maybe all objects take damage? maybe? at the very least, all NPCs, but as a function
   * Mentor to investigate the work here once the Patroller branch is in
 * Consider making Npc.__init__() take max hp as a parameter to do setup once
 * Should remove the specific combat mode - only have menu and worldmap
 * Should convert to super() instead of direct class super calls
 * Do we want to add a melee attack for the hero and/or some of the NPCs?
   * Effective model: short radius auto-hit attack, maybe?
   * Do we want to allow the player to block? NPCs?
 * Consider an improved, enum-ized render/update/input model, maybe?
   * Would allow us to see in one spot what order things happen, allow reorder easily, insert, etc.
 * Consider a "freeze" or "slow" attack/aura for NPCs - reduce hero movement speed
 * Do we have any balance considerations?
 * Do we want inventory and inventory management?
   * Current model makes this seem unnecessary
 * Do we want to have an experience model and grow the hero stronger?
   * support grinding in the world?
   * unlock equipment, or just do stat gains?
   * allow player choice, or simply increase things automatically via whatever forumulas we cook up?
 * What is hero death model?
   * Do we start again, prior room?
   * Do we allow some kind of actual progress save system?
