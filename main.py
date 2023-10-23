import pyray as rl

GRID_SIZE = 800
GRID_COUNT = 16
GRID_SQUARE_SIZE = GRID_SIZE // GRID_COUNT


def draw_grid(size: int, padding: int, color: rl.Color):
    for x in range(size):
        for y in range(size):
            size_x = GRID_SIZE // size
            size_y = GRID_SIZE // size
            rl.draw_rectangle(x * size_x + padding, y * size_y + padding,
                              size_x - padding * 2, size_y - padding * 2, color)


def world_to_grid(pos: rl.Vector2) -> tuple[int, int]:
    return int(pos.x // GRID_SQUARE_SIZE), int(pos.y // GRID_SQUARE_SIZE)


class Sprite:
    def __init__(self, texture: rl.Texture, pos: rl.Vector2):
        self.texture = texture
        self.pos = pos
        self.moving = False

    def draw(self):
        rl.draw_texture(self.texture, round(self.pos.x), round(self.pos.y), rl.WHITE)


class MovableHandler:
    def __init__(self):
        self.moving_item: Sprite | None = None

    def handle(self, movable_items: list[Sprite]):
        if self.moving_item is None and rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            for item in reversed(movable_items):
                if world_to_grid(item.pos) == world_to_grid(rl.get_mouse_position()):
                    self.moving_item = item
                    break

        if self.moving_item is not None and rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
            clamped_mouse_pos = rl.vector2_clamp(rl.get_mouse_position(),
                                                 rl.Vector2(GRID_SQUARE_SIZE / 2, GRID_SQUARE_SIZE / 2),
                                                 rl.Vector2(GRID_SIZE - GRID_SQUARE_SIZE / 2,
                                                            GRID_SIZE - GRID_SQUARE_SIZE / 2))
            grid_pos = world_to_grid(clamped_mouse_pos)
            self.moving_item.pos = rl.Vector2(grid_pos[0] * GRID_SQUARE_SIZE, grid_pos[1] * GRID_SQUARE_SIZE)
            self.moving_item = None

        if self.moving_item is not None:
            clamped_mouse_pos = rl.vector2_clamp(rl.get_mouse_position(),
                                                 rl.Vector2(GRID_SQUARE_SIZE / 2, GRID_SQUARE_SIZE / 2),
                                                 rl.Vector2(GRID_SIZE - GRID_SQUARE_SIZE / 2,
                                                            GRID_SIZE - GRID_SQUARE_SIZE / 2))
            self.moving_item.pos = rl.vector2_subtract(clamped_mouse_pos,
                                                       rl.Vector2(GRID_SQUARE_SIZE / 2, GRID_SQUARE_SIZE / 2))


def main():
    rl.init_window(800, 800, "Pathfinder")
    rl.set_target_fps(60)

    robot_img = rl.load_image("./res/robot.png")
    rl.image_resize(robot_img, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)
    robot_tex = rl.load_texture_from_image(robot_img)

    finish_img = rl.load_image("./res/finish.png")
    rl.image_resize(finish_img, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)
    finish_tex = rl.load_texture_from_image(finish_img)

    robot = Sprite(robot_tex, rl.Vector2(0, 0))
    finish = Sprite(finish_tex, rl.Vector2(GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))

    movable_handler = MovableHandler()
    movable_items: list[Sprite] = [finish, robot]

    while not rl.window_should_close():
        movable_handler.handle(movable_items)
        rl.begin_drawing()
        rl.clear_background(rl.Color(252, 251, 251, 255))
        draw_grid(size=GRID_COUNT, padding=2, color=rl.Color(221, 213, 213, 255))
        for item in movable_items:
            item.draw()
        rl.end_drawing()


if __name__ == '__main__':
    main()
