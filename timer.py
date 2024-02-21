import pygame
class PausableTimer:
    def __init__(self):
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False
        self.started = False

    def start(self): # start the timer once game starts
        self.start_time = pygame.time.get_ticks()
        self.started = True

    def pause(self): # pause the timer when the player pauses the game
        if not self.is_paused:
            self.paused_time = pygame.time.get_ticks() - self.start_time
            self.is_paused = True

    def resume(self): # resume the timer when player resumes game
        if self.is_paused:
            self.start_time = pygame.time.get_ticks() - self.paused_time
            self.is_paused = False
        
    #display correct timer depending on whether player is on pause menu or not
    def get_elapsed_time(self): 
        if self.is_paused:
            return self.paused_time
        else:
            return pygame.time.get_ticks() - self.start_time
    
    def reset_timer(self):
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False
        self.started = False