import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbworld import RBWorld
from rbbase.rbgameobject import RBGameObject
from rbbase.rbgameobjects import RBRectangle, RBSprite
from rbbase.rbplayer import RBPlayer
from rbgraphics.rbgraphicsobjects import RBImage, RBTextGraphic, RBGraphicRectangle
from rbbase.rbgame import RBGame
from rbbase.rbbase import RB2DPosition
from rbai.rbbehaviour import RBMoveUp

class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(200, 200)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.world = RBWorld(self._graphics)

        playerPos = RB2DPosition(0, 100)
        playerGraphic = RBGraphicRectangle(playerPos, 20, 20, "red", "red")
        self.testPlayer = RBPlayer(playerPos, playerGraphic, speed=80)
        self.testPlayer.initTopDownControls(self.testController)
        self.testImage = RBSprite("ship.png", RB2DPosition(100, 100))
        self.count = 0
        self.testText = RBTextGraphic(self.count, RB2DPosition(100, 150))

        self.movingBlock = RBRectangle(RB2DPosition(50, 50), 20, 20, "blue", "blue")
        self.movingBlock.addBehaviour(RBMoveUp(20))
        self.world.addObject(self.movingBlock)
        self.world.addObject(self.testText)
        self.world.addObject(self.testImage)
        self.world.addObject(self.testPlayer)

        # Solid wall: the player is stopped by it through the movement system.
        self.world.addObject(RBRectangle(RB2DPosition(50, 100), 5, 100, fill="black", solid=True))

    def onUpdate(self, deltaTime):
        self.count += 1
        self.testText.setText(self.count)
        self.world.update(deltaTime)

    def onDraw(self):
        self.world.draw()

test = TestGame()
test.run()
