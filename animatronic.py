import pygame


class Animatronic:
    def __init__(self, x, y, waypoints):
        self.x = x
        self.y = y
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 1.5

    def moveToWaypoint(self):
        tX, tY = self.waypoints[self.current_waypoint]
        dX = tX - self.x
        dY = tY - self.y
        distance = (dX**2 + dY**2)**0.5

        if distance > self.speed:
            self.x += (dX / distance) * self.speed
            self.y += (dY / distance) * self.speed
        else:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 10)
