import sys
import os
from math import pi, sin
from random import uniform

sys.path.append(os.path.join(".."))

from rbphysics.rbvelocity import RBVelocity


class RBBehaviour(object):
    """Base class for reusable, attachable object behaviours.

    A behaviour is one self-contained piece of per-frame logic. Attach any
    number to a game object with addBehaviour(); the world calls execute() on
    each every frame. Because they only touch the object passed in, the same
    behaviour class can be reused across many different objects.
    """

    def execute(self, obj, deltaTime):
        pass


def _targetPos(target):
    """Resolve a target to (x, y), accepting a game object or a position."""
    if hasattr(target, "getPos"):
        target = target.getPos()
    return target.x, target.y


def _ensureVelocity(obj):
    """Return the object's velocity, creating a zeroed one if it has none."""
    velocity = obj.getVelocity()
    if velocity is None:
        velocity = RBVelocity(0, 0)
        obj.setVelocity(velocity)
    return velocity


class RBSeek(RBBehaviour):
    """Steer the object's velocity toward a target at a fixed speed.

    target may be a static position or another game object, in which case the
    object keeps chasing it as it moves. Once within arriveRadius the object
    stops so it does not jitter on top of the target.
    """

    def __init__(self, target, speed, arriveRadius=0.0):
        self._target = target
        self._speed = speed
        self._arriveRadius = arriveRadius

    def execute(self, obj, deltaTime):
        tx, ty = _targetPos(self._target)
        pos = obj.getPos()
        dx = tx - pos.x
        dy = ty - pos.y
        velocity = _ensureVelocity(obj)
        distance = (dx * dx + dy * dy) ** 0.5
        if distance == 0 or distance <= self._arriveRadius:
            velocity.set_velocity_components(0.0, 0.0)
            return
        scale = self._speed / distance
        velocity.set_velocity_components(dx * scale, dy * scale)


class RBFlee(RBBehaviour):
    """Steer the object's velocity directly away from a target.

    With panicRadius set, the object only flees while the target is within that
    distance and stays still otherwise; leave it None to always flee.
    """

    def __init__(self, target, speed, panicRadius=None):
        self._target = target
        self._speed = speed
        self._panicRadius = panicRadius

    def execute(self, obj, deltaTime):
        tx, ty = _targetPos(self._target)
        pos = obj.getPos()
        dx = pos.x - tx
        dy = pos.y - ty
        velocity = _ensureVelocity(obj)
        distance = (dx * dx + dy * dy) ** 0.5
        if distance == 0 or (self._panicRadius is not None and distance > self._panicRadius):
            velocity.set_velocity_components(0.0, 0.0)
            return
        scale = self._speed / distance
        velocity.set_velocity_components(dx * scale, dy * scale)


class RBPatrol(RBBehaviour):
    """Move through a list of waypoints in order at a fixed speed.

    On reaching a waypoint (within reachRadius) it heads for the next. With
    loop=True it cycles back to the first waypoint; otherwise it reverses and
    patrols back and forth. Waypoints may be positions or game objects.
    """

    def __init__(self, waypoints, speed, loop=True, reachRadius=2.0):
        if len(waypoints) < 2:
            raise ValueError("RBPatrol needs at least two waypoints")
        self._waypoints = waypoints
        self._speed = speed
        self._loop = loop
        self._reachRadius = reachRadius
        self._index = 0
        self._direction = 1

    def execute(self, obj, deltaTime):
        tx, ty = _targetPos(self._waypoints[self._index])
        pos = obj.getPos()
        dx = tx - pos.x
        dy = ty - pos.y
        velocity = _ensureVelocity(obj)
        distance = (dx * dx + dy * dy) ** 0.5
        if distance <= self._reachRadius:
            self._advance()
            return
        scale = self._speed / distance
        velocity.set_velocity_components(dx * scale, dy * scale)

    def _advance(self):
        if self._loop:
            self._index = (self._index + 1) % len(self._waypoints)
            return
        nextIndex = self._index + self._direction
        if nextIndex >= len(self._waypoints) or nextIndex < 0:
            self._direction *= -1
        self._index += self._direction


class RBOscillate(RBBehaviour):
    """Bob the object back and forth along an axis with a sine wave.

    Gives a smooth hover/float effect (amplitude in pixels, frequency in cycles
    per second) by nudging the position directly, so it layers on top of any
    velocity the object already has. axis is a (dx, dy) direction, normalised.
    """

    def __init__(self, amplitude, frequency, axis=(0, 1)):
        self._amplitude = amplitude
        self._frequency = frequency
        length = (axis[0] ** 2 + axis[1] ** 2) ** 0.5 or 1.0
        self._axis = (axis[0] / length, axis[1] / length)
        self._time = 0.0
        self._offset = 0.0

    def execute(self, obj, deltaTime):
        self._time += deltaTime
        target = self._amplitude * sin(2 * pi * self._frequency * self._time)
        delta = target - self._offset
        self._offset = target
        obj.movePos(self._axis[0] * delta, self._axis[1] * delta)


class RBTurn(RBBehaviour):
    """Continuously rotate the object's velocity heading.

    Turns the velocity by turnRate degrees per second, curving the path (a
    positive rate turns one way, negative the other). Combined with a forward
    speed this makes the object arc or circle. Does nothing without a velocity.
    """

    def __init__(self, turnRate):
        self._turnRate = turnRate

    def execute(self, obj, deltaTime):
        velocity = obj.getVelocity()
        if velocity is None:
            return
        velocity.changeAngle(self._turnRate * deltaTime)


class RBAccelerate(RBBehaviour):
    """Apply a constant acceleration to the object's velocity each frame.

    Useful for gravity, thrust or drag: ax/ay are in units per second squared
    and are integrated into the velocity components over time.
    """

    def __init__(self, ax, ay):
        self._ax = ax
        self._ay = ay

    def execute(self, obj, deltaTime):
        velocity = _ensureVelocity(obj)
        velocity.set_velocity_components(
            velocity.getVelocityX() + self._ax * deltaTime,
            velocity.getVelocityY() + self._ay * deltaTime,
        )


class RBWander(RBBehaviour):
    """Drift with a randomly wandering heading at a fixed speed.

    Each frame the heading is nudged by up to jitter degrees, giving aimless,
    organic movement for idle NPCs. A velocity is created at the given speed if
    the object has none.
    """

    def __init__(self, speed, jitter=90.0):
        self._speed = speed
        self._jitter = jitter

    def execute(self, obj, deltaTime):
        velocity = _ensureVelocity(obj)
        velocity.setSpeed(self._speed)
        velocity.changeAngle(uniform(-self._jitter, self._jitter) * deltaTime)


class RBDespawnAfter(RBBehaviour):
    """Mark the object for removal after a fixed lifetime in seconds.

    Handy for temporary effects, projectiles or spawned particles that should
    clean themselves up.
    """

    def __init__(self, seconds):
        self._seconds = seconds
        self._elapsed = 0.0

    def execute(self, obj, deltaTime):
        self._elapsed += deltaTime
        if self._elapsed >= self._seconds:
            obj.removeObject()


class RBDespawnOutsideBounds(RBBehaviour):
    """Mark the object for removal once it leaves a rectangular region.

    Stops fire-and-forget objects (projectiles, particles) from lingering and
    accumulating after they travel off screen. Bounds are in world coordinates.
    """

    def __init__(self, minX, minY, maxX, maxY):
        self._minX = minX
        self._minY = minY
        self._maxX = maxX
        self._maxY = maxY

    def execute(self, obj, deltaTime):
        pos = obj.getPos()
        if (pos.x < self._minX or pos.x > self._maxX
                or pos.y < self._minY or pos.y > self._maxY):
            obj.removeObject()

