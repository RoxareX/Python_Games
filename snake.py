import time
import pygame, sys
import random
import math
import os
from pygame import mixer
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

orangecolor = (255, 123, 7)
blackcolor = (0, 0, 0)
redcolor = (213, 50, 80)
greencolor = (0, 255, 0)
bluecolor = (50, 153, 213)

display_width = 600
display_height = 400
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')
snake_block = 10
snake_speed = 15
snake_list = []


# Defines the snake's structure and position
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, orangecolor, [x[0], x[1], snake_block, snake_block])


# Main function
def snakegame():
    game_over = False
    game_end = False
    # Co-ordinates of the snake
    x1 = display_height / 2
    y1 = display_height / 2
    # When the snake moves
    x1_change = 0
    y1_change = 0

    snake_list = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10

    # Score
    score_value = 0
    font = pygame.font.SysFont("comicsansms", 20)

    textX = 10
    TextY = 10

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 0, 0))
        dis.blit(score, (x, y))

    while not game_over:
        while game_end == True:
            dis.fill(bluecolor)
            font_style = pygame.font.SysFont("comicsansms", 25)
            mesg = font_style.render("You Lost! Wanna play again? Press P", True, redcolor)
            dis.blit(mesg, [display_width / 6, display_height / 3])

            score = Length_of_snake - 1
            score_font = pygame.font.SysFont("comicsansms", 35)
            value = score_font.render("Your Score: " + str(score), True, greencolor)
            dis.blit(value, [display_width / 3, display_height / 5])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        snakegame()
                if event.type == pygame.QUIT:
                    game_over = True  # The game window is still open
                    game_end = False  # Game has been ended

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    os.startfile('F:\Pycharm\Game Bot\main.py')
                    exit()
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_end = True
        # Updated co-ordinates with the changed positions
        x1 += x1_change
        y1 += y1_change
        # dis.fill(blackcolor)
        # RGB - Red, Green, Blue
        dis.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.draw.rect(dis, greencolor, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        show_score(textX, TextY)

        if len(snake_list) > Length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_end = True
        snake(snake_block, snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score_value += 1
            print(score_value)
        clock.tick(snake_speed)
    pygame.quit()
    exit()

    # Game loop
    running = True
    while running:
        show_score(textX, TextY)
        pygame.display.update()


snakegame()
