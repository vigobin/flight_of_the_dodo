#!/usr/bin/python3

import pygame
import random
import os
from pygame import mixer


pygame.init()

# dimensions and variables
SCREEN_WIDTH = 1000
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

# Play music and sound fx
pygame.mixer.music.load('assets/music/sega1.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)
cloud_fx = pygame.mixer.Sound('assets/music/hit_cloud3.mp3')
fall_fx = pygame.mixer.Sound('assets/music/die1.mp3')
gameover = pygame.mixer.Sound('assets/music/game_over.mp3')


# images to be loaded
bg_image = pygame.image.load('assets/images/sky1.png').convert_alpha()
dodo_image = pygame.image.load('assets/images/dodo1.png').convert_alpha()
cloud_image = pygame.image.load('assets/images/cloud.png').convert_alpha()


def draw_text(text, font, text_col, x, y):
    """Function to output text to the screen"""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def score_board():
    """Function to show the scores at the top"""
    draw_text('SCORE: ' + str(score), font_small, BLACK, 25, 10)
    draw_text('HIGH SCORE: ' + str(high_score), font_small, BLACK, 800, 10)


def draw_bg(bg_scroll):
    """Function to draw the the background"""
    screen.blit(bg_image, (0, 0 + bg_scroll))


class Player():
    """Defines the player class"""
    def __init__(self, x, y):
        self.image = pygame.transform.scale(dodo_image, (100, 100))
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
            self.flip = False
        if key[pygame.K_RIGHT]:
            delta_x = 10
            self.flip = True

        # Creates the falling effect
        self.vel_y += GRAVITY
        delta_y += self.vel_y

        # Prevents the player from moving off the sides of the screen
        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
        if self.rect.right + delta_x > SCREEN_WIDTH:
            delta_x = SCREEN_WIDTH - self.rect.right

        # cloud collision check in y direction
        for cloud in cloud_group:
            if cloud.rect.colliderect(self.rect.x, self.rect.y + delta_y,
                                      self.width, self.height):
                if self.rect.bottom < cloud.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = cloud.rect.top
                        delta_y = 0
                        self.vel_y = -20
                        cloud_fx.play()

        # This has been removed to let the player fall off the
        # bottom of the screen
        """if self.rect.bottom + delta_y > SCREEN_HEIGHT:
            delta_y = 0
            self.vel_y = -20"""

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


class Clouds(pygame.sprite.Sprite):
    """Defines the clouds"""
    def __init__(self, x, y, width):
        """instantiate clouds"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(cloud_image, (150, 125))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        """updates the clouds vertical position"""
        self.rect.y += scroll

        # Checks that clouds are off the screen and
        # terminates the instance
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# creates the player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create the cloud instance
cloud_group = pygame.sprite.Group()

# creates a starting cloud for the player
cloud = Clouds(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 50)
cloud_group.add(cloud)

# This is the game loop
run = True
while run:

    clock.tick(FRAMES)

    if game_over is False:
        scroll = player.move()

        # creates the background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(scroll)

        # generated clouds
        if len(cloud_group) < MAX_CLOUDS:
            c_width = random.randint(20, 20)
            c_x = random.randint(0, SCREEN_WIDTH - c_width)
            c_y = cloud.rect.y - random.randint(60, 80)
            cloud = Clouds(c_x, c_y, c_width)
            cloud_group.add(cloud)

        cloud_group.update(scroll)

        # updated scores
        if scroll > 0:
            score += scroll

        # draw sprites
        cloud_group.draw(screen)
        player.draw()
        score_board()

        # Game over check
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
            pygame.mixer.music.stop()
            fall_fx.play()
            gameover.play()

    else:
        draw_text('GAME OVER', font_big, BLACK, 375, 200)
        draw_text('SCORE: ' + str(score), font_big, BLACK, 375, 250)
        draw_text('PRESS SPACE TO RESTART', font_big,  BLACK, 225, 300)

        # update high score
        if score > high_score:
            high_score = score
            with open('score.txt', 'w') as file:
                file.write(str(high_score))

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # reset variables
            game_over = False
            score = 0
            scroll = 0
            # reposition player
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            cloud_group.empty()
            # create starting cloud
            cloud = Clouds(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 50)
            cloud_group.add(cloud)
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
