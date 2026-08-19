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

    def __init__(self, image, pos, anchor="nw"):
        super(RBImage, self).__init__(pos)
        self._img = tk.PhotoImage(file=image, master=_root)
        self._anchor = anchor

    def create(self, canvas, x, y):
        return canvas.create_image(x, y, image=self._img, anchor=self._anchor)
            
    @property
    def width(self):
        return self._img.width()

    @property
    def height(self):
        return self._img.height()


class RBAnimatedImage(RBGraphicObject):

    @classmethod
    def fromSpriteSheet(cls, spriteSheet, pos, frameWidth, frameHeight,
                        frameCount=None, columns=None, frameIndices=None,
                        frameRate=10, loop=True, autoplay=True, margin=0,
                        spacing=0, anchor="nw"):
        if frameWidth <= 0 or frameHeight <= 0:
            raise ValueError("Frame dimensions must be greater than zero")
        if margin < 0 or spacing < 0:
            raise ValueError("margin and spacing cannot be negative")
        if frameCount is not None and frameCount <= 0:
            raise ValueError("frameCount must be greater than zero")
        if frameIndices is not None and frameCount is not None:
            raise ValueError("Pass frameCount or frameIndices, not both")

        sheet = tk.PhotoImage(file=spriteSheet, master=_root)
        availableColumns = ((sheet.width() - 2 * margin + spacing)
                            // (frameWidth + spacing))
        availableRows = ((sheet.height() - 2 * margin + spacing)
                         // (frameHeight + spacing))
        if availableColumns <= 0 or availableRows <= 0:
            raise ValueError("Frame dimensions do not fit inside the sprite sheet")
        if columns is None:
            columns = availableColumns
        if columns <= 0 or columns > availableColumns:
            raise ValueError("columns exceeds the sprite sheet width")

        capacity = columns * availableRows
        if frameIndices is None:
            if frameCount is None:
                frameCount = capacity
            frameIndices = range(frameCount)
        else:
            frameIndices = list(frameIndices)
            if not frameIndices:
                raise ValueError("frameIndices must contain at least one frame")

        frames = []
        for frameIndex in frameIndices:
            if not isinstance(frameIndex, int) or not 0 <= frameIndex < capacity:
                raise ValueError("frame index is outside the sprite sheet")
            row, column = divmod(frameIndex, columns)
            x = margin + column * (frameWidth + spacing)
            y = margin + row * (frameHeight + spacing)
            frame = tk.PhotoImage(width=frameWidth, height=frameHeight,
                                  master=_root)
            frame.tk.call(frame, "copy", sheet, "-from", x, y,
                          x + frameWidth, y + frameHeight, "-to", 0, 0)
            frames.append(frame)

        animation = cls.__new__(cls)
        RBGraphicObject.__init__(animation, pos)
        animation._spriteSheet = sheet
        animation._configureFrames(frames, frameRate, loop, autoplay, anchor)
        return animation

    def __init__(self, frames, pos, frameRate=10, loop=True, autoplay=True,
                 anchor="nw"):
        super(RBAnimatedImage, self).__init__(pos)
        if not frames:
            raise ValueError("RBAnimatedImage needs at least one frame")
        loadedFrames = [tk.PhotoImage(file=frame, master=_root)
                        for frame in frames]
        self._configureFrames(loadedFrames, frameRate, loop, autoplay, anchor)

    def _configureFrames(self, frames, frameRate, loop, autoplay, anchor):
        if frameRate <= 0:
            raise ValueError("frameRate must be greater than zero")
        dimensions = {(frame.width(), frame.height())
                      for frame in frames}
        if len(dimensions) != 1:
            raise ValueError("All animation frames must have the same dimensions")

        self._frames = frames
        self._anchor = anchor
        self._frameDuration = 1.0 / frameRate
        self._loop = loop
        self._playing = autoplay
        self._frameIndex = 0
        self._elapsed = 0.0

    @property
    def width(self):
        return self._frames[0].width()

    @property
    def height(self):
        return self._frames[0].height()

    @property
    def frameIndex(self):
        return self._frameIndex

    def isPlaying(self):
        return self._playing

    def play(self):
        self._playing = True

    def pause(self):
        self._playing = False

    def stop(self):
        self._playing = False
        self._elapsed = 0.0
        self._setFrame(0)

    def update(self, deltaTime):
        if not self._playing or len(self._frames) == 1:
            return

        self._elapsed += deltaTime
        framesToAdvance = int(self._elapsed / self._frameDuration)
        if framesToAdvance == 0:
            return
        self._elapsed -= framesToAdvance * self._frameDuration

        nextFrame = self._frameIndex + framesToAdvance
        if self._loop:
            self._setFrame(nextFrame % len(self._frames))
        elif nextFrame >= len(self._frames):
            self._setFrame(len(self._frames) - 1)
            self._playing = False
            self._elapsed = 0.0
        else:
            self._setFrame(nextFrame)

    def _setFrame(self, frameIndex):
        if frameIndex != self._frameIndex:
            self._frameIndex = frameIndex
            self._recreate = True

    def create(self, canvas, x, y):
        return canvas.create_image(x, y,
                                   image=self._frames[self._frameIndex],
                                   anchor=self._anchor)


class RBTextGraphic(RBGraphicObject):

    def __init__(self, text, pos, colour="black", font_family="TkDefaultFont",
                 font_size=10, font_weight="normal", anchor="center",
                 justify="left", width=None):
        super(RBTextGraphic, self).__init__(pos)
        self._text = text
        self._colour = colour
        self._font_family = font_family
        self._font_size = font_size
        self._font_weight = font_weight
        self._anchor = anchor
        self._justify = justify
        self._width = width

    def setText(self, text):
        self._text = text
        self._recreate = True

    def setColour(self, colour):
        self._colour = colour
        self._recreate = True

    def setFont(self, family=None, size=None, weight=None):
        if family is not None:
            self._font_family = family
        if size is not None:
            self._font_size = size
        if weight is not None:
            self._font_weight = weight
        self._recreate = True

    def setAnchor(self, anchor):
        self._anchor = anchor
        self._recreate = True

    def setJustify(self, justify):
        self._justify = justify
        self._recreate = True

    def setWidth(self, width):
        self._width = width
        self._recreate = True

    def create(self, canvas, x, y):
        options = {
            "text": self._text,
            "fill": self._colour,
            "font": (self._font_family, self._font_size, self._font_weight),
            "anchor": self._anchor,
            "justify": self._justify,
        }
        if self._width is not None:
            options["width"] = self._width
        return canvas.create_text(x, y, **options)

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

    @property
    def radius(self):
        return self._radius

    def create(self, canvas, x, y):
        x1 = self._pos.getX() - self._radius
        y1 = self._pos.getY() - self._radius
        x2 = self._pos.getX() + self._radius
        y2 = self._pos.getY() + self._radius
        return canvas.create_oval(x1, y1, x2, y2,
                                        {"fill": self._fill,
                                        "outline": self._colour})


class RBGraphicRectangle(RBGraphicsShape):

    def __init__(self, pos, width, height, colour="black", fill=""):
        super(RBGraphicRectangle, self).__init__(pos, colour, fill)
        self._height = height
        self._width = width

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def create(self, canvas, x, y):
        x1 = self._pos.getX()
        y1 = self._pos.getY()
        x2 = self._pos.getX() + self._width
        y2 = self._pos.getY() + self._height
        return canvas.create_rectangle(x1, y1, x2, y2,
                                            {"fill": self._fill,
                                            "outline": self._colour})
