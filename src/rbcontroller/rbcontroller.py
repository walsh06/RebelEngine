KEY_DOWN = "key_down"
KEY_UP = "key_up"
KEY_HELD = "key_held"

from rbbase.rbbase import RB2DPosition

class RBBaseController(object):

    def __init__(self):
        self._keyMap = {KEY_UP: {}, KEY_DOWN: {}, KEY_HELD: {}}
        self._heldKeys = set()
        self._mousePos = RB2DPosition(0,0)

    def _keyDown(self, key):
        """
        Called when a key is pressed
        """
        key = key.lower()
        if key not in self._heldKeys:
            self._keyMap[KEY_DOWN].get(key, lambda: None)()
            self._heldKeys.add(key)

    def _keyUp(self, key):
        """
        Called when a key is released
        """
        key = key.lower()
        self._heldKeys.discard(key)
        self._keyMap[KEY_UP].get(key, lambda: None)()

    def _moveMouse(self, x, y):
        self._mousePos = RB2DPosition(x, y)

    @property
    def mousePos(self):
        return self._mousePos

    def update(self, deltaTime):
        """
        Called every game step to update held keys
        """
        for key in self._heldKeys:
            self._keyMap[KEY_HELD].get(key, lambda: None)()

    def registerKeyFunction(self, key, func, eventType=KEY_DOWN):
        """
        Register a function for a key on a given key event.
        Events: KEY_DOWN, KEY_UP, KEY_HELD
        """
        self._keyMap[eventType][key.lower()] = func
