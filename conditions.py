from re import S
import pygame

class GameConditions:
    def __init__(self):
        self.gameLength = 28800 # 8 mins, in frames
        self.currentFrame = 0 # gets updated once per frame

    def incrFrameCt(self):
        self.currentFrame += 1

    def hasWon(self):
        if self.currentFrame == self.gameLength:
            return True #means the user has won, and main should flip to the win screen
        else:
            return False #keep going