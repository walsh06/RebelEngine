import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbgameobject import RBGameObject, DEFAULT_GAME_OBJECT
from rbgraphics.rbgraphicsobjects import (RBAnimatedImage, RBGraphicCircle,
                                          RBGraphicRectangle, RBImage,
                                          RBTextGraphic)
from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle


class RBRectangle(RBGameObject):

    def __init__(self, pos, width, height, colour="black", fill="", hasCollider=True, behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT, solid=False):
        graphic = RBGraphicRectangle(pos, width, height, colour, fill)
        bounding_box = RBBoundingBox(pos, width, height) if hasCollider else None
        super(RBRectangle, self).__init__(pos, graphic=graphic, collider=bounding_box, behaviours=behaviours, gameObjectType=gameObjectType, solid=solid)
        self._width = width
        self._height = height

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)


class RBCircle(RBGameObject):
    
    def __init__(self, centre, radius, colour="black", fill="", hasCollider=True,behaviours=None, gameObjectType=DEFAULT_GAME_OBJECT, solid=False):
        graphic = RBGraphicCircle(centre, radius, colour, fill)
        bounding_circle = RBBoundingCircle(centre, radius) if hasCollider else None
        super(RBCircle, self).__init__(centre, graphic=graphic, collider=bounding_circle, behaviours=behaviours, gameObjectType=gameObjectType, solid=solid)
        self._radius = radius

    def setColour(self, colour):
        self._graphic.setColour(colour)

    def setFill(self, fill):
        self._graphic.setFill(fill)

class RBSprite(RBGameObject):

    def __init__(self, img, pos, hasCollider=True, behaviours=None, velocity=None, gameObjectType=DEFAULT_GAME_OBJECT, solid=False):
        graphic = RBImage(img, pos, anchor="nw")
        collider = RBBoundingBox.fromGraphic(pos, graphic) if hasCollider else None
        super(RBSprite, self).__init__(pos, graphic, collider, behaviours, velocity, gameObjectType, solid)


class RBAnimatedSprite(RBGameObject):

    @classmethod
    def fromSpriteSheet(cls, spriteSheet, pos, frameWidth, frameHeight,
                        frameCount=None, columns=None, frameIndices=None,
                        frameRate=10, loop=True, autoplay=True, margin=0,
                        spacing=0, hasCollider=True, behaviours=None,
                        velocity=None, gameObjectType=DEFAULT_GAME_OBJECT,
                        solid=False):
        graphic = RBAnimatedImage.fromSpriteSheet(
            spriteSheet, pos, frameWidth, frameHeight, frameCount, columns,
            frameIndices, frameRate, loop, autoplay, margin, spacing,
            anchor="nw")
        collider = RBBoundingBox.fromGraphic(pos, graphic) if hasCollider else None
        sprite = cls.__new__(cls)
        RBGameObject.__init__(sprite, pos, graphic, collider, behaviours,
                              velocity, gameObjectType, solid)
        return sprite

    def __init__(self, frames, pos, frameRate=10, loop=True, autoplay=True,
                 hasCollider=True, behaviours=None, velocity=None,
                 gameObjectType=DEFAULT_GAME_OBJECT, solid=False):
        graphic = RBAnimatedImage(frames, pos, frameRate, loop, autoplay,
                                  anchor="nw")
        collider = RBBoundingBox.fromGraphic(pos, graphic) if hasCollider else None
        super(RBAnimatedSprite, self).__init__(
            pos, graphic, collider, behaviours, velocity, gameObjectType, solid)

    def onUpdate(self, deltaTime):
        self._graphic.update(deltaTime)

    def play(self):
        self._graphic.play()

    def pause(self):
        self._graphic.pause()

    def stop(self):
        self._graphic.stop()

    def isPlaying(self):
        return self._graphic.isPlaying()

    def getFrameIndex(self):
        return self._graphic.frameIndex


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
