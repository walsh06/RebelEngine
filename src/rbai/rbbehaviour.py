class RBMoveBehaviourBase(object):

	def updatePosition(self, pos):
		pass


class RBMoveDown(RBMoveBehaviourBase):

	def updatePosition(self, pos):
		pos.setPos(pos.getX(), pos.getY() + 1)


class RBMoveUp(RBMoveBehaviourBase):

	def updatePosition(self, pos):
		pos.setPos(pos.getX(), pos.getY() - 1)
