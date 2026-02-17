#video 4:42:00
from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from assets import AssetManager

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mouse.set_visible(False)

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.spawn_postitions = []

        self.load_images()
        self.set_up()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.gun.can_shoot:
            Bullet(self.gun, (self.all_sprites, self.bullet_sprites), self.assets.get('Gun')['bullet'][0], self.collision_sprites, self.enemy_sprites)
            self.gun.shoot()
            
    def set_up(self):
        map = load_pygame(join('vampire survivor', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y*TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollsionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollsionSprite((obj.x, obj.y), pygame.surface.Surface((obj.width, obj.height)), (self.collision_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.assets.get('Player'))
                self.gun = Gun(self.player, self.all_sprites, self.assets.get('Gun'))

            if obj.name == 'Enemy':
                self.spawn_postitions.append((obj.x, obj.y))

    def load_images(self):
        self.assets = AssetManager()
        self.assets.load_images(join('Vampire survivor', 'images', 'player'), 'Player')
        self.assets.load_images(join('Vampire survivor', 'images', 'gun'), 'Gun')
        self.assets.load_images(join('Vampire survivor', 'images', 'enemies'), 'Enemies')

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == self.enemy_event:
                    Enemy(random.choice(self.spawn_postitions), self.assets.get('Enemies'), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites)
                
                

            #updatew
            self.input()
            self.all_sprites.update(dt)
                    
            #draw
            self.window.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()