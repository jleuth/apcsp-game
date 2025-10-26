import pygame
from animatronic import Animatronic
from door import Door

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FNAF Horror")
clock = pygame.time.Clock()

# Game state
gameStateMenu = 0
gameStateGame = 1
gameState = gameStateMenu

# Assets
mapImage = pygame.image.load('map.png')

# Game objects
waypoints = [(100, 100), (700, 100), (700, 500), (100, 500)]
anim = Animatronic(100, 100, waypoints)
doors = [
    Door(362, 542, 7, 33, "Left door"),
    Door(448, 542, 7, 33, "Right door"),
]

def handleMenuInput(event):
    global gameState
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        gameState = gameStateGame

def handleGameInput(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            doors[0].toggle()
        elif event.key == pygame.K_d:
            doors[1].toggle()

def drawMenu():
    fontTitle = pygame.font.SysFont(None, 64)
    fontInstr = pygame.font.SysFont(None, 36)
    title = fontTitle.render("FNAF Clone", True, (255, 255, 255))
    instr = fontInstr.render("Press ENTER to Start", True, (255, 255, 255))
    
    screen.blit(title, title.get_rect(center=(400, 200)))
    screen.blit(instr, instr.get_rect(center=(400, 300)))

def drawGame():
    screen.blit(mapImage, (0, 0))
    anim.draw(screen)
    for door in doors:
        door.draw(screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif gameState == gameStateMenu:
            handleMenuInput(event)
        elif gameState == gameStateGame:
            handleGameInput(event)
    
    # Update
    if gameState == gameStateGame:
        anim.moveToWaypoint()
    
    # Draw
    screen.fill((0, 0, 0))
    if gameState == gameStateMenu:
        drawMenu()
    elif gameState == gameStateGame:
        drawGame()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()