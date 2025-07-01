from util.vectorsprites import VectorSprite

class Point(VectorSprite):

    # Class attributes
    pointlist = [(0, 0), (1, 1), (1, 0), (0, 1)]

    def __init__(self, position, heading, stage):
        VectorSprite.__init__(self, position, heading, self.pointlist)
        self.stage = stage
        self.ttl = 30

    def move(self):
        self.ttl -= 1
        VectorSprite.move(self)