from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
    def draw(self, display_surface):
        for sprite in self:
            for i in range(5):
                display_surface.blit(sprite.shadow_surf, sprite.rect.topleft + pygame.Vector2(i, i))

        for sprite in self:
            display_surface.blit(sprite.image, sprite.rect)
