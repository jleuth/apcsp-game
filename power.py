import pygame
import random

class Power:
    def __init__(self):
        self.currentPower = 100
        self.basePowerLossRate = 0.1667 #haha 67 also this is in percent/s. this is if the user doesnt even use cameras
        self.currentPowerLossRate = 0
        self.camPowerLossRate = 0.05
        self.doorPowerLossRate = 0.08 # per door
        self.isLeftDoorInUse = False
        self.isRightDoorInUse = False
        self.isCamInUse = False

    def losePower(self): # called once per sec
        #calc current loss rate
        self.currentPowerLossRate = self.basePowerLossRate + (self.camPowerLossRate if self.isCamInUse else 0) + (self.doorPowerLossRate if self.isLeftDoorInUse else 0) + (self.doorPowerLossRate if self.isRightDoorInUse else 0)
        self.currentPower -= self.currentPowerLossRate

