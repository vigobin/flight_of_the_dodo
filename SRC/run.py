import pygame
import random
import os

pygame.init()

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

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

bg_image = pygame.image.load('assets/images/sky.png').convert_alpha()
dodo_image = pygame.image.load('assets/images/dodo.png').convert_alpha()
cloud_image = pygame.image.load('assets/images/cloud.png').convert_alpha()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def score_board():
    draw_text('SCORE: ' + str(score), font_small, BLACK, 0, 0)
    draw_text('HIGH SCORE: ' + str(high_score), font_small, BLACK, 1000, 0)


def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(dodo_image, (80, 80))
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
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

        self.vel_y += GRAVITY
        delta_y += self.vel_y

        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
        if self.rect.right + delta_x > SCREEN_WIDTH:
            delta_x = SCREEN_WIDTH - self.rect.right

        for cloud in cloud_group:
            if cloud.rect.colliderect(self.rect.x, self.rect.y + delta_y,
                                      self.width, self.height):
                if self.rect.bottom < cloud.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = cloud.rect.top
                        delta_y = 0
                        self.vel_y = -20

        """This has been removed to let the player fall off the
        bottom of the screen"""
        """if self.rect.bottom + delta_y > SCREEN_HEIGHT:
            delta_y = 0
            self.vel_y = -20"""

        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -delta_y

        self.rect.x += delta_x
        self.rect.y += delta_y + scroll

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x, self.rect.y))


class Clouds(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(cloud_image, (150, 125))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

cloud_group = pygame.sprite.Group()


cloud = Clouds(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 50)
cloud_group.add(cloud)


run = True
while run:

    scroll = player.move()

    clock.tick(FRAMES)
    if game_over is False:
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(scroll)

        if len(cloud_group) < MAX_CLOUDS:
            c_width = random.randint(20, 20)
            c_x = random.randint(0, SCREEN_WIDTH - c_width)
            c_y = cloud.rect.y - random.randint(60, 80)
            cloud = Clouds(c_x, c_y, c_width)
            cloud_group.add(cloud)

        cloud_group.update(scroll)

        if scroll > 0:
            score += scroll

        draw_text('HIGH SCORE', font_small, BLACK, SCREEN_WIDTH - 130,
                  score - high_score + SCROLL_THRESH)

        cloud_group.draw(screen)
        player.draw()
        score_board()

        """Game over check"""
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
    else:
        draw_text('GAME OVER', font_big, BLACK, 500, 200)
        draw_text('SCORE: ' + str(score), font_big, BLACK, 500, 250)
        draw_text('PRESS SPACE TO RESTART', font_big,  BLACK, 400, 300)

        if score > high_score:
            high_score = score
            with open('score.txt', 'w') as file:
                file.write(str(high_score))

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            scroll = 0
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            cloud_group.empty()
            cloud = Clouds(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 50)
            cloud_group.add(cloud)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
