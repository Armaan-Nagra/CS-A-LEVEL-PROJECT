import pygame
from settings import *
from functions import *
import json

class button():

    clicked = False

    def __init__(self, gx,gy,gh,gw,ggd,gbuttoncolour,gcurrent, gdestination, gtext, gfontsize,glettercolour,gevents):
        self.x = gx
        self.y = gy
        self.h = gh
        self.w = gw
        self.gd = ggd
        self.bc = gbuttoncolour
        self.gc = glettercolour
        self.current = gcurrent
        self.destination = gdestination
        self.text = gtext
        self.fs = gfontsize
        self.events = gevents
        self.exists = False

    
    #draws the button onto the game display
    def draw(self):
        base_font = pygame.font.Font(None,self.fs)
        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.gd, self.bc, button_rect)
        text_surface = base_font.render(self.text, True, self.gc)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.gd.blit(text_surface, text_rect.topleft)


    #checks if the user is clicking the button    
    def update(self):

        #button is drawn
        self.draw()

        #x and y co-ordinates of mouse are retrieved and assigned to the 2 variables below
        mouse_x, mouse_y = pygame.mouse.get_pos()

        #self.clicked changes to True if the user is clicking the button
        if self.events["left-click"]==1:
            if mouse_x > self.x and mouse_x < self.x + self.w:
                if mouse_y > self.y and mouse_y < self.y + self.h:
                    if self.events["left-click"] == 1:
                        self.clicked = True


    #appropriate decisions made after the user enters their name
    def name(self,name):
        self.update()
        if self.clicked == True:

            #if user tries to input empty name an error is displayed
            if name == '':
                display_text(red, 200, 100, "Enter valid name!", base_font)
                return self.current
            else:

                #load JSON file into variable name_score as a dictionary
                name_score = load_name_score()

                #if the name exists, it is loaded and user can go onto next screen
                for x in name_score["users"]:
                    if x["username"] == name.upper():
                        self.exists = True
                        return self.destination
                        break

                #if the name is not in the JSON file, it is added to it and user goes to next screen
                if not self.exists:
                    new_user = {
                        "username" : name.upper(),
                        "high_score" : 0
                    }
                    name_score["users"].append(new_user)
                    with open("name_score.json","w") as json_file:
                        json.dump(name_score, json_file, indent=4)
                    return self.destination
        else:
            return self.current


    #the gamestate is appropriately returned, the destination gamestate is only returned if the user clicks the button
    def redirect(self):
        self.update()
        if self.clicked == True:
            return self.destination
        else:
            return self.current

