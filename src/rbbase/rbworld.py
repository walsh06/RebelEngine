from itertools import chain
import rbphysics.rbcollision as rbcollision
from rbbase.rbgameobject import RBGameObject
from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle
from rbgraphics.rbscene import RBScene
from rbgraphics.rbgraphicsobjects import RBGraphicRectangle, RBGraphicCircle

class RBWorld(RBScene):
    def __init__(self, canvas):
        super(RBWorld, self).__init__(canvas)
        # List of simulated game objects in the world
        self._worldObjects = []
        # Debug overlay: red collider outlines, keyed by game object
        self._debugDraw = False
        self._debugGraphics = {}

    def setDebugDraw(self, enabled):
        """
        Toggle drawing of collider outlines in red for debugging.
        """
        self._debugDraw = bool(enabled)

    def isDebugDraw(self):
        """
        Return whether collider debug drawing is enabled.
        """
        return self._debugDraw

    def clear(self, layer=None):
        """
        Clear objects from the scene and from the simulation list to prevent
        stale game objects from continuing to update after a reset.
        """
        if layer is None:
            objects = list(self._worldObjects)
            for obj in objects:
                if obj in self._worldObjects:
                    self._worldObjects.remove(obj)
            super(RBWorld, self).clear(layer)
            return

        if layer in self.layers:
            for obj in list(self.layers[layer]):
                if isinstance(obj, RBGameObject) and obj in self._worldObjects:
                    self._worldObjects.remove(obj)
        super(RBWorld, self).clear(layer)

    def update(self, deltaTime):
        """
        Update the world and all its game objects.
        
        Update sequence:
        1. Run all active behaviours
        2. Call onUpdate hooks for custom logic
        3. Apply velocity-based movement
        4. Detect and dispatch collisions
        5. Remove marked objects
        """
        objects = self._worldObjects
        
        # Step 1: Run behaviours
        for obj in objects:
            obj.runBehaviours(deltaTime)
        
        # Step 2: Run custom update hooks
        for obj in objects:
            obj.onUpdate(deltaTime)

        # Step 3: Apply velocity-based movement, stopping at solid objects.
        # This must happen before collision detection so collisions see correct positions
        solids = [o for o in objects if o.isSolid() and o.getCollider() is not None]
        for obj in objects:
            if obj.hasVelocity() and not obj.isSolid():
                self._moveWithVelocity(obj, solids, deltaTime)
            else:
                obj.applyVelocity(deltaTime)

        # Step 4: Dispatch collisions (before removing objects)
        self._dispatchCollisions([obj for obj in objects
                                  if obj.isActive() and obj.getCollider()])
        
        # Step 5: Remove objects marked for deletion
        for obj in list(objects):
            if obj.shouldRemove():
                self.removeObject(obj)

    def _dispatchCollisions(self, objects):
        """
        Check for collisions between all pairs of objects and dispatch collision events.
        """
        # Every pair, which is fine at these sizes but wants a broadphase
        # before it is used for anything large.
        for index, first in enumerate(objects):
            for second in objects[index + 1:]:
                if rbcollision.overlaps(first, second):
                    first.onCollision(second)
                    second.onCollision(first)

    def tryMove(self, obj, dx, dy, solids=None):
        """
        Move obj by (dx, dy) but stop it against solid objects instead of
        letting it penetrate them. The axes are resolved separately so the
        object slides along a surface (e.g. keeps walking while pressed against
        a wall or resting on the ground).

        Args:
            obj: the game object to move.
            dx, dy: the desired displacement this step.
            solids: optional pre-filtered list of solid objects to test
                against; computed from the world when omitted.

        Returns:
            (blockedX, blockedY): whether motion was stopped on each axis.
        """
        if solids is None:
            solids = [o for o in self._worldObjects
                      if o.isSolid() and o is not obj and o.getCollider() is not None]
        blockedX = self._sweepAxis(obj, solids, dx, 0.0)
        blockedY = self._sweepAxis(obj, solids, 0.0, dy)
        return blockedX, blockedY

    def _sweepAxis(self, obj, solids, dx, dy):
        """
        Tentatively move obj along a single axis; if that lands it inside a
        solid, undo just this axis so it rests flush against the surface.
        Returns True when the move was blocked.
        """
        if dx == 0.0 and dy == 0.0:
            return False
        pos = obj.getPos()
        pos.movePos(dx, dy)
        obj.setPos(pos)
        for solid in solids:
            if rbcollision.overlaps(obj, solid):
                pos.movePos(-dx, -dy)
                obj.setPos(pos)
                return True
        return False

    def _moveWithVelocity(self, obj, solids, deltaTime):
        """
        Integrate an object's velocity for this step against solids, zeroing the
        blocked axis so it stops dead rather than bouncing.
        """
        velocity = obj.getVelocity()
        dx = velocity.getVelocityX() * deltaTime
        dy = velocity.getVelocityY() * deltaTime
        blockedX, blockedY = self.tryMove(obj, dx, dy, solids)
        if blockedX:
            velocity.set_velocity_components(0.0, velocity.getVelocityY())
        if blockedY:
            velocity.set_velocity_components(velocity.getVelocityX(), 0.0)

    def addObject(self, obj, layer=0):
        """
        Add a game object to the world in the specified layer.
        """
        super(RBWorld, self).addObject(obj, layer)
        if isinstance(obj, RBGameObject):
            self._worldObjects.append(obj)

    def removeObject(self, obj, layer=None):
        """
        Remove a game object from the world.
        """
        super(RBWorld, self).removeObject(obj, layer)
        if isinstance(obj, RBGameObject) and obj in self._worldObjects:
            self._worldObjects.remove(obj)

    def draw(self):
        """
        Draw the scene, then overlay red collider outlines when debug drawing
        is enabled.
        """
        super(RBWorld, self).draw()
        self._drawDebug()

    def _drawDebug(self):
        """
        Draw a red outline over each collider, reusing cached debug graphics so
        tk item ids follow objects instead of being recreated every frame.
        """
        if not self._debugDraw:
            if self._debugGraphics:
                self._clearDebug()
            return

        live = set()
        for obj in self._worldObjects:
            collider = obj.getCollider()
            if collider is None:
                continue
            live.add(obj)
            graphic = self._debugGraphics.get(obj)
            if graphic is None:
                graphic = self._makeDebugGraphic(collider)
                if graphic is None:
                    continue
                self._debugGraphics[obj] = graphic
            self._syncDebugGraphic(graphic, collider)
            graphic.draw(self.canvas)
            self.canvas.tag_raise(graphic._id)

        # Drop overlays for objects that no longer exist or lost their collider.
        for obj in [o for o in self._debugGraphics if o not in live]:
            self._debugGraphics.pop(obj).undraw(self.canvas)

    def _clearDebug(self):
        """
        Undraw and forget all debug overlays.
        """
        for graphic in self._debugGraphics.values():
            graphic.undraw(self.canvas)
        self._debugGraphics.clear()

    def _makeDebugGraphic(self, collider):
        """
        Build a red outline graphic matching the collider's shape.
        """
        if isinstance(collider, RBBoundingBox):
            return RBGraphicRectangle(collider.getPos(), collider.width,
                                      collider.height, colour="red")
        if isinstance(collider, RBBoundingCircle):
            return RBGraphicCircle(collider.getCentre(), collider.getRadius(),
                                   colour="red")
        return None

    def _syncDebugGraphic(self, graphic, collider):
        """
        Point the debug graphic at the collider's current position.
        """
        if isinstance(collider, RBBoundingBox):
            graphic.setPos(collider.getPos())
        elif isinstance(collider, RBBoundingCircle):
            graphic.setPos(collider.getCentre())
            
            