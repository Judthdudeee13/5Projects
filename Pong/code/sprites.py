from typing import Any
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        #image
        self.image = pygame.Surface(SIZE['paddle'])
        self.image.fill(COLORS['paddle'])

        #rect & movment
        self.rect = self.image.get_frect(center = pos)
        self.direction = 0

        self.speed = SPEED['player']

    def move(self, dt):
        self.rect.centery += self.direction *self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

    def update(self, dt):
        self.get_direction()
        self.move(dt)

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites):
        super().__init__(groups)


        #image
        self.image = pygame.Surface(SIZE['ball'])
        self.image.fill(COLORS['ball'])

        #rect
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, ))