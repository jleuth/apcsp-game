import pygame
from animatronic import Animatronic
from door import Door
from camera import Camera, CameraManager

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
cameras = [
    Camera(200, 7, 290, 285, "Atrium"),
    Camera(487, 45, 100, 125, "Back Room 1"),
    Camera(487, 170, 150, 152, "Back Room 2"),
    Camera(239, 467, 100, 120, "Office Left"),
    Camera(479, 467, 100, 120, "Office Right"),
    Camera(479, 319, 100, 150, "Office Upper Right"),
    Camera(239, 289, 100, 180, "Office Upper Left"),
]

cameraMgr = CameraManager(cameras)
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
        elif pygame.K_1 <= event.key <= pygame.K_9:
            cameraMgr.switchCamera(event.key - pygame.K_1)

def drawMenu():
    global fontTitle, fontInstr
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

    if cameraMgr.isVisible(anim.x, anim.y):
        anim.draw(screen)

    currentCam = fontInstr.render("Current camera:", True, (255, 255, 255))
    camName = fontInstr.render(cameraMgr.activeCamera.name, True, (255, 255, 255))
    screen.blit(currentCam, currentCam.get_rect(center = (100, 550)))
    screen.blit(camName, camName.get_rect(center = (115, 580)))

    cameraMgr.drawDarkness(screen)

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