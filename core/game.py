#!/usr/bin/env python3

import json
import random

from models import *

# XY CORRDINATES ARE ALWAYS REPRESENTED AS A TUPLE '(x_pos, y_pos)' --
X = 0
Y = 1

class GameManager:
    """UTILITY CLASS TO MANAGE INDIVIDUAL INSTANCES OF THE GAME"""
    config_file_name = "game_config.json"
    config = json.loads(
        DataRetrieverTool.get_file_data(config_file_name)
    )
    DISPLAY_SETTINGS = config.get("display_settings")
    SOUNDS = config.get("sounds")
    CONSTANTS = config.get("game_constants")
    HIGH_SCORE = DataRetrieverTool.get_file_data(
        config.get("high_score")
    )

    def __init__(self):
        """INITALIZES A NEW INSTANCE OF THE GAME"""
        self.screen = ""
        self.sound_mix = None
        self.clock = pygame.time.Clock()
        self.player = None
        self.cloud_group = pygame.sprite.Group()
        self.scroll = 0
        self.bg_scroll = 0
        self.is_active = True
        self.game_over = False

        while is_active:

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
            else:
                draw_text('GAME OVER', font_big, BLACK, 500, 200)
                draw_text('SCORE: ' + str(score), font_big, BLACK, 500, 250)
                draw_text('PRESS SPACE TO RESTART', font_big,  BLACK, 400, 300)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()


    def redraw_player(self):
        """REDRAWS PLAYER CHARACTER IN UPDATED POSITION ON SCREEN"""
        self.screen.blit(
            pygame.transform.flip(player.image, player.flip, False),
            (player.rect.x, player.rect.y)
        )


    def spawn_cloud(self, cloud_pos, width):

    @classmethod
    def draw_text(cls, game, text, text_pos):
        """OUTPUT TEXT TO GIVEN SCREEN LOCATION"""
        img = font.render(text, True, text_col)
        screen.blit(img, (text_pos[X], text_pos[Y]))


    @classmethod
    def score_board(cls, game):
        """Function to show the scores at the top"""
        draw_text('SCORE: ' + str(score), font_small, BLACK, 0, 0)
        draw_text('HIGH SCORE: ' + str(high_score), font_small, BLACK, 1000, 0)


    @classmethod
    def draw_background(cls, game):
        """DRAWS THE BACKGROUND"""
        game.screen.blit(
            bg_image,
            (0, (0 + game.bg_scroll))
        )
