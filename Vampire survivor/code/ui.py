from settings import *

class GameOver:
    def __init__(self, player, window, assets):
        self.player = player
        self.bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.bg.fill((255, 0, 0, 150))
        self.rect = self.bg.get_frect(topleft = (0,0))
        self.window = window
        self.is_game_over = False
        self.font = assets.get_font('Game Over')
        self.messages = ['Game Over']
        self.images  = assets.get('Game Over')['Game Over']

    def button(self):
        self.image = self.images[0]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 25*SCALE))
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.images[1]
        if pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

    def restart(self):
        if self.button():
            self.player.restart()
            pygame.mouse.set_visible(False)
            

    def text(self):
        font = self.font.render(random.choice(self.messages), True, (0, 0, 0))
        rect = font.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2-(100*SCALE)))
        self.window.blit(font, rect)

    def game_over(self):
        if not self.is_game_over:
            self.window.blit(self.bg, self.rect)
            self.is_game_over = True
            self.text()
            pygame.mouse.set_visible(True)
        self.restart()
        self.window.blit(self.image, self.rect)
        
        