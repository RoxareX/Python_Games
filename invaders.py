import time
import pygame
import random
import math
import os
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background Sound
mixer.music.load('Space_invaders/background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

# Name of the pygame window
pygame.display.set_caption('Game Console')

# Icon of the window
icon = pygame.image.load('Space_invaders/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Space_invaders/space-invaders.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
enemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = random.randint(5, 10)
# random.randint(2, 6)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Space_invaders/enemy.png'))
    EnemyX.append(random.randint(64, 736))
    EnemyY.append(random.randint(50, 100))
    EnemyX_change.append(0.2)
    EnemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load('Space_invaders/bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 1
Bullet_state = "ready"

# Particles

# Score
score_value = 0
font = pygame.font.Font('Symtext.ttf', 32)

textX = 10
TextY = 10

# Game over
over_font = pygame.font.Font('Symtext.ttf', 64)
rest_font = pygame.font.Font('Symtext.ttf', 32)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER : " + str(score_value), True, (25, 25, 255))
    rest_text = rest_font.render("Press P to restart ", True, (25, 25, 255))
    screen.blit(over_text, (140, 200))
    screen.blit(rest_text, (190, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check if it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                PlayerX_change = -0.25
            if event.key == pygame.K_d:
                PlayerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    bullet_Sound = mixer.Sound('Space_invaders/laser.wav')
                    bullet_Sound.play()
                    bullet_Sound.set_volume(0.3)
                    # Get the current x cordinate of the ship
                    BulletX = PlayerX
                    fire_bullet(BulletX, PlayerY)
            # ------------------------------------------------------------------------------------------------------
            if event.key == pygame.K_p:
                os.startfile('F:\Pycharm\Game Bot\invaders.py')
                exit()
            if event.type == pygame.QUIT:
                break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                PlayerX_change = 0
            elif event.key == pygame.K_ESCAPE:
                os.startfile('F:\Pycharm\Game Bot\main.py')
                exit()

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    PlayerX += PlayerX_change

    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if EnemyY[i] > 300:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_change[i]

        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.2
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -0.2
            EnemyY[i] += EnemyY_change[i]

        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            enemy_Sound = mixer.Sound('Space_invaders/explosion.wav')
            enemy_Sound.play()
            enemy_Sound.set_volume(0.3)
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(64, 736)
            EnemyY[i] = random.randint(50, 100)

        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    if Bullet_state == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, TextY)
    pygame.display.update()
pygame.quit()
exit()
