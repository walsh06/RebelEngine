import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbworld import RBWorld
from rbbase.rbgameobject import RBGameObject
from rbbase.rbgameobjects import RBRectangle, RBSolidBlock, RBSprite
from rbgraphics.rbgraphicsobjects import RBImage, RBTextGraphic
from rbbase.rbgame import RBGame
from rbbase.rbbase import RB2DPosition
from rbai.rbbehaviour import RBMoveUp
from rbcontroller.rbcontroller import KEY_HELD

class TestPlayer(RBRectangle):

    def __init__(self, pos):
        super(TestPlayer, self).__init__(pos, 20, 20, "red", "red")

    def moveLeft(self):
        self.movePos(-1, 0)

    def moveRight(self):
        self.movePos(1, 0)

    def moveUp(self):
        self.movePos(0, -1)

    def moveDown(self):
        self.movePos(0, 1)

class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(200, 200)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testPlayer = TestPlayer(RB2DPosition(0, 100))
        self.testController.registerKeyFunction("Left", self.testPlayer.moveLeft, KEY_HELD)
        self.testController.registerKeyFunction("Right", self.testPlayer.moveRight, KEY_HELD)
        self.testController.registerKeyFunction("Up", self.testPlayer.moveUp, KEY_HELD)
        self.testController.registerKeyFunction("Down", self.testPlayer.moveDown, KEY_HELD)
        self.testImage = RBSprite("ship.png", RB2DPosition(100, 100))
        self.count = 0
        self.testText = RBTextGraphic(self.count, RB2DPosition(100, 150))

        self.world = RBWorld(self._graphics)
        self.movingBlock = RBRectangle(RB2DPosition(50, 50), 20, 20, "blue", "blue")
        self.movingBlock.addBehaviour(RBMoveUp(20))
        self.world.addObject(self.movingBlock)
        self.world.addObject(self.testText)
        self.world.addObject(self.testImage)
        self.world.addObject(self.testPlayer)

        self.world.addObject(RBSolidBlock(RB2DPosition(50, 100), 5, 100, fill="black"))

    def onUpdate(self, deltaTime):
        self.count += 1
        self.testText.setText(self.count)
        self.world.update(deltaTime)

    def onDraw(self):
        self.world.draw()

test = TestGame()
test.run()
