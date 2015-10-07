import Tkinter as tk

from rbgraphics import _root


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


class RBCircle(RBGraphicObject):

    def __init__(self, centre, radius, colour="black", fill=""):
        super(RBCircle, self).__init__(centre)
        self._radius = radius
        self._colour = colour
        self._fill = fill
        self._id = None

    def draw(self, canvas, x, y):
        if self._id is None:
            self.setObjectPos(x, y)
            x1 = self._pos.getX() - self._radius
            y1 = self._pos.getY() - self._radius
            x2 = self._pos.getX() + self._radius
            y2 = self._pos.getY() + self._radius
            self._id = canvas.create_oval(x1, y1, x2, y2,
                                          {"fill": self._fill,
                                           "outline": self._colour})
            canvas.update()
        else:
            dx = x - self._pos.getX()
            dy = y - self._pos.getY()
            canvas.move(self._id, dx, dy)
        self.setObjectPos(x, y)
        _root.update()


class RBRectangle(RBGraphicObject):

    def __init__(self, pos, height, width, colour="black", fill=""):
        super(RBRectangle, self).__init__(pos)
        self._height = height
        self._width = width
        self._colour = colour
        self._fill = fill
        self._id = None

    def draw(self, canvas, x, y):
        if self._id is None:
            self.setObjectPos(x, y)
            x1 = self._pos.getX()
            y1 = self._pos.getY()
            x2 = self._pos.getX() + self._width
            y2 = self._pos.getY() + self._height
            self._id = canvas.create_rectangle(x1, y1, x2, y2,
                                               {"fill": self._fill,
                                                "outline": self._colour})
            canvas.update()
        else:
            dx = x - self._pos.getX()
            dy = y - self._pos.getY()
            canvas.move(self._id, dx, dy)
        self.setObjectPos(x, y)
        _root.update()
