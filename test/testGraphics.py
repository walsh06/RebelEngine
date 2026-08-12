import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbgame import RBGame
from rbgraphics.rbgraphicsobjects import RBText, RBGraphicCircle, RBGraphicRectangle
from rbbase.rbbase import RB2DPosition
from rbgraphics.rbscene import RBScene
from rbbase.rbgameobject import RBRectangle

class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(300, 300)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testText = RBText("TEST", RB2DPosition(100, 150))
        self.countText = RBText("COUNT", RB2DPosition(100, 200))
        self.testCircle = RBGraphicCircle(RB2DPosition(20, 20), 10, "red", "red")
        self.testRec = RBRectangle(RB2DPosition(50, 50), 10, 20, "black", "")
        self.scene = RBScene(self._graphics)
        self.scene.addObject(self.testCircle)
        self.scene.addObject(self.testRec)
        self.scene.addObject(self.testText)
        self.scene.addObject(self.countText)
        self.x = 20
        self.y = 20
        self.count = 0

    def onUpdate(self):
        self.x += 1
        self.y += 1

        self.count += 1
        self.countText.setText(f"COUNT: {self.count}")
        
        if self.count > 20:
            self.testRec.setColour("blue")
            self.testRec.setFill("blue")

        self.testRec.setPos(RB2DPosition(self.x, self.y))

    def onDraw(self):
        self.scene.draw()

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.run()
