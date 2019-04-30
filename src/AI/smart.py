import random
from .actions import *
from tiles import *

dirs = [[Action.LEFT, -1, 0], [Action.RIGHT, 1, 0], [Action.UP, 0, 1], [Action.DOWN, 0, -1]]

class Smart():
    def __init__(self):
        self.type = "Smart"

    def think(self, world, us):
        good = []
        okay = []
        x, y = us.head[0], us.head[1]

        for a, dx, dy in dirs:
            nx, ny = x + dx, y + dy

            # Avoid snake collisions
            quit = False
            for snake in world.snakes:
                if [nx, ny] in snake.body:
                    quit = True
                    break
                elif [nx, ny] == snake.head:
                    quit = True
                    break
            if quit:
                continue

            # Bad -- Hitting walls or eating poison
            if world.get(nx, ny) in [Tile.WALL, Tile.POISON]:
                continue

            # Good -- Eat rats
            if [nx, ny] in [rat.head for rat in world.rats]:
                good.append(a)
                continue

            # Good -- Eat food
            if world.get(nx, ny) in [Tile.FOOD]:
                good.append(a)
                continue

            # Okay -- Go somewhere empty
            if world.get(nx, ny) in [Tile.EMPTY]:
                okay.append(a)

        if good:
            return random.choice(good)
        elif okay:
            return random.choice(okay)
        else:
            return None
