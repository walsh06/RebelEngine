import time
import sys
import os
import tkinter as tk

sys.path.append(os.path.join(".."))

from rbcontroller.rbcontroller import RBBaseController
from rbgraphics.rbgraphics import RBGraphics


class RBGame(object):

    def __init__(self):
        self._updateRate = 0.03
        self._frameRate = 1.0/60.0
        self._maxFrameTime = 0.25
        self._graphics = None
        self._controller = None
        self._running = False

    def update(self):
        time.sleep(self._updateRate)

    def onUpdate(self):
        pass

    def onDraw(self):
        pass

    def run(self):
        """Run the game loop until quit() is called or the window closes.
        The loop separates three things that naively get tangled together:
        - Input is pumped every frame, so keys are never missed.
        - Game logic runs at a fixed timestep (``_updateRate``), so speed does
          not depend on how long a frame takes to render, and physics stays
          reproducible.
        - Drawing happens once per frame, at whatever rate ``_frameRate``
          allows.
        Because logic and rendering run at different rates, a slow frame is
        made up by running several updates back to back rather than by taking
        one large, unstable step.
        """
        # Graphics own the window, the event pump and the close flag, so the
        # loop cannot run without them.
        if self._graphics is None:
            raise RuntimeError("initGraphics must be called before run")

        self._running = True
        try:
            # Timestamp of the previous frame, used to measure real elapsed time.
            previous = time.perf_counter()
            # Real time that has passed but not yet been simulated.
            accumulator = 0.0

            # Stop when quit() was called or the user closed the window.
            while self._isRunning():
                frameStart = time.perf_counter()

                # Bank the time since the last frame. The clamp stops a long
                # stall (a breakpoint, or a dragged window) from queueing up
                # hundreds of catch-up updates, which would freeze the game
                # while it tried to simulate them all.
                accumulator += min(frameStart - previous, self._maxFrameTime)
                previous = frameStart

                try:
                    # Process pending window and keyboard events, firing any
                    # controller callbacks. Done before updating so this frame
                    # acts on the newest input. Returns False once the window
                    # is gone.
                    if not self._graphics.flushEvents():
                        break

                    # Spend the banked time in fixed-size steps. Usually this
                    # runs once; after a slow frame it runs several times to
                    # catch up. Leftover time smaller than one step stays in
                    # the accumulator for the next frame.
                    while accumulator >= self._updateRate:
                        self.onUpdate()
                        accumulator -= self._updateRate
                        # onUpdate may have called quit() or closed the window,
                        # so stop rather than simulating a dead game.
                        if not self._isRunning():
                            break

                    # Do not draw to a window that just went away.
                    if not self._isRunning():
                        break

                    self.onDraw()
                    # Flush this frame's drawing to the screen in one go.
                    self._graphics.flushEvents()
                except tk.TclError:
                    # Tk raises this if the window is destroyed mid-frame, which
                    # is a normal way to quit rather than an error.
                    break

                # Sleep out the rest of the frame budget so the loop does not
                # spin at full speed burning CPU. If the frame overran there is
                # nothing left to sleep and we go straight into the next one.
                remaining = self._frameRate - (time.perf_counter() - frameStart)
                if remaining > 0:
                    time.sleep(remaining)
        finally:
            # Always restore immediate drawing and clear the running flag, even
            # if the game raised, so the engine can be run again afterwards.
            self._running = False

    def _isRunning(self):
        return self._running and not self._graphics.isClosed()
    
    def quit(self):
        self._running = False

    def initController(self):
        if self._graphics:
            self._controller = RBBaseController()
            self._graphics.registerController(self._controller)

    def initGraphics(self, width, height):
        self._graphics = RBGraphics(width, height)
