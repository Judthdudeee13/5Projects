#video 3:20:00
import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image =  pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        #cool down
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        

    def laser(self):
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def move(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize() 
        self.rect.center += self.direction * self.speed * dt 


    def update(self, dt):
        self.move(dt)
        self.laser()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 400

    def update(self, dt):
        self.rect.centery -= self.speed *dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        pos = randint(0, WINDOW_WIDTH), randint(-200, -100)
        self.rect = self.image.get_frect(center = pos)
        self.speed = randint(400, 500)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()

def collisions():
    global run
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        run = False
    for laser in laser_sprites:
        meteors = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if meteors:
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks()// 100
    text_surface = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surface.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-50))
    window.blit(text_surface, text_rect)
    box_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(window, (240, 240, 240), box_rect.move(0, -8), 5, 10)
    

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
run = True
clock = pygame.time.Clock()

#import
meteor_surface = pygame.image.load(join("space shooter", 'images', 'meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join("space shooter", 'images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join("space shooter", 'images', 'star.png')).convert_alpha()
font = pygame.font.Font(join('Space Shooter','images', 'Oxanium-Bold.ttf'), 40)


#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> metor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


while run:
    dt = clock.tick() / 1000
    #eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == meteor_event:
            Meteor(meteor_surface, (all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)
    collisions()

    #draw the game
    window.fill("#3a2e3f")
    all_sprites.draw(window)
    display_score()

    pygame.display.flip()


pygame.quit()