import pygame
import random
from animatronic import Animatronic
from door import Door
from camera import Camera, CameraManager
from conditions import GameConditions, Controls
from power import Power

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("FNAF Horror")
clock = pygame.time.Clock()

# Game state
#Menu = 0
#In game = 1
#Lose screen = 2
#Win screen = 3
gameState = 0
gameConditions = GameConditions()
power = Power()

# Assets
mapImage = pygame.image.load('map.png')
mapImageCropped = mapImage.subsurface(pygame.Rect(200, 0, mapImage.get_width() - 200, mapImage.get_height())) #move to the left

# Game objects 
waypointsFreddy = [(-40, 100), (60, 100), (60, 200), (-40, 200)]
waypointsBonnie = [(560, 100), (560, 200), (460, 200), (460, 100)]
waypointsChica = [(560, 500), (460, 500), (460, 400), (560, 400)]
waypointsFoxy = [(-40, 500), (60, 500), (60, 400), (-40, 400)]
animatronics = [
    Animatronic(-40, 100, waypointsFreddy, (139, 69, 19)),
    Animatronic(60, 100, waypointsBonnie, (75, 0, 130)),
    Animatronic(160, 100, waypointsChica, (255, 255, 0)),
    Animatronic(260, 100, waypointsFoxy, (255, 0, 0)),
]
doors = [
    Door(222, 542, 7, 33, "Left door"),
    Door(308, 542, 7, 33, "Right door"),
]
cameras = [
    
    Camera(195, 438, 145, 148, "Office"),
    Camera(60, 7, 290, 285, "Atrium"),
    Camera(347, 45, 100, 125, "Back Room 1"),
    Camera(347, 170, 150, 152, "Back Room 2"),
    Camera(99, 467, 100, 120, "Office Left"),
    Camera(339, 467, 100, 120, "Office Right"),
    Camera(339, 319, 100, 150, "Office Upper Right"),
    Camera(99, 289, 100, 180, "Office Upper Left"),
]

cameraMgr = CameraManager(cameras)
controls = Controls(cameras)
def handleMenuInput(event):
    global gameState
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        gameState = 1 # now in game

def handleGameInput(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        camera_index = controls.getClickedCamera(event.pos)
        if camera_index is not None:
            cameraMgr.switchCamera(camera_index)
        door_index = controls.getClickedDoor(event.pos)
        if door_index is not None:
            doors[door_index].toggle()
            if door_index == 0:
                power.isLeftDoorInUse = doors[0].locked
            elif door_index == 1:
                power.isRightDoorInUse = doors[1].locked

def drawMenu():
    global fontTitle, fontInstr
    fontTitle = pygame.font.SysFont(None, 64)
    fontInstr = pygame.font.SysFont(None, 36)
    title = fontTitle.render("FNAF Clone", True, (255, 255, 255))
    instr = fontInstr.render("Press ENTER to Start", True, (255, 255, 255))
    
    screen.blit(title, title.get_rect(center=(450, 200)))
    screen.blit(instr, instr.get_rect(center=(450, 300)))

def drawGame():
    screen.blit(mapImageCropped, (60, 0))

    pygame.draw.rect(screen, (100, 100, 100), (500, 0, 5, 600)) # divider
    
    for door in doors:
        door.draw(screen)

    for anim in animatronics:
        anim.draw(screen)
        if cameraMgr.isVisible(anim.x, anim.y):
            anim.draw(screen)

    camText = fontInstr.render(cameraMgr.activeCamera.name, True, (255, 255, 255))
    screen.blit(camText, camText.get_rect(topright = (880, 10)))

    # add time display
    timeText = fontInstr.render(gameConditions.getFormattedTime(), True, (255, 255, 255))
    screen.blit(timeText, timeText.get_rect(topleft = (520, 10)))

    # add power display
    powerText = fontInstr.render(f"{power.currentPower:.1f}%", True, (255, 255, 255))
    screen.blit(powerText, powerText.get_rect(topleft = (520, 500)))

    cameraMgr.drawDarkness(screen)
    controls.draw(screen)

def evalMvmtOpportunity(anim):
    check = anim.betweenTimeCounter()

    if check == True: # hit mvmt opportunity, now roll dice to check if we succeed
        roll = anim.rollDie(5) #hardcode for now
        if roll:
            return True
    return False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif gameState == 0: #menu
            handleMenuInput(event)
        elif gameState == 1: #game
            handleGameInput(event)
    
    if gameState == 1: #game
        if gameConditions.currentFrame % 60 == 0:
            power.losePower()
        
        for anim in animatronics:
            if evalMvmtOpportunity(anim):
                anim.moveToWaypoint()

        if gameConditions.hasWon() == False:
            gameConditions.incrFrameCt()         
        # Every 30 seconds (1800 frames at 60fps), print in-game time
            if gameConditions.currentFrame % 1800 == 0:
                print("In-game time:", gameConditions.getFormattedTime())
        else:
            print('clock that tea')
    
    # Draw
    screen.fill((0, 0, 0))
    if gameState == 0:
        drawMenu()
    elif gameState == 1:
        drawGame()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()