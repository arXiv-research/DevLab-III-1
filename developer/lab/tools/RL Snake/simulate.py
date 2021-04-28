import argparse
import random
import sys

import sdl2
import sdl2.ext as lib
import sdl2.sdlgfx as gfx

import tensorflow as tf

import numpy as np

from rlsnake.game.snake import Snake
from rlsnake.networks.actor_critic import ActorCriticNetwork
from rlsnake.agents.tfagent import TfAgent

parser = argparse.ArgumentParser(description='Simulate a snake match using an agent')
parser.add_argument('--x', type=int, default=4, metavar='X',
                help='number of tiles in horizontal direction (default: 4)')
parser.add_argument('--y', type=int, default=4, metavar='Y',
                help='number of tiles in vertical direction (default: 4)')
parser.add_argument('--visibility-range', type=int, default=4, metavar='VR',
                help='visibility range in each direction for the snake (default: 4)')
parser.add_argument('--seed', type=int, default=42, metavar='N',
                    help='random seed (default: 42)')
parser.add_argument('--neurons', type=int, default=512, metavar='NE',
                    help='how many neurons in each layer (default: 512)')
parser.add_argument('--model-path', type=str, default='./model.pt', metavar='MP',
                    help='path to trained model (default: ./model.pt)')
parser.add_argument('--sleep', type=int, default=100, metavar='MP',
                    help='how long to sleep between frames/steps')
parser.add_argument('--autoplay', dest='autoplay', action='store_const',
                    const=True, default=False,
                    help='automatically play in an endless loop')
args = parser.parse_args()

np.random.seed(args.seed)
tf.random.set_seed(args.seed)
random.seed(args.seed)

n_grid_x = args.x
n_grid_y = args.y
window_width = 800 + 1
grid_cell_size = int(800/n_grid_x)
window_height = n_grid_y*grid_cell_size + 1

COLOR_SNAKE = sdl2.ext.Color(255, 100, 100)
COLOR_SNAKE_EATEN = sdl2.ext.Color(100, 255, 100)
COLOR_SNAKE_HEAD = sdl2.ext.Color(255, 140, 140)
COLOR_SNAKE_HEAD_EATEN = sdl2.ext.Color(140, 255, 140)
COLOR_SNAKE_GAME_OVER = sdl2.ext.Color(100, 100, 100)
COLOR_FOOD = sdl2.ext.Color(100, 255, 100)

COLOR_VIEW_RANGE = sdl2.ext.Color(100, 100, 255, 50)

MAX_MOVES = 500

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
    blendmode = renderer.blendmode
    renderer.blendmode = sdl2.blendmode.SDL_BLENDMODE_ADD
    renderer.fill(((x*grid_cell_size+1, y*grid_cell_size+1, grid_cell_size-1, grid_cell_size-1)), color=color)
    renderer.blendmode = blendmode

def fill_circle(renderer, x, y, color=lib.Color(255, 255, 255)):
    gfx.filledCircleRGBA(renderer.sdlrenderer, x*grid_cell_size+int(grid_cell_size/2)+1, y*grid_cell_size+int(grid_cell_size/2)+1, int(grid_cell_size/4), color.r, color.g, color.b, color.a)

def run():
    lib.init()
    window = lib.Window('RLSnake', size=(window_width, window_height))
    window.show()

    renderer = lib.Renderer(window)
    fontManager = sdl2.ext.FontManager(font_path = "assets/fonts/Roboto-Regular.ttf", size = 14)
    factory = sdl2.ext.SpriteFactory(renderer=renderer)
    text = factory.from_text("Current score: ",fontmanager=fontManager)

    snake = Snake(n_grid_x, n_grid_y)
    snake.set_visibility_range(args.visibility_range)
    snake.reset()

    network = ActorCriticNetwork(4, fc1_dims=args.neurons, fc2_dims=args.neurons)
    agent = TfAgent(network)
    agent.load_weights(args.model_path)

    autoplay = args.autoplay
    moves = 0
    running = True
    game_over = False
    old_score = 0
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
                if event.key.keysym.sym == 112:
                    autoplay = not autoplay
                if event.key.keysym.sym == 114:
                    snake.reset()
                    moves = 0
                    old_score = 0
                    game_over = False
                    current_tiles = snake.get_tiles()
                    break
                if not game_over:
                    if not autoplay:
                        if event.key.keysym.sym == sdl2.SDLK_SPACE:
                            action = agent.get_action(snake.get_view_obs())
                            _, game_over, _ = snake.step(action)
                            current_tiles = snake.get_tiles()
                            moves += 1

        if autoplay:
            action = agent.get_action(snake.get_view_obs())
            _, game_over, _ = snake.step(action)
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
                        if snake.get_score() > old_score:
                            fill_tile(renderer, int(x), int(y), COLOR_SNAKE_EATEN)
                        else:
                            fill_tile(renderer, int(x), int(y), COLOR_SNAKE)
                if tile == 4:
                    if game_over:
                        fill_tile(renderer, int(x), int(y), COLOR_SNAKE_GAME_OVER)
                    else:
                        if snake.get_score() > old_score:
                            fill_tile(renderer, int(x), int(y), COLOR_SNAKE_HEAD_EATEN)
                        else:    
                            fill_tile(renderer, int(x), int(y), COLOR_SNAKE_HEAD)
                if tile == 3:
                    fill_circle(renderer, int(x), int(y), COLOR_FOOD)

        for tile in snake.get_current_view():
            fill_tile(renderer, int(tile[0]), int(tile[1]), COLOR_VIEW_RANGE)

        if snake.get_score() > old_score:
            old_score = snake.get_score()

        text = factory.from_text("Current score: " + str(snake.get_score()), fontmanager=fontManager)
        renderer.copy(text, dstrect=(0, 0, text.size[0],text.size[1]))
        if autoplay:
            text = factory.from_text("Move: " + str(moves) + " / " + str(MAX_MOVES), fontmanager=fontManager)
        else:
            text = factory.from_text("Move: " + str(moves), fontmanager=fontManager)
        renderer.copy(text, dstrect=(0, 14, text.size[0],text.size[1]))

        renderer.present()

        sdl2.SDL_Delay(args.sleep)

        if autoplay and (game_over or moves >= MAX_MOVES):
            snake.reset()
            moves = 0
            old_score = 0
            game_over = False

    return 0

if __name__ == "__main__":
    sys.exit(run())
