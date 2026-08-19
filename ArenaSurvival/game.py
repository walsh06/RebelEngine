import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbgameobjects import RBRectangle, RBCircle, RBTimer, RBUpdatingText, RBProgressBar, RBText
from rbbase.rbgameobject import RBGameObjectType, RBGameObject
from rbbase.rbgame import RBGame
from rbbase.rbbase import RB2DPosition
from rbbase.rbworld import RBWorld
from rbai.rbbehaviour import RBDespawnOutsideBounds
from rbphysics.rbvelocity import RBVelocity
from rbgraphics.rbgraphicsobjects import RBGraphicRectangle
from rbbase.rbplayer import RBPlayer

PLAYER_TYPE = RBGameObjectType(1, "Player")
COIN_TYPE = RBGameObjectType(2, "Coin")
BULLET_TYPE = RBGameObjectType(3, "Bullet")
PICKUP_TYPE = RBGameObjectType(4, "Pickup")
ENEMY_TYPE = RBGameObjectType(5, "Enemy")

HUD_LAYER = 0
PLAYER_LAYER = 1
GAME_LAYER = 2

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

RUNNING_STATE = "RUNNING"
PAUSED_STATE = "PAUSED"

class Enemy(RBCircle):

    def __init__(self, pos, velocity, health=1):
        removeBehaviour = RBDespawnOutsideBounds(-50, -50, WINDOW_WIDTH + 50, WINDOW_HEIGHT + 50)
        super(Enemy, self).__init__(pos, 10 * health, colour="black", fill="red", behaviours=[removeBehaviour], gameObjectType=ENEMY_TYPE)
        self.setVelocity(velocity)
        self.health = health

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.removeObject()

class Bullet(RBCircle):

    def __init__(self, player, pos, velocity, damage):
        super(Bullet, self).__init__(pos, 10, "black", "gold", gameObjectType=BULLET_TYPE)
        self.setVelocity(velocity)
        self.damage = damage
        self.player = player

    def onCollision(self, other):
        if other.ObjectTypeId == ENEMY_TYPE.id:
            other.hit(self.damage)
            self.removeObject()
            self.player.updateXP(1)


class Player(RBPlayer):

    def __init__(self, pos, mouse, bulletCallback, progressBar):
        graphic = RBGraphicRectangle(pos, 20, 20, "black", "green")
        super(Player, self).__init__(pos, graphic, speed=100, gameObjectType=PLAYER_TYPE)
        
        self.mouse = mouse
        self.aimPos = RB2DPosition(0,0)
        self.bulletCallback = bulletCallback
        self.progressBar = progressBar
        self.resetPlayer()

    def onUpdate(self, deltaTime):
        super(Player, self).onUpdate(deltaTime)
        mousePos = self.mouse.mousePos
        self.aimPos.setPos(mousePos.x, mousePos.y)

        self.time += deltaTime

        if self.xp >= self.levelUp:
            self.damage += 1
            self.lives += 1
            self.levelUp *= 2
            self.xp = 0
            self.progressBar.maxValue = self.levelUp

        if self.time >= self.cooldown:
            velocity = RBVelocity.fromPositions(self.bulletSpeed, self._pos, self.aimPos)
            self.bulletCallback(RB2DPosition(self.getPos().x, self.getPos().y), velocity, self.damage)
            self.time = 0

    def getLives(self):
        return self.lives

    def onCollision(self, other):
        if other.ObjectTypeId == ENEMY_TYPE.id:
            self.lives -= 1
            other.removeObject()

    def getXpString(self):
        return "{}/{}xp".format(self.xp, self.levelUp)

    def updateXP(self, xp):
        self.xp += xp
        self.progressBar.setProgress(self.xp)

    def resetPlayer(self):
        self.cooldown = 1
        self.time = 0
        self.damage = 1
        self.bulletSpeed = 200
        self.lives = 3
        self.xp = 0
        self.levelUp = 10


class Mouse(RBCircle):

    def __init__(self, controller):
        super(Mouse, self).__init__(RB2DPosition(0,0), 5, "blue", "blue")
        self.mouse = controller

    def onUpdate(self, deltaTime):
        self.setPos(self.mouse.mousePos)


class Game(RBGame):

    def __init__(self):
        super(Game, self).__init__()
        self.initGraphics(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.initController()

        self._controller.registerKeyFunction("q", self.quit)

        self.world = RBWorld(self._graphics)

        self.progressBar = RBProgressBar(10, RB2DPosition(350, 50), 100, 20, blocks=5, colour="green")
        self.world.addObject(self.progressBar, HUD_LAYER)

        self.player = Player(RB2DPosition(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), self._controller, self._spawnBullet, self.progressBar)
        self.player.initTopDownControls(self._controller)
        self.world.addObject(self.player, PLAYER_LAYER)

        self.mouse = Mouse(self._controller)
        self.world.addObject(self.mouse, PLAYER_LAYER)

        self.spawnCooldown = 1
        self.spawnTimer = 0

        self.gameTimer = RBTimer(RB2DPosition(250, 50))
        self.world.addObject(self.gameTimer, HUD_LAYER)
        self.world.addObject(RBUpdatingText(RB2DPosition(100, 50), "Lives: {}", self.player.getLives), HUD_LAYER)
        self.gameText = RBText("Press Space to Start Game.", RB2DPosition(250, 150))
        self.world.addObject(self.gameText, HUD_LAYER)

        self._controller.registerKeyFunction("space", self.startGame)
        self.addWorld(self.world)
        self.state = PAUSED_STATE

    def onUpdate(self, deltaTime):
        if self.state == RUNNING_STATE:
            super(Game, self).onUpdate(deltaTime)
            self.spawnTimer += deltaTime
            if self.spawnTimer >= self.spawnCooldown:
                self._spawnEnemy()
                self.spawnTimer = 0
        if self.player.lives <= 0 and self.state == RUNNING_STATE:
            self.state = PAUSED_STATE
            self.gameText.setText("Game Over!! Press Space to start again.")
            self.world.addObject(self.gameText, HUD_LAYER)

    def startGame(self):
        if self.state == PAUSED_STATE:
            self.state = RUNNING_STATE
            self.world.removeObject(self.gameText, HUD_LAYER)
            self.player.resetPlayer()
            self.gameTimer.reset()
            self.world.clear(GAME_LAYER)

    def _spawnBullet(self, pos, velocity, damage):
        self.world.addObject(Bullet(self.player, pos, velocity, damage), GAME_LAYER)

    def _spawnEnemy(self):
        spawnZone = random.randint(0, 3)
        if spawnZone < 2:
            x = random.randint(0, WINDOW_WIDTH)
            y = -20 if spawnZone == 0 else WINDOW_HEIGHT + 20
        else:
            x = -20 if spawnZone == 2 else WINDOW_WIDTH + 20
            y = random.randint(0, WINDOW_HEIGHT)
        pos = RB2DPosition(x, y)
        velocity = RBVelocity.fromPositions(100, pos, self.player.getPos())
        health = int(self.gameTimer.time / 30) + 1
        enemy = Enemy(pos, velocity, health)
        self.world.addObject(enemy, GAME_LAYER)

if __name__ == "__main__":
    game = Game()
    game.run()