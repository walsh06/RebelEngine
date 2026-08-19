import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbgameobject import RBGameObject, DEFAULT_GAME_OBJECT
from rbphysics.rbcollisionobjects import RBBoundingBox
from rbphysics.rbvelocity import RBVelocity
from rbcontroller.rbcontroller import KEY_DOWN, KEY_UP


class RBPlayer(RBGameObject):
    """A controllable game object that is stopped by solid objects.

    Movement respects solids without the game having to resolve collisions:
    - Velocity-driven: give the player a velocity and the world integrates it,
      stopping it against solids automatically. initTopDownControls() wires the
      keyboard straight into the velocity for a ready-made control scheme.
    - Input-driven: call move()/moveDirection() each frame; both route through
      RBWorld.tryMove so the player slides along walls and rests on the ground
      instead of penetrating them.
    """

    def __init__(self, pos, graphic, collider=None, speed=0, behaviours=None,
                 gameObjectType=DEFAULT_GAME_OBJECT):
        if collider is None:
            collider = RBBoundingBox.fromGraphic(pos, graphic)
        super(RBPlayer, self).__init__(pos, graphic=graphic, collider=collider,
                                       behaviours=behaviours,
                                       gameObjectType=gameObjectType, solid=False)
        self._speed = speed
        self._moveDirs = {"up": False, "down": False, "left": False, "right": False}

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        if self._velocity is not None:
            self._updateVelocityFromDirs()

    ## Movement

    def move(self, world, dx, dy):
        """
        Move by (dx, dy) this frame, blocked per-axis by the world's solids.

        Returns:
            (blockedX, blockedY): whether motion was stopped on each axis.
        """
        return world.tryMove(self, dx, dy)

    def moveDirection(self, world, dirX, dirY, deltaTime):
        """
        Move along the (dirX, dirY) direction at the player's speed, blocked by
        solids. The direction is normalised so diagonals are not faster.

        Returns:
            (blockedX, blockedY): whether motion was stopped on each axis.
        """
        magnitude = (dirX * dirX + dirY * dirY) ** 0.5
        if magnitude == 0:
            return (False, False)
        step = self._speed * deltaTime
        return world.tryMove(self, dirX / magnitude * step, dirY / magnitude * step)

    ## Keyboard setup

    def initTopDownControls(self, controller):
        """
        Bind WASD and the arrow keys to top-down movement (a/left, w/up, s/down,
        d/right). Held keys drive the player's velocity, so the world moves and
        blocks it automatically; nothing else needs wiring in the game loop.
        """
        if self._velocity is None:
            self.setVelocity(RBVelocity(0, 0))
        bindings = {
            "up": ("w", "up"),
            "down": ("s", "down"),
            "left": ("a", "left"),
            "right": ("d", "right"),
        }
        for direction, keys in bindings.items():
            for key in keys:
                controller.registerKeyFunction(key, self._setMoveDir(direction, True), KEY_DOWN)
                controller.registerKeyFunction(key, self._setMoveDir(direction, False), KEY_UP)

    def _setMoveDir(self, direction, active):
        def handler():
            self._moveDirs[direction] = active
            self._updateVelocityFromDirs()
        return handler

    def _updateVelocityFromDirs(self):
        dx = (1 if self._moveDirs["right"] else 0) - (1 if self._moveDirs["left"] else 0)
        dy = (1 if self._moveDirs["down"] else 0) - (1 if self._moveDirs["up"] else 0)
        if dx == 0 and dy == 0:
            self._velocity.set_velocity_components(0.0, 0.0)
            return
        magnitude = (dx * dx + dy * dy) ** 0.5
        self._velocity.set_velocity_components(dx / magnitude * self._speed,
                                               dy / magnitude * self._speed)


