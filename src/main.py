import pyray as rl

from grid import Grid


def main():
    rl.init_window(800, 800, "Pathfinder")
    rl.set_target_fps(60)

    grid = Grid(grid_size=800, grid_count=16)

    while not rl.window_should_close():
        grid.update()
        rl.begin_drawing()
        rl.clear_background(rl.Color(252, 251, 251, 255))
        grid.draw()
        rl.end_drawing()


if __name__ == '__main__':
    main()
