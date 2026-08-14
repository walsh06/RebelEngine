import sys
from math import atan2, degrees, hypot
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbgame import RBGame
from rbbase.rbbase import RB2DPosition
from rbbase.rbgameobject import RBRectangle, RBCircle, RBGameObjectType
from rbbase.rbworld import RBWorld
from rbcontroller.rbcontroller import KEY_HELD
from rbphysics.rbvelocity import RBVelocity
from rbgraphics.rbgraphicsobjects import RBText

BLOCK_TYPE = RBGameObjectType(1, "Block")
BALL_TYPE = RBGameObjectType(2, "Ball")
PADDLE_TYPE = RBGameObjectType(3, "Paddle")
WALL_TYPE = RBGameObjectType(4, "Wall")

class Block(RBRectangle):

    def __init__(self, pos, w, h, colour, objectType=BLOCK_TYPE):
        super(Block, self).__init__(pos, w, h, colour, colour, gameObjectType=objectType)

class Ball(RBCircle):

    def __init__(self, pos):
        super(Ball, self).__init__(pos, 5, solid=True, gameObjectType=BALL_TYPE)
        self.velocity = RBVelocity(200, 270)
        self._lastPos = RB2DPosition(pos.getX(), pos.getY())

    def onUpdate(self, deltaTime):
        self._lastPos = RB2DPosition(self.getPos().getX(), self.getPos().getY())
        self.movePos(self.velocity.getVelocityX() * deltaTime, self.velocity.getVelocityY() *deltaTime)

    def onCollision(self, other):
        if other.ObjectTypeId == BLOCK_TYPE.id:
            self._bounceOffBlock(other)
            other.removeObject()
        elif other.ObjectTypeId == WALL_TYPE.id:
            self._bounceOffBlock(other)
        elif other.ObjectTypeId == PADDLE_TYPE.id:   
            self._bounceOffPaddle(other)

    def _bounceOffBlock(self, block):
        ballX = self.getPos().getX()
        ballY = self.getPos().getY()
        prevX = self._lastPos.getX()
        prevY = self._lastPos.getY()
        radius = self._radius

        rect = block.getCollider()
        left = rect.left
        right = rect.right
        top = rect.top
        bottom = rect.bottom

        prevLeft = prevX - radius
        prevRight = prevX + radius
        prevTop = prevY - radius
        prevBottom = prevY + radius

        currLeft = ballX - radius
        currRight = ballX + radius
        currTop = ballY - radius
        currBottom = ballY + radius

        hitLeft = prevRight <= left and currRight >= left
        hitRight = prevLeft >= right and currLeft <= right
        hitTop = prevBottom <= top and currBottom >= top
        hitBottom = prevTop >= bottom and currTop <= bottom

        vx = self.velocity.getVelocityX()
        vy = self.velocity.getVelocityY()

        if hitLeft or hitRight:
            vx = -abs(vx) if hitLeft else abs(vx)
            self.velocity._velocity.setVector(vx, vy)
        elif hitTop or hitBottom:
            vy = -abs(vy) if hitTop else abs(vy)
            self.velocity._velocity.setVector(vx, vy)
        else:
            self.velocity._velocity.setVector(-vx, -vy)

    def _bounceOffPaddle(self, paddle):
        speed = hypot(self.velocity.getVelocityX(), self.velocity.getVelocityY())
        if speed == 0:
            speed = 100

        paddleLeft = paddle.getPos().getX()
        paddleWidth = paddle._width
        paddleCenterX = paddleLeft + paddleWidth / 2
        ballCenterX = self.getPos().getX()

        # Map the hit position across the paddle width to a value in [-1, 1].
        # Center hit => straight up, left edge => more left/up, right edge => more right/up.
        hitRatio = ((ballCenterX - paddleCenterX) / (paddleWidth / 2))
        hitRatio = max(-1.0, min(1.0, hitRatio))

        # Angle range: about 60 degrees of spread from center to edges.
        angle = 270 + hitRatio * 60

        # Make sure the ball leaves headed upward, regardless of the side it hit.
        self.velocity = RBVelocity(speed, angle)


class Paddle(RBRectangle):

    def __init__(self, pos):
        super(Paddle, self).__init__(pos, 100, 10, "black", "black", gameObjectType=PADDLE_TYPE)

    def moveLeft(self):
        self.movePos(-3, 0)

    def moveRight(self):
        self.movePos(3, 0)

    def onUpdate(self, deltaTime):
        x = self.getPos().getX()
        y = self.getPos().getY()
        if x < 5:
            self.setPos(RB2DPosition(0, y))
        elif x > 500:
            self.setPos(RB2DPosition(500, y))


class BlockBreaker(RBGame):

    def __init__(self):
        super(BlockBreaker, self).__init__()

        self.gameState = "Paused"
        self.initGraphics(600, 300)
        # controls
        self.initController()
        self._controller.registerKeyFunction("q", self.quit)
        self._controller.registerKeyFunction("space", self.restartGame)

        # world setup
        self._world = RBWorld(self._graphics)

        self._instructions = RBText("Press Space to start, Q to quit", RB2DPosition(275, 150))
        self.paddle = Paddle(RB2DPosition(220, 250))
        self._controller.registerKeyFunction("left", self.paddle.moveLeft, KEY_HELD)
        self._controller.registerKeyFunction("right", self.paddle.moveRight, KEY_HELD)

        self.lives = 3
        self.livesText = RBText(f"Lives: {self.lives}", RB2DPosition(300, 20))
        self.ball = None

        self._resetWorld()

    def _resetWorld(self):
        self._world.clear()

        self._world.addObject(Block(RB2DPosition(0, 0), 600, 5, "grey", WALL_TYPE), WALL_TYPE.id)
        self._world.addObject(Block(RB2DPosition(0, 0), 5, 300, "grey", WALL_TYPE), WALL_TYPE.id)
        self._world.addObject(Block(RB2DPosition(0, 300), 600, 5, "grey", WALL_TYPE), WALL_TYPE.id)
        self._world.addObject(Block(RB2DPosition(600, 0), 5, 300, "grey", WALL_TYPE), WALL_TYPE.id)
        self.paddle.setPos(RB2DPosition(220, 250))
        self._world.addObject(self.paddle, PADDLE_TYPE.id)

        self.ball = Ball(RB2DPosition(275, 230))
        self._world.addObject(self.ball)

        colours = ["red", "blue", "green"]
        colourCounter = 0
        for i in range(30, 100, 25):
            for j in range(20, 550, 55):
                self._world.addObject(Block(RB2DPosition(j, i), 50, 20, colours[colourCounter]))
            colourCounter += 1

        self.livesText.setText(f"Lives: {self.lives}")
        self._world.addObject(self.livesText)

        if self.gameState == "Paused":
            self._world.addObject(self._instructions)

    def restartGame(self):
        self.gameState = "Running"
        self._world.removeObject(self._instructions)
        self._resetWorld()
        self.lives = 3
        self.livesText.setText(f"Lives: {self.lives}")

    def onUpdate(self, deltaTime):
        if self.gameState == "Running":
            self._world.update(deltaTime)

        if self.ball is not None:
            if self.ball.getPos().getY() > 280:
                self.lives -= 1
                self.livesText.setText(f"Lives: {self.lives}")
                if self.lives <= 0:
                    self.gameState = "Paused"
                    self.livesText.setText(f"Game Over")
                    self._world.addObject(self._instructions)

                self.ball.setPos(RB2DPosition(275, 230))
                self.ball.velocity = RBVelocity(200, 270)

    def onDraw(self):
        self._world.draw()

game = BlockBreaker()
game.run()