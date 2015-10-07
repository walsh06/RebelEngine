import sys
import os
import pdb
from random import randint

sys.path.append(os.path.join("..", "src"))

from rbbase.rbgame import RBGame
from rbbase.rbplayer import RBPlayer
from rbbase.rbbase import RB2DPosition
from rbgraphics.rbgraphicsobjects import RBImage, RBText, RBCircle, RBRectangle
from rbai.rbai import RBAI 
from rbai.rbbehaviour import RBMoveDown
from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle
from rbphysics.rbcollision import RBCollision
from rbphysics.rbvelocity import RBVelocity
from rbsound.rbsound import RBSound
SCR_HEIGHT = 400
SCR_WIDTH = 400

class Block(object):
    
    def __init__(self, x, y, colour):
        self._rec = RBRectangle(RB2DPosition(x, y), 20, 50, fill=colour)
        self._pos = RB2DPosition(x, y)
        self._box = RBBoundingBox(self._pos, 20, 50)

    def draw(self, graphics):
        self._rec.draw(graphics, self._pos.getX(), self._pos.getY())

class BlockManager(object):

    def __init__(self):
        self._blocks = []
        self._colours = ["red", "blue", "green", "yellow"]
        self._collision = RBCollision()
        self._removedBlocks = []
        for x in range(0, 8):
            for y in range(0, 4):
                self._blocks.append(Block(x * 50, y * 20, self._colours[randint(0, 3)]))
    
    def update(self, ball):
        for block in self._blocks:
            if self._collision.collideCircleToRectangle(ball._circle, block._box):
                print ball._circle._centre.getX(), ball._circle._centre.getY()
                print block._box._pos.getX(), block._box._pos.getY()
                self._blocks.remove(block)
                self._removedBlocks.append(block)
                ball._v.changeAngle(90)

    def draw(self, graphics):
        for block in self._blocks:
            block.draw(graphics)

        for block in self._removedBlocks:
            block._rec.undraw(graphics)

class Ball(object):
    
    def __init__(self):
        self._ball = RBCircle(RB2DPosition(200, 350), 5, "red", "red")
        self._pos = RB2DPosition(200, 350)
        self._v = RBVelocity(3, -90)
        self._circle = RBBoundingCircle(self._pos, 5)

    def update(self):
        if self._pos.getX() < 0 or self._pos.getX() > SCR_WIDTH:
            self._v.changeAngle(90)
        elif self._pos.getY() < 0 or self._pos.getY() > SCR_HEIGHT:
            self._v.changeAngle(90)
        self._pos.movePos(self._v.getVelocityX(), self._v.getVelocityY())
        self._circle.setCentre(self._pos)

    def draw(self, graphics):
        self._ball.draw(graphics, self._pos.getX(), self._pos.getY())

class Player(RBPlayer):

    def __init__(self):
        super(Player, self).__init__(200, 350)
        self._speed = 2
        self._halfWidth = 50
        self._leftPaddle = RBRectangle(RB2DPosition(self._pos.getX() - self._halfWidth, self._pos.getY()),
                                       10, self._halfWidth, "white", "white")
        self._rightPaddle = RBRectangle(RB2DPosition(self._pos.getX(), self._pos.getY()),
                                       10, self._halfWidth, "white", "white")

    def moveLeft(self):
        self._pos.movePos(-self._speed, 0)

    def moveRight(self):
        self._pos.movePos(self._speed, 0)

    def draw(self, graphics):
        self._leftPaddle.draw(graphics, self._pos.getX() - self._halfWidth, self._pos.getY())
        self._rightPaddle.draw(graphics, self._pos.getX(), self._pos.getY())

class BlockBreaker(RBGame):
    def __init__(self):
        super(BlockBreaker, self).__init__()

        self.initGraphics(SCR_WIDTH, SCR_HEIGHT)
        self.initController()
        self._player = Player() 
        self._ball = Ball()
        self._blockManager = BlockManager()
        self._controller.registerKeyFunction("left", self._player.moveLeft)
        self._controller.registerKeyFunction("right", self._player.moveRight)
        self._controller.registerKeyFunction("q", self.quit)
        self._running = True
    
    def update(self):
        gameOver = False
        while self._running and not gameOver:
            super(BlockBreaker, self).update()
            self._player.draw(self._graphics)

            self._ball.update()
            self._ball.draw(self._graphics)

            self._blockManager.update(self._ball)
            self._blockManager.draw(self._graphics)

    def quit(self):
        self._running = False


game = BlockBreaker()
game.update()