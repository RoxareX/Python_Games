import pygame
import random
import sys
import os


class CreateParticle:
    def __init__(self, screen, circle_radius, radius_x, radius_y, gravity):
        self.particles = []
        self.radius = circle_radius
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.screen = screen
        self.gravity = gravity

    # Moves and draws the particles
    def emit(self, color):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                # move, shrink, draw a circle around the particle
                particle[0][1] += particle[2][1]
                particle[0][0] += particle[2][0]
                particle[2][1] += self.gravity
                particle[1] -= self.radius
                pygame.draw.circle(self.screen, color, particle[0], int(particle[1]))

    # Adds particles
    def add_particles(self, x, y, direction_x, direction_y):
        pos_x = x
        pos_y = y
        radius = random.randint(self.radius_x, self.radius_y)
        direction_x = direction_x
        direction_y = direction_y
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


""" ----------------------------------------------------------------
Image Particle:


---------------------------------------------------------------- """
global animation_frames
animation_frames = {}


class CreateImgParticle:
    def __init__(self, screen, gravity):
        self.particles = []
        self.screen = screen
        self.gravity = gravity
    
    def update_img(self, image):
        self.img = image
    
    def emit(self, particle_frame, particle_action, image):
        if self.particles:
            self.delete_particles(particle_frame, particle_action)
            for particle in self.particles:
                # move, shrink, draw a circle around the particle
                # [0] = pos, [1] = radius, [2] = direction
                particle[0][1] += particle[2][1]
                particle[0][0] += particle[2][0]
                particle[2][1] += self.gravity

                self.update_img(image)
                self.screen.blit(self.img, particle[0])

    def add_particles(self, x, y, direction_x, direction_y):
        pos_x = x
        pos_y = y
        radius = random.randint(6, 10)
        direction_x = direction_x
        direction_y = direction_y
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)
    
    def delete_particles(self, particle_frame, particle_action):
        for particle in self.particles:
            if particle_frame >= len(animation_database[particle_action]):
                self.particles.pop(self.particles.index(particle))

        # particle_copy = [particle for particle in self.particles if particle[0][0] > 500]
        # self.particles = particle_copy


def load_animation(path,frame_durations): # [7,7] every 7 frames, the amount of 7 is the amount of pictures that you have
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data
    
def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

global animation_database
animation_database = {}