import pygame
import random 
from settings import *

class powerups():
    def __init__(self,gplayer,gweapon,gx,gy,gopacity,ggd):
        self.player = gplayer
        self.weapon = gweapon
        self.x = gx
        self.y = gy        
        self.opacity = gopacity
        self.first = random.randint(30,40)
        self.second = random.randint(10,29) 
        self.third = random.randint(1,9) 
        self.powerups_list = [self.first,self.second,self.third]
        self.crate = crate
        self.moving = False
        self.shot = False
        self.message_x = 0
        self.message_y = 0
        self.message_photo = None
        self.show_message = False
        self.type = None 
        self.size = None
        self.gd = ggd
    
    def update(self,soldiers,x,y,left_click):
        #check whether the amount of enemies left equals any of the randomly generated integers in the self.powerups_list list
        for powerup in self.powerups_list:
            if powerup == soldiers and self.moving==False:
                #choose a random power up
                self.type = random.choice(["health","ammo","damage"])
                #removes the random integer from the list so that multiple power ups are not spawned
                self.powerups_list.remove(powerup)
                #flag is turned on to spawn the power up
                self.moving = True
        
        if self.moving:
            #self.shot is reset to False because if it is not, power ups won't respawn again
            self.shot = False
            self.draw()
            self.move() 
            self.check_collision(x,y,left_click)
        
        if self.show_message == True:
            self.visual_effect()
            #make message/visual effect go up
            self.message_y-=0.5
            #make the message "fade" away by decreasing opacity
            self.opacity -=1.5
            #once the opacity is less than or equal to 5 (almost faded away), message is not shown anymore
            if self.opacity <= 5:
                self.show_message = False


    def draw(self):
        #draw the crate only when the player has not shot it and a power up exists
        if self.type != None and self.shot == False:
            self.gd.blit(self.crate,(self.x,self.y))



    def move(self):
        #if the y co-ordinate of the crate is less than or equal to 350, it's increased by 5
        if self.y <= 350:
            self.y+=1
        
        #if self.y is greater than or equal to 350 (crate has reached the floor), the x co-ordinate of the crate increase proportionally to background
        if self.y >= 350:
            self.x -= scroll_speed
        
        #if the crate's x co ordinate is less than or equal to -100 (player has not shot it and it's left the screen)
        if self.x <= -100:
            #x and y co ordinates are reset, self.moving flag is also reset to False
            self.x = random.randint(800,1100)
            self.y = -100
            self.moving = False
    
    def check_collision(self,mouse_x,mouse_y,mouse_left):
        #if the mouse left side is being clicked and crate has not been shot
        if mouse_left and self.shot == False:
            #checks if the cursor is over the crate
            if mouse_x > self.x and mouse_x < self.x +100:
                if mouse_y > self.y and mouse_y < self.y +80:
                    self.use_power_up()
                    self.shot = True
                    self.x = random.randint(800,1100)
                    self.y = -100
                    self.moving = False
    
    def use_power_up(self):
        if self.type == "health":
            self.player.change_health(50)
            slurp.play()
            
            #attributes related to the visual effects/message shown
            self.message_x = 0
            self.message_y = 25
            self.message_photo = hearts
            self.show_message = True
            self.size = (1000,200)
            self.opacity = 300

        if self.type == "ammo":
            self.weapon.change_bullets(20)
            chaching.play()

            #attributes related to the visual effects/message shown
            self.message_x = 750
            self.message_y = 780
            self.message_photo = add_ammo
            self.show_message = True
            self.size = (100,100)
            self.opacity = 300

        if self.type == "damage":
            self.weapon.more_damage(red,machine_gun)
    
    def visual_effect(self):
        #surface created with the size of the message/image
        temp = pygame.Surface(self.size).convert()
        #what does this actually do??!!
        temp.blit(self.gd, (-self.message_x, -self.message_y))
        #photo of visual effect drawn onto surface
        temp.blit(self.message_photo, (0, 0))
        #opacity of the image is changed to "opacity"
        temp.set_alpha(self.opacity)        
        #surface drawn onto game display
        self.gd.blit(temp, (self.message_x,self.message_y))
        