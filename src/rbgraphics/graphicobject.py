import Tkinter as tk

from graphics import _root

class Image(object):
	def __init__(self, image, x = 0, y = 0):
		self._img = tk.PhotoImage(file=image, master=_root)
		self._id = None
		self.setOrigin(x, y)

	def setOrigin(self, x, y):
		self._x = x
		self._y = y

	def draw(self, canvas, x, y):
		if self._id == None:	
			self._id = canvas.create_image(x, y, image=self._img)
			canvas.update()
		else:
			dx = x - self._x
			dy = y - self._y
			canvas.move(self._id, dx, dy)
			self.setOrigin(x, y)
		_root.update()

	def undraw(self):
		self._id = None

class Text(object):

	def __init__(self, text, x, y):
		self._id = None
		self._text = text
		self._x = x
		self._y = y
		self._textChange = False

	def setText(self, text):
		self._text = text
		self._textChange = True

	def draw(self, canvas):
		if self._id == None:
			self._id = canvas.create_text(self._x, self._y, {"text": self._text})
		elif self._textChange == True:
			canvas.delete(self._id)
			self._id = canvas.create_text(self._x, self._y, {"text": self._text})
			self._textChange = False
		_root.update()
