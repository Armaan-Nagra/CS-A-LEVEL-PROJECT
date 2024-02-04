import pygame

class player():
    def __init__(self,gscore,ghigh_score,ghealth):
        self.name = ""
        self.score = gscore
        self.high_score = ghigh_score
        self.health = ghealth
        self.current_score = 0



    def change_health(self,amount):
        self.health += amount


    def health_bar(self,gd):
        ratio = self.health/100
        pygame.draw.rect(gd, "red", (400,5, 200,50))
        pygame.draw.rect(gd, "green", (400,5, 200 * ratio, 50))

    def change_name(self,name):
        self.name = name

    def calculate_score(self,ammo,timer,enemies_killed,tanks_shot):
	    self.current_score = 500 + (200*enemies_killed)+(500*tanks_shot)-((100-self.health)+(100-ammo)) - (timer*0.01)


