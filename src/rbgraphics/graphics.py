import Tkinter as tk
import time, os, sys
_root = tk.Tk()
_root.withdraw()

class Graphics(tk.Canvas):
	def __init__(self, width, height):
		self._width = width
		self._height = height
		master = tk.Toplevel(_root)
		master.protocol("WM_DELETE_WINDOW", self.close)
		tk.Canvas.__init__(self, master, width=width, height=height)
		self.pack()
		self.closed = False
		self.autoflush = True
		self.lastKey = None
		self.bind_all("<Key>", self._onKeyPress)
		_root.update()
		self._images = []
		self._controller = None

	def close(self):
		"""Close the window"""
		if self.closed: return
		self.closed = True
		self.master.destroy()
		self.__autoflush()

	def __autoflush(self):
		if self.autoflush:
			_root.update()

	def isClosed(self):
		return False

	def checkKey(self):
		"""Return last key pressed or None if no key pressed since last call"""
		self.update()
		key = self.lastKey
		return key

	def resetKey(self):
		self.lastKey = ""
	
	def _onKeyPress(self, event):
		if self._controller:
			self._controller._pressKey(event.keysym)

	def draw(self, image, x, y):
		image.draw(self, x, y)

	def remove(self, image):
		self.delete(image._id)
		_root.update()

	def startDrawing(self):
		#self.delete("all")
		self._images = []

	def endDrawing(self):
		pass

	def registerController(self, controller):
		self._controller = controller