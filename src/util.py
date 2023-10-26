import pyray as rl


class Sprite:
    def __init__(self, texture: rl.Texture, pos: rl.Vector2):
        self.texture = texture
        self.pos = pos
        self.moving = False

    def draw(self, offset_x=0, offset_y=0):
        rl.draw_texture(self.texture, round(self.pos.x) + offset_x, round(self.pos.y) + offset_y, rl.WHITE)
