import json
import os
import random

import pyray as rl

from grid import Grid
from astar import pathfind_astar
from greedy import pathfind_greedy_first
from dijkstra import pathfind_dijkstra

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


def gen_random(grid):
    perlin_image = rl.gen_image_perlin_noise(16, 16, random.randint(0, 2 ** 16), random.randint(0, 2 ** 16),
                                             5.0)
    for x in range(16):
        for y in range(16):
            noise = rl.get_image_color(perlin_image, x, y)
            grid.walls[x][y] = noise.r > 150
    x_range = [*range(16)]
    y_range = [*range(16)]
    random.shuffle(x_range)
    random.shuffle(y_range)
    for x in x_range:
        for y in y_range:
            if not grid.walls[x][y]:
                grid.robot_sprite.pos = rl.Vector2(x * grid.square_size(), y * grid.square_size())
    random.shuffle(x_range)
    random.shuffle(y_range)
    for x in x_range:
        for y in y_range:
            if not grid.walls[x][y]:
                grid.finish_sprite.pos = rl.Vector2(x * grid.square_size(), y * grid.square_size())


def main():
    rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pathfinder")
    rl.set_target_fps(60)

    grid = Grid(grid_size=800, grid_count=16, draw_x_pos=0, draw_y_pos=0)

    roboto = rl.load_font_ex("./res/Roboto-Medium.ttf", 24, None, 0)
    rl.gui_set_font(roboto)

    data = []
    while not rl.window_should_close() and len(data) < 4000:
        grid.update()
        rl.begin_drawing()

        gen_random(grid)
        path_greedy, visited_greedy = pathfind_greedy_first(grid)
        path_dijkstra, visited_dijkstra = pathfind_dijkstra(grid)
        path_astar, visited_astar = pathfind_astar(grid)

        if path_greedy is not None and path_dijkstra is not None and path_astar is not None:
            data.append({
                "greedy": {
                    "cost": len(path_greedy),
                    "visited": visited_greedy
                },
                "dijkstra": {
                    "cost": len(path_dijkstra),
                    "visited": visited_dijkstra
                },
                "astar": {
                    "cost": len(path_astar),
                    "visited": visited_astar
                }
            })
            print(len(data))

        rl.clear_background(rl.Color(252, 251, 251, 255))
        grid.draw_background()
        grid.draw_items()
        rl.end_drawing()

    if not os.path.exists("./data"):
        os.mkdir("./data")
    for i in range(1024):
        if not os.path.exists(f"./data/{i}.json"):
            with open(f"./data/{i}.json", "w") as file:
                json.dump(data, file)
            break


if __name__ == '__main__':
    main()
