#!/usr/bin/env python3

import pygame

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
