# Setup Python ----------------------------------------------- #
import pygame, sys, random

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 16)


# Classes ---------------------------------------------------- #
# class obstacles():
# def __init__(self, loc):
# self.loc = loc

# def render(self, screen):
# screen.blit(obstacles_img, (self.loc[0], self.loc[1]))

# def get_rect(self):
# return pygame.Rect(self.loc[0], self.loc[1], 120, 60)

# def collision_test(self, rect):
# obstacles_rect = self.get_rect()
# return obstacles_rect.colliderect(rect)

def create_obs():
    random_obs_pos = random.choice(obs_width)
    bottom_obs = obs_surface.get_rect(midleft=(random.randint(100, 500), random_obs_pos))
    top_obs = obs_surface.get_rect(midright=(random.randint(100, 500), random_obs_pos))
    return bottom_obs, top_obs


def move_obs(obss):
    for obst in obss:
        obst.centery += 3
    return obss


def draw_obs(obss):
    for obst in obss:
        screen.blit(obs_surface, obst)


def check_collision(obss):
    for obs in obss:
        if player_hitbox.colliderect(obs):
            pygame.quit()
            quit()


def score_display():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(250, 70))
    screen.blit(score_surface, score_rect)


# if player is too much at the top or bottom
# if player_hitbox.top <= -100 or player_hitbox.bottom >= 900:
# return False


rect_color = 100, 30, 80
obstacles_x = random.randint(0, 500)
obs_surface = pygame.image.load('particle_game/images/obstacle.png')
obs_width = [10, 50, -10]
SPAWNOBS = pygame.USEREVENT
pygame.time.set_timer(SPAWNOBS, 1200)
bg = pygame.image.load('particle_game/images/bg.png')
bg = pygame.transform.scale2x(bg)

# Player ----------------------------------------------------- #

player_up = False
player_down = False
player_right = False
player_left = False
player_x = 235
player_y = 215
player = pygame.image.load('particle_game/images/player.png').convert()
player = pygame.transform.scale2x(player)
player_hitb_img = pygame.image.load('particle_game/images/player_hitbox.png')
player_hitb_img = pygame.transform.scale2x(player_hitb_img)
player.set_colorkey((255, 255, 255))
player_hitbox = player_hitb_img.get_rect(center=(0, 0))

# Score ------------------------------------------------------ #
score = 0
game_font = pygame.font.SysFont(None, 40)

# a particle is...
# a thing that exists at a location
# typically moves around
# typically changes over time
# and typically disappears after a certain amount of time

obstacles_obj = []
obs_list = []

# for i in range(5):
# obstacles_obj.append(obstacles((random.randint(0, 500))))

# [loc, velocity, timer]
particles = []
particles2 = []

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((50, 100, 100))
    screen.blit(bg, (0, 0))
    mx, my = pygame.mouse.get_pos()
    particles.append([[player_x + 9, player_y + 32], [random.randint(0, 10) / 10 - 1, -2], random.randint(1, 4)])
    particles2.append([[player_x + 23, player_y + 32], [random.randint(0, 10) / 10 - 1, -2], random.randint(1, 4)])
    obs_list = move_obs(obs_list)
    draw_obs(obs_list)
    player_hitbox.centerx = player_x + 16
    player_hitbox.centery = player_y + 16
    check_collision(obs_list)

    for particle in particles:
        # particle[0][0] += particle[1][0]
        particle[0][1] -= particle[1][1]
        particle[2] -= 0.2
        particle[1][1] -= 0.5
        pygame.draw.circle(screen, (255, 252, 187), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

    for particle2 in particles2:
        # particle2[0][0] -= particle2[1][0]
        particle2[0][1] -= particle2[1][1]
        particle2[2] -= 0.2
        particle2[1][1] -= 0.5
        pygame.draw.circle(screen, (255, 252, 187), [int(particle2[0][0]), int(particle2[0][1])], int(particle2[2]))
        if particle2[2] <= 0:
            particles2.remove(particle2)

    # New obstacles ------------------------------------------ #
    for obs in obstacles_obj:
        obs.render(screen)

    # Player movement ---------------------------------------- #
    if player_up == True:
        player_y -= 5
        player_hitbox.centery -= 5
    if player_down == True:
        player_y += 5
        player_hitbox.centery += 5
    if player_right == True:
        player_x += 5
        player_hitbox.centerx += 5
    if player_left == True:
        player_x -= 5
        player_hitbox.centerx -= 5

    # Border ------------------------------------------------- #
    if player_x > 470:
        player_x = 2
    if player_x < -5:
        player_x = 470
    if player_y < 250:
        player_y += 5
    if player_y > 470 - 1:
        player_y -= 5

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWNOBS:
            obs_list.extend(create_obs())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_w:
                player_up = True
            if event.key == pygame.K_s:
                player_down = True
            if event.key == pygame.K_a:
                player_left = True
            if event.key == pygame.K_d:
                player_right = True
            if event.key == pygame.K_p:
                player_hitbox.center = (235, 215)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_up = False
            if event.key == pygame.K_s:
                player_down = False
            if event.key == pygame.K_a:
                player_left = False
            if event.key == pygame.K_d:
                player_right = False

    # Get the player on the screen --------------------------- #
    screen.blit(player, (player_x, player_y))
    # Player's Hitbox
    # pygame.draw.rect(screen, (255, 0, 0), player_hitbox, 2)

    # Score display
    score += 0.01
    score_display()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
