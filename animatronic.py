import pygame
import random

class Animatronic:
    def __init__(self, x, y, waypoints, color):
        self.x = x
        self.y = y
        self.color = color
        self.waypoints = waypoints
        self.currentWaypoint = 0
        self.speed = 1.5
        self.count = 60 #start at 60, assuming 60fps
        self.opportunity = random.randint(240, 420) # a mvmt opportunity can be ANY FRAME between 4-7 seconds at 60fps
        self.close_voice_triggered = False


    def moveToWaypoint(self, doors=None):
        next_wp = self.waypoints[(self.currentWaypoint + 1) % len(self.waypoints)]
        if doors:
            for door in doors:
                if door.locked:
                    door_x = door.rect.x + door.rect.width / 2
                    current_side = self.x < door_x
                    next_side = next_wp[0] < door_x
                    if current_side != next_side:
                        return  # Can't move, door is locked
        self.currentWaypoint = (self.currentWaypoint + 1) % len(self.waypoints)
        self.x, self.y = self.waypoints[self.currentWaypoint]
    

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 10)

    def rollDie(self, aiLevel):
        #d20 roll, if less than or equal to the ai level, we suceed a movement opportunity
        roll = random.randint(1, 20)

        if roll <= aiLevel:
            #print('succeeded')
            return True # succeeded mvmt opportunity
        else:
            #print('failed')
            return False

    def betweenTimeCounter(self):
        if self.count == self.opportunity: # we hit a mvmt opportunity, reset count and opportunity
            self.count = 60
            self.opportunity = random.randint(60, 600)
            #print(f'hit mvmt opportunity, new opportunity {self.opportunity}')
            return True
        else:
            self.count += 1
            return False
