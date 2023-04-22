import pygame
import random


pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FRAMES = 40

SCROLL_THRESH = 200
GRAVITY = 1
MAX_CLOUDS = 10
scroll = 0

bg_image = pygame.image.load('assets/images/sky.png').convert_alpha()
dodo_image = pygame.image.load('assets/images/dodo.png').convert_alpha()
cloud_image = pygame.image.load('assets/images/cloud.png').convert_alpha()


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

        if self.rect.bottom + delta_y > SCREEN_HEIGHT:
            delta_y = 0
            self.vel_y = -20

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


player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

cloud_group = pygame.sprite.Group()

for c in range(MAX_CLOUDS):
    c_width = random.randint(40, 60)
    c_x = random.randint(0, SCREEN_WIDTH - c_width)
    c_y = c * random.randint(80, 120)
    cloud = Clouds(c_x, c_y, c_width)
    cloud_group.add(cloud)

run = True
while run:

    player.move()

    clock.tick(FRAMES)

    screen.blit(bg_image, (0, 0))

    pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH),
                     (SCREEN_WIDTH, SCROLL_THRESH))

    cloud_group.update(scroll)

    cloud_group.draw(screen)

    player.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
