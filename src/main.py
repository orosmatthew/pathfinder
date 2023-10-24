import pyray as rl

from grid import Grid
from astar import pathfind_astar
from greedy import pathfind_greedy_first


def main():
    rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)
    rl.init_window(800, 800, "Pathfinder")
    rl.set_target_fps(60)

    grid = Grid(grid_size=800, grid_count=16)

    path: list[tuple[int, int]] | None = None
    path_index = 0

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
            path = pathfind_astar(grid)
            path_index = 0

        if rl.is_key_pressed(rl.KeyboardKey.KEY_G):
            path = pathfind_greedy_first(grid)
            path_index = 0

        if path is not None and rl.is_key_pressed(rl.KeyboardKey.KEY_N):
            grid.robot_sprite.pos = rl.Vector2(path[path_index][0] * grid.square_size(),
                                               path[path_index][1] * grid.square_size())
            path_index += 1

        grid.update()
        rl.begin_drawing()
        rl.clear_background(rl.Color(252, 251, 251, 255))
        grid.draw()
        if path is not None:
            for i in range(len(path) - 1):
                rl.draw_line_ex(rl.Vector2(path[i][0] * grid.square_size() + grid.square_size() / 2,
                                           path[i][1] * grid.square_size() + grid.square_size() / 2),
                                rl.Vector2(path[i + 1][0] * grid.square_size() + grid.square_size() / 2,
                                           path[i + 1][1] * grid.square_size() + grid.square_size() / 2), 4,
                                rl.RED)
        rl.end_drawing()


if __name__ == '__main__':
    main()