import pygame
from animatronic import Animatronic
from door import Door

# Init window/meta-game stuff
map = pygame.image.load('map.png')
gameStarted = False



# Initialize waypoints and animatronic
waypoints = [(100, 100), (700, 100), (700, 500), (100, 500)]
anim = Animatronic(100, 100, waypoints)
doors = [
    Door(362, 542, 7, 33, "Left door"),
    Door(448, 542, 7, 33, "Right door"),
]

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
        elif gameStarted:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                doors[1].toggle()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                doors[0].toggle()

    # Clear screen
    screen.fill((0, 0, 0))

    if not gameStarted:  # Menu
        # menu with title and instructions
        font_title = pygame.font.SysFont(None, 64)
        font_instr = pygame.font.SysFont(None, 36)
        title_surf = font_title.render("FNAF Clone", True, (255,255,255)) # WORKING TITLE
        instr_surf = font_instr.render("Press ENTER to Start", True, (255,255,255))

        # Center title and instruction on screen
        title_rect = title_surf.get_rect(center=(400, 200))
        instr_rect = instr_surf.get_rect(center=(400, 300))

        screen.blit(title_surf, title_rect)
        screen.blit(instr_surf, instr_rect)
    else:  # Gameplay
        screen.blit(map, (0,0))

        for door in doors:
            door.draw(screen)


    # Update display
    pygame.display.flip()

pygame.quit()
