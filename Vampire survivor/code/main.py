#video 4:42:00
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame

from random import randint
class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.set_up()

        # sprites
        self.player = Player((400, 300), self.all_sprites, self.collision_sprites)
        

    def set_up(self):
        map = load_pygame(join('vampire survivor', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y*TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            Collsion_sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            Collsion_sprite((obj.x, obj.y), pygame.surface.Surface((obj.width, obj.height)), (self.collision_sprites))
        
        

        

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #update
            self.window.fill('black')
            self.all_sprites.update(dt)
                    
            #draw
            self.all_sprites.draw(self.window)
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()