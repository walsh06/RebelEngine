from itertools import chain

from rbbase.rbgameobject import RBGameObject
from rbgraphics.rbscene import RBScene

class RBWorld(RBScene):
    def __init__(self, canvas):
        super(RBWorld, self).__init__(canvas)
        # List of simulated game objects in the world
        self._worldObjects = []

    def update(self, deltaTime):
        """
        Update the world and all its game objects.
        """
        objects = self._worldObjects
        for obj in objects:
            obj.runBehaviours(deltaTime)
        for obj in objects:
            obj.onUpdate(deltaTime)

        for obj in objects:
            if obj.shouldRemove():
                self.removeObject(obj)

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
            
            