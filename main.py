import pygame
import os
import sys
from random import sample, randint
from time import time
from pygame.locals import *
import sqlite3


class Menu:

    def __init__(self):
        # load all image-----------------------------------------
        self.button_play = LoadSprites.load_image('menu/button_play.png')
        self.button_settings = LoadSprites.load_image('menu/button_settings.png')
        self.button_score = LoadSprites.load_image('menu/button_scoreboard.png')
        self.background = LoadSprites.load_image('menu/menu_background.png')
        self.button_restart = LoadSprites.load_image('menu/button_restart.png')
        self.game_over_img = LoadSprites.load_image('menu/game_over.png')

        # scale some image-----------------------------------------
        self.background = pygame.transform.scale(self.background, (width, height))

        # constants------------------------------------------------
        self.games_started = False
        self.button_play_size = self.button_play.get_size()
        self.button_settings_size = self.button_settings.get_size()
        self.button_score_size = self.button_score.get_size()

        # pos to buttons---------------------------------------
        self.button_play_rect = self.button_play.get_rect().move(
            width // 2 - self.button_play_size[0] // 2,
            height // 3 - self.button_play_size[1] // 2
        )

        self.button_settings_rect = self.button_settings.get_rect().move(
            width // 2 - self.button_settings_size[0] // 2,
            height - height // 3 - self.button_settings_size[1] // 2
        )

        self.button_score_rect = self.button_score.get_rect().move(
            width // 2 - self.button_score_size[0] // 2,
            height // 2 - self.button_score_size[1] // 2
        )

        self.button_restart_rect = self.button_restart.get_rect().move(
            width // 2 - self.button_restart.get_size()[0] // 2,
            height // 2 - self.button_restart.get_size()[1] // 2
        )

    def draw_menu(self):
        # draw background
        screen.blit(self.background, (0, 0))

        # button "start player"
        screen.blit(
            self.button_play, (width // 2 - self.button_play_size[0] // 2
                               , height // 3 - self.button_play_size[1] // 2)
        )

        screen.blit(
            self.button_score, (width // 2 - self.button_score_size[0] // 2
                                , height // 2 - self.button_score_size[1] // 2)
        )

        screen.blit(
            self.button_settings, (width // 2 - self.button_settings_size[0] // 2
                                   , height - height // 3 - self.button_settings_size[1] // 2)
        )

    def game_over(self):
        # image of game over
        screen.blit(self.game_over_img, (
            width // 2 - self.game_over_img.get_size()[0] // 2,
            height // 3 - self.game_over_img.get_size()[1] // 2
        ))

        # restart button
        screen.blit(self.button_restart, (
            width // 2 - self.button_restart.get_size()[0] // 2,
            height // 2 - self.button_restart.get_size()[1] // 2
        ))

    def update(self, pos):
        # if user clicked to 'button'
        if not self.games_started:
            if self.button_play_rect.collidepoint(pos):
                self.games_started = True

            elif self.button_score_rect.collidepoint(pos):
                score_board.draw_score()

            elif self.button_settings_rect.collidepoint(pos):
                print('SETTINGS')

        elif self.games_started:
            if self.button_restart_rect.collidepoint(pos):
                print('RESTART')


class SettingsMenu:
    def __init__(self):
        pass


class ScoreBoard:
    def __init__(self):
        pass

    def draw_score(self):
        screen.fill('white')


class LoadSprites(pygame.sprite.Sprite):
    def __init__(self):
        super(LoadSprites, self).__init__(coin_group)
        # load_image------------
        self.image = self.load_image('coin.png')
        self.road = self.load_image('road.png')
        self.hp = self.load_image('hp.png')

        # scale_image---------
        self.road = pygame.transform.scale(self.road, (width, height))

        # constants-----------
        self.rect = self.image.get_rect()

    @staticmethod
    def load_image(name, color_key=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        return pygame.image.load(fullname)

    def draw_ground(self):
        screen.blit(self.road, (0, 0))

    def draw_hp(self, hp):
        offset_y = self.hp.get_size()[1]
        x_pos = 5
        y_pos = 5

        for _ in range(hp):
            screen.blit(self.hp, (x_pos, y_pos))
            y_pos += offset_y

    def draw_coin(self, pos):
        self.rect.center = list(pos)[0], 0

    def update(self):
        global coin_counter
        if pygame.sprite.spritecollide(player, coin_group, True):
            coin_counter += 1
        else:
            self.rect.y += speed


class Pause:

    def __init__(self):
        # constants-----------------------
        self.is_pause_on = False

        # load image-----------------------
        self.pause_img = LoadSprites.load_image('pause/background.png')

        # scale image
        self.pause_img = pygame.transform.scale(self.pause_img, (width, height))

    def pause(self):
        if self.is_pause_on:
            screen.blit(self.pause_img, (0, 0))


class Player(pygame.sprite.Sprite):
    player_img = LoadSprites.load_image('enemy/car.png')
    player_img = pygame.transform.scale(player_img, (110, 155))

    def __init__(self):
        super(Player, self).__init__(player_group)
        self.image = self.player_img
        self.rect = self.image.get_rect()
        self.rect.center = width // 2, height // 2
        self.size = {'x': self.image.get_size()[0],
                     'y': self.image.get_size()[1]}
        self.step_y = 3
        self.step_x = width // 4
        self.quantity = 0

    def moving(self, direction):
        global start

        delay = 0.5

        if direction == 'left' and \
                self.rect.centerx - \
                self.step_x >= width // 4 and \
                end - start >= delay:
            self.rect.x -= self.step_x
            start = time()

        elif direction == 'right' and \
                self.rect.centerx + \
                self.step_x <= width - width // 4 and \
                end - start >= delay:
            self.rect.x += self.step_x
            start = time()

        elif direction == 'up' and \
                self.rect.centery - self.step_y \
                >= self.size['y'] // 2:
            self.rect.y -= self.step_y

        elif direction == 'down' and \
                self.rect.centery + self.step_y \
                <= height - self.size['y'] // 2:
            self.rect.y += self.step_y

    def update(self, users_time=time()):
        global invulnerability,\
            health_points,\
            invulnerability_time,\
            is_game_over

        if invulnerability:
            self.quantity += 1

            if time() - users_time >= 2:
                invulnerability = False

            if self.quantity % 2 != 0:
                self.image.set_alpha(127)

            else:
                self.image.set_alpha(254)
        else:
            self.quantity = 0
            self.image.set_alpha(254)

        if pygame.sprite.spritecollide(player, mobs_group, False) \
                and not invulnerability:
            health_points -= 1
            invulnerability = True
            invulnerability_time = time()

        if health_points <= 0:
            is_game_over = True


class Opponents(pygame.sprite.Sprite):

    def __init__(self, x):
        super(Opponents, self).__init__(mobs_group)
        self.enemy = 'enemy' + str(randint(1, 5)) + '.png'
        self.image = LoadSprites.load_image('enemy/' + self.enemy)
        self.image = pygame.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect()
        self.rect.center = x, -self.image.get_size()[1]
        self.speed = 1

    def update(self, speed):
        global opponents
        if speed >= 5:
            speed = 5
        if self.rect.y <= height:
            self.rect.y += speed


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()
    mobs_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    size = width, height = 600, 600
    health_points = 3
    invulnerability = False
    invulnerability_time = time()
    speed = 1
    coin_counter = 0
    screen = pygame.display.set_mode(size=size)
    is_game_paused = False
    is_game_over = False

    menu = Menu()
    player = Player()
    background = LoadSprites()
    start = time()
    pause = Pause()
    score_board = ScoreBoard()

    pos_for_ops = [width // 4, width // 2, width - width // 4]
    opponents = []

    # add new opponents
    for pos in sample(pos_for_ops, 2):
        opponents.append(Opponents(pos))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started:
                menu.update(event.pos)

            # pause menu
            elif event.type == pygame.KEYDOWN and menu.games_started:
                if event.key == pygame.K_ESCAPE:
                    if is_game_paused:
                        pause.is_pause_on = False
                        is_game_paused = False
                    else:
                        pause.is_pause_on = True
                        is_game_paused = True
                    pause.pause()

        if pygame.key.get_pressed()[K_UP]:
            end = time()
            player.moving('up')

        elif pygame.key.get_pressed()[K_DOWN]:
            end = time()
            player.moving('down')

        elif pygame.key.get_pressed()[K_LEFT]:
            end = time()
            player.moving('left')

        elif pygame.key.get_pressed()[K_RIGHT]:
            end = time()
            player.moving('right')

        if menu.games_started and not is_game_paused and not is_game_over:
            background.draw_ground()
            player.update(invulnerability_time)
            mobs_group.draw(screen)
            mobs_group.update(speed)
            player_group.draw(screen)
            background.draw_hp(health_points)
            coin_group.draw(screen)
            coin_group.update()

        elif not menu.games_started and not is_game_paused and not is_game_over:
            screen.fill('white')
            menu.draw_menu()

        elif is_game_paused:
            pause.pause()

        elif is_game_over:
            menu.games_started = False
            menu.game_over()

        # add new opponents
        if opponents[-1].rect.y >= height // 2 \
                and opponents[-2].rect.y >= height // 2:
            used_pos = sample(pos_for_ops, 2)
            for pos in used_pos:
                opponents.append(Opponents(pos))
                speed += 0.5
            if 2 == 2:
                background.draw_coin(set(pos_for_ops).difference(used_pos))

        # del opponents that was out of screen
        if opponents[0].rect.y >= height \
                and opponents[0].rect.y >= height:
            opponents.pop(0) and opponents.pop(0)

        pygame.display.flip()
        clock.tick(fps)
        # print(coin_counter)
    pygame.quit()
