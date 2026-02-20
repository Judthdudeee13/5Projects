from settings import *
from assets import AssetManager

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, images):
        super().__init__(groups)
        #images
        self.frames = images
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500 *SCALE

        # grops
        self.collision_sprites = collision_sprites

        #health
        self.is_alive = True
        self.health = 100


    def recive_damage(self, damage):
        self.health -= damage

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def animate(self, dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        #animate
        if self.direction:
            self.frame_index += 7 * dt
        else:
            self.frame_index = 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        if self.health <= 0:
            self.is_alive = False

class Health(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.image = pygame.Surface((10*SCALE, 100*SCALE))
        self.rect = self.health_bar.get_frect(bottomright = (WINDOW_WIDTH-10*SCALE, WINDOW_HEIGHT-10*SCALE))

    def update(self, dt):
        self.image = pygame.transform.scale(self.image, (-1*SCALE, 0))