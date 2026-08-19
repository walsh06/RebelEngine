import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbgameobject import RBGameObject, DEFAULT_GAME_OBJECT
from rbgraphics.rbgraphicsobjects import RBGraphicCircle, RBGraphicRectangle, RBImage, RBTextGraphic
from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle


class RBRectangle(RBGameObject):

    def __init__(self, pos, width, height, colour="black", fill="", hasCollider=True, behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBGraphicRectangle(pos, width, height, colour, fill)
        bounding_box = RBBoundingBox(pos, width, height) if hasCollider else None
        super(RBRectangle, self).__init__(pos, graphic=graphic, collider=bounding_box, behaviours=behaviours, gameObjectType=gameObjectType)
        self._width = width
        self._height = height

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)


class RBCircle(RBGameObject):
    
    def __init__(self, centre, radius, colour="black", fill="", hasCollider=True,behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBGraphicCircle(centre, radius, colour, fill)
        bounding_circle = RBBoundingCircle(centre, radius) if hasCollider else None
        super(RBCircle, self).__init__(centre, graphic=graphic, collider=bounding_circle, behaviours=behaviours, gameObjectType=gameObjectType)
        self._radius = radius

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)


class RBSolidBlock(RBRectangle):

    def __init__(self, pos, width, height, colour="black", fill="", behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT):
        super(RBSolidBlock, self).__init__(pos, width, height, colour, fill, True, behaviours, gameObjectType)

    def onCollision(self, other):
        """
        Prevent another object from penetrating this solid block by default.
        The collision has already been detected, so we resolve it by pushing
        the other object out along the smaller penetration axis and reflecting
        its velocity away from the block.
        """
        if other is None:
            return

        blockCollider = self.getCollider()
        otherCollider = other.getCollider()
        if blockCollider is None or otherCollider is None:
            return

        if not isinstance(blockCollider, RBBoundingBox):
            return

        blockLeft = self.getPos().getX()
        blockTop = self.getPos().getY()
        blockRight = blockLeft + self._width
        blockBottom = blockTop + self._height
        blockCenterX = blockLeft + (self._width / 2.0)
        blockCenterY = blockTop + (self._height / 2.0)

        if isinstance(otherCollider, RBBoundingBox):
            otherLeft = otherCollider.left
            otherRight = otherCollider.right
            otherTop = otherCollider.top
            otherBottom = otherCollider.bottom
            otherCenterX = (otherLeft + otherRight) / 2.0
            otherCenterY = (otherTop + otherBottom) / 2.0
        elif isinstance(otherCollider, RBBoundingCircle):
            centre = otherCollider._centre
            radius = otherCollider._radius
            otherLeft = centre.getX() - radius
            otherRight = centre.getX() + radius
            otherTop = centre.getY() - radius
            otherBottom = centre.getY() + radius
            otherCenterX = centre.getX()
            otherCenterY = centre.getY()
        else:
            return

        overlapLeft = max(blockLeft, otherLeft)
        overlapRight = min(blockRight, otherRight)
        overlapTop = max(blockTop, otherTop)
        overlapBottom = min(blockBottom, otherBottom)

        overlapX = max(0.0, overlapRight - overlapLeft)
        overlapY = max(0.0, overlapBottom - overlapTop)
        if overlapX <= 0 or overlapY <= 0:
            return

        pos = other.getPos()

        if overlapX < overlapY:
            if otherCenterX < blockCenterX:
                pos.movePos(blockLeft - otherRight, 0)
            else:
                pos.movePos(blockRight - otherLeft, 0)

            if other.hasVelocity():
                vx = other.getVelocity().getVelocityX()
                vy = other.getVelocity().getVelocityY()
                other.getVelocity().set_velocity_components(-vx, vy)
        else:
            if otherCenterY < blockCenterY:
                pos.movePos(0, blockTop - otherBottom)
            else:
                pos.movePos(0, blockBottom - otherTop)

            if other.hasVelocity():
                vx = other.getVelocity().getVelocityX()
                vy = other.getVelocity().getVelocityY()
                other.getVelocity().set_velocity_components(vx, -vy)

        other.setPos(pos)
        if otherCollider is not None:
            otherCollider.setPos(pos)


class RBSprite(RBGameObject):

    def __init__(self, img, pos, hasCollider=True, behaviours=None, velocity=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBImage(img, pos, anchor="nw")
        collider = RBBoundingBox(pos, graphic.width, graphic.height) if hasCollider else None
        super(RBSprite, self).__init__(pos, graphic, collider, behaviours, velocity, gameObjectType)


class RBText(RBGameObject):

    def __init__(self, text, pos, behaviours=None, velocity=None, gameObjectType=DEFAULT_GAME_OBJECT):
        graphic = RBTextGraphic(text, pos)
        super(RBText, self).__init__(pos, graphic, None, behaviours, velocity, gameObjectType)

    def setText(self, text):
        self._graphic.setText(text)


class RBTimer(RBText):
    """
    Timer object that will update its time on each update and draw
    it to the screen.
    """

    def __init__(self, pos, label="Time:"):
        self.label = label
        self.text = f"{self.label} 0"
        super(RBTimer, self).__init__(self.text, pos)
        self.timer = 0

    def onUpdate(self, deltaTime):
        self.timer += deltaTime
        self.setText(f"{self.label} {self.timer:.2f}")

    def reset(self):
        self.timer = 0

    @property
    def time(self):
        return self.timer


class RBUpdatingText(RBText):
    """
    Text object that will automatically update in game.
    argFunc is a function that will supply the variable for the text
    and will be updated over time.
    """
    
    def __init__(self, pos, text, argFunc):
        self.text = text
        self.argFunc = argFunc
        self.lastText = text.format(argFunc())
        super(RBUpdatingText, self).__init__(self.lastText, pos)

    def onUpdate(self, deltaTime):
        updatedText = self.text.format(self.argFunc())
        if updatedText != self.lastText:
            self.setText(updatedText)
            self.lastText = updatedText
