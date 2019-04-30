from entity import *

class Snake(Entity):
    def __init__(self, x, y, brain=None, l=1):
        assert l >= 1
        Entity.__init__(self, x, y, brain)
        # Body
        self.body = []
        for i in range(l-1):
            self.grow()

    def grow(self):
        self.body.insert(0, [self.head[0], self.head[1]])

    def left(self):
        self.body.pop()
        self.grow()
        Entity.left(self)

    def right(self):
        self.body.pop()
        self.grow()
        Entity.right(self)

    def up(self):
        self.body.pop()
        self.grow()
        Entity.up(self)

    def down(self):
        self.body.pop()
        self.grow()
        Entity.down(self)
