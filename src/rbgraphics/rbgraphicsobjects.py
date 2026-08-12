import tkinter as tk

from rbgraphics.rbgraphics import _root


class RBGraphicObject(object):

    def __init__(self, pos):
        self._pos = pos
        self._recreate = True
        self._id = None
        self._drawnX = None
        self._drawnY = None

    def setPosXY(self, x, y):
        self._pos.setPos(x, y)

    def setPos(self, pos):
        self._pos = pos

    def undraw(self, canvas):
        canvas.remove(self)
        self._id = None

    def draw(self, canvas, x=None, y=None):
        if x is not None and y is not None:
            self.setPosXY(x, y)

        posX = self._pos.getX()
        posY = self._pos.getY()
        if self._id is None or self._recreate:
            if self._id is not None:
                canvas.delete(self._id)
            self._id = self.create(canvas, posX, posY)
            self._recreate = False
        elif self._drawnX != posX or self._drawnY != posY:
            canvas.move(self._id, posX - self._drawnX, posY - self._drawnY)
        self._drawnX = posX
        self._drawnY = posY

    def undraw(self, canvas):
        if self._id is not None:
            canvas.delete(self._id)
            self._id = None

    def create(self, canvas, x, y):
        pass  # This method should be implemented in subclasses


class RBImage(RBGraphicObject):

    def __init__(self, image, pos):
        super(RBImage, self).__init__(pos)
        self._img = tk.PhotoImage(file=image, master=_root)

    def create(self, canvas, x, y):
        return canvas.create_image(x, y, image=self._img)
            

class RBText(RBGraphicObject):

    def __init__(self, text, pos):
        super(RBText, self).__init__(pos)
        self._id = None
        self._text = text

    def setText(self, text):
        self._text = text
        self._recreate = True

    def create(self, canvas, x, y):
        return canvas.create_text(x, y, {"text": self._text})

class RBGraphicsShape(RBGraphicObject):
    
    def __init__(self, pos, colour="black", fill=""):
        super(RBGraphicsShape, self).__init__(pos)
        self._colour = colour
        self._fill = fill

    def setColour(self, colour):
        self._colour = colour
        self._recreate = True

    def setFill(self, fill):
        self._fill = fill
        self._recreate = True
    
class RBGraphicCircle(RBGraphicsShape):

    def __init__(self, centre, radius, colour="black", fill=""):
        super(RBGraphicCircle, self).__init__(centre, colour, fill)
        self._radius = radius

    def create(self, canvas, x, y):
        x1 = self._pos.getX() - self._radius
        y1 = self._pos.getY() - self._radius
        x2 = self._pos.getX() + self._radius
        y2 = self._pos.getY() + self._radius
        return canvas.create_oval(x1, y1, x2, y2,
                                        {"fill": self._fill,
                                        "outline": self._colour})


class RBGraphicRectangle(RBGraphicsShape):

    def __init__(self, pos, height, width, colour="black", fill=""):
        super(RBGraphicRectangle, self).__init__(pos, colour, fill)
        self._height = height
        self._width = width

    def create(self, canvas, x, y):
        x1 = self._pos.getX()
        y1 = self._pos.getY()
        x2 = self._pos.getX() + self._width
        y2 = self._pos.getY() + self._height
        return canvas.create_rectangle(x1, y1, x2, y2,
                                            {"fill": self._fill,
                                            "outline": self._colour})
