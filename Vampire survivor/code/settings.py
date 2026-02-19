import pygame 
from os.path import join 
from os import walk
from math import atan2, degrees
import random

pygame.init()

ASPECT_WIDTH, ASPECT_HEIGHT = 1280,720 
TILE_SIZE = 64

ASPECT_RATIO = ASPECT_WIDTH/ASPECT_HEIGHT

SIZE = pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT = SIZE.current_w, SIZE.current_h

WINDOW_ASSPECT_RATIO = WINDOW_WIDTH /WINDOW_HEIGHT

SCALE_X = WINDOW_WIDTH / ASPECT_WIDTH
SCALE_Y = WINDOW_HEIGHT / ASPECT_HEIGHT

SCCALE = SCALE = min(SCALE_X, SCALE_Y)
pygame.quit()