import pygame
from animatronic import Animatronic

# Init window/meta-game stuff
map = pygame.image.load('map.png')
gameStarted = False



# Initialize waypoints and animatronic
waypoints = [(100, 100), (700, 100), (700, 500), (100, 500)]
anim = Animatronic(100, 100, waypoints)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Window")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not gameStarted:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                gameStarted = True

    # Clear screen
    screen.fill((0, 0, 0))

    if not gameStarted:  # Menu
        pass  # (Draw menu here if desired)
    else:  # Gameplay
        screen.blit(map, (0,0))

    # Update display
    pygame.display.flip()

pygame.quit()
