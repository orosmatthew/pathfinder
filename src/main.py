import pyray as rl

from grid import Grid
from astar import pathfind_astar
from greedy import pathfind_greedy_first
from dijkstra import pathfind_dijkstra

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 860


def main():
    rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pathfinder")
    rl.set_target_fps(60)

    grid_offset_x = 0
    grid_offset_y = 60

    grid = Grid(grid_size=800, grid_count=16, draw_x_pos=grid_offset_x, draw_y_pos=grid_offset_y)

    path: list[tuple[int, int]] | None = None
    path_index = 0

    roboto = rl.load_font_ex("./res/Roboto-Medium.ttf", 24, None, 0)
    rl.gui_set_font(roboto)

    while not rl.window_should_close():

        grid.update()
        rl.begin_drawing()

        if rl.gui_button(rl.Rectangle(10, 10, 100, 40), "Greedy"):
            path = pathfind_greedy_first(grid)
            path_index = 0
        if rl.gui_button(rl.Rectangle(10 + 120, 10, 100, 40), "Dijkstra"):
            path = pathfind_dijkstra(grid)
            path_index = 0
        if rl.gui_button(rl.Rectangle(10 + 120 * 2, 10, 100, 40), "A-Star"):
            path = pathfind_astar(grid)
            path_index = 0

        if path is not None and path_index + 1 != len(path) and rl.gui_button(
                rl.Rectangle(SCREEN_WIDTH - 120 * 2, 10, 100, 40), "Next"):
            if path_index + 1 < len(path):
                path_index += 1
            grid.robot_sprite.pos = rl.Vector2(path[path_index][0] * grid.square_size(),
                                               path[path_index][1] * grid.square_size())

        if path is not None and rl.gui_button(rl.Rectangle(SCREEN_WIDTH - 120, 10, 100, 40), "Clear"):
            path = None

        rl.clear_background(rl.Color(252, 251, 251, 255))
        grid.draw_background()
        if path is not None:
            for i in range(len(path) - 1):
                rl.draw_line_ex(rl.Vector2(path[i][0] * grid.square_size() + grid.square_size() / 2 + grid_offset_x,
                                           path[i][1] * grid.square_size() + grid.square_size() / 2 + grid_offset_y),
                                rl.Vector2(path[i + 1][0] * grid.square_size() + grid.square_size() / 2 + grid_offset_x,
                                           path[i + 1][
                                               1] * grid.square_size() + grid.square_size() / 2 + grid_offset_y), 8,
                                rl.Color(198, 120, 221, 255))
        grid.draw_items()
        rl.end_drawing()


if __name__ == '__main__':
    main()
