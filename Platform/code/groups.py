from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Vector2()

    def draw(self, window, targot_pos):
        self.offset.x = -(targot_pos[0] - WINDOW_WIDTH/2)
        self.offset.y = -(targot_pos[1] - WINDOW_HEIGHT/2)

        for sprite in self:
            window.blit(sprite.image, sprite.rect.topleft + self.offset)