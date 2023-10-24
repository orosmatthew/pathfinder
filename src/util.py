import pyray as rl


class Sprite:
    def __init__(self, texture: rl.Texture, pos: rl.Vector2):
        self.texture = texture
        self.pos = pos
        self.moving = False

    def draw(self):
        rl.draw_texture(self.texture, round(self.pos.x), round(self.pos.y), rl.WHITE)
