class RBCollision(object):

    def collideRectangleToRectangle(self, rectangleOne, rectangleTwo):
        return not(rectangleOne._left > rectangleTwo._right or
                   rectangleOne._right < rectangleTwo._left or
                   rectangleOne._top > rectangleTwo._bottom or
                   rectangleOne._bottom < rectangleTwo._top)
