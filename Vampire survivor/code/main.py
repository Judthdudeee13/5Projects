#video 4:42:00
from settings import *
from player import *
from sprites import *
from groups import AllSprites
from ui import *
from pytmx.util_pygame import load_pygame
from assets import AssetManager

class Game:
    def __init__(self):
        #setup
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mouse.set_visible(False)

        #groups
        self.all_sprites = AllSprites()
        self.ui = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.spawn_postitions = []

        self.load_images()
        self.load_audio()
        self.load_fonts()
        self.assets.play_music()
        self.set_up()

        self.Game_over = GameOver(self.player, self.window, self.assets)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.gun.can_shoot:
            Bullet(self.gun, (self.all_sprites, self.bullet_sprites), self.assets.get('Gun')['bullet'][0], self.collision_sprites, self.enemy_sprites)
            self.gun.shoot()
            self.assets.play_audio('Shoot')
            
    def set_up(self):
        map = load_pygame(join('vampire survivor', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            scaled_image = pygame.transform.scale(image,(int(image.get_width() * SCALE), int(image.get_height() * SCALE)))
            Sprite((x * TILE_SIZE *SCALE,y*TILE_SIZE*SCALE), scaled_image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            scaled_image = pygame.transform.scale(obj.image,(int(obj.image.get_width() * SCALE), int(obj.image.get_height() * SCALE)))
            CollsionSprite((obj.x*SCALE, obj.y*SCALE), scaled_image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollsionSprite((obj.x*SCALE, obj.y*SCALE), pygame.surface.Surface((obj.width*SCALE, obj.height*SCALE)), (self.collision_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x*SCALE, obj.y*SCALE), self.all_sprites, self.collision_sprites, self.assets.get('Player'))
                self.gun = Gun(self.player, self.all_sprites, self.assets.get('Gun'))
                self.health_bar = Health(self.ui, self.player)

            if obj.name == 'Enemy':
                self.spawn_postitions.append((obj.x*SCALE, obj.y*SCALE))

    def load_images(self):
        self.assets = AssetManager()
        self.assets.load_images(join('Vampire survivor', 'images', 'player'), 'Player')
        self.assets.load_images(join('Vampire survivor', 'images', 'gun'), 'Gun')
        self.assets.load_images(join('Vampire survivor', 'images', 'enemies'), 'Enemies')
        self.assets.load_images(join('Vampire survivor', 'images', 'buttons'), 'Game Over')

    def load_audio(self):
        self.assets.load_audio(join('Vampire survivor', 'audio', 'impact.ogg'), 100, 'Hit')
        self.assets.load_audio(join('Vampire survivor', 'audio', 'shoot.wav'), 25, 'Shoot')
        self.assets.load_music(join("Vampire survivor", "Audio", "music_epic.mp3"))

    def load_fonts(self):
        self.assets.load_font(join('Vampire survivor', 'data', 'fonts', 'PressStart2p.ttf'), 'Game Over', 100)

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
                        self.running = False

                if event.type == self.enemy_event and self.player.is_alive:
                    Enemy(random.choice(self.spawn_postitions), self.assets.get('Enemies'), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites, self.bullet_sprites, self.assets.play_audio)
            if self.player.is_alive:
                #updatew
                self.input()
                self.all_sprites.update(dt)
                self.ui.update(dt)
                        
                #draw
                self.all_sprites.draw(self.player.rect.center)
                self.ui.draw(self.window)
            else:
                self.Game_over.game_over()
                for sprite in self.enemy_sprites:
                    sprite.kill()
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()