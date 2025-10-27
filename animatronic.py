import pygame
import random

class Animatronic:
    def __init__(self, x, y, waypoints):
        self.x = x
        self.y = y
        self.waypoints = waypoints
        self.currentWaypoint = 0
        self.speed = 1.5
        self.count = 60 #start at 60, assuming 60fps
        self.opportunity = random.randint(60, 300) # a mvmt opportunity can be ANY FRAME between 1-5 seconds


    def moveToWaypoint(self):
        tX, tY = self.waypoints[self.currentWaypoint]
        dX = tX - self.x
        dY = tY - self.y
        distance = (dX**2 + dY**2)**0.5

        if distance > self.speed:
            self.x += (dX / distance) * self.speed
            self.y += (dY / distance) * self.speed
        else:
            self.currentWaypoint = (self.currentWaypoint + 1) % len(self.waypoints)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 10)

    def rollDie(self, aiLevel):
        #d20 roll, if less than or equal to the ai level, we suceed a movement opportunity
        roll = random.randint(1, 20)

        if roll <= aiLevel:
            return True # succeeded mvmt opportunity
        else:
            return False

    def betweenTimeCounter(self):
        if self.count == self.opportunity: # we hit a mvmt opportunity, reset count and opportunity
            self.count = 60
            self.opportunity = random.randint(60, 300)
            return True
        else:
            self.count += 1
            return False
