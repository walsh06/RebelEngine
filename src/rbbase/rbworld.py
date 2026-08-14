from itertools import chain
import rbphysics.rbcollision as rbcollision
from rbbase.rbgameobject import RBGameObject
from rbgraphics.rbscene import RBScene

class RBWorld(RBScene):
    def __init__(self, canvas):
        super(RBWorld, self).__init__(canvas)
        # List of simulated game objects in the world
        self._worldObjects = []

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
        """
        objects = self._worldObjects
        for obj in objects:
            obj.runBehaviours(deltaTime)
        for obj in objects:
            obj.onUpdate(deltaTime)

        self._dispatchCollisions([obj for obj in objects
                                  if obj.isActive() and obj.getCollider()])
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
            
            