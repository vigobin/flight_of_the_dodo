#!/usr/bin/env python3

import pygame
import random
import os

pygame.init()

# dimensions and variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAMES = 40
SCROLL_THRESH = 250
GRAVITY = 1
MAX_CLOUDS = 10
scroll = 0
bg_scroll = 0
game_over = False
font_small = pygame.font.SysFont('', 30)
font_big = pygame.font.SysFont('', 60)
score = 0

# creates score file
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set frame per seconds, refer to FRAMES variable
clock = pygame.time.Clock()

# images to be loaded
bg_image = pygame.image.load('assets/images/sky.png').convert_alpha()
dodo_image = pygame.image.load('assets/images/dodo.png').convert_alpha()
cloud_image = pygame.image.load('assets/images/cloud.png').convert_alpha()


def draw_text(text, font, text_col, x, y):
    """Function to output text to the screen"""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def score_board():
    """Function to show the scores at the top"""
    draw_text('SCORE: ' + str(score), font_small, BLACK, 0, 0)
    draw_text('HIGH SCORE: ' + str(high_score), font_small, BLACK, 1000, 0)


def draw_bg(bg_scroll):
    """Function to draw the the background"""
    screen.blit(bg_image, (0, 0 + bg_scroll))


class Player():
    """Defines the player class"""
    def __init__(self, x, y):
        self.image = pygame.transform.scale(dodo_image, (80, 80))
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        """Uses left and right arrows for player movement"""
        delta_x = 0
        delta_y = 0
        scroll = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            delta_x = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            delta_x = 10
            self.flip = False

        # Creates the falling effect
        self.vel_y += GRAVITY
        delta_y += self.vel_y

        # Prevents the player from moving off the sides of the screen
        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
        if self.rect.right + delta_x > SCREEN_WIDTH:
            delta_x = SCREEN_WIDTH - self.rect.right

        # cloud collision check
        for cloud in cloud_group:
            if cloud.rect.colliderect(self.rect.x, self.rect.y + delta_y,
                                      self.width, self.height):
                if self.rect.bottom < cloud.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = cloud.rect.top
                        delta_y = 0
                        self.vel_y = -20

        # Checks that the player has reached a specific threshold
        # towards the top
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -delta_y

        # This rectangle moves with the player to define to position
        self.rect.x += delta_x
        self.rect.y += delta_y + scroll

        return scroll

    def draw(self):
        """Defines the player position"""
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x, self.rect.y))




# creates the player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create the cloud instance
cloud_group = pygame.sprite.Group()

# creates a starting cloud for the player
cloud = Clouds(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 50)
cloud_group.add(cloud)