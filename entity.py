class Entity:
    def __init__(self, x, y, brain=None):
        self.head = [x, y]
        self.brain = None
        self.age = 0
        self.food = 0
        self.dead = False
        self.brain = brain()

    def think(self, world):
        if not self.dead and self.brain:
            return self.brain.think(world, self)

    def left(self):
        self.head[0] -= 1

    def right(self):
        self.head[0] += 1

    def up(self):
        self.head[1] += 1

    def down(self):
        self.head[1] -= 1
