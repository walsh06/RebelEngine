import Tkinter as tk

from graphics import _root


class RBGraphicObject(object):

    def __init__(self, pos):
        self._pos = pos 

    def setObjectPos(self, x, y):
        self._pos.setPos(x, y)

    def undraw(self, canvas):
        canvas.remove(self)
        self._id = None


class RBImage(RBGraphicObject):

    def __init__(self, image, pos):
        super(RBImage, self).__init__(pos)
        self._img = tk.PhotoImage(file=image, master=_root)
        self._id = None

    def draw(self, canvas, x, y):
        if self._id is None:
            self._id = canvas.create_image(x, y, image=self._img)
            canvas.update()
        else:
            dx = x - self._pos.getX()
            dy = y - self._pos.getY()
            canvas.move(self._id, dx, dy)
        self.setObjectPos(x, y)
        _root.update()


class RBText(RBGraphicObject):

    def __init__(self, text, pos):
        super(RBText, self).__init__(pos)
        self._id = None
        self._text = text
        self._textChange = False

    def setText(self, text):
        self._text = text
        self._textChange = True

    def draw(self, canvas):
        if self._id is None:
            self._id = canvas.create_text(self._pos.getX(),
                                          self._pos.getY(),
                                          {"text": self._text})
        elif self._textChange is True:
            canvas.delete(self._id)
            self._id = canvas.create_text(self._pos.getX(),
                                          self._pos.getY(),
                                          {"text": self._text})
            self._textChange = False
        _root.update()
