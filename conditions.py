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
        self.door_buttons = []
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

        door_button_width = 180
        door_button_height = 50
        door_button_y = button_y + 10
        door_button_x1 = 515
        door_button_x2 = 515 + door_button_width + 5

        self.door_buttons.append({
            'rect': pygame.Rect(door_button_x1, door_button_y, door_button_width, door_button_height),
            'door_index': 0,
            'name': 'Left Door'
        })
        self.door_buttons.append({
            'rect': pygame.Rect(door_button_x2, door_button_y, door_button_width, door_button_height),
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
            text_rect = text.get_rect(center=button['rect'].center)
            surface.blit(text, text_rect)

        for button in self.door_buttons:
            # Draw button background
            pygame.draw.rect(surface, (120, 60, 60), button['rect'])
            # Draw button border
            pygame.draw.rect(surface, (180, 100, 100), button['rect'], 2)
            # Draw text
            text = self.font.render(button['name'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            surface.blit(text, text_rect)

    def getClickedCamera(self, mouse_pos):
        for button in self.buttons:
            if button['rect'].collidepoint(mouse_pos):
                return button['camera_index']
        return None

    def getClickedDoor(self, mouse_pos):
        for button in self.door_buttons:
            if button['rect'].collidepoint(mouse_pos):
                return button['door_index']
        return None