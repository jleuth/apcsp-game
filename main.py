import pygame
import random
import threading
from animatronic import Animatronic
from door import Door
from camera import Camera, CameraManager
from conditions import GameConditions, Controls
from power import Power
from ai import Eleven, OpenRouter
import cv2
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("FNAF Horror")
clock = pygame.time.Clock()

# Animatronic configuration
ANIMATRONICS = {
    "Freddy": {"voiceId": "H0UBSjjChzJlSBB61i5D", "fileKey": "freddy"},
    "Bonnie": {"voiceId": "PiE7En4dJh0s0VBPcv22", "fileKey": "bonnie"},
    "Chica": {"voiceId": "fRpr7OEGjVNEQNSEEuzC", "fileKey": "chica"},
    "Foxy": {"voiceId": "kcL2RMG6ULWtjU02cKAg", "fileKey": "foxy"}
}

# Game state
#Menu = 0
#In game = 1
#Lose screen = 2
#Win screen = 3
gameState = 0
gameConditions = GameConditions()
power = Power()
eleven = Eleven()
openrouter = OpenRouter()

# Voice line tracking
lastVoiceFrame = 0
voiceCooldown = random.randint(600, 1200)
batteryWarningGiven = False
doorBlockVoiceTriggered = False
closeVoiceTriggered = False
voiceQueue = []
currentlySpeaking = False

# Ambience
ambienceStarted = False

# Assets
mapImage = pygame.image.load('resources/map.png')
mapImageCropped = mapImage.subsurface(pygame.Rect(200, 0, mapImage.get_width() - 200, mapImage.get_height())) #move to the left

# Game objects 

waypointsFreddy = [
    (202, 120), (380, 121), (431, 235), (119, 142), (171, 349), (128, 513), (287, 544)
]

waypointsFoxy = [
    (300, 91), (405, 76), (417, 244), (361, 379), (362, 509), (287, 544)
]

waypointsBonnie = [
    (278, 183), (383, 142), (408, 273), (367, 385), (414, 564), (287, 544)
]

waypointsChica = [
    (213, 204), (189, 241), (174, 383), (143, 515), (287, 544)
]
animatronics = [
    Animatronic(210, 35, waypointsFreddy, (139, 69, 19)),
    Animatronic(250, 35, waypointsBonnie, (75, 0, 130)),
    Animatronic(290, 35, waypointsChica, (255, 255, 0)),
    Animatronic(325, 35, waypointsFoxy, (255, 0, 0)),
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
        cameraIndex = controls.getClickedCamera(event.pos)

        if cameraIndex is not None:
            cameraMgr.switchCamera(cameraIndex)
            if cameraMgr.activeCamera.name == 'Office':
                power.isCamInUse = False
                #print('cam not in use')
            else:
                power.isCamInUse = True
                #print('cam in use')
        doorIndex = controls.getClickedDoor(event.pos)
        if doorIndex is not None:
            doors[doorIndex].toggle()
            # update states according to door lock status
            power.isLeftDoorInUse = doors[0].locked
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
        if cameraMgr.isVisible(anim.x, anim.y):
            anim.draw(screen)

    camText = fontInstr.render(cameraMgr.activeCamera.name, True, (255, 255, 255))
    screen.blit(camText, camText.get_rect(topright=(880, 10)))

    # add time display
    timeText = fontInstr.render(gameConditions.getFormattedTime(), True, (255, 255, 255))
    screen.blit(timeText, timeText.get_rect(topleft=(520, 10)))

    # add power display
    powerText = fontInstr.render(f"{power.currentPower:.1f}%", True, (255, 255, 255))
    screen.blit(powerText, powerText.get_rect(topleft=(675, 10)))

    cameraMgr.drawDarkness(screen)
    controls.draw(screen)

def evalMvmtOpportunity(anim):
    check = anim.betweenTimeCounter()
    if check == True: # hit mvmt opportunity, now roll dice to check if we succeed
        roll = anim.rollDie(2) #lowered from 5 to slow down animatronics
        if roll:
            return True
    return False
def playQueuedVoice():
    global currentlySpeaking
    if voiceQueue and not currentlySpeaking:
        currentlySpeaking = True
        voiceData = voiceQueue.pop(0)
        threading.Thread(target=lambda: _playVoice(voiceData), daemon=True).start()

def _playVoice(voiceData):
    global currentlySpeaking
    if voiceData['type'] == 'low_battery':
        line = openrouter.generateVoiceLine("Freddy", "power_warning", f"power at {int(power.currentPower)}%")
        eleven.generateSpeech(line, ANIMATRONICS["Freddy"]["voiceId"])
    elif voiceData['type'] == 'out_of_battery':
        line = openrouter.generateVoiceLine("Bonnie", "power_warning", "no power left")
        eleven.generateSpeech(line, ANIMATRONICS["Bonnie"]["voiceId"])
    elif voiceData['type'] == 'close_animatronic':
        line = openrouter.generateVoiceLine(voiceData['anim'], "movement", f"distance {int(voiceData['dist'])}")
        eleven.generateSpeech(line, ANIMATRONICS[voiceData['anim']]["voiceId"])
    elif voiceData['type'] == 'door_lock':
        line = openrouter.generateVoiceLine(voiceData['anim'], "door_lock", "")
        eleven.generateSpeech(line, ANIMATRONICS[voiceData['anim']]["voiceId"])
    currentlySpeaking = False

def startAmbience():
    global ambienceStarted
    if not ambienceStarted:
        pygame.mixer.music.load('resources/ambience.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 loops forever
        ambienceStarted = True

def playJumpscare(animFilepath):
    global ambienceStarted
    # Stop ambience during jumpscare
    pygame.mixer.music.stop()
    ambienceStarted = False

    # Play audio
    audioFilepath = animFilepath.replace('.mp4', '.wav')
    pygame.mixer.music.load(audioFilepath)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    cap = cv2.VideoCapture(animFilepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frameDelay = int(1000 / fps) if fps > 0 else 33

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (900, 600))
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameArray = pygame.surfarray.make_surface(frameRgb.swapaxes(0, 1))
        screen.blit(frameArray, (0, 0))
        pygame.display.flip()
        pygame.time.wait(frameDelay)

    cap.release()
    pygame.mixer.music.set_volume(1) # we have to reset this globally

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
        startAmbience()
        playQueuedVoice()

        if gameConditions.currentFrame % 60 == 0:
            power.losePower()

            # Voice line for low battery
            if power.currentPower < 25 and power.currentPower > 0 and not batteryWarningGiven and gameConditions.currentFrame - lastVoiceFrame > voiceCooldown:
                voiceQueue.append({'type': 'low_battery'})
                lastVoiceFrame = gameConditions.currentFrame
                voiceCooldown = random.randint(180, 600)
                batteryWarningGiven = True

            # Voice line for out of battery
            if power.currentPower <= 0 and gameConditions.currentFrame - lastVoiceFrame > voiceCooldown:
                voiceQueue.append({'type': 'out_of_battery'})
                lastVoiceFrame = gameConditions.currentFrame
                voiceCooldown = random.randint(300, 900)

            # Reset battery warning when power recovers
            if power.currentPower >= 50:
                batteryWarningGiven = False

            if power.currentPower == 0:
                playJumpscare('outofpower.mp4')

        for anim in animatronics:
            if evalMvmtOpportunity(anim):
                movementSuccess = anim.moveToWaypoint(doors)
                # Door block voice trigger (40% chance, one time only)
                if not movementSuccess and not doorBlockVoiceTriggered and random.random() < 0.4:
                    animName = ["Freddy", "Bonnie", "Chica", "Foxy"][animatronics.index(anim)]
                    voiceQueue.append({'type': 'door_lock', 'anim': animName})
                    doorBlockVoiceTriggered = True

            # Voice line when animatronic gets close to office (only once)
            distanceToOffice = ((anim.x - 287)**2 + (anim.y - 544)**2)**0.5
            if distanceToOffice < 200 and not closeVoiceTriggered:
                animName = ["Freddy", "Bonnie", "Chica", "Foxy"][animatronics.index(anim)]
                voiceQueue.append({'type': 'close_animatronic', 'anim': animName, 'dist': distanceToOffice})
                closeVoiceTriggered = True

            if anim.x == 287 and anim.y == 544: #this checks if any animatronic has hit the waypoint that is in the office
                animName = ["freddy", "bonnie", "chica", "foxy"][animatronics.index(anim)]
                playJumpscare(f'resources/{animName}.mp4')
                gameState = 2

        if gameConditions.hasWon() == False:
            gameConditions.incrFrameCt()
        # Every 30 seconds (1800 frames at 60fps), print in-game time
        else:
            playJumpscare('resources/win.mp4')
            gameState = 3

    elif gameState == 2 or gameState == 3:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 60)
            text = font.render("Wanna play again? Restart the game!", True, (255, 255, 255))
            textRect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, textRect)
            pygame.display.flip()
            pygame.time.wait(5000)

    # Draw
    screen.fill((0, 0, 0))
    if gameState == 0:
        drawMenu()
    elif gameState == 1:
        drawGame()

    pygame.display.flip()
    clock.tick(60)
# for hallie :3
pygame.quit()