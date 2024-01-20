import pygame
pygame.mixer.init()
pygame.font.init()

#load background and music
main_background = pygame.image.load('Stages/Stage 1/monkey.png')
message1 = pygame.image.load('Stages/Stage 2/message1.png')
message2 = pygame.image.load('Stages/Stage 2/message2.png')
background_music = pygame.mixer.Sound("Stages/Stage 1/background.mp3")

#colours
white = (255,255,255)
black =(27,26,26)
yellow = (255,164,0)
dark_green = (12,83,15)
navy_blue = (0,38,114)
red = (212, 0, 0)
orange = (255, 117, 24)

#fonts
arcade_font = pygame.font.Font("Stages/Stage 2/pixel.ttf", 36)
base_font = pygame.font.Font(None,100)
name_score_font = pygame.font.Font(None,50)
leaderboard_font = pygame.font.Font(None,100)
level_font = pygame.font.Font(None,50)

#name
name_placeholder = ''

#creating rectangle
input_rect = pygame.Rect(500,700,140,100)

#check to see if user is inside_box
inside_input_box = False

#gunshot
gunshot_sound = pygame.mixer.Sound("Stages/Stage 5/sounds/uzi-new.mp3")

#bullets
bullets = 100


#uzi
uzi = pygame.image.load('Stages/Stage 5/photos/uzi-new.png')
gunshot_sound = pygame.mixer.Sound("Stages/Stage 5/sounds/uzi-new.mp3")
black_cross = pygame.image.load('Stages/Stage 5/photos/INGAME/black_cross.png')

#grenade
grenade_image = pygame.image.load('Stages/Stage 5/photos/grenade-new.png')
grenade_sound = pygame.mixer.Sound("Stages/Stage 5/sounds/explosion.mp3")
grenade_visual = pygame.image.load('Stages/Stage 5/photos/INGAME/explosion.png')

#level background
background_image = pygame.image.load('Stages/Stage 5/photos/backgroundtest.png')

#scrolling speed of background
scroll_speed = 0.5
background_x = 0

#load soldiers
shooting_soldier = pygame.image.load('Stages/Stage 5/photos/INGAME/shooter.png')
run1 = pygame.image.load('Stages/Stage 5/photos/INGAME/run1.png')
run2 = pygame.image.load('Stages/Stage 5/photos/INGAME/run2.png')
white_shoot = pygame.image.load('Stages/Stage 5/photos/INGAME/white shoot.png')
soldier_headshot = pygame.image.load('Stages/Stage 5/photos/INGAME/soldier_headshot.png')
#load spritesheet
#soldier_spritesheet = pygame.image.load("Stages/Stage 5/photos/INGAME/invSpritesheet.png")

#load tanks
tank_white = pygame.image.load('Stages/Stage 5/photos/INGAME/tank shoot.png')
tank1 = pygame.image.load('Stages/Stage 5/photos/INGAME/tank.png')
tank2 = pygame.image.load('Stages/Stage 5/photos/INGAME/tank2.png')
tank_shoot = pygame.image.load('Stages/Stage 5/photos/INGAME/tank3.png')
tank_small = pygame.image.load('Stages/Stage 5/photos/INGAME/tank_small.png')

global max_soldiers, soldiers_killed, soldiers_left

soldiers_left = 40
soldiers_killed = 0
max_soldiers = 5

max_tanks = 1
tanks_left = 5
tanks_shot = 0

no_soldiers = False

#photos of powerups
health_boost = pygame.image.load('Stages/Stage 5/photos/INGAME/healthboost.png')
add_ammo = pygame.image.load('Stages/Stage 5/photos/INGAME/+15.png')
hearts = pygame.image.load('Stages/Stage 5/photos/INGAME/hearts.png')

#powerups sounds
chaching = pygame.mixer.Sound('Stages/Stage 5/sounds/chaching.mp3')
slurp = pygame.mixer.Sound('Stages/Stage 5/sounds/slurp.mp3')
machine_gun = pygame.mixer.Sound('Stages/Stage 5/sounds/machine-gun.mp3')
