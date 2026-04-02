from settings import * 
from sprites import *
from groups import *
from assets import Assets
from timer import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        #asset loader
        self.assets = Assets()

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #load game
        self.load_assets()
        self.setup()

        #timers
        self.bee_timer = Timer(1000, func = self.create_bee, autostart = True, repeat = True)
        
    def create_bee(self):
        Bee(((randint(300, 600)), (randint(300, 600))), self.assets.load_asset('Bee'), (self.all_sprites, self.enemy_sprites))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 33 if direction == 1 else pos[0] + direction * 33 - self.assets.load_asset('Bullet').get_width()
        Bullet(self.assets.load_asset('Bullet'), (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.assets.load_asset('Fire'), pos, self.all_sprites, self.player)

    def load_assets(self):
        #graphicss
        self.assets.import_folder('Player', 'Platform', 'images', 'player')          # player
        self.assets.import_image('Bullet', 'Platform', 'images', 'gun', 'bullet')    # Bullet 
        self.assets.import_image('Fire', 'Platform', 'images', 'gun', 'fire')        # Fire
        self.assets.import_folder('Bee', 'Platform', 'images', 'enemies', 'bee')     # Bee
        self.assets.import_folder('Worm', 'Platform', 'images', 'enemies', 'worm')   # worm
        
        #sounds
        self.assets.import_audio('Hit', 'ogg' 'Platform', 'audio', 'impact')         # Hit 
        self.assets.import_audio('Shoot', 'ogg' 'Platform', 'audio', 'Shoot')        # Shoot
        self.assets.import_audio('Music', 'ogg' 'Platform', 'audio', 'music')        # Music

    def setup(self):
        tmx_map = load_pygame(join('Platform', 'data', 'maps', 'world.tmx'))

        for x, y, image, in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image, in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.assets.load_asset('Player'), self.create_bullet)

        Worm((700, 600), self.assets.load_asset('Worm'), (self.all_sprites, self.enemy_sprites))


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)

            # draw 
            self.window.fill(BG_COLOR)
            self.all_sprites.draw(self.window, self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 