import pygame

class Camera:
    def __init__(self, x, y, width, height, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.active = False

    def isPointInCamera(self, x, y): # check if animatronic is in view of cam
        return self.rect.collidepoint()

    def drawOverlay(self, surface): #this hides inactive rooms
        if not self.active:
            darkness = pygame.Surface((self.rect.width, self.rect.height))
            darkness.fill((0, 0, 0))
            surface.blit(darkness, self.rect)

class CameraManager: #the word "camera" has lost all meaning to me
    def __init__(self, cameras):
        self.cameras = cameras
        self.activeCamera = cameras[0] if cameras else None
        if self.activeCamera:
            self.activeCamera.active = True

    def switchCamera(self, cameraNum):
        if self.activeCamera:
            self.activeCamera.active = False

        if 0 <= cameraNum < len(self.cameras):
            self.activeCamera = self.cameras[cameraNum]
            self.activeCamera.active = True

    def isVisible(self, x, y):
        return self.activeCamera.isPointInCamera(x, y) if self.activeCamera else False

    def drawDarkness(self, surface):
        for c in self.cameras:
            if not camera.active:
                camera.draw_overlay(surface)