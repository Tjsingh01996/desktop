import pygame
import numpy as np
from pygame.locals import *

running = True
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.init()

def render():
    pygame.draw.line(screen, (255, 255, 255), [0,0], [200,-600]) # Clear the screen with black
    pygame.display.update()
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
    render()
    
    


pygame.quit()
