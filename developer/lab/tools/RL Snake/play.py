import argparse
import sys

import sdl2
import sdl2.ext as lib
import sdl2.sdlgfx as gfx

from rlsnake.game.snake import Snake

parser = argparse.ArgumentParser(description='Simulate a snake match using an agent')
parser.add_argument('--x', type=int, default=4, metavar='X',
                help='number of tiles in horizontal direction (default: 4)')
parser.add_argument('--y', type=int, default=4, metavar='Y',
                help='number of tiles in vertical direction (default: 4)')
args = parser.parse_args()

n_grid_x = args.x
n_grid_y = args.y
window_width = 800 + 1
grid_cell_size = int(800/n_grid_x)
window_height = n_grid_y*grid_cell_size + 1

COLOR_SNAKE = sdl2.ext.Color(255, 100, 100)
COLOR_SNAKE_HEAD = sdl2.ext.Color(255, 140, 140)
COLOR_SNAKE_GAME_OVER = sdl2.ext.Color(100, 100, 100)
COLOR_FOOD = sdl2.ext.Color(100, 255, 100)

def draw_grid(renderer):
    x = 0
    while x < 1 + n_grid_x * grid_cell_size:
        renderer.draw_line([x, 0, x, window_height], lib.Color(255,255,255))
        x += grid_cell_size

    y = 0
    while y < 1 + n_grid_y * grid_cell_size:
        renderer.draw_line([0, y, window_width, y], lib.Color(255,255,255))
        y += grid_cell_size

def fill_tile(renderer, x, y, color=lib.Color(255,255,255)):
    renderer.fill(((x*grid_cell_size+1, y*grid_cell_size+1, grid_cell_size-1, grid_cell_size-1)), color=color)

def fill_circle(renderer, x, y, color=lib.Color(255, 255, 255)):
    gfx.filledCircleRGBA(renderer.sdlrenderer, x*grid_cell_size+int(grid_cell_size/2)+1, y*grid_cell_size+int(grid_cell_size/2)+1, int(grid_cell_size/4), color.r, color.g, color.b, color.a)

def run():
    lib.init()
    window = lib.Window('RLSnake', size=(window_width, window_height))
    window.show()

    renderer = lib.Renderer(window)
    font_manager = sdl2.ext.FontManager(font_path = "assets/fonts/Roboto-Regular.ttf", size = 14)
    factory = sdl2.ext.SpriteFactory(renderer=renderer)
    text = factory.from_text("Current score: ",fontmanager=font_manager)

    snake = Snake(n_grid_x, n_grid_y)
    snake.reset()

    moves = 0
    running = True
    game_over = False
    current_tiles = snake.get_tiles()
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                if event.key.keysym.sym == 114:
                    snake.reset()
                    game_over = False
                    current_tiles = snake.get_tiles()
                    moves = 0
                    break
                if not game_over:
                    if event.key.keysym.sym == sdl2.SDLK_UP:
                        _, game_over, _ = snake.step(3)
                        current_tiles = snake.get_tiles()
                        moves += 1
                    elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                        _, game_over, _ = snake.step(2)
                        current_tiles = snake.get_tiles()
                        moves += 1
                    elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                        _, game_over, _ = snake.step(1)
                        current_tiles = snake.get_tiles()
                        moves += 1
                    elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                        _, game_over, _ = snake.step(0)
                        current_tiles = snake.get_tiles()
                        moves += 1

        renderer.clear(sdl2.ext.Color(0, 0, 0))
        draw_grid(renderer)

        for x in range(len(current_tiles)):
            for y in range(len(current_tiles[x])):
                tile = current_tiles[x][y]
                if tile == 0:
                    continue
                if tile == 1:
                    continue
                if tile == 2:
                    if game_over:
                        fill_tile(renderer, int(x), int(y), COLOR_SNAKE_GAME_OVER)
                    else:
                        fill_tile(renderer, int(x), int(y), COLOR_SNAKE)
                if tile == 4:
                    if game_over:
                        fill_tile(renderer, int(x), int(y), COLOR_SNAKE_GAME_OVER)
                    else:
                        fill_tile(renderer, int(x), int(y), COLOR_SNAKE_HEAD)
                if tile == 3:
                    fill_circle(renderer, int(x), int(y), COLOR_FOOD)

        text = factory.from_text("Current score: " + str(snake.get_score()), fontmanager=font_manager)
        renderer.copy(text, dstrect=(0, 0, text.size[0],text.size[1]))
        text = factory.from_text("Move: " + str(moves), fontmanager=font_manager)
        renderer.copy(text, dstrect=(0, 14, text.size[0],text.size[1]))

        renderer.present()

        sdl2.SDL_Delay(33)
    return 0

if __name__ == "__main__":
    sys.exit(run())
