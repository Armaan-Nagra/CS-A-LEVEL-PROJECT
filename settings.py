import pygame
pygame.mixer.init()
pygame.font.init()

#welcome and name input screen
main_background = pygame.image.load('Stages/Stage 1/background_image.png')
message1 = pygame.image.load('Stages/Stage 2/message1.png')
message2 = pygame.image.load('Stages/Stage 2/message2.png')
background_music = pygame.mixer.Sound("Stages/Stage 1/background_music.mp3")
inside_input_box = False
input_rect = pygame.Rect(500,700,140,100)
name_placeholder = ''

#colours
white = (255,255,255)
black =(27,26,26)
yellow = (255,164,0)
dark_green = (12,83,15)
navy_blue = (0,38,114)
red = (212, 0, 0)
orange = (255, 117, 24)

#fonts
arcade_font = pygame.font.Font("Stages/Stage 2/arcade_font.ttf", 36)
base_font = pygame.font.Font(None,100)
name_score_font = pygame.font.Font(None,50)
leaderboard_font = pygame.font.Font(None,100)
level_font = pygame.font.Font(None,50)

#uzi
uzi = pygame.image.load('Stages/Stage 5/photos/ingame/uzi.png')
gunshot_sound = pygame.mixer.Sound("Stages/Stage 5/sounds/uzi.mp3")
black_cross = pygame.image.load('Stages/Stage 5/photos/INGAME/black_cross.png')

#grenade
grenade_image = pygame.image.load('Stages/Stage 5/photos/ingame/grenade.png')
grenade_sound = pygame.mixer.Sound("Stages/Stage 5/sounds/explosion.mp3")
grenade_visual = pygame.image.load('Stages/Stage 5/photos/INGAME/explosion.png')

#level scrolling background
level_background = pygame.image.load('Stages/Stage 5/photos/test.png')
scroll_speed = 0.5
scroll_background_x = 0

#soldiers
global max_soldiers, soldiers_killed, soldiers_left, no_soldiers

soldiers = pygame.sprite.Group()

soldier = pygame.image.load('Stages/Stage 5/photos/INGAME/soldier.png')
soldier2 = pygame.image.load('Stages/Stage 5/photos/INGAME/soldier2.png')
shooting_soldier = pygame.image.load('Stages/Stage 5/photos/INGAME/shooting_soldier.png')
shooting_soldier2 = pygame.image.load('Stages/Stage 5/photos/INGAME/shooting_soldier2.png')

soldier_spritesheet = []
soldier_spritesheet.append(soldier)
soldier_spritesheet.append(soldier2)
soldier_spritesheet.append(shooting_soldier)
soldier_spritesheet.append(shooting_soldier2)

soldier_icon = pygame.image.load('Stages/Stage 5/photos/INGAME/soldier_icon.png')

soldiers_left = 40
soldiers_killed = 0
max_soldiers = 5
no_soldiers = False

#tanks
tanks = pygame.sprite.Group()

tank = pygame.image.load('Stages/Stage 5/photos/INGAME/tank.png')
tank2 = pygame.image.load('Stages/Stage 5/photos/INGAME/tank2.png')
shooting_tank = pygame.image.load('Stages/Stage 5/photos/INGAME/shooting_tank.png')    
shooting_tank2 = pygame.image.load('Stages/Stage 5/photos/INGAME/shooting_tank2.png')

tank_spritesheet = []
tank_spritesheet.append(tank)
tank_spritesheet.append(tank2)
tank_spritesheet.append(shooting_tank)
tank_spritesheet.append(shooting_tank2) 

tank_icon = pygame.image.load('Stages/Stage 5/photos/INGAME/tank_icon.png')

max_tanks = 1
tanks_left = 5
tanks_shot = 0

#powerups
crate = pygame.image.load('Stages/Stage 5/photos/INGAME/crate.png')
add_ammo = pygame.image.load('Stages/Stage 5/photos/INGAME/add_ammo.png')
hearts = pygame.image.load('Stages/Stage 5/photos/INGAME/hearts.png')
chaching = pygame.mixer.Sound('Stages/Stage 5/sounds/chaching.mp3')
slurp = pygame.mixer.Sound('Stages/Stage 5/sounds/slurp.mp3')
machine_gun = pygame.mixer.Sound('Stages/Stage 5/sounds/machine-gun.mp3')

#pause menu
pause_menu = pygame.image.load('Stages/Stage 6/images/pause_menu.png')

#loss screen
global alpha_counter, last_stamp, sound_playing
alpha_counter = 0
last_stamp = 0
sound_playing = False
loss_sound = pygame.mixer.Sound('Stages/Stage 7/sounds/game_over.wav')
game_over = pygame.image.load('Stages/Stage 7/images/Gameover.png')

#win screen
global win_counter,win_sound,win_screen_counter
win_counter = 0
win_sound = pygame.mixer.Sound('Stages/Stage 8/sounds/win_sound.mp3')
winning_image = pygame.image.load('Stages/Stage 8/images/winning_image.png')
mission_completed = pygame.image.load('Stages/Stage 8/images/mission_completed.png')
stamp = pygame.mixer.Sound("Stages/Stage 8/sounds/stamp.mp3")
win_screen_image = pygame.image.load('Stages/Stage 8/images/mission_passed.png')
win_screen_counter = 0


