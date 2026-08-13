import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbcontroller.rbcontroller import RBBaseController, KEY_DOWN, KEY_HELD, KEY_UP


def key_down():
    print("Test Key Down")

def key_up():
    print("Test Key UP")

def key_held():
    print("Test Key Held")

controller = RBBaseController()

controller.registerKeyFunction("a", key_down)
controller.registerKeyFunction("b", key_up, KEY_UP)
controller.registerKeyFunction("c", key_held, KEY_HELD)

controller._keyDown("a")
controller._keyDown("b")
controller._keyUp("a")
controller._keyUp("b")

controller._keyDown("c")
for x in range(0,10):
    controller.update(x)
controller._keyUp("c")



