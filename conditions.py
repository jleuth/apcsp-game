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
        