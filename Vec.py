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

	def __radd__(self, other):
		"""Adds this to the other operand and returns the result (Vec only)."""

		if not isinstance(other, Vec):
			return NotImplemented

		return Vec(other.x + self.x, other.y + self.y)

	def __rsub__(self, other):
		"""Subtracts this vector from the other operand and returns the result (Vec only)."""

		if not isinstance(other, Vec):
			return NotImplemented

		return Vec(other.x - self.x, other.y - self.y)

	def __rmul__(self, other):
		"""Multiplies the other operand by this vector and returns the result (Numeric only)."""

		if not isinstance(other, numbers.Number):
			return NotImplemented

		return Vec(other * self.x, other * self.y)

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
