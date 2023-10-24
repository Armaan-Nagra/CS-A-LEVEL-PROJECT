import pygame
from settings import *

class enemy(pygame.sprite.Sprite):
    def __init__(self,gx,gy,ghealth,gspritesheet,gstops,gdirection,gspeed):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.x = gx
        self.y = gy
        self.health = ghealth
        self.spritesheet = gspritesheet
        self.stops = gstops
        self.direction = gdirection
        self.killed = False
        self.offscreen = False
        self.speed = gspeed


    def draw(self,gd):
        self.x += self.speed
        self.frame = self.frame + 1
        if self.frame >= 3:
            self.frame = 0
        
        gd.blit(self.spritesheet[self.frame],(self.x,self.y))

        
    
