import pygame
import time
from functions import *
from settings import *

class weapon(pygame.sprite.Sprite):
    def __init__(self,gtype,gammo,gdelay,gsound):
        self.type = gtype
        self.ammo = gammo
        self.shot_delay = gdelay
        self.sound = gsound

        self.last_shot = 0 #time taken since last shot
        self.uzi_damage = 100
        self.current_bullets = 0 # copy of the amount of uzi bullets before more damage is activated
        self.font_colour = black # font colour of icon in bottom right of screen
        self.more_damage_active = False


    def draw_hitbox(self,gd,colour,w,h): #draws the hitbox or reticle
        pygame.mouse.set_visible(False)
        pygame.draw.rect(gd,colour, [self.x + 8, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - 8 - h, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y + 8 ,w,h])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y - 8 -h,w,h])


    def check_collision(self, sprite_group):

        #if the more damage powerup is picked up, I increase bullets, damage and make a copy of the current bullets
        if self.more_damage_active == True:
            self.current_bullets = self.ammo
            self.ammo += 15
            self.uzi_damage = 250
            self.more_damage_active = False
        
        #once the current bullets are equal to the copy of the bullets before the powerup, damage is reset
        if self.ammo <= self.current_bullets:
            self.uzi_damage = 100
            self.font_colour = black
            self.sound = gunshot_sound

        #iterate through each sprite object in the group
        for x in sprite_group:
            if x.rect.collidepoint(self.pos) and self.type == "uzi": #if bullet fired at sprite
                x.change_health(self.uzi_damage) #change the sprite's health by the self.uzi_damage integer.

            #if the weapon is a grenade, the sprite's health is subtracted with a larger amount (500)
            if self.type == "grenade" and x.rect.colliderect(self.rect):
                x.change_health(500)

        
    def shoot_effects(self,event,visual,gd,x,y,ex,ey,sprite_group):
        #x and y co-ordinates of the cursor/reticle/cursor
        self.x = x
        self.y = y
        #x and y co-ordinates of the visual effect
        self.ex = ex
        self.ey = ey
        self.pos = (self.x, self.y)

        if self.type == "grenade":
            #get the size of the visual effect of the grenade
            self.rect = visual.get_rect()
            self.rect.x = self.ex
            self.rect.y = self.ey 

        #if the mouse is left-clicked and there's ammo      
        if event == 1 and self.ammo > 0:
            #fire each shot or grenade after a delay equal to self.shot_delay
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.shot_delay:
                #play an appropriate sound for the weapon
                self.sound.play()
                #display a visual effect
                gd.blit(visual,(self.ex,self.ey))
                self.ammo -= 1
                for x in sprite_group:
                    self.check_collision(x)
                self.last_shot = pygame.time.get_ticks()


    def display_icon(self,image,gd,ix,iy,bx,by):
        #display the image if the weapon icon at the co-ordinates (ix,iy)
        gd.blit(image,(ix,iy))
        #display the amount of ammo left at (bx,by)
        display_text(self.font_colour,bx,by,str(self.ammo),level_font)


    def change_bullets(self,amount):
        self.ammo += amount


    def more_damage(self,font_colour,sound):
        self.more_damage_active = True
        self.font_colour = font_colour
        self.sound = sound
    

    def reset_weapon(self):
        #reset the "copy" of the bullets taken when powerup used
        self.current_bullets = 0
        #reset the damage, bullets, colour and sound of the uzi gun
        if self.type == "uzi":
            self.ammo = 101
            self.uzi_damage = 100
            self.font_colour = black
            self.sound = gunshot_sound
        #reset the amount of bullets and sound of grenade
        if self.type == "grenade":
            self.ammo = 5
            self.sound = grenade_sound
        self.last_shot = 0
        self.more_damage_active = False
            




                
