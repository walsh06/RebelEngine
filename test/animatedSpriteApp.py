import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbbase import RB2DPosition
from rbbase.rbgame import RBGame
from rbbase.rbgameobjects import RBAnimatedSprite, RBText
from rbbase.rbworld import RBWorld
from rbcontroller.rbcontroller import KEY_HELD


class AnimatedSpriteGame(RBGame):

    def __init__(self):
        super(AnimatedSpriteGame, self).__init__()
        self.initGraphics(400, 240)
        self.initController()
        self.world = RBWorld(self._graphics)

        sheet = Path(__file__).with_name("animated_character_sheet.png")
        self.character = RBAnimatedSprite.fromSpriteSheet(
            str(sheet), RB2DPosition(184, 104),
            frameWidth=32, frameHeight=32,
            frameCount=4, columns=4, frameRate=8,
            hasCollider=False)

        self.world.addObject(self.character)
        self.world.addObject(RBText(
            "Move: WASD / arrows    Quit: Q", RB2DPosition(200, 30)))

        for key in ("w", "Up"):
            self._controller.registerKeyFunction(key, self.moveUp, KEY_HELD)
        for key in ("s", "Down"):
            self._controller.registerKeyFunction(key, self.moveDown, KEY_HELD)
        for key in ("a", "Left"):
            self._controller.registerKeyFunction(key, self.moveLeft, KEY_HELD)
        for key in ("d", "Right"):
            self._controller.registerKeyFunction(key, self.moveRight, KEY_HELD)
        self._controller.registerKeyFunction("q", self.quit)

    def moveUp(self):
        self.character.movePos(0, -4)

    def moveDown(self):
        self.character.movePos(0, 4)

    def moveLeft(self):
        self.character.movePos(-4, 0)

    def moveRight(self):
        self.character.movePos(4, 0)

    def onUpdate(self, deltaTime):
        self.world.update(deltaTime)

    def onDraw(self):
        self.world.draw()


if __name__ == "__main__":
    AnimatedSpriteGame().run()