import pygame
import os
import sys
from random import sample, randint
from time import time
from pygame.locals import *
import sqlite3


class Menu:

    def __init__(self):
        # load all image-------------------------------------------
        self.button_play = \
            LoadSprites.load_image('menu/button_play.png')
        self.button_settings = \
            LoadSprites.load_image('menu/button_settings.png')
        self.button_score = \
            LoadSprites.load_image('menu/button_scoreboard.png')
        self.background = \
            LoadSprites.load_image('menu/menu_background.png')
        self.button_restart = \
            LoadSprites.load_image('menu/button_restart.png')
        self.game_over_img = \
            LoadSprites.load_image('menu/game_over.png')

        # scale image----------------------------------------------
        self.background = pygame.transform.scale(
            self.background,
            (width, height))

        # constants------------------------------------------------
        self.games_started = False
        self.button_play_size = self.button_play.get_size()
        self.button_settings_size = self.button_settings.get_size()
        self.button_score_size = self.button_score.get_size()

        # pos to buttons-------------------------------------------
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
            self.button_play, (width // 2
                               - self.button_play_size[0] // 2,
                               height // 3
                               - self.button_play_size[1] // 2)
        )

        screen.blit(
            self.button_score, (width // 2
                                - self.button_score_size[0] // 2,
                                height // 2
                                - self.button_score_size[1] // 2)
        )

        screen.blit(
            self.button_settings, (width // 2
                                   - self.button_settings_size[0] // 2,
                                   height -
                                   height // 3 -
                                   self.button_settings_size[1] // 2)
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
        if not self.games_started and not is_game_over:
            if self.button_play_rect.collidepoint(pos):
                self.games_started = True

            elif self.button_score_rect.collidepoint(pos):
                score_board.is_scoreboard_on = True

            elif self.button_settings_rect.collidepoint(pos):
                settings.settings_on = True

        elif is_game_over:
            if self.button_restart_rect.collidepoint(pos):
                Main.start()


class SettingsMenu:
    def __init__(self):
        # load all image-----------------------------------------
        self.background = \
            LoadSprites.load_image('settings/background.png')
        self.percent_0 = \
            LoadSprites.load_image('settings/0.0.png')
        self.percent_25 = \
            LoadSprites.load_image('settings/0.25.png')
        self.percent_50 = \
            LoadSprites.load_image('settings/0.50.png')
        self.percent_75 = \
            LoadSprites.load_image('settings/0.75.png')
        self.percent_100 = \
            LoadSprites.load_image('settings/0.100.png')
        self.button_up = \
            LoadSprites.load_image('settings/button_up.png')
        self.button_down = \
            LoadSprites.load_image('settings/button_down.png')

        # scale image----------------------------------------------
        self.background = pygame.transform.scale(
            self.background,
            (width, height)
        )

        # constants------------------------------------------------
        self.settings_on = False
        self.button_up_music_rect = self.button_up.get_rect().move(
            width // 2,
            height // 3
        )
        self.button_down_music_rect = self.button_up.get_rect().move(
            width // 2 + self.button_up.get_size()[0] + 10,
            height // 3
        )
        self.button_up_vfx_rect = self.button_up.get_rect().move(
            width // 2,
            height // 2
        )
        self.button_down_vfx_rect = self.button_up.get_rect().move(
            width // 2 + self.button_up.get_size()[0] + 10,
            height // 2)
        self.percents = [
            self.percent_0,
            self.percent_25,
            self.percent_50,
            self.percent_75,
            self.percent_100
        ]

    def draw_menu(self):
        screen.blit(self.background, (0, 0))

        screen.blit(self.button_up, (
            (width // 2,
             height // 3)
        ))

        screen.blit(self.button_down, ((
            width // 2 + self.button_up.get_size()[0] + 10,
            height // 3)
        ))

        screen.blit(self.button_up, ((
            width // 2,
            height // 2)
        ))

        screen.blit(self.button_down, ((
            width // 2 + self.button_up.get_size()[0] + 10,
            height // 2)
        ))

        self.draw_percent(
            self.percents[volume_music // 25],
            self.percents[volume_vfx // 25]
        )

    def update(self, pos):
        global volume_music, volume_vfx
        if self.button_up_music_rect.collidepoint(pos):
            if volume_music != 100:
                volume_music += 25

        elif self.button_down_music_rect.collidepoint(pos):
            if volume_music != 0:
                volume_music -= 25

        elif self.button_up_vfx_rect.collidepoint(pos):
            if volume_vfx != 100:
                volume_vfx += 25

        elif self.button_down_vfx_rect.collidepoint(pos):
            if volume_vfx != 0:
                volume_vfx -= 25

        coin_sound.set_volume(volume_vfx / 100)
        player_crush.set_volume(volume_vfx / 100)
        main_sound.set_volume(volume_music / 100)
        menu_sound.set_volume(volume_music / 100)
        pause_sound.set_volume(volume_music / 100)
        game_over_sound.set_volume(volume_music / 100)
        self.draw_percent(
            self.percents[volume_music // 25],
            self.percents[volume_vfx // 25]
        )

    def draw_percent(self, percent_music, percent_vfx):
        screen.blit(percent_music, (
            width // 2 - percent_music.get_size()[0] - 10,
            height // 3
        ))

        screen.blit(percent_vfx, (
            width // 2 - percent_vfx.get_size()[0] - 10,
            height // 2
        ))


class ScoreBoard:
    def __init__(self):
        # load all image-----------------------------------------
        self.main_background = LoadSprites.load_image('scoreboard/main_background.png')
        self.background = LoadSprites.load_image('scoreboard/background.png')
        self.button_left = LoadSprites.load_image('scoreboard/left.png')
        self.button_right = LoadSprites.load_image('scoreboard/right.png')

        # scale image----------------------------------------------
        self.main_background = pygame.transform.scale(
            self.main_background,
            (width, height)
        )
        self.background = pygame.transform.scale(
            self.background,
            (width, height)
        )

        # constants------------------------------------------------
        self.button_right_rect = self.button_right.get_rect().move(
            (width - 30 - self.button_right.get_size()[0],
             height - 30)
        )
        self.button_left_rect = self.button_left.get_rect().move(
            (30,
             height - 30)
        )
        self.is_scoreboard_on = False

    def draw_score(self):
        screen.blit(self.main_background, (0, 0))
        screen.blit(self.button_left, self.button_left_rect)
        screen.blit(self.button_right, self.button_right_rect)

    def update(self, pos):
        if self.button_left_rect.collidepoint(pos):
            print('left')
        elif self.button_right_rect.collidepoint(pos):
            print('right')


class Main:
    def __init__(self):
        pass

    @staticmethod
    def start():
        global health_points, invulnerability, \
            invulnerability_time, speed, coin_counter, is_game_paused, \
            is_game_over, menu, player, background, start, \
            pause, score_board, mobs_group, player_group, \
            coin_group, opponents, text, coins, used_pos

        health_points = 3
        invulnerability = False
        invulnerability_time = time()
        speed = 1
        coin_counter = 0
        is_game_paused = False
        is_game_over = False
        opponents = []
        coins = []
        used_pos = sample(pos_for_ops, 2)
        text = font.render(str(coin_counter), False, (0, 0, 0))

        player = Player()
        background = LoadSprites()

        mobs_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        coin_group = pygame.sprite.Group()

        for position in used_pos:
            opponents.append(Opponents(position))
            if randint(0, 5) == 2:
                coins.append(
                    LoadSprites().draw_coin(
                        set(pos_for_ops).difference(used_pos)
                    )
                )

    @staticmethod
    def move():
        global end
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

    @staticmethod
    def draw_game():
        background.draw_ground()
        player.update(invulnerability_time)
        mobs_group.draw(screen)
        mobs_group.update()
        player_group.draw(screen)
        background.draw_hp(health_points)
        coin_group.update()
        coin_group.draw(screen)
        screen.blit(text, (width - 25 * len(str(coin_counter)), 5))

    @staticmethod
    def get_data_from_db():
        cur = con.cursor()
        try:
            data = cur.execute(''' SELECT * 
            FROM records''').fetchall()
        except sqlite3.OperationalError:
            cur.execute('''CREATE TABLE IF NOT EXISTS records(
            user_name TEXT,
            score INTEGER)''').fetchall()
            con.commit()
            data = []
        return data


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
        self.rect.center = -self.image.get_size()[0], 0

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
        global coin_counter, text, speed
        if pygame.sprite.spritecollide(player, coin_group, True):
            coin_counter += 1
            text = font.render(str(coin_counter), False, (0, 0, 0))
            coin_sound.play()
        else:
            if speed >= 5:
                speed = 5
            self.rect.y += speed

        screen.blit(self.image, self.rect)


class Pause:

    def __init__(self):
        # constants-----------------------
        self.is_pause_on = False

        # load image-----------------------
        self.background = \
            LoadSprites.load_image('pause/background.png')
        self.button_resume = \
            LoadSprites.load_image('pause/button_resume.png')
        self.button_settings = \
            LoadSprites.load_image('pause/button_settings.png')
        self.button_restart = \
            LoadSprites.load_image('pause/button_restart.png')

        # scale image----------------------
        self.background = pygame.transform.scale(
            self.background,
            (width, height)
        )

        # constants------------------------
        self.button_resume_rect = self.button_resume.get_rect().move(
            width // 2 - self.button_resume.get_size()[0] // 2,
            height // 3 - self.button_resume.get_size()[1] // 2)
        self.button_settings_rect = self.button_settings.get_rect().move(
            width // 2 - self.button_settings.get_size()[0] // 2,
            height // 2 - self.button_settings.get_size()[1] // 2)
        self.button_restart_rect = self.button_restart.get_rect().move(
            width // 2 - self.button_restart.get_size()[0] // 2,
            height - height // 3 - self.button_restart.get_size()[1] // 2)

    def pause(self):
        if self.is_pause_on:
            screen.blit(self.background, (0, 0))
            screen.blit(self.button_resume, (
                self.button_resume_rect
            ))

            screen.blit(self.button_settings, (
                self.button_settings_rect
            ))

            screen.blit(self.button_restart, (
                self.button_restart_rect
            ))

    def update(self, pos):
        if self.is_pause_on:
            if self.button_resume_rect.collidepoint(pos):
                self.is_pause_on = False

            elif self.button_restart_rect.collidepoint(pos):
                self.is_pause_on = False
                Main.start()

            elif self.button_settings_rect.collidepoint(pos):
                settings.settings_on = True


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__(player_group)

        # load image-------------------------
        self.image = LoadSprites.load_image('enemy/car.png')

        # scale image------------------------
        self.image = pygame.transform.scale(self.image, (90, 135))

        # constants--------------------------
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
        global invulnerability, \
            health_points, \
            invulnerability_time, \
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
            if health_points != 0:
                player_crush.play()

        if health_points <= 0:
            is_game_over = True
            main_sound.stop()
            game_over_sound.play()

        screen.blit(self.image, self.rect)


class Opponents(pygame.sprite.Sprite):

    def __init__(self, x):
        super(Opponents, self).__init__(mobs_group)
        self.enemy = 'enemy' + str(randint(1, 5)) + '.png'
        self.image = LoadSprites.load_image('enemy/' + self.enemy)
        self.image = pygame.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect()
        self.rect.center = x, -self.image.get_size()[1]
        self.speed = 1

    def update(self):
        global opponents, speed
        speed = 5 if speed >= 5 else speed

        if self.rect.y <= height:
            self.rect.y += speed


if __name__ == '__main__':
    pygame.font.init()
    pygame.init()
    fps = 100
    clock = pygame.time.Clock()
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size=size)

    mobs_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    main_sound = pygame.mixer.Sound('data/music/main.ogg')
    game_over_sound = pygame.mixer.Sound('data/music/dead.ogg')
    coin_sound = pygame.mixer.Sound('data/music/coin.ogg')
    player_crush = pygame.mixer.Sound('data/music/crush.ogg')
    menu_sound = pygame.mixer.Sound('data/music/menu.ogg')
    pause_sound = pygame.mixer.Sound('data/music/pause.ogg')

    is_pause_sound_on = False
    is_menu_sound_on = True
    is_main_sound_on = False

    running = True
    health_points = 3
    invulnerability = False
    invulnerability_time = time()
    speed = 1
    coin_counter = 0
    is_game_paused = False
    is_game_over = False
    font = pygame.font.Font(None, 36)
    text = font.render(str(coin_counter), False, (0, 0, 0))
    menu_sound.play()
    volume_music = 100
    volume_vfx = 100
    con = sqlite3.connect('data/score_db.db')

    menu = Menu()
    player = Player()
    background = LoadSprites()
    start = time()
    pause = Pause()
    score_board = ScoreBoard()
    settings = SettingsMenu()

    pos_for_ops = [width // 4, width // 2, width - width // 4]
    used_pos = sample(pos_for_ops, 2)
    opponents = []
    coins = []

    # add new opponents
    for pos in used_pos:
        opponents.append(Opponents(pos))
        if randint(0, 5) == 2:
            coins.append(
                LoadSprites().draw_coin(
                    set(pos_for_ops).difference(used_pos)
                )
            )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started \
                    and not score_board.is_scoreboard_on \
                    and not settings.settings_on:
                menu.update(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and pause.is_pause_on \
                    and not settings.settings_on:
                pause.update(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and settings.settings_on:
                settings.update(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and score_board.is_scoreboard_on:
                score_board.update(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause.is_pause_on and \
                            menu.games_started and not \
                            settings.settings_on:
                        pause.is_pause_on = False
                        pause_sound.stop()

                    elif not settings.settings_on and not \
                            pause.is_pause_on and \
                            menu.games_started:
                        pause.is_pause_on = True

                    elif settings.settings_on:
                        settings.settings_on = False
                        if menu.games_started:
                            Main.draw_game()

                    elif score_board.is_scoreboard_on:
                        score_board.is_scoreboard_on = False
        Main.move()

        if menu.games_started and not \
                pause.is_pause_on and not \
                is_game_over and not \
                settings.settings_on and not \
                score_board.is_scoreboard_on:
            Main.draw_game()
            if not is_main_sound_on:
                main_sound.play(10)
                pause_sound.stop()
                menu_sound.stop()
                game_over_sound.stop()
                is_main_sound_on = True
                is_pause_sound_on = False
                is_menu_sound_on = False

        elif not menu.games_started and not \
                pause.is_pause_on and not \
                is_game_over and not \
                settings.settings_on and not \
                score_board.is_scoreboard_on:
            menu.draw_menu()
            if not is_menu_sound_on:
                main_sound.stop()
                pause_sound.stop()
                menu_sound.play(10)
                game_over_sound.stop()
                is_main_sound_on = False
                is_pause_sound_on = False
                is_menu_sound_on = True

        elif pause.is_pause_on and not \
                settings.settings_on:
            pause.pause()
            if not is_pause_sound_on:
                main_sound.stop()
                pause_sound.play(10)
                menu_sound.stop()
                game_over_sound.stop()
                is_main_sound_on = False
                is_pause_sound_on = True
                is_menu_sound_on = False

        elif is_game_over:
            if menu.games_started:
                Main.draw_game()
            menu.games_started = False
            menu.game_over()

        elif score_board.is_scoreboard_on:
            score_board.draw_score()

        elif settings.settings_on:
            settings.draw_menu()

        # add new opponents
        if opponents[-1].rect.y >= height // 2 \
                and opponents[-2].rect.y >= height // 2:
            used_pos = sample(pos_for_ops, 2)
            for pos in used_pos:
                opponents.append(Opponents(pos))
                speed += 0.05
            if randint(0, 5) == 2:
                coins.append(
                    LoadSprites().draw_coin(
                        set(pos_for_ops).difference(used_pos)
                    )
                )

        # del opponents that was out of screen
        if opponents[0].rect.y >= height \
                and opponents[0].rect.y >= height:
            opponents.pop(0) and opponents.pop(0)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
