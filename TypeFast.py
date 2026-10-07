import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        # pygame.QUIT means the user clicked X to close the window
        if event.type == pygame.QUIT: 
                running = False

screen.fill("black")

pygame.display.flip()

clock.tick(60)

pygame.quit()