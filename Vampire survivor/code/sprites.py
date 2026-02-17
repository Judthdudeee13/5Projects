from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollsionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups, image):
        #player connection 
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1, 0)

        # sprite setup
        super().__init__(groups)
        self.gun_surf = image['gun'][0]
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        self.can_shoot = True
        self.shoot_time = 0
        self.cool_down = 100

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos-player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cool_down:
                self.can_shoot = True
    
    def shoot(self):
        self.shoot_time = pygame.time.get_ticks()
        self.can_shoot = False

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.timer()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun, groups, image, collision_sprites):
        self.gun = gun
        super().__init__(groups)
        self.direction = self.gun.player_direction
        self.speed = 1200
        self.bullet_surf = image
        angle = degrees(atan2(self.direction.x, self.direction.y))
        self.image = pygame.transform.rotozoom(self.bullet_surf, angle, 1)
        pos = self.gun.rect.center + self.direction * 50
        self.rect = self.image.get_frect(center = pos)

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2000
        self.collision_sprites = collision_sprites

    def update(self, dt):
        self.rect.center += self.direction*self.speed*dt

        for collision_sprite in self.collision_sprites:
            if self.rect.colliderect(collision_sprite.rect):
                self.kill()

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemies, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        types = ['bat', 'blob', 'skeleton']
        frames = enemies[random.choice(types)]

        #image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350

    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
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
        #animate
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.move(dt)
        self.animate(dt)