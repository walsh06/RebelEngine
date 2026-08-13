class RBScene(object):
    """
    A scene that manages multiple RBGraphicObjects or RBGameObjects and draws them in layers.
    """
    def __init__(self, canvas):
        self.canvas = canvas
        self.layers = {}
        self._drawIds = {}
        self._reorder = False

    def addObject(self, obj, layer=0):
        """
        Add an RBGraphicObject or RBGameObject to the scene in the specified layer.
        """
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append(obj)
        self._reorder = True

    def removeObject(self, obj, layer=None):
        """
        Remove an RBGraphicObject or RBGameObject from the scene.
        """
        if layer is None:
            for l, objects in self.layers.items():
                if obj in objects:
                    self.layers[l].remove(obj)
                    break
        else:
            if layer in self.layers and obj in self.layers[layer]:
                self.layers[layer].remove(obj)
        obj.undraw(self.canvas)
        self._reorder = True

    def draw(self):
        """
        Draw all objects in the scene, 
        called from onDraw in the game loop.
        """
        for layer in sorted(self.layers.keys()):
            for obj in self.layers[layer]:
                obj.draw(self.canvas)

                if self._drawIds.get(obj) != obj._id:
                    self._drawIds[obj] = obj._id
                    self._reorder = True

        if self._reorder:
            for layer in sorted(self.layers.keys()):
                for obj in self.layers[layer]:
                    self.canvas.tag_raise(obj._id)
            self._reorder = False

    def clear(self, layer=None):
        """
        Clear all objects from the scene, or from a specific layer if provided.
        """
        if layer is None:
            for layer in self.layers:
                for obj in self.layers[layer]:
                    obj.undraw(self.canvas)
            self.layers.clear()
        else:
            if layer in self.layers:
                for obj in self.layers[layer]:
                    obj.undraw(self.canvas)
                del self.layers[layer]
