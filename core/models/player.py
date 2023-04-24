#!/usr/bin/env python3

import pygame

class Player():
    """DEFINES THE PLACER CHARACTER"""
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
        """CALCULATES THE PLAYERS POSITION ON SCREEN TO TO RE-DRAW"""
        return (
            pygame.transform.flip(self.image, self.flip, False),
            (self.rect.x, self.rect.y)
        )
