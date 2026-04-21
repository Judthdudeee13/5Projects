from settings import *

class UI:
    def __init__(self, monster, player_monsters, simple_surfs, get_input):
        self.window = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT / 2 +50
        self.monster = monster
        self.get_input = get_input

        # control
        self.general_options = ['attack', 'heal', 'switch', 'escape']
        self.general_index = {'col': 0, 'row': 0}
        self.attack_index = {'col': 0, 'row': 0}
        self.switch_index = 0
        self.state = 'general'
        self.rows, self.cols = 2, 2
        self.visable_monsters = 4
        self.player_monsters = player_monsters
        self.availible_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]

        #images
        self.simple_surfs = simple_surfs

    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == 'general':
            self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_s]) - int(keys[pygame.K_w])) % self.rows
            self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_d]) - int(keys[pygame.K_a])) % self.cols
            if keys[pygame.K_SPACE]:
                self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]

        elif self.state == 'attack':
            self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_s]) - int(keys[pygame.K_w])) % self.rows
            self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_d]) - int(keys[pygame.K_a])) % self.cols
            if keys[pygame.K_SPACE]:
                attack = self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2]
                self.get_input(self.state, attack)
                self.state = 'general'
                
        
        elif self.state == 'switch':
            self.switch_index = (self.switch_index + int(keys[pygame.K_s]) - int(keys[pygame.K_w])) % len(self.availible_monsters)
            if keys[pygame.K_SPACE]:
                self.get_input(self.state, self.availible_monsters[self.switch_index])
                self.state = 'general'

        elif self.state == 'heal':
            self.get_input('heal')
            self.state = 'general'
        
        elif self.state == 'escape':
            self.get_input('escape')
            
                

        if keys[pygame.K_LSHIFT]:
            self.general_index = {'col': 0, 'row': 0}
            self.attack_index = {'col': 0, 'row': 0}
            self.switch_index = 0
            self.state = 'general'

    def quad_select(self, index, options):
        # bg
        rect = pygame.FRect(self.left +40, self.top +60, 400, 200)
        pygame.draw.rect(self.window, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.window, COLORS['gray'], rect, 4, 4)
        #menu
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left +rect.width/ (self.cols*2) +(rect.width / self.cols) * col
                y = rect.top +rect.height/ (self.rows*2) +(rect.height / self.rows) * row
                i = col + 2 * row
                color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']

                text_surf = self.font.render(options[i], True, color)
                text_rect = text_surf.get_frect(center = (x,y))
                self.window.blit(text_surf, text_rect)

    def switch(self):
        #bg
        rect = pygame.FRect(self.left+40, self.top - 140, 400, 400)
        pygame.draw.rect(self.window, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.window, COLORS['gray'], rect, 4, 4)
        
        #menu
        v_offset = 0 if self.switch_index < self.visable_monsters else -(self.switch_index -self.visable_monsters + 1) * rect.height / self.visable_monsters
        for i in range(len(self.availible_monsters)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visable_monsters * 2) + rect.height / self.visable_monsters * i + v_offset

            color = COLORS['gray'] if i == self.switch_index else COLORS['black']

            name = self.availible_monsters[i].name

            simple_surf = self.simple_surfs[name]
            simple_rect =  simple_surf.get_frect(center = (x - 100, y))

            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_frect(midleft = (x,y))

            if rect.collidepoint(text_rect.center):
                self.window.blit(text_surf, text_rect)
                self.window.blit(simple_surf, simple_rect)
            

    def update(self):
        self.input()

    def draw(self):
        match self.state:
            case 'general' : self.quad_select(self.general_index, self.general_options)
            case 'attack' : self.quad_select(self.attack_index, self.monster.abilities)
            case 'switch' : self.switch()