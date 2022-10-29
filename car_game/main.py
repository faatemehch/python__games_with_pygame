import pygame
from pygame import mixer
import random

# Initialize the pygame
pygame.init()
# Create the Screen: (width, height) -> pixel
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# background
BG = pygame.image.load("carGame/img/background.jpeg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
# background sound
mixer.music.load("carGame/sounds/backgroundSound.wav")
mixer.music.play(-1)  # -1 -> plays on loop
# Title and Icon
pygame.display.set_caption("Pass Through Street")
icon = pygame.image.load("carGame/img/icon.png")
pygame.display.set_icon(icon)
# ---------------- Player ------------------
playerImg = pygame.image.load("carGame/img/pedestrian.png")
# Set the size for the image
DEFAULT_IMAGE_SIZE = (64, 64)
# Scale the image to needed size
playerImg = pygame.transform.scale(playerImg, DEFAULT_IMAGE_SIZE)
# Set a default position
playerX,  playerY = WIDTH, HEIGHT / 2 - playerImg.get_height() / 2
playerXChange, playerYChange = 0, 0
# ---------------- Cars ---------------------
# load , resize, rotate images
car1 = pygame.transform.scale(
    pygame.image.load("carGame/img/car1.png"), DEFAULT_IMAGE_SIZE)
car2 = pygame.transform.scale(
    pygame.image.load("carGame/img/car2.png"), DEFAULT_IMAGE_SIZE)
car3 = pygame.transform.scale(
    pygame.image.load("carGame/img/car3.png"), DEFAULT_IMAGE_SIZE)
# from up to down cars
list_of_cars = [car1, car2, car3]
# from_up_cars = [car1, pygame.transform.rotate(car2, 180), car3]
# from down to top
# from_down_cars = [pygame.transform.rotate(
#     car1, 180), car2, pygame.transform.rotate(car3, 180)]
# --------------------------------------------
FPS = 60  # frame pre second
# --------------------------------------------
class Player:
    MAX_HEALTH = 100

    def __init__(self, x, y, img, health=100, score=0):
        self.x = x
        self.y = y
        self.health = health
        self.score = 0
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.flip_right = False
        self.flip_left = True

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.healthbar(window)
        if self.health <= 0:
            self.gameover(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               playerImg.get_height() + 10, playerImg.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + playerImg.get_height() + 10, playerImg.get_width()*(self.health/self.MAX_HEALTH), 10))

    def show_live(self, window):
        live_font = pygame.font.Font("carGame/fonts/Weird Garden.ttf", 32)
        live_font = live_font.render(
            f"Live: {self.health // 10}", 1,  (255, 255, 255))
        window.blit(live_font, (15, 15))

    def show_score(self, window):
        score_font = pygame.font.Font("carGame/fonts/Weird Garden.ttf", 32)
        score_font = score_font.render(
            f"Score: {self.score}", 1,  (255, 255, 255))
        window.blit(score_font, (WIDTH - score_font.get_width() - 15, 15))

    def gameover(self, window):
        gameover_font = pygame.font.Font("carGame/fonts/Funroot-Regular.ttf", 64)
        gameover_font = gameover_font.render(f"Game Over", 1,  (0, 255, 0))
        window.blit(gameover_font, (WIDTH / 2 - gameover_font.get_width() /
                    2, HEIGHT/2 - gameover_font.get_height()/2))
        self.health = 0
        gameover_sound = mixer.Sound("carGame/sounds/gameOver.wav")
        gameover_sound.play()

class Car:
    CAR_VELOCITY = 1

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        self.CAR_VELOCITY += .001
        window.blit(self.img, (self.x, self.y))

# if overlap happen
def isCollision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None:
        collide_sound = mixer.Sound("carGame/sounds/collide.wav")
        collide_sound.play()
        return True
    else:
        return False

# object initialization
player = Player(playerX, playerY, playerImg)  # player

def create_car_object():
    global from_up_cars, from_down_cars
    from_up_cars = []
    from_down_cars = []
    for i in range(3):  # cars
        up_x, up_y = random.randint(
            25, WIDTH / 2 - 100), random.randint(-1000, -100)
        down_x, down_y = random.randint(
            WIDTH / 2 + 50, WIDTH - 100), random.randint(100, 1000)
        # override list of images into list of Car objects
        from_up_cars.append(Car(up_x, up_y, list_of_cars[i]))
        from_down_cars.append(Car(down_x, down_y, pygame.transform.rotate(list_of_cars[i], 180)))

create_car_object()
# ------------------------------------------------------------
running = True  # To Keep Open the game window
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    # RGB: Red Green Blue (search color to rgb)
    screen.fill((1, 0, 0))
    screen.blit(BG, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerYChange = -5
            if event.key == pygame.K_DOWN:
                playerYChange = 5
            if event.key == pygame.K_LEFT:
                if not player.flip_left:
                    player.img = pygame.transform.flip(player.img, True, False)
                    player.flip_left = True
                    player.flip_right = False
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                if not player.flip_right:
                    player.img = pygame.transform.flip(player.img, True, False)
                    player.flip_left = False
                    player.flip_right = True
                playerXChange = 5
            if event.key == pygame.K_SPACE: # To Restart The Game
                create_car_object()
                player.health = 100
                player.score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerXChange = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerYChange = 0
    if player.health <=0:
        playerXChange, playerYChange = 0 , 0
    # player
    player.x += playerXChange
    player.y += playerYChange
    player.draw(screen)
    player.show_live(screen)
    player.show_score(screen)
    if player.x < 0:
        player.x = WIDTH
        player.score += 1
    elif player.x > WIDTH:
        player.x = WIDTH - player.img.get_width()
    if player.y < 0:
        player.y = HEIGHT
    elif player.y > HEIGHT:
        player.y = 0
    # cars
    for car in from_up_cars[:]:
        car.y += car.CAR_VELOCITY
        car.draw(screen)
        if car.y > HEIGHT:
            car.y = random.randint(-1000, -100)
            car.x = random.randint(35, WIDTH / 2 - 50)
        if isCollision(car, player):
            player.health -= 1
        if player.health <= 0:
                from_up_cars.remove(car)

    for car in from_down_cars[:]:
        car.y -= car.CAR_VELOCITY
        car.draw(screen)
        if car.y < 0:
            car.y = random.randint(HEIGHT + 100, 2000)
            car.x = random.randint(WIDTH / 2 + 50, WIDTH - 100)
        if isCollision(car, player):
            player.health -= 1
        if player.health <= 0:
                from_down_cars.remove(car)
    pygame.display.update()
