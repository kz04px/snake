import ctypes
from world import *
from AI.dumb import *
from AI.smart import *
from sdl2 import *
from sdl2.sdlttf import *

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
PURPLE = (255, 0, 255)

def text(font, renderer, string, colour):
    surf = TTF_RenderText_Blended(font, str.encode(string), colour)
    texture = SDL_CreateTextureFromSurface(renderer, surf)
    SDL_FreeSurface(surf)
    return texture

def main():
    SDL_Init(SDL_INIT_VIDEO)
    TTF_Init()

    # Window settings
    window_width = 800
    window_height = 600

    # Window
    window   = SDL_CreateWindow(b"Snake 0u0", 0, 0, window_width, window_height, SDL_WINDOW_SHOWN)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

    font = TTF_OpenFont(str.encode("fonts/OpenSans-Regular.ttf"), 24);
    paused_texture = text(font, renderer, "PAUSED", SDL_Color(255,0,0,255))
    dumb_texture = text(font, renderer, "D", SDL_Color(20,0,0,255))
    smart_texture = text(font, renderer, "S", SDL_Color(20,0,0,255))

    # World -- Dimensions
    world = World(40, 30)
    # World -- Food
    for i in range(20):
        world.add_food()
    # World -- Poison
    for i in range(2):
        world.add_poison()
    # World -- Snakes
    for i in range(0):
        world.add_snake(Dumb)
    for i in range(2):
        world.add_snake(Smart)
    # World -- Rats
    for i in range(8):
        world.add_rat(Dumb)

    for i in range(20):
        x = random.randint(0, world.w-1)
        y = random.randint(0, world.h-1)
        world.set(x, y, Tile.WALL)
        world.set(world.w-x-1, y, Tile.WALL)

    # Grid sizes
    grid_width = int(window_width/world.w)
    grid_height = int(window_height/world.h)

    # Print details
    print(F"Window: {window_width}, {window_height}")
    print(F"World:  {world.w}, {world.h}")
    print(F"Grid:   {grid_width}, {grid_height}")

    running = True
    paused = False
    debug = True
    event = SDL_Event()
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_SPACE:
                    paused = not paused
                elif event.key.keysym.sym == SDLK_d:
                    debug = not debug

        # Update
        if not paused:
            world.step()

        # Render -- Clear
        SDL_SetRenderDrawColor(renderer, 20, 20, 20, 255)
        SDL_RenderClear(renderer)

        # Render -- Tiles
        for x in range(world.w):
            for y in range(world.h):
                if world.grid[x][y] == Tile.EMPTY:
                    continue
                elif world.grid[x][y] == Tile.FOOD:
                    SDL_SetRenderDrawColor(renderer, 128, 0, 255, 255)
                elif world.grid[x][y] == Tile.WALL:
                    SDL_SetRenderDrawColor(renderer, 128, 128, 128, 255)
                elif world.grid[x][y] == Tile.POISON:
                    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
                else:
                    assert False

                r = SDL_Rect(grid_width*x + 1,
                             grid_height*y + 1,
                             grid_width - 2,
                             grid_height - 2)
                SDL_RenderFillRect(renderer, r)

        # Render -- Snake bodies
        SDL_SetRenderDrawColor(renderer, 0, 200, 0, 255)
        for snake in world.snakes:
            for x, y in snake.body:
                r = SDL_Rect(grid_width*x + 1,
                             grid_height*y + 1,
                             grid_width - 2,
                             grid_height - 2)
                SDL_RenderFillRect(renderer, r)

        # Render -- Snake heads
        SDL_SetRenderDrawColor(renderer, 0, 150, 0, 255)
        for snake in world.snakes:
            r = SDL_Rect(grid_width*snake.head[0] + 1,
                         grid_height*snake.head[1] + 1,
                         grid_width - 2,
                         grid_height - 2)
            SDL_RenderFillRect(renderer, r)

        # Render -- Rats
        SDL_SetRenderDrawColor(renderer, 102, 50, 0, 255)
        for rat in world.rats:
            r = SDL_Rect(grid_width*rat.head[0] + 1,
                         grid_height*rat.head[1] + 1,
                         grid_width - 2,
                         grid_height - 2)
            SDL_RenderFillRect(renderer, r)

        # Render -- Grid
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        for x in range(world.w):
            SDL_RenderDrawLine(renderer, grid_width*x, 0, grid_width*x, window_height)
        for y in range(world.h):
            SDL_RenderDrawLine(renderer, 0, grid_height*y, window_width, grid_height*y)

        if debug:
            for snake in world.snakes:
                dst = SDL_Rect(snake.head[0]*grid_width, snake.head[1]*grid_height, grid_width, grid_height)
                if snake.brain.type == "Dumb":
                    SDL_RenderCopy(renderer, dumb_texture, None, dst)
                elif snake.brain.type == "Smart":
                    SDL_RenderCopy(renderer, smart_texture, None, dst)

        # Render -- Paused message
        if paused:
            dst = SDL_Rect(30, 30, 300, 300)
            SDL_RenderCopy(renderer, paused_texture, None, dst)

        # Flip
        SDL_RenderPresent(renderer)

        SDL_Delay(250)

    SDL_DestroyTexture(paused_texture)
    SDL_DestroyTexture(dumb_texture)
    SDL_DestroyTexture(smart_texture)
    TTF_CloseFont(font)
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()

if __name__ == "__main__":
    main()
