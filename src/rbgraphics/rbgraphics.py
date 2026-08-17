import tkinter as tk

_root = tk.Tk()
_root.withdraw()

def flush():
    _root.update()


class RBGraphics(tk.Canvas):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.pack()
        self.closed = False
        self.lastKey = None
        self.bind_all("<KeyPress>", self._onKeyPress)
        self.bind_all("<KeyRelease>", self._onKeyRelease)
        self.bind("<Motion>", self._moveMouse)

        _root.update()
        self._images = []
        self._controller = None

    def close(self):
        """Close the window"""
        if self.closed:
            return
        self.closed = True
        self.master.destroy()
        flush()

    def isClosed(self):
        return False

    def flushEvents(self):
        if self.closed:
            return False
        try:
            _root.update()
        except tk.TclError:
            self.closed = True
            return False
        return True

    def checkKey(self):
        """Return last key pressed or None if no key pressed since last call"""
        self.update()
        key = self.lastKey
        return key

    def resetKey(self):
        self.lastKey = ""

    def _onKeyPress(self, event):
        if self._controller:
            self._controller._keyDown(event.keysym)

    def _onKeyRelease(self, event):
        if self._controller:
            self._controller._keyUp(event.keysym)

    def _moveMouse(self, event):
        if self._controller:
            self._controller._moveMouse(event.x, event.y)
            
    def draw(self, image, x, y):
        image.draw(self, x, y)

    def remove(self, image):
        self.delete(image._id)
        _root.update()

    def startDrawing(self):
        self._images = []

    def endDrawing(self):
        pass

    def registerController(self, controller):
        self._controller = controller
