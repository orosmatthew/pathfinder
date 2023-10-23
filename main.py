import pyray as rl

GRID_SIZE = 800
GRID_COUNT = 16
GRID_SQUARE_SIZE = GRID_SIZE // GRID_COUNT


def draw_grid(size: int, padding: int, color: rl.Color):
    screen_width = rl.get_screen_width()
    screen_height = rl.get_screen_height()
    for x in range(size):
        for y in range(size):
            size_x = screen_width // size
            size_y = screen_height // size
            rl.draw_rectangle(x * size_x + padding, y * size_y + padding,
                              size_x - padding * 2, size_y - padding * 2, color)


def world_to_grid(pos: rl.Vector2) -> tuple[int, int]:
    return int(pos.x // (800 // GRID_COUNT)), int(pos.y // (800 // GRID_COUNT))


class Sprite:
    def __init__(self, texture: rl.Texture, pos: rl.Vector2):
        self.texture = texture
        self.pos = pos
        self.moving = False

    def update(self):
        if not self.moving and (rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT) and
                                world_to_grid(rl.get_mouse_position()) == self.pos):
            self.moving = True
        elif self.moving and rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
            self.moving = False
            self.pos = world_to_grid(rl.get_mouse_position())

    def draw(self):
        if self.moving:
            rl.draw_texture(self.texture,
                            int(rl.get_mouse_x() - GRID_SQUARE_SIZE / 2),
                            int(rl.get_mouse_y() - GRID_SQUARE_SIZE / 2),
                            rl.WHITE)
        else:
            rl.draw_texture(self.texture, int(self.pos.x), int(self.pos.y), rl.WHITE)


def main():
    rl.init_window(800, 800, "Pathfinder")
    rl.set_target_fps(60)

    robot_img = rl.load_image("./res/robot.png")
    rl.image_resize(robot_img, 800 // GRID_COUNT, 800 // GRID_COUNT)
    robot_tex = rl.load_texture_from_image(robot_img)

    finish_img = rl.load_image("./res/finish.png")
    rl.image_resize(finish_img, 800 // GRID_COUNT, 800 // GRID_COUNT)
    finish_tex = rl.load_texture_from_image(finish_img)

    robot = Sprite(robot_tex, rl.Vector2(0, 0))
    finish = Sprite(finish_tex, rl.Vector2(GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))

    while not rl.window_should_close():
        robot.update()
        finish.update()

        rl.begin_drawing()
        rl.clear_background(rl.Color(252, 251, 251, 255))
        draw_grid(size=GRID_COUNT, padding=2, color=rl.Color(221, 213, 213, 255))
        finish.draw()
        robot.draw()

        rl.end_drawing()


if __name__ == '__main__':
    main()
