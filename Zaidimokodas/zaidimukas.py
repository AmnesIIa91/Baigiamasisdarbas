import pygame
import random
import math
from pygame import mixer

pygame.init()

# screen size
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg')

# background sound
mixer.music.load('backgroundss.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# name and icon
pygame.display.set_caption("Kosmoso invazija")
icon = pygame.image.load('ufo 32.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('alien.png'))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)

# Laser
# ready - u can't see a bullet on screen
# fire - the bullet is currently moving
LaserImg = pygame.image.load('Laser.png')
LaserX = 0.3
LaserY = 480
LaserX_change = 0
LaserY_change = 1
Laser_state = "ready"

# score count
score_value = 0
font = pygame.font.Font('BTTF.ttf', 15)

testX = 10
testY = 10

# Game over text
over_font = pygame.font.Font('BTTF.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_laser(x, y):
    global Laser_state
    Laser_state = "fire"
    screen.blit(LaserImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, LaserX, LaserY):
    distance = math.sqrt(math.pow(enemyX - LaserX, 2)) + (math.pow(enemyY - LaserY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop , for window to not turn off after running a code.
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking if the buttons a pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if Laser_state == "ready":
                    Bullet_sound = mixer.Sound('gunsound.wav')
                    Bullet_sound.play()
                    # Get the current x coordinates of the space ship
                    LaserX = playerX
                    fire_laser(LaserX, LaserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0


    playerX += playerX_change
    # checking if player does not goes off from boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # checking that enemy wont go off from boundaries
    for i in range(num_of_enemies):

        # game over
        if EnemyY[i] > 450:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -0.3
            EnemyY[i] += EnemyY_change[i]

        collision = isCollision(EnemyX[i], EnemyY[i], LaserX, LaserY)
        if collision:
            explosion_sound = mixer.Sound('explosions.wav')
            explosion_sound.play()
            LaserY = 480
            Laser_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)
        Enemy(EnemyX[i], EnemyY[i], i)

    # laser movement
    if LaserY <= 0:
        LaserY = 480
        Laser_state = "ready"

    if Laser_state == "fire":
        fire_laser(LaserX, LaserY, )
        LaserY -= LaserY_change

    player(playerX, playerY)
    show_score(testX, testY)
    pygame.display.update()
