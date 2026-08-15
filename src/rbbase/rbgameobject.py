import sys
import os

sys.path.append(os.path.join(".."))

from rbgraphics.rbgraphicsobjects import RBGraphicCircle, RBGraphicRectangle
from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle

class RBGameObjectType(object):
    """
    Type definition for a game object that contains an id and name.
    Can be used to group objects or find its type during collision resolution.

    Game Objects use the default ObjectType unless specified.
    Default Object: ID=0 Name="Default"
    """
    def __init__(self, id, name):
        self._name = name
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

DEFAULT_GAME_OBJECT = RBGameObjectType(0, "Default")

class RBGameObject(object):
    def __init__(self, pos, graphic=None, collider=None, behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        self._pos = pos
        self._graphic = graphic
        self._collider = collider
        self._behaviours = behaviours if behaviours is not None else []
        self._active = True
        self._remove = False
        self._gameObjectType = gameObjectType

    @property
    def ObjectTypeId(self):
        """
        Return the game object type id
        """
        return self._gameObjectType.id

    @property
    def ObjectTypeName(self):
        """
        Return the game object type name
        """
        return self._gameObjectType.name

    def getObjectType(self):
        """
        Return the game object type
        """
        return self._gameObjectType

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

    def removeObject(self):
        """
        Mark the game object for removal.
        """
        self._remove = True

    def shouldRemove(self):
        """
        Check if the game object should be removed.
        """
        return self._remove

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
        if self._graphic and self._active:
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

    def runBehaviours(self, deltaTime):
        """
        Execute all behaviours associated with the game object.
        """
        for behaviour in self._behaviours:
            behaviour.execute(self, deltaTime)

    ## Collisions

    def setCollider(self, collider):
        """
        Set the collider for the game object.
        """
        self._collider = collider

    def getCollider(self):
        """
        Get the collider of the game object.
        """
        return self._collider
    
    ## Hooks for subclasses to override

    def onUpdate(self, deltaTime):
        """
        Called every frame to update the game object's state.
        """
        pass

    def onCollision(self, other):
        """
        Called when the game object collides with another object.
        """
        pass

class RBRectangle(RBGameObject):

    def __init__(self, pos, width, height, colour="black", fill="", solid=True, behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBGraphicRectangle(pos, width, height, colour, fill)
        bounding_box = RBBoundingBox(pos, width, height)
        super(RBRectangle, self).__init__(pos, graphic=graphic, collider=bounding_box, behaviours=behaviours, gameObjectType=gameObjectType)
        self._width = width
        self._height = height

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)

class RBCircle(RBGameObject):
    
    def __init__(self, centre, radius, colour="black", fill="", solid=True,behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBGraphicCircle(centre, radius, colour, fill)
        bounding_circle = RBBoundingCircle(centre, radius)
        super(RBCircle, self).__init__(centre, graphic=graphic, collider=bounding_circle, behaviours=behaviours, gameObjectType=gameObjectType)
        self._radius = radius

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)
