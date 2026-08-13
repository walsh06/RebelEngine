import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbworld import RBWorld
from rbbase.rbgameobject import RBRectangle
from rbgraphics.rbgraphicsobjects import RBImage, RBText
from rbbase.rbgame import RBGame
from rbbase.rbplayer import RBPlayer
from rbbase.rbbase import RB2DPosition
from rbai.rbbehaviour import RBMoveUp

class TestPlayer(RBPlayer):

    def __init__(self, x, y, img):
        super(TestPlayer, self).__init__(x, y)
        self._img = RBImage(img, RB2DPosition(x, y))

    def moveLeft(self):
        self._pos.movePos(-1, 0)

    def moveRight(self):
        self._pos.movePos(1, 0)


class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(200, 200)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testPlayer = TestPlayer(0, 0, "ship.png")
        self.testController.registerKeyFunction("Left", self.testPlayer.moveLeft)
        self.testController.registerKeyFunction("Right", self.testPlayer.moveRight)
        self.testImage = RBImage("ship.png", RB2DPosition(100, 100))
        self.count = 0
        self.testText = RBText(self.count, RB2DPosition(100, 150))

        self.world = RBWorld(self._graphics)
        self.movingBlock = RBRectangle(RB2DPosition(50, 50), 20, 20, "blue", "blue")
        self.movingBlock.addBehaviour(RBMoveUp(20))
        self.world.addObject(self.movingBlock)
        self.world.addObject(self.testText)
        self.world.addObject(self.testImage)

    def onUpdate(self, deltaTime):
        self.count += 1
        self.testText.setText(self.count)
        self.world.update(deltaTime)

    def onDraw(self):
        self.world.draw()

test = TestGame()
test.run()
