import random
import pygame

class GameConditions:
    def __init__(self):
        self.gameLength = random.randint(22400, 28800) # any frame between like 6m 13s and 8m, for variety
        self.currentFrame = 0 # gets updated once per frame

    def incrFrameCt(self):
        self.currentFrame += 1

    def hasWon(self):
        if self.currentFrame == self.gameLength:
            return True #means the user has won, and main should flip to the win screen
        else:
            return False #keep going

    def getFormattedTime(self): # THIS WAS DONE BY CURSOR - I CAN'T DO MATH FOR SHIT. oh wait i get it, it just does a multiplier of the speed based on the picked game length
        # Calculate progress through the game (0.0 to 1.0)
        progress = self.currentFrame / self.gameLength

        # Map to 6 hours (21,600 seconds total)
        totalSeconds = progress * 21600

        # Convert to hours (12 AM + elapsed hours)
        hoursElapsed = int(totalSeconds // 3600)
        displayHour = (12 + hoursElapsed) % 24

        # Convert to minutes
        minutesElapsed = int((totalSeconds % 3600) // 60)

        # Format as 12-hour time with AM
        if displayHour == 0:
            displayHour = 12
        elif displayHour > 12:
            displayHour -= 12

        return f"{displayHour}:{minutesElapsed:02d} AM"

class Controls:
    def __init__(self, cameras):
        self.buttons = []
        self.doorButtons = []
        self.font = pygame.font.SysFont(None, 20)

        # Create a button for each camera
        buttonWidth = 370
        buttonHeight = 50
        buttonX = 515
        buttonY = 50
        spacing = 5

        for i, camera in enumerate(cameras):
            buttonRect = pygame.Rect(buttonX, buttonY, buttonWidth, buttonHeight)
            self.buttons.append({
                'rect': buttonRect,
                'camera_index': i,
                'name': camera.name
            })
            buttonY += buttonHeight + spacing

        doorButtonWidth = 180
        doorButtonHeight = 50
        doorButtonY = buttonY + 10
        doorButtonX1 = 515
        doorButtonX2 = 515 + doorButtonWidth + 5

        self.doorButtons.append({
            'rect': pygame.Rect(doorButtonX1, doorButtonY, doorButtonWidth, doorButtonHeight),
            'door_index': 0,
            'name': 'Left Door'
        })
        self.doorButtons.append({
            'rect': pygame.Rect(doorButtonX2, doorButtonY, doorButtonWidth, doorButtonHeight),
            'door_index': 1,
            'name': 'Right Door'
        })

    def draw(self, surface):
        for button in self.buttons:
            # Draw button background
            pygame.draw.rect(surface, (60, 60, 90), button['rect'])
            # Draw button border
            pygame.draw.rect(surface, (100, 100, 150), button['rect'], 2)
            # Draw text
            text = self.font.render(button['name'], True, (255, 255, 255))
            textRect = text.get_rect(center=button['rect'].center)
            surface.blit(text, textRect)

        for button in self.doorButtons:
            # Draw button background
            pygame.draw.rect(surface, (120, 60, 60), button['rect'])
            # Draw button border
            pygame.draw.rect(surface, (180, 100, 100), button['rect'], 2)
            # Draw text
            text = self.font.render(button['name'], True, (255, 255, 255))
            textRect = text.get_rect(center=button['rect'].center)
            surface.blit(text, textRect)

    def getClickedCamera(self, mousePos):
        for button in self.buttons:
            if button['rect'].collidepoint(mousePos):
                return button['camera_index']
        return None

    def getClickedDoor(self, mousePos):
        for button in self.doorButtons:
            if button['rect'].collidepoint(mousePos):
                return button['door_index']
        return None