# Vec.py
#
# Copyright (c) 2012 by David Meyer
import math
import numbers

class Vec:
	"""Simple 2-d vector class supporting various common operations."""

	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def Len(self):
		"""Returns the length of this vector."""

		return math.sqrt(self.x * self.x + self.y * self.y)

	def Normal(self):
		"""Returns a normalized version of this vector."""

		s = self.Len()
		if s < 0.00001:
			return Vec(0, 0)

		sInv = 1.0 / s
		return sInv * self

	def __add__(self, other):
		"""Adds this to the other operand and returns the result (Vec only)."""

		if not isinstance(other, Vec):
			return NotImplemented

		return Vec(other.x + self.x, other.y + self.y)

	def __sub__(self, other):
		"""Subtracts the other vector from this and returns the result (Vec only)."""

		if not isinstance(other, Vec):
			return NotImplemented

		return Vec(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		"""Multiplies the other operand by this vector and returns the result (Numeric only)."""

		if not isinstance(other, numbers.Number):
			return NotImplemented

		return Vec(other * self.x, other * self.y)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __repr__(self):
		"""Prints out a version of this vector."""

		return "(%.3f, %.3f)" % (self.x, self.y)



def VecLimitLen(vec, sMax):
	"""Returns a vector that's in the same direction as the input, but with length limited"""
	""" to at most the given maximum."""

	sVec = vec.Len()
	if sVec < sMax:
		return vec
	else:
		return sMax * vec.Normal()

def SDistPos(pos0, pos1):
	"""Returns the distance between the two given points."""

	dPos = pos0 - pos1
	return dPos.Len()

def VecCircle(radAngle, sLength):
	"""Returns a vector representing the given angle and then given length."""

	x = math.cos(radAngle) * sLength
	y = math.sin(radAngle) * sLength
	return Vec(x, y)

def Lerp(t0, t1, u):
	"""Interpolates between t0 and t1 based on u (u=0 gives t0)"""

	# BB (davidm) hacky/fragile...would be better to handle types here more explicitly, I think?

	if isinstance(t0, (tuple, list)):
		assert isinstance(t1, (tuple, list))
		return tuple([Lerp(x0, x1, u) for x0, x1 in zip(t0, t1)])

	dT = t1 - t0
	return t0 + u * dT
