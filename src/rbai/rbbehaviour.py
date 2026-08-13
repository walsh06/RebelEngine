class RBBehaviour(object):

    def execute(self, obj, deltaTime):
        pass


class RBMoveDown(RBBehaviour):

    def __init__(self, speed):
        self._speed = speed

    def execute(self, obj, deltaTime):
        obj.movePos(0, self._speed * deltaTime)


class RBMoveUp(RBBehaviour):

    def __init__(self, speed):
        self._speed = speed

    def execute(self, obj, deltaTime):
        obj.movePos(0, -self._speed * deltaTime)

