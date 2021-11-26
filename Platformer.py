import pygame, sys, random, os, noise, time
import data.engine as e

# Try to figure out how to make enemy jump when near a block / DONE
# Make world destructible / Last
# Better trees
# Water and more objects
# Add sand
# Add clouds
# Learn more

clock = pygame.time.Clock()

from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32, )  # initiate the window

display = pygame.Surface((300, 200))  # used as the surface for rendering, which is scaled

pos = 0
framerate = 60

last_time = time.time()

fullscreen = False
right = False
left = False

enemy_right = False
enemy_left = False
enemy_alive = True
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0, 0]

e_pressed = False
hitbox_value = 0

game_font = pygame.font.Font('Symtext.ttf', 15)
door_text = game_font.render('Press E to continue', 1, (160, 25, 0))
doors_text = False

# Items ---------------------------------------------------------------------------------------------------------------#
sword1_use = False
mouse_click = False

# Particles -----------------------------------------------------------------------------------------------------------#

# particles = e.particle(100, 99, 'data/images/particles/circle', 180, 50, (200, 200, 200))

# CHUNK_SIZE ----------------------------------------------------------------------------------------------------------#
CHUNK_SIZE = 12


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Classes -------------------------------------------------------------------------------------------------------------#
class jumper_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 8, 9)

    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)


class tree_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(tree_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 8, 9)


class sword_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(sword_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 16, 16)

    def collision_test(self, rect):
        sword_rect = self.get_rect()
        return sword_rect.colliderect(rect)


class finish_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(goal_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 8, 15)

    def collision_test(self, rect):
        finish_rect = self.get_rect()
        return finish_rect.colliderect(rect)


global animation_frames
animation_frames = {}

e.load_animations('data/images/entities/')
# e.load_particle_images('data/images/particles/')

game_map = load_map('data/map')
lvl1_map = load_map('data/lvl1')

# Images --------------------------------------------------------------------------------------------------------------#
back_view = pygame.image.load('data/images/back_view.png')
back_view.set_colorkey((255, 255, 255))
grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
grass_top_left_img = pygame.image.load('data/images/grass_top_left.png')
grass_top_left_img.set_colorkey((255, 255, 255))
grass_top_right_img = pygame.image.load('data/images/grass_top_right.png')
grass_top_right_img.set_colorkey((255, 255, 255))
grass_left_img = pygame.image.load('data/images/grass_left.png')
grass_right_img = pygame.image.load('data/images/grass_right.png')
stone_img = pygame.image.load('data/images/stone.png')
plant_img = pygame.image.load('data/images/plant.png').convert()
plant_img.set_colorkey((255, 255, 255))
tree_img = pygame.image.load('data/images/tree.png')
tree_img.set_colorkey((255, 255, 255))
sapling_img = pygame.image.load('data/images/sapling.png').convert()
sapling_img.set_colorkey((255, 255, 255))
jumper_img = pygame.image.load('data/images/jumper.png').convert()
jumper_img.set_colorkey((255, 255, 255))
sword_img = pygame.image.load('data/images/sword.png').convert()
sword_img.set_colorkey((255, 255, 255))
goal_img = pygame.image.load('data/images/goal.png').convert()
goal_img.set_colorkey((255, 255, 255))

cursor = pygame.image.load('data/images/cursor/cursor1.png')

tile_index = {1: grass_img,
              2: dirt_img,
              3: plant_img,
              4: sapling_img,
              5: tree_img
              }

jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'), pygame.mixer.Sound('data/audio/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.play(-1)

grass_sound_timer = 0

# Player --------------------------------------------------------------------------------------------------------------#
player = e.entity(100, 100, 5, 13, 'player')

# Enemy ---------------------------------------------------------------------------------------------------------------#
enemies = []

# Particle
# particles = e.particle(100, 99, 'circle', 180, 50, (200, 200, 200))

for i in range(5):
    enemies.append([0, e.entity(random.randint(0, 600) - 300, 80, 5, 13, 'enemy')])

# 0.5 = light green, 0.25 = dark green
background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 40, 40, 400]], [0.25, [400, 20, 40, 400]],
                      [0.25, [500, 20, 60, 400]], [0.25, [600, 10, 40, 400]], [0.25, [700, 40, 60, 400]],
                      [0.25, [800, 10, 70, 400]], [0.25, [990, 40, 40, 400]], [0.25, [1200, 20, 40, 400]],
                      [0.25, [1380, 20, 60, 400]], [0.25, [1500, 10, 40, 400]], [0.25, [1680, 40, 60, 400]],
                      # -----------------------------------------------------------------------------------------------#
                      [0.5, [50, 40, 40, 400]], [0.5, [275, 100, 120, 400]], [0.5, [500, 60, 60, 400]],
                      [0.5, [720, 90, 100, 400]], [0.5, [970, 80, 50, 400]], [0.5, [1350, 60, 80, 400]],
                      [0.5, [1500, 40, 40, 400]], [0.5, [1750, 100, 120, 400]], [0.5, [1990, 60, 60, 400]],
                      [0.5, [2200, 90, 100, 400]], [0.5, [2470, 80, 50, 400]], [0.5, [2630, 60, 80, 400]],

                      # Same in reverse
                      # -----------------------------------------------------------------------------------------------#
                      [0.25, [-120, 10, 70, 400]], [0.25, [-280, 40, 40, 400]], [0.25, [-400, 20, 40, 400]],
                      [0.25, [-500, 20, 60, 400]], [0.25, [-600, 10, 40, 400]], [0.25, [-700, 40, 60, 400]],
                      [0.25, [-850, 10, 70, 400]], [0.25, [-970, 40, 40, 400]], [0.25, [-1100, 20, 40, 400]],
                      [0.25, [-1260, 20, 60, 400]], [0.25, [-1400, 10, 40, 400]], [0.25, [-1600, 40, 60, 400]],
                      # -----------------------------------------------------------------------------------------------#
                      [0.5, [-50, 40, 40, 400]], [0.5, [-275, 100, 120, 400]], [0.5, [-500, 60, 60, 400]],
                      [0.5, [-720, 90, 100, 400]], [0.5, [-970, 80, 50, 400]], [0.5, [-1350, 60, 80, 400]],
                      [0.5, [-1550, 40, 40, 400]], [0.5, [-1775, 100, 120, 400]], [0.5, [-1900, 60, 60, 400]],
                      [0.5, [-2200, 90, 100, 400]], [0.5, [-2470, 80, 50, 400]], [0.5, [-2650, 60, 80, 400]]]

# Objects -------------------------------------------------------------------------------------------------------------#
jumper_objects = []
tree_objects = []
sword_object = []
finish_object = []

# Hitbox --------------------------------------------------------------------------------------------------------------#
hitbox = pygame.Rect(player.x, player.y, 7, 13)
weapon_hitbox = pygame.Rect(player.x + 4, player.y, 3, 3)

# Random placement in the x-axes within 780 pixels and the y-axes
for i in range(5):
    jumper_objects.append(jumper_obj((780, 70)))

for i in range(5):
    tree_objects.append(tree_obj((190, 50)))
    tree_objects.append(tree_obj((3500, 64)))

for i in range(5):
    sword_object.append(sword_obj((140, 48)))

for i in range(5):
    finish_object.append(finish_obj((4040, 33)))
    finish_object.append(finish_obj((850, 17)))

while True:  # Game loop ----------------------------------------------------------------------------------------------#

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    display.fill((146, 244, 255))  # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    mx, my = pygame.mouse.get_pos()
    mx -= cursor.get_width() / 2
    my -= cursor.get_height() / 2

    true_scroll[0] += (player.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if moving_right == True:
        hitbox_value = -7
    if moving_left == True:
        hitbox_value = 7

    weapon_hitbox = pygame.Rect(player.x - hitbox_value, player.y, 7, 6)

    # Background tiles ------------------------------------------------------------------------------------------------#
    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    pygame.draw.rect(display, (7, 80, 60), pygame.Rect(0, 160, 300, 80))
    screen.blit(back_view, (0, 120))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                               background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                               background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    # Tile rendering --------------------------------------------------------------------------------------------------#
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '3':
                display.blit(grass_top_left_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '4':
                display.blit(grass_top_right_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '5':
                display.blit(grass_left_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '6':
                display.blit(grass_right_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '7':
                display.blit(stone_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    y = 0
    for layer in lvl1_map:
        x = 200
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '3':
                display.blit(grass_top_left_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '4':
                display.blit(grass_top_right_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '5':
                display.blit(grass_left_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '6':
                display.blit(grass_right_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '7':
                display.blit(stone_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    # Player movement -------------------------------------------------------------------------------------------------#
    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2 * dt
    if moving_left == True:
        player_movement[0] -= 2 * dt
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2 * dt
    if vertical_momentum > 3:
        vertical_momentum = 3 * dt

    # Player animation ------------------------------------------------------------------------------------------------#

    if sword1_use == False:
        if player_movement[0] == 0:
            player.set_action('idle')
        if player_movement[0] > 0:
            player.set_flip(False)
            player.set_action('run')
        if player_movement[0] < 0:
            player.set_flip(True)
            player.set_action('run')
    if sword1_use == True:
        if mouse_click == False:
            if player_movement[0] == 0:
                player.set_action('sword')
            if player_movement[0] > 0:
                player.set_flip(False)
                player.set_action('swordrun')
            if player_movement[0] < 0:
                player.set_flip(True)
                player.set_action('swordrun')

    if mouse_click == True:
        if player_movement[0] == 0:
            player.set_action('sword_swing')
        if player_movement[0] > 0:
            player.set_flip(False)
            player.set_action('sword_swing')
        if player_movement[0] < 0:
            player.set_flip(True)
            player.set_action('sword_swing')

    collisions_types = player.move(player_movement, tile_rects)

    if collisions_types['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 15
                random.choice(grass_sounds).play()
    else:
        air_timer += 1 * dt

    player.change_frame(1)
    player.display(display, scroll)

    # New objects -----------------------------------------------------------------------------------------------------#
    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            vertical_momentum = -5

    # display_r = pygame.Rect(scroll[0], scroll[1], 320, 220)

    for enemy in enemies:
        if enemy_alive == True:
            # if display_r.colliderect(enemy[1].obj.rect):
            enemy[0] += 0.2
            if enemy[0] > 3:
                enemy[0] - 3
            enemy_movement = [0, enemy[0]]
            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 1
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1
            collisions_types = enemy[1].move(enemy_movement, tile_rects)
            if collisions_types['bottom'] == True:
                enemy[0] = 0
                if collisions_types['left'] == True:
                    enemy[0] -= 5
                if collisions_types['right'] == True:
                    enemy[0] -= 5

            enemy[1].display(display, scroll)

            if player.obj.rect.colliderect(enemy[1].obj.rect):
                vertical_momentum = -4

            if sword1_use == True:
                if mouse_click == True:
                    if weapon_hitbox.colliderect(enemy[1].obj.rect):
                        enemy_alive = False
                        enemy.pop()

    for tree in tree_objects:
        tree.render(display, scroll)

    for sword in sword_object:
        sword.render(display, scroll)
        if sword.collision_test(player.obj.rect):
            sword_object.remove(sword)
            sword1_use = True

    for finish_obj in finish_object:
        finish_obj.render(display, scroll)
        if finish_obj.collision_test(player.obj.rect):
            if e_pressed == False:
                doors_text = True
            if e_pressed == True:
                player = e.entity(3250, 100, 5, 13, 'player')
        if not finish_obj.collision_test(player.obj.rect):
            doors_text = False

    if right == True:
        player.x += 100
    if left == True:
        player.x -= 100

    # Particles -------------------------------------------------------------------------------------------------------#
    # particles.draw(screen, scroll)
    # pygame.draw.rect(display, (255, 0, 0), weapon_hitbox, 2)
    # if enemy_alive == True:
    #   pygame.draw.rect(display, (0, 255, 0), enemy[1].obj.rect, 2)
    # pygame.draw.rect(display, (0, 100, 100), player.obj.rect, 2)

    for event in pygame.event.get():  # Event loop --------------------------------------------------------------------#
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if sword1_use == True:
                    mouse_click = True
                    print("work")
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_click = False
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_e:
                e_pressed = True
            if event.key == pygame.K_t:
                framerate = 144
            if event.key == pygame.K_r:
                framerate = 60
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_o:
                pygame.mixer.music.fadeout(1000)
            if event.key == pygame.K_p:
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w:
                if air_timer < 6:
                    jump_sound.play()
                    jump_sound.set_volume(0.2)
                    vertical_momentum = -5
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    pygame.display.set_mode(monitor_size, pygame.FULLSCREEN, 0, 32)
                else:
                    pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_e:
                e_pressed = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    if fullscreen:
        screen.blit(pygame.transform.scale(display, monitor_size), (0, 0))
    screen.blit(cursor, (mx, my))
    for finish_obj in finish_object:
        if not fullscreen:
            if doors_text == True:
                screen.blit(door_text, (finish_obj.loc[0] + 100 - scroll[0], finish_obj.loc[1] + 80 - scroll[1]))
        if fullscreen:
            if doors_text == True:
                screen.blit(door_text, (finish_obj.loc[0] + 100 / 25 + monitor_size[0] / 2.5 - scroll[0],
                                        finish_obj.loc[1] + 100 / 25 + monitor_size[1] / 2.5 - scroll[1]))
    # print(player.x, player.y)
    pygame.display.update()
    clock.tick(framerate)
