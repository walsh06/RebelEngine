import sys
import os
import pdb
from random import randint

sys.path.append(os.path.join("..", "src"))

from rbbase.rbgame import RBGame
from rbbase.rbplayer import RBPlayer
from rbbase.rbbase import RB2DPosition
from rbgraphics.graphicsobjects import RBImage, RBText
from rbai.rbai import RBAI 
from rbai.rbbehaviour import RBMoveDown
from rbphysics.collisionobjects import RBBoundingBox
from rbsound.rbsound import RBSound
SCR_HEIGHT = 400
SCR_WIDTH = 400

class Enemy(RBAI):

	def __init__(self, x, y):
		super(Enemy, self).__init__(x, y)
		self.setBehaviour(RBMoveDown())
		self._img = RBImage("alien.png", x, y)
		self._box = RBBoundingBox(self._pos.getX(), self._pos.getY(), 50, 50) 

	def update(self):
		super(Enemy, self).update()
		self._box.setPosition(self._pos.getX(), self._pos.getY())

	def draw(self, canvas):
		self._img.draw(canvas, self._pos.getX(), self._pos.getY())


class EnemyManager(object):

	def __init__(self):
		self._enemies = []
		self._timer = 0

	def update(self):
		self._timer += 1
		if self._timer % 50 == 0:
			self._enemies.append(Enemy(randint(10, SCR_WIDTH - 20), 0))

		for enemy in self._enemies:
			enemy.update()
			if enemy._pos.getY() > SCR_HEIGHT:
				return True
		return False

	def draw(self, canvas):
		for enemy in self._enemies:
			enemy.draw(canvas)

class Bullet(object):

	def __init__(self, posX, posY):
		self._posX = posX
		self._posY = posY
		self._speed = 10
		self._img = RBImage("laser.png", self._posX, self._posY)
		self._box = RBBoundingBox(self._posX, self._posY, 10, 20)

	def update(self):
		self._posY -= self._speed
		self._box.setPosition(self._posX, self._posY)

	def draw(self, canvas):
		self._img.draw(canvas, self._posX, self._posY)


class Player(RBPlayer):

	def __init__(self):
		super(Player, self).__init__(200, 350)
		self._speed = 3
		self._bullets = []
		self._img = RBImage("ship.png", self._pos.getX(), self._pos.getY())
		self._shootSound = RBSound("Laser_Shoot.wav")

	def moveLeft(self):
		self._pos.movePos(-self._speed, 0)

	def moveRight(self):
		self._pos.movePos(self._speed, 0)

	def shoot(self):
		self._bullets.append(Bullet(self._pos.getX() + 5, self._pos.getY()))
		self._shootSound.play()

	def update(self, canvas):
		for bullet in self._bullets:
			bullet.update()
			if bullet._posY < 0:
				bullet._img.undraw(canvas)
				self._bullets.remove(bullet)

	def draw(self, canvas):
		for bullet in self._bullets:
			bullet.draw(canvas)
		super(Player, self).draw(canvas)

class AlienInvaders(RBGame):

	def __init__(self):
		super(AlienInvaders, self).__init__()

		self.initGraphics(SCR_WIDTH, SCR_HEIGHT)
		self.initController()
		self._player = Player() 
		self._controller.registerKeyFunction("left", self._player.moveLeft)
		self._controller.registerKeyFunction("right", self._player.moveRight)
		self._controller.registerKeyFunction("up", self._player.shoot)
		self._controller.registerKeyFunction("space", self.quit)
		self._running = True
		self._enemyManager = EnemyManager()
		self._score = 0
		self._scoreText = RBText(str(self._score), 200, 50)
	
	def update(self):
		gameOver = False
		while self._running and not gameOver:
			super(AlienInvaders, self).update()
			self._player.update(self._graphics)
			gameOver = self._enemyManager.update()

			self._enemyManager.draw(self._graphics)
			self._player.draw(self._graphics)

			for enemy in self._enemyManager._enemies:
				for bullet in self._player._bullets:
					if enemy._box.collideWithBox(bullet._box):
						enemy._img.undraw(self._graphics)
						bullet._img.undraw(self._graphics)
						self._player._bullets.remove(bullet)
						self._enemyManager._enemies.remove(enemy)
						self._score += 1
						self._scoreText.setText(str(self._score))
			
			self._scoreText.draw(self._graphics)

	def quit(self):
		self._running = False


game = AlienInvaders()
game.update()