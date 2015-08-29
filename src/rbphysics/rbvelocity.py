from math import cos, sin, radians


class RBVector(object):

    def __init__(self, x=0, y=0, magnitude=None, angle=None):
        if magnitude is None or angle is None:
            self.setVector(x, y)
        else:
            self.calculateVector(magnitude, angle)

    def setVector(self, x, y):
        self._x = x
        self._y = y

    def calculateVector(self, magnitude, angle):
        print angle, radians(angle)
        self._x = magnitude * cos(radians(angle))
        self._y = magnitude * sin(radians(angle))
        print self._x, self._y

    def getX(self):
        return self._x

    def getY(self):
        return self._y


class RBVelocity(object):

    def __init__(self, speed=0, angle=0):
        self._speed = speed
        self._angle = angle
        self._velocity = RBVector(magnitude=self._speed, angle=self._angle)

    def calculateVelocity(self):
        self._velocity.calculateVector(self._speed, self._angle)

    def setSpeed(self, speed):
        self._speed = speed
        self.calculateVelocity()

    def setAngle(self, angle):
        self._angle = angle
        self.calculateVelocity()

    def changeSpeed(self, speedChange):
        self.setSpeed(self._speed + speedChange)

    def changeAngle(self, angleChange):
        self.setAngle(self._angle + angleChange)

    def getVelocityVector(self):
        return self._velocity

    def getVelocityX(self):
        return self._velocity.getX()

    def getVelocityY(self):
        return self._velocity.getY()

    def setExitVelocity(self, direction):
        if direction.lower() == "up" or direction.lower() == "down":
            self._velocity._y *= -1
        elif direction.lower() == "left" or direction.lower() == "right":
            self._velocity._x *= -1
