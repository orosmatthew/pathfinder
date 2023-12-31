import pyray as rl
from enum import Enum

from util import Sprite


class Grid:
    class WallState(Enum):
        NONE = 0
        PLACING = 1
        REMOVING = 2

    def __init__(self, grid_size: int, grid_count: 16, draw_x_pos: int, draw_y_pos: int):
        self._grid_size = grid_size
        self._grid_count = grid_count
        self._draw_x_pos = draw_x_pos
        self._draw_y_pos = draw_y_pos

        self.moving_item: Sprite | None = None

        self.walls = [[False] * self._grid_count for _ in range(self._grid_count)]
        self.wall_state = Grid.WallState.NONE

        robot_img = rl.load_image("./res/robot.png")
        rl.image_resize(robot_img, self.square_size(), self.square_size())
        robot_tex = rl.load_texture_from_image(robot_img)

        finish_img = rl.load_image("./res/finish.png")
        rl.image_resize(finish_img, self.square_size(), self.square_size())
        finish_tex = rl.load_texture_from_image(finish_img)

        self.robot_sprite = Sprite(robot_tex, rl.Vector2(0, 0))
        self.finish_sprite = Sprite(finish_tex, rl.Vector2(self.square_size(), self.square_size()))

        self.movable_items: list[Sprite] = [self.finish_sprite, self.robot_sprite]

    def square_size(self) -> int:
        return self._grid_size // self._grid_count

    def world_to_grid(self, pos: rl.Vector2) -> tuple[int, int]:
        return int(pos.x // self.square_size()), int(pos.y // self.square_size())

    def _get_offset_mouse(self):
        return rl.vector2_subtract(rl.get_mouse_position(), rl.Vector2(self._draw_x_pos, self._draw_y_pos))

    def _clamped_mouse_position(self) -> rl.Vector2:
        return rl.vector2_clamp(self._get_offset_mouse(),
                                rl.Vector2(self.square_size() / 2, self.square_size() / 2),
                                rl.Vector2(self._grid_size - self.square_size() / 2,
                                           self._grid_size - self.square_size() / 2))

    def _cropped_mouse_position(self):
        mouse_pos = rl.get_mouse_position()
        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(self._draw_x_pos, self._draw_y_pos, self._grid_size,
                                                                self._grid_size)):
            return rl.vector2_subtract(mouse_pos, rl.Vector2(self._draw_x_pos, self._draw_y_pos))
        return None

    def _handle_movables(self):
        if self.moving_item is None and rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            for item in reversed(self.movable_items):
                if self.world_to_grid(item.pos) == self.world_to_grid(self._get_offset_mouse()):
                    self.moving_item = item
                    rl.set_mouse_cursor(rl.MouseCursor.MOUSE_CURSOR_POINTING_HAND)
                    break

        if self.moving_item is not None and rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
            grid_pos = self.world_to_grid(self._clamped_mouse_position())
            self.moving_item.pos = rl.Vector2(grid_pos[0] * self.square_size(), grid_pos[1] * self.square_size())
            self.moving_item = None
            rl.set_mouse_cursor(rl.MouseCursor.MOUSE_CURSOR_DEFAULT)

        if self.moving_item is not None:
            self.moving_item.pos = rl.vector2_subtract(self._clamped_mouse_position(),
                                                       rl.Vector2(self.square_size() / 2, self.square_size() / 2))

    def _handle_walls(self):
        if self.wall_state == Grid.WallState.NONE and rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            grid_pos = self.world_to_grid(self._get_offset_mouse())
            if not self.walls[grid_pos[0]][grid_pos[1]]:
                self.wall_state = Grid.WallState.PLACING
            elif grid_pos:
                self.wall_state = Grid.WallState.REMOVING

        if self.wall_state == Grid.WallState.PLACING:
            if rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
                self.wall_state = Grid.WallState.NONE
                return
            mouse = self._cropped_mouse_position()
            if mouse is not None:
                grid_pos = self.world_to_grid(mouse)
                self.walls[grid_pos[0]][grid_pos[1]] = True
        elif self.wall_state == Grid.WallState.REMOVING:
            if rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
                self.wall_state = Grid.WallState.NONE
                return
            mouse = self._cropped_mouse_position()
            if mouse is not None:
                grid_pos = self.world_to_grid(mouse)
                self.walls[grid_pos[0]][grid_pos[1]] = False

    def _draw_background(self, padding: int, color: rl.Color) -> None:
        for x in range(self._grid_count):
            for y in range(self._grid_count):
                rl.draw_rectangle(x * self.square_size() + padding + self._draw_x_pos,
                                  y * self.square_size() + padding + self._draw_y_pos,
                                  self.square_size() - padding * 2, self.square_size() - padding * 2, color)

    def _draw_walls(self):
        for x in range(self._grid_count):
            for y in range(self._grid_count):
                if self.walls[x][y]:
                    rl.draw_rectangle(x * self.square_size() + self._draw_x_pos,
                                      y * self.square_size() + self._draw_y_pos,
                                      self.square_size(), self.square_size(), rl.GRAY)

    def update(self):
        self._handle_movables()
        if not self.moving_item:
            self._handle_walls()

    def draw_background(self):
        self._draw_background(padding=2, color=rl.Color(221, 213, 213, 255))
        self._draw_walls()

    def draw_items(self):
        for sprite in self.movable_items:
            sprite.draw(self._draw_x_pos, self._draw_y_pos)

    def start_pos(self) -> tuple[int, int]:
        return self.world_to_grid(self.robot_sprite.pos)

    def end_pos(self) -> tuple[int, int]:
        return self.world_to_grid(self.finish_sprite.pos)

    def grid_count(self) -> int:
        return self._grid_count

    def in_bounds(self, square: tuple[int, int]) -> bool:
        return 0 <= square[0] < self._grid_count and 0 <= square[1] < self._grid_count

    def neighbors(self, square: tuple[int, int]) -> list[tuple[int, int]]:
        if not self.in_bounds(square):
            return []
        potential = [(square[0] + 1, square[1]), (square[0] - 1, square[1]),
                     (square[0], square[1] + 1), (square[0], square[1] - 1)]
        potential = [s for s in potential if self.in_bounds(s)]
        return [s for s in potential if not self.walls[s[0]][s[1]]]
