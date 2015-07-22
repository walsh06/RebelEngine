class BaseController(object):

	def __init__(self):
		self._keyMap = {"left":None,
						"right": None,
						"up": None,
						"down": None,
						"space": None}

	def _pressKey(self, key):
		if key.lower() in self._keyMap and self._keyMap[key.lower()] != None:
			self._keyMap[key.lower()]()

	def registerKeyFunction(self, key, func):
		if key.lower() in self._keyMap:
			self._keyMap[key.lower()] = func