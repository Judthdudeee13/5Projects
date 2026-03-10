from settings import * 
from sprites import *

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()


        #groups
        self.all_sprites = pygame.sprite.Group()

        #variables
        self.running = True

        #sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        self.player = Player((self.all_sprites, self.paddle_sprites), POS['player'])

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            #update
            self.all_sprites.update(dt)
            
            #draw
            self.window.fill(COLORS['bg'])
            self.all_sprites.draw(self.window)
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
