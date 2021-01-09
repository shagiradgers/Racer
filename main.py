import pygame
import os
import sys
from random import sample, randint
from time import time
from pygame.locals import *


class Menu:

    def __init__(self):
        self.color = (0, 0, 0)
        self.games_started = False
        self.button = LoadSprites.load_image('button.png')
        self.button_size = self.button.get_size()
        self.background = LoadSprites.load_image('menu_background.png')
        self.background = pygame.transform.scale(
            self.background, (width, height))

    def draw_menu(self):
        # draw background
        screen.blit(self.background, (0, 0))

        # button "start player"
        screen.blit(
            self.button, (width // 2 - self.button_size[0] // 2
                          , width // 2 - self.button_size[1] // 2)
        )

    def update(self, pos):
        # if user clicked to 'button'
        if width // 2 + self.button_size[0] >= pos[0] >= \
                width // 2 - self.button_size[0] and \
                height // 2 + self.button_size[1] >= \
                pos[0] >= width // 2 - self.button_size[1]:
            self.games_started = True


class SettingsMenu:
    def __init__(self):
        pass


class Scoreboard:
    def __init__(self):
        pass


class LoadSprites(pygame.sprite.Sprite):

    @staticmethod
    def load_image(name, color_key=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        return pygame.image.load(fullname)

    def draw_ground(self):
        road_img = self.load_image('road.png')
        screen.blit(pygame.transform.scale(road_img, (
            width, height)), (0, 0))


class MainGame:

    def __init__(self):
        pass

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    player_img = LoadSprites.load_image('car.png')
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
                self.rect.centery - self.step_y >= 0:
            self.rect.y -= self.step_y

        elif direction == 'down' and \
                self.rect.centery + self.step_y <= height:
            self.rect.y += self.step_y

    def update(self, users_time=time()):
        global invulnerability
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


class Opponents(pygame.sprite.Sprite):

    def __init__(self, x, speed):
        super(Opponents, self).__init__(mobs_group)
        self.image = LoadSprites.load_image('enemy' +
                                            str(randint(1, 5)) +
                                            '.png')
        self.image = pygame.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect()
        self.rect.center = x, -self.image.get_size()[1]
        self.speed = speed

    def update(self):
        if self.rect.y <= height:
            self.rect.y += self.speed


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()
    mobs_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    size = width, height = 600, 700
    health_points = 5
    invulnerability = False
    invulnerability_time = time()

    screen = pygame.display.set_mode(size=size)
    menu = Menu()
    player = Player()
    background = LoadSprites()
    start = time()
    speed = 1

    pos_for_ops = [width // 4, width // 2, width - width // 4]
    opponents = []

    # add new opponents
    for pos in sample(pos_for_ops, 2):
        opponents.append(Opponents(pos, speed))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started:
                menu.update(event.pos)

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

        pygame.display.flip()
        if menu.games_started:
            background.draw_ground()
            player.update(invulnerability_time)
            mobs_group.draw(screen)
            mobs_group.update()
            player_group.draw(screen)
        else:
            screen.fill('white')
            menu.draw_menu()

        # add new opponents
        if opponents[-1].rect.y >= height // 2 \
                and opponents[-2].rect.y >= height // 2:
            for pos in sample(pos_for_ops, 2):
                opponents.append(Opponents(pos, speed))
                speed += 0.001

        # del opponents that was out of screen
        if opponents[0].rect.y >= height \
                and opponents[0].rect.y >= height:
            opponents.pop(0) and opponents.pop(0)

        # rewrite this peace of code
        if pygame.sprite.spritecollide(player, mobs_group, False) and not invulnerability:
            health_points -= 1
            print(health_points)
            invulnerability = True
            invulnerability_time = time()

        if health_points == 0:
            print('GAME OVER')

        clock.tick(fps)
    pygame.quit()
