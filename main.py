import pygame
import random
import threading
from animatronic import Animatronic
from door import Door
from camera import Camera, CameraManager
from conditions import GameConditions, Controls, AiConditions
from power import Power
from ai import Eleven, OpenRouter
import cv2
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
eleven = Eleven()
openrouter = OpenRouter()

# Voice line tracking
last_voice_frame = 0
voice_cooldown = random.randint(600, 1200)
battery_warning_given = False
voice_queue = []
currently_speaking = False

# Assets
mapImage = pygame.image.load('resources/map.png')
mapImageCropped = mapImage.subsurface(pygame.Rect(200, 0, mapImage.get_width() - 200, mapImage.get_height())) #move to the left

# Game objects 

waypointsFreddy = [
    (222, 120), (400, 121), (451, 235), (139, 142), (191, 349), (148, 513), (287, 544)
]

waypointsFoxy = [
    (320, 91), (425, 76), (437, 244), (381, 379), (382, 509), (287, 544)
]

waypointsBonnie = [
    (298, 183), (403, 142), (428, 273), (387, 385), (434, 564), (287, 544)
]

waypointsChica = [
    (233, 204), (209, 241), (194, 383), (163, 515), (287, 544)
]
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
            if cameraMgr.activeCamera.name == 'Office':
                power.isCamInUse = False
                print('cam not in use')
            else:
                power.isCamInUse = True
                print('cam in use')
        door_index = controls.getClickedDoor(event.pos)
        if door_index is not None:
            doors[door_index].toggle()
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
    screen.blit(powerText, powerText.get_rect(topleft = (675, 10)))

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
    global currently_speaking
    if voice_queue and not currently_speaking:
        currently_speaking = True
        voice_data = voice_queue.pop(0)
        threading.Thread(target=lambda: _playVoice(voice_data), daemon=True).start()

def _playVoice(voice_data):
    global currently_speaking
    if voice_data['type'] == 'low_battery':
        line = openrouter.generateVoiceLine("Freddy", "power_warning", f"power at {int(power.currentPower)}%")
        eleven.generateSpeech(line, "PiE7En4dJh0s0VBPcv22")
    elif voice_data['type'] == 'out_of_battery':
        line = openrouter.generateVoiceLine("Bonnie", "power_warning", "no power left")
        eleven.generateSpeech(line, "PiE7En4dJh0s0VBPcv22")
    elif voice_data['type'] == 'close_animatronic':
        line = openrouter.generateVoiceLine(voice_data['anim'], "movement", f"distance {int(voice_data['dist'])}")
        eleven.generateSpeech(line, "PiE7En4dJh0s0VBPcv22")
    currently_speaking = False

def playJumpscare(anim_filepath):
    """Play jumpscare video using cv2 with audio"""
    try:
        # Play audio
        audio_filepath = anim_filepath.replace('.mp4', '.wav')
        pygame.mixer.music.load(audio_filepath)
        pygame.mixer.music.play()

        cap = cv2.VideoCapture(anim_filepath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = int(1000 / fps) if fps > 0 else 33

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (900, 600))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_array = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            screen.blit(frame_array, (0, 0))
            pygame.display.flip()
            pygame.time.wait(frame_delay)

        cap.release()
    except:
        pass

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
        playQueuedVoice()

        if gameConditions.currentFrame % 60 == 0:
            power.losePower()

            # Voice line for low battery
            if power.currentPower < 25 and power.currentPower > 0 and not battery_warning_given and gameConditions.currentFrame - last_voice_frame > voice_cooldown:
                voice_queue.append({'type': 'low_battery'})
                last_voice_frame = gameConditions.currentFrame
                voice_cooldown = random.randint(180, 600)
                battery_warning_given = True

            # Voice line for out of battery
            if power.currentPower <= 0 and gameConditions.currentFrame - last_voice_frame > voice_cooldown:
                voice_queue.append({'type': 'out_of_battery'})
                last_voice_frame = gameConditions.currentFrame
                voice_cooldown = random.randint(300, 900)

            # Reset battery warning when power recovers
            if power.currentPower >= 50:
                battery_warning_given = False

        for anim in animatronics:
            if evalMvmtOpportunity(anim):
                anim.moveToWaypoint(doors)

            # Voice line when animatronic gets close to office (only once)
            distance_to_office = ((anim.x - 287)**2 + (anim.y - 544)**2)**0.5
            if distance_to_office < 200 and not anim.close_voice_triggered:
                anim_name = ["Freddy", "Bonnie", "Chica", "Foxy"][animatronics.index(anim)]
                voice_queue.append({'type': 'close_animatronic', 'anim': anim_name, 'dist': distance_to_office})
                anim.close_voice_triggered = True

            if anim.x == 287 and anim.y == 544: #this checks if any animatronic has hit the waypoint that is in the office
                anim_name = ["freddy", "bonnie", "chica", "foxy"][animatronics.index(anim)]
                playJumpscare(f'resources/{anim_name}.mp4')
                gameState = 2
                '''
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 60)
                text = font.render("Wanna play again? Restart the game!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(5000)
                '''

        if gameConditions.hasWon() == False:
            gameConditions.incrFrameCt()         
        # Every 30 seconds (1800 frames at 60fps), print in-game time
            if gameConditions.currentFrame % 1800 == 0:
                print("In-game time:", gameConditions.getFormattedTime())
        else:
            playJumpscare('resources/win.mp4')
            gameState = 3

    elif gameState == 2 or gameState == 3:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 60)
            text = font.render("Wanna play again? Restart the game!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)
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

pygame.quit()