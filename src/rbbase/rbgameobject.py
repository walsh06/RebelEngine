import sys
import os

sys.path.append(os.path.join(".."))

from rbphysics.rbvelocity import RBVelocity

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
    def __init__(self, pos, graphic=None, collider=None, behaviours=None, velocity=None, gameObjectType=DEFAULT_GAME_OBJECT):
        self._pos = pos
        self._graphic = graphic
        self._collider = collider
        self._behaviours = behaviours if behaviours is not None else []
        self._active = True
        self._remove = False
        self._gameObjectType = gameObjectType
        self._velocity = velocity

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

    ## Velocity methods

    def setVelocity(self, velocity):
        """
        Set the velocity for physics-based movement.
        
        Args:
            velocity: An RBVelocity object, or None to disable velocity-based movement
        
        Example:
            obj.setVelocity(RBVelocity(speed=100, angle=45))
        """
        if velocity is not None and not isinstance(velocity, RBVelocity):
            raise TypeError(f"Expected RBVelocity or None, got {type(velocity).__name__}")
        self._velocity = velocity

    def getVelocity(self):
        """
        Get the current velocity, or None if no velocity is set.
        
        Returns:
            RBVelocity object or None
        """
        return self._velocity

    def hasVelocity(self):
        """
        Check if the game object has an active velocity.
        
        Returns:
            bool: True if velocity is set, False otherwise
        """
        return self._velocity is not None

    def applyVelocity(self, deltaTime):
        """
        Apply velocity-based movement to update the object's position.
        Called automatically by the world update loop.
        
        This method:
        - Checks if the object has velocity
        - If yes: updates position based on velocity and deltaTime
        - If no: does nothing (object remains static)
        
        Args:
            deltaTime: Time elapsed since last frame (in seconds)
        """
        if self._velocity is not None:
            # Calculate displacement: displacement = velocity * time
            dx = self._velocity.getVelocityX() * deltaTime
            dy = self._velocity.getVelocityY() * deltaTime
            
            # Update position
            self._pos.movePos(dx, dy)
            
            # Sync graphics and collider to new position
            if self._graphic is not None:
                self._graphic.setPos(self._pos)
            if self._collider is not None:
                self._collider.setPos(self._pos)

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
