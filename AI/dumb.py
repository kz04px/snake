import random
from .actions import *
from tiles import *

class Dumb():
    def __init__(self):
        self.type = "Dumb"

    def think(self, world, us):
        actions = []
        x, y = us.head[0], us.head[1]

        if world.get(x-1, y) == Tile.EMPTY:
            actions.append(Action.LEFT)
        if world.get(x+1, y) == Tile.EMPTY:
            actions.append(Action.RIGHT)
        if world.get(x, y+1) == Tile.EMPTY:
            actions.append(Action.UP)
        if world.get(x, y-1) == Tile.EMPTY:
            actions.append(Action.DOWN)

        if actions:
            return random.choice(actions)

        return None
