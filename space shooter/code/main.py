#video 2:00:00
import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
run = True
clock = pygame.time.Clock()

#plain surface
surface = pygame.Surface((100, 200))
surface.fill("orange")
x = 100

player = Player()

# imports
# player_surface = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
# player_rect = player_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
# player_direction = pygame.math.Vector2()
# player_speed = 300

star_surface = pygame.image.load(join("space shooter", 'images', 'star.png')).convert_alpha()
star_postitions = [(randint(0, WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)) for i in range(20)]

meteor_surface = pygame.image.load(join("space shooter", 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surface = pygame.image.load(join("space shooter", 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT-20))



while run:
    dt = clock.tick() / 1000
    #eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #input
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    # player_direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_direction * player_speed * dt

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print("Fire Laser")


    #draw the game
    window.fill("darkgray")
    for pos in star_postitions:
        window.blit(star_surface, pos)

    window.blit(meteor_surface, meteor_rect)
    window.blit(laser_surface, laser_rect)
    #window.blit(player_surface, player_rect)


    pygame.display.flip()


pygame.quit()
    