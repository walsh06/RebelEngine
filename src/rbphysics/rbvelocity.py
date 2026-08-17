from math import cos, sin, radians, atan2, degrees, hypot


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
        self._x = magnitude * cos(radians(angle))
        self._y = magnitude * sin(radians(angle))

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    # Properties - Pythonic access to vector components
    @property
    def x(self):
        """X component of the vector"""
        return self._x

    @property
    def y(self):
        """Y component of the vector"""
        return self._y

    @property
    def magnitude(self):
        """Length of the vector"""
        return hypot(self._x, self._y)

    @property
    def angle(self):
        """Angle of the vector in degrees"""
        return degrees(atan2(self._y, self._x))

    # Vector arithmetic operations
    def __add__(self, other):
        """Add two vectors: vector1 + vector2"""
        if not isinstance(other, RBVector):
            raise TypeError(f"Cannot add RBVector and {type(other).__name__}")
        return RBVector(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        """Subtract two vectors: vector1 - vector2"""
        if not isinstance(other, RBVector):
            raise TypeError(f"Cannot subtract {type(other).__name__} from RBVector")
        return RBVector(self._x - other._x, self._y - other._y)

    def __mul__(self, scalar):
        """Multiply vector by scalar: vector * scalar"""
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Cannot multiply RBVector by {type(scalar).__name__}")
        return RBVector(self._x * scalar, self._y * scalar)

    def __rmul__(self, scalar):
        """Right multiplication: scalar * vector"""
        return self.__mul__(scalar)

    def normalize(self):
        """Return a unit vector (magnitude = 1) in the same direction"""
        mag = self.magnitude
        if mag > 0:
            return RBVector(self._x / mag, self._y / mag)
        return RBVector(0, 0)

    def __repr__(self):
        """String representation for debugging"""
        return f"RBVector(x={self._x:.2f}, y={self._y:.2f}, mag={self.magnitude:.2f}, angle={self.angle:.1f}°)"

    def __str__(self):
        """Readable string representation"""
        return f"({self._x:.2f}, {self._y:.2f})"



class RBVelocity(object):

    @classmethod
    def fromPositions(cls, speed, posOne, posTwo):
        vel = cls(speed, 0)
        vecOne = RBVector(posOne.x, posOne.y)
        vecTwo = RBVector(posTwo.x, posTwo.y)
        vec = vecTwo - vecOne
        vec = vec.normalize()
        vec = vec * speed
        vel.set_velocity_components(vec.x, vec.y)
        return vel
        
    def __init__(self, speed=0, angle=0):
        if speed < 0:
            raise ValueError(f"Speed cannot be negative (got {speed})")
        self._speed = speed
        self._angle = angle
        self._velocity = RBVector(magnitude=self._speed, angle=self._angle)

    def calculateVelocity(self):
        self._velocity.calculateVector(self._speed, self._angle)

    def setSpeed(self, speed):
        if speed < 0:
            raise ValueError(f"Speed cannot be negative (got {speed})")
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

    # Properties - Pythonic access to velocity components
    @property
    def speed(self):
        """Current speed magnitude"""
        return self._speed

    @speed.setter
    def speed(self, value):
        """Set speed magnitude"""
        self.setSpeed(value)

    @property
    def angle(self):
        """Current angle in degrees"""
        return self._angle

    @angle.setter
    def angle(self, value):
        """Set angle in degrees"""
        self.setAngle(value)

    @property
    def velocity_x(self):
        """X component of velocity"""
        return self._velocity.getX()

    @property
    def velocity_y(self):
        """Y component of velocity"""
        return self._velocity.getY()

    def set_velocity_components(self, x, y):
        """Set velocity by x/y components directly, recalculate speed/angle"""
        self._velocity.setVector(x, y)
        self._syncFromVector()

    def reflect(self, direction):
        """
        Reflect velocity in a direction (like bouncing off a wall).
        
        Args:
            direction: "up", "down", "left", or "right"
                      - "up"/"down" reflect y-component (vertical wall)
                      - "left"/"right" reflect x-component (horizontal wall)
        """
        if direction.lower() in ("up", "down"):
            self._velocity.setVector(self.velocity_x, -self.velocity_y)
        elif direction.lower() in ("left", "right"):
            self._velocity.setVector(-self.velocity_x, self.velocity_y)
        else:
            raise ValueError(f"Invalid direction: {direction}. Must be 'up', 'down', 'left', or 'right'")
        self._syncFromVector()

    def _syncFromVector(self):
        """Update speed/angle from x/y components after direct modification"""
        x = self._velocity.getX()
        y = self._velocity.getY()
        self._speed = hypot(x, y)
        self._angle = degrees(atan2(y, x))

