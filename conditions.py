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
        total_seconds = progress * 21600
        
        # Convert to hours (12 AM + elapsed hours)
        hours_elapsed = int(total_seconds // 3600)
        display_hour = (12 + hours_elapsed) % 24
        
        # Convert to minutes
        minutes_elapsed = int((total_seconds % 3600) // 60)
        
        # Format as 12-hour time with AM
        if display_hour == 0:
            display_hour = 12
        elif display_hour > 12:
            display_hour -= 12
        
        return f"{display_hour}:{minutes_elapsed:02d} AM"

class Controls:
    def __init__(self, cameras):
        self.buttons = []
        self.font = pygame.font.SysFont(None, 20)

        # Create a button for each camera
        button_width = 370
        button_height = 50
        button_x = 515
        button_y = 50
        spacing = 5

        for i, camera in enumerate(cameras):
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons.append({
                'rect': button_rect,
                'camera_index': i,
                'name': camera.name
            })
            button_y += button_height + spacing

    def draw(self, surface):
        for button in self.buttons:
            # Draw button background
            pygame.draw.rect(surface, (60, 60, 90), button['rect'])
            # Draw button border
            pygame.draw.rect(surface, (100, 100, 150), button['rect'], 2)
            # Draw text
            text = self.font.render(button['name'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            surface.blit(text, text_rect)