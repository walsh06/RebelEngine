class RBMoveBehaviourBase(object):

	def __init__(self, speed):
		self._speed = speed

	def updatePosition(self, pos):
		pass


class RBMoveDown(RBMoveBehaviourBase):

	def __init__(self, speed):
		super(RBMoveDown, self).__init__(speed)

	def updatePosition(self, pos):
		pos.movePos(0, self._speed)


class RBMoveUp(RBMoveBehaviourBase):

	def __init__(self, speed):
		super(RBMoveUp, self).__init__(speed)

	def updatePosition(self, pos):
		pos.movePos(0, -self._speed)
