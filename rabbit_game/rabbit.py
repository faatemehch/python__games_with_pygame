import pygame
import math
from pygame import mixer
from random import *

# Initialize the pygame
pygame.init()
# Create the Screen: (width, height) -> pixel 
WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Load Background Image
backgroundImage = pygame.image.load("rabbit_game/img/background.png")
# Backgroung Music
mixer.music.load("rabbit_game/sounds/background.wav")
mixer.music.play(-1)
# ------------------ Player ------------------
playerImg = pygame.image.load("rabbit_game/img/rabbit.png")
playerImg = pygame.transform.scale(playerImg, (64,64))
playerX = 350
playerY = 420 
changes = 0
score = 0
level = 1
lost = False # default lost
main_font = pygame.font.SysFont("rabbit_game/fonts/Honey Mints.ttf", 32)
gameover_font = pygame.font.SysFont("rabbit_game/fonts/Honey Mints.ttf", 64)
#------------------ Carrot ------------------
carrotImg = pygame.image.load("rabbit_game/img/carrot.png")
carrotImg = pygame.transform.scale(carrotImg, (32,32))
carrot_number  = 10
carrot_velocity = 1
carrotX = []
carrotY = []
carrots_list = []
for i in range(carrot_number):
    img = pygame.transform.rotate(carrotImg, randint(0, 180))
    carrots_list.append(img)
    carrotX.append(randint(40, WIDTH-40))
    carrotY.append(randint(-1000, -100))
# ------------------ Bomb ------------------
bombImg = pygame.image.load("rabbit_game/img/bomb.png") 
bombImg = pygame.transform.scale(bombImg, (32,32))
bomb_number  = 10
bomb_velocity = 2
bombX = []
bombY = []
bomb_list = []
for i in range(carrot_number):
    bomb_list.append(bombImg)
    bombX.append(randint(40, WIDTH-40))
    bombY.append(randint(-1000, -100))
# -------------- Functions --------------
def player(x, y):
    screen.blit(playerImg, (x, y))

def draw_game_objects(x, y, img):
    screen.blit(img, (x, y))

def isCollision(x1, y1, x2, y2, img1, img2):
    offset_x = x1 - x2
    offset_y = y1 - y2
    obj1 = pygame.mask.from_surface(img1)
    obj2 = pygame.mask.from_surface(img2)
    overlaped = obj1.overlap(obj2, (offset_x, offset_y))
    if overlaped!= None:
        print(overlaped)
        return True
    else:
        return False

def show_game_info():
    score_font = main_font.render(f"Score: {score}",True, (255,0,0))
    level_font = main_font.render(f"Level: {level}",True, (0,0,255))
    screen.blit(score_font, (10, 10))
    screen.blit(level_font, (WIDTH - level_font.get_width() - 10 , 10))

def gameover():
    font = gameover_font.render(f"Geme Over :(",True, (255,0,255))
    screen.blit(font, (WIDTH /2 - font.get_width()/2, HEIGHT /2 - font.get_height()/2))
# -------------- Game --------------
clock = pygame.time.Clock()
running = True # To Keep Open The Screen
while running:
    clock.tick(60)
    screen.blit(backgroundImage, (0,0))
    if score == 0 and lost:
        gameover()
    show_game_info()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # To Exit The Game
        if event.type == pygame.KEYDOWN: # if press down any button
            if event.key == pygame.K_a:  # if pressed "a" button
                changes = -5
            if event.key == pygame.K_d:  # if pressed "d" button
                changes = 5
        if event.type == pygame.KEYUP:   # if release any button
            if event.key == pygame.K_a or event.key == pygame.K_d: # if release a or d button 
                changes = 0 # to stop the player(rabbit) at current position
    playerX = playerX + changes # Change x to move the player
    player(playerX, playerY)
    # Carrot
    for i in range(carrot_number):
        draw_game_objects(carrotX[i], carrotY[i], carrots_list[i])
        carrotY[i] += 2
        if isCollision(playerX, playerY, carrotX[i], carrotY[i], playerImg, carrots_list[i]):
            score += carrot_velocity
            if score % 10 == 0:
                level += 1
                bomb_velocity += 1
                carrot_velocity += 1
            carrotY[i] = randint(-1000, -100)
            carrotX[i] = randint(40, WIDTH-40)
        if carrotY[i] >= HEIGHT:
            carrotY[i] = randint(-1000, -100)
            carrotX[i] = randint(40, WIDTH-40)
    # Bomb
    for i in range(bomb_number):
        draw_game_objects(bombX[i], bombY[i], bomb_list[i])
        bombY[i] += bomb_velocity
        if isCollision(playerX, playerY, bombX[i], bombY[i], playerImg, bomb_list[i]):
            if score <= 0:
                lost = True
            else:
                score -= 1
            bombY[i] = randint(-1000, -100)
            bombX[i] = randint(40, WIDTH-40)
        if bombY[i] >= HEIGHT:
            bombY[i] = randint(-1000, -100)
            bombX[i] = randint(40, WIDTH-40)
    
    pygame.display.update()