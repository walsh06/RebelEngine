import sys
import os

sys.path.append(os.path.join(".."))

from rbgraphics.rbgraphicsobjects import RBGraphicRectangle

class RBGameObject(object):
    def __init__(self, pos, graphic=None, collider=None, behaviours=[]):
        self._pos = pos
        self._graphic = graphic
        self._collider = collider
        self._behaviours = behaviours
        self._active = True

    def isActive(self):
        """
        Check if the game object is active.
        """
        return self._active

    def setActive(self, active):
        """
        Set the active state of the game object.
        """
        self._active = active

    ## Position

    def setPos(self, pos):
        """
        Set the position of the game object.
        """
        self._pos = pos
        if self._graphic is not None:
            self._graphic.setPos(pos)
        if self._collider is not None:
            self._collider.setPos(pos)

    def getPos(self):
        """
        Get the position of the game object.
        """
        return self._pos

    def movePos(self, dx, dy):
        """
        Move the position of the game object.
        """
        self._pos.movePos(dx, dy)

    ## Drawing methods

    def draw(self, canvas):
        """
        Draw the game object on the canvas.
        """
        if self._graphic:
            self._graphic.draw(canvas)

    def undraw(self, canvas):
        """
        Undraw the game object from the canvas.
        """
        if self._graphic:
            self._graphic.undraw(canvas)

    @property
    def _id(self):
        return self._graphic._id if self._graphic else None

    ## Behaviour methods

    def addBehaviour(self, behaviour):
        """
        Add a behaviour to the game object.
        """
        self._behaviours.append(behaviour)

    def removeBehaviour(self, behaviour):
        """
        Remove a behaviour from the game object.
        """
        if behaviour in self._behaviours:
            self._behaviours.remove(behaviour)

    def runBehaviours(self):
        """
        Execute all behaviours associated with the game object.
        """
        for behaviour in self._behaviours:
            behaviour.execute(self)

    ## Hooks for subclasses to override

    def onUpdate(self):
        """
        Called every frame to update the game object's state.
        """
        pass

    def onCollision(self):
        """
        Called when the game object collides with another object.
        """
        pass

class RBRectangle(RBGameObject):

    def __init__(self, pos, width, height, colour="black", fill=""):
        graphic = RBGraphicRectangle(pos, width, height, colour, fill)
        super(RBRectangle, self).__init__(pos, graphic)
        self._width = width
        self._height = height

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)