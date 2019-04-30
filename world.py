import random
from AI.actions import *
from snake import *
from tiles import *

class World:
    def __init__(self, w, h, walled=True):
        assert w > 0
        assert h > 0
        self.w = w
        self.h = h
        self.grid = [[Tile.EMPTY for y in range(h)] for x in range(w)]
        self.rats = []
        self.snakes = []
        self.frame = 0
        self.wrap = False
        # Add a perimeter wall
        if walled:
            for x in range(w):
                self.set(x, 0, Tile.WALL)
                self.set(x, h-1, Tile.WALL)
            #for y in range(1, h-1):
            #    self.set(0, y, Tile.WALL)
            #    self.set(w-1, y, Tile.WALL)

    def get(self, x, y):
        return self.grid[x%self.w][y%self.h]

    def set(self, x, y, n):
        assert n in Tile
        self.grid[x%self.w][y%self.h] = n

    def add_food(self, retries=10):
        for i in range(retries):
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if self.get(x, y) == Tile.EMPTY:
                self.set(x, y, Tile.FOOD)
                return True
        return False

    def add_poison(self, retries=10):
        for i in range(retries):
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if self.get(x, y) == Tile.EMPTY:
                self.set(x, y, Tile.POISON)
                return True
        return False

    def add_snake(self, brain, retries=100):
        for i in range(retries):
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if self.get(x, y) == Tile.EMPTY:
                self.snakes.append(Snake(x, y, brain, 2))
                return True
        return False

    def add_rat(self, brain, retries=100):
        for i in range(retries):
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if self.get(x, y) == Tile.EMPTY:
                self.rats.append(Entity(x, y, brain))
                return True
        return False

    def step(self):
        for rat in self.rats:
            rat.age += 1

            # Age
            if rat.age > 1000:
                rat.dead = True

            # RIP
            if rat.dead == True:
                continue

            if rat.age%2 == 0:
                continue

            # Think
            action = rat.think(self)

            # Move
            if action == Action.LEFT:
                rat.left()
            elif action == Action.RIGHT:
                rat.right()
            elif action == Action.UP:
                rat.up()
            elif action == Action.DOWN:
                rat.down()

            # Position wrap
            rat.head[0] = rat.head[0]%self.w
            rat.head[1] = rat.head[1]%self.h

        for snake in self.snakes:
            snake.age += 1

            # Age
            if snake.age > 1000:
                snake.dead = True

            # RIP
            if snake.dead == True:
                continue

            # Think
            action = snake.think(self)

            # Move
            if action == Action.LEFT:
                snake.left()
            elif action == Action.RIGHT:
                snake.right()
            elif action == Action.UP:
                snake.up()
            elif action == Action.DOWN:
                snake.down()
            elif action == None:
                snake.dead = True
            else:
                assert False

            # Position wrap
            snake.head[0] = snake.head[0]%self.w
            snake.head[1] = snake.head[1]%self.h

            # Collision -- Wall
            if self.get(snake.head[0], snake.head[1]) == Tile.WALL:
                snake.dead = True
            # Collision -- Food
            elif self.get(snake.head[0], snake.head[1]) == Tile.FOOD:
                self.set(snake.head[0], snake.head[1], Tile.EMPTY)
                snake.grow()
                self.add_food()
            # Collision -- Poison
            elif self.get(snake.head[0], snake.head[1]) == Tile.POISON:
                self.set(snake.head[0], snake.head[1], Tile.EMPTY)
                snake.dead = True

            # Collision -- Self
            if snake.head in snake.body[1:]:
                snake.dead = True
            # Collision -- Rats
            for rat in self.rats:
                if snake.head == rat.head:
                    snake.grow()
                    snake.grow()
                    self.rats.remove(rat)

            # Collision -- Other snakes
            for snake2 in self.snakes:
                if snake == snake2:
                    continue

                if snake.head in snake2.body:
                    snake.dead = True
                elif snake.head in snake2.head:
                    snake.dead = True

        # Dead snakes
        for snake in self.snakes:
            if snake.dead:
                print("Death:")
                print(F"Age:   {snake.age}")
                print(F"Size:  {len(snake.body)+1}")
                print(F"Brain: {snake.brain.type}")
                self.snakes.remove(snake)

        self.frame += 1
