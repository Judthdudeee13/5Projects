from settings import *

class GameOver:
    def __init__(self, player, window, assets):
        self.player = player
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 150))
        self.rect = self.image.get_frect(topleft = (0,0))
        self.window = window
        self.is_game_over = False
        self.font = assets.get_font('Game Over')
        self.messages = ['Game Over']

    def text(self):
        font = self.font.render(random.choice(self.messages), True, (0, 0, 0))
        rect = font.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2-(100*SCALE)))
        self.window.blit(font, rect)

    def game_over(self):
        if not self.is_game_over:
            self.window.blit(self.image, self.rect)
            self.is_game_over = True
            self.text()
        
        