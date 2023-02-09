# Vector Math

## Basics

These are some hopefully helpful tips about how to work with vector math generally, and how to do
some things specifically with the vector class in this project (provided by Vec.py).

A vector in this project is a pair of numbers (x,y) which can represent at least two different but
related things:

 * A vector can be used to represent the position of something in the game, where the
   (x,y) values indicate which column (x) and row (y) we want something to be at. (Typically we use this
   to mean where the upper left-hand corner of the object or surface will be, which is maybe odd but is
   how we're doing things here.)
 * A vector can be used to represent an offset between two other positions, or a "delta" or adjustment
   to apply to some other vector (either a position or a delta/offset). In this case the (x,y) do not
   mean a specific column/row, but instead mean how much to change or offset a column and a row.

Examples:

 * To keep track of a position at column 10, row 3, we could write `pos = Vec.Vec(10, 3)`
 * If we wanted to know an offset by 4 columns and 0 rows, we could write `dPos = Vec.Vec(4, 0)`
 * Offsets can also be negative! `dPos = Vec.Vec(-3, -2)`

## Operators

Vectors become particularly useful when you start doing math with them. If you're familiar with
algebra, then you're actually pretty much familiar with vectors as well and you can do a lot of
what you may want. There are a couple of things that are important to keep in mind which will
simplify much of what you do with vector math, particularly as we use it in this project:

 * If you add an offset to a position, you effectively get a new position that is the result of
   starting at the original position and moving by the offset from there: `posEnd = posStart + dPosOffset`
   * Tip: It's rare for us to need to subtract an offset from a point, but it sometimes happens. If you
     do that, e.g. `posEnd = posStart - dPosOffset` you'll offset *backwards* from what the offset says.
 * If you subtract two positions, you'll get the offset which is necessary to get to the end
   position from the start position: `dPosOffset = posEnd - posStart`
   * **NOTE** The order you subtract matters! Always subtract the start from the end!
   * Tip: You can also think about this algebraicly: If `dPos = posEnd - posStart` then by algebra
     it should be that `posStart + dPos = posStart + posEnd - posStart = posStart - posStart + posEnd = posEnd`
     and so that `dPos` means how to get to `posEnd` starting from `posStart`
 * If you multiply a vector by a plain number, you scale the vector, which changes its length but
   doesn't change the direction it points: `dPosDouble = 2 * dPosOrig` or `dPosHalf = 0.5 * dPosOrig`
 * Multiplying two vectors together doesn't really make sense for what we're doing, and isn't supported

Examples:

 * If we want to know how to move an NPC to the hero, we calculate `dPos = posHero - posNpc`
 * If we only want to move 10% of the way from our start to our target, and have `dPos = posTarget - posStart`,
   we can do `posNext = posStart + 0.1 * dPos`

## Helpful Functions

The Vec module also contains a few helpful functions, one on the Vec class, and a few that are standalone.
These are useful to handle some very common cases of things that I've wanted to do.

 * The `Vec` class has a `Len()` function which tells you how long a vector is. This doesn't usually make sense
   if you are using a vector as a position, but when using one as an offset/delta, knowing the length is very
   useful because it tells you how far apart two positions are from each other, etc.: `dist = dPos.Len()`
 * The `VecLimitLen()` function lets you get a new vector from an existing one that is at most as long as what
   you asked: `dPosLimited = Vec.VecLimitLen(dPosOrig, 3)` gives you a copy of `dPosOrig` that is at most length 3,
   for example. (If `dPosOrig` is less than 3 units long, you'll just get back `dPosOrig`.) This is useful for
   cases where you want something to move toward a goal, but not just teleport there -- you can calculate the
   offset to get to the goal from the current position, but then limit the length, and add that to the current
   to take a "step" along the way: `dPosFull = posGoal - posStart; dPosLim = Vec.VecLimitLen(dPosFull, 2); posNext = posStart + dPosLim`
 * The `Vec` class has a `Normal()` function which gives you a special *normalized* version of a vector, which
   means that the length is 1 but the direction matches the original vector's direction. You probably won't
   end up needing to use this often (the common use cases have more helpful functions that package up more
   stuff, but I'm mentioning it here): `dPosNormal = dPos.Normal()`

