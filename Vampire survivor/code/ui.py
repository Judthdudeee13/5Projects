from settings import *

class GameOver:
    def __init__(self, player, window):
        self.player = player
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 150))
        self.rect = self.image.get_frect(topleft = (0,0))
        self.window = window
        self.is_game_over = False

    def game_over(self):
        if not self.is_game_over:
            self.window.blit(self.image, self.rect)
            self.is_game_over = True