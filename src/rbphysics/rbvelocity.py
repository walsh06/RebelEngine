import math


class RBVector(object):

	def __init__(self, x=0, y=0):
		self.setVector(x, y)

	def setVector(self, x, y):
		self._x = x
		self._y = y

	def calculateVector(self, magnitude, angle):
		self._x = magnitude * math.cos(math.radians(angle))
		self._y = magnitude * math.sin(math.radians(angle))


class RBVelocity(object):

	def __init__(self, speed=0, angle=0):
		self._speed = speed
		self._angle = angle
		self._velocity = RBVector()

	def calculateVelocity(self):
		self._velocity.calculateVector(self._speed, self._angle)

	def setSpeed(self, speed):
		self._speed = speed
		self.calculateVelocity()

	def setAngle(self, angle):
		self._angle = angle
		self.calculateVelocity()
