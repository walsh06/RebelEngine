from math import sqrt


class RBCollision(object):

    def collideRectangleToRectangle(self, rectangleOne, rectangleTwo):
        return not(rectangleOne._left > rectangleTwo._right or
                   rectangleOne._right < rectangleTwo._left or
                   rectangleOne._top > rectangleTwo._bottom or
                   rectangleOne._bottom < rectangleTwo._top)

    def collideCirlceToRectangle(self, circle, rectangle):
    	recCentreX = rectangle._left + (rectangle._w/2)
    	recCentreY = rectangle._top + (rectangle._h/2)

    	dist = sqrt( (recCentreX - circle._centre.getX())**2 + 
    				 (recCentreY - circle._centre.getY())**2 )

    	return dist < circle._radius

    def pointInRectangle(self, pos, rec):
    	x = pos.getX()
    	y = pos.getY()

    	return (x > rec._left and x < rec._right and 
    			y > rec._top and y < rec._bottom)

   	def IntersectCirlce(self, cornerOne, cornerTwo, circle)
    def collideCircleToCirlce(self, c1, c2):
    	dist = sqrt((c1._centre.getX() - c2._centre.getX())**2 + 
    				(c1._centre.getY()- c2._centre.getY())**2 )

    	return dist < (c1._radius + c2._radius)

