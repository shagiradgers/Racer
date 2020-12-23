import pygame
import os
import sys
from random import randint


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (0, 0, 0)
        self.games_started = False

    def draw_menu(self):
        pygame.draw.rect(screen, self.color, [
            (self.width // 2 - 50, self.height // 2 - 50),
            (100, 100)])

    def update(self, pos):
        # if user clicked to 'button'
        if self.width // 2 + 50 >= pos[0] >= self.width // 2 - 50 and \
                self.height // 2 + 50 >= pos[0] >= self.width // 2 - 50:
            self.games_started = True


class SettingsMenu:
    def __init__(self):
        pass


class MainGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.opponent_pos = []
        self.color = 'blue'
        self.color_opponent = 'red'
        self.x = self.width // 2
        self.y = self.height // 2

    # draw user's car
    def draw_car(self):
        pygame.draw.rect(screen, self.color,
                         [
                             (self.x - 50, self.y - 50),
                             (100, 100)
                         ])

    # draw opponent car
    def draw_opponent(self):
        pygame.draw.rect(screen, self.color_opponent,
                         [
                             (randint(0, self.width - 100), randint(0, self.height - 100)),
                             (100, 100)
                         ])


class Scoreboard:
    def __init__(self):
        pass


class LoadSprites:
    def __init__(self):
        pass

    '''I still this func from book :)'''

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()

    # in future user can change this values in the settings,
    # but now i prefer use this values :)
    size = width, height = 500, 500

    screen = pygame.display.set_mode(size=size)
    menu = Menu(width, height)
    game = MainGame(width, height)
    step = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not menu.games_started:
                menu.update(event.pos)

            elif event.type == pygame.KEYDOWN and menu.games_started:
                if event.key == pygame.K_d and game.x + step + 50 <= width:
                    game.x += step
                    print(game.x)

                elif event.key == pygame.K_a and game.x - step - 50 >= 0:
                    game.x -= step

                elif event.key == pygame.K_w and game.y - step - 50 >= 0:
                    game.y -= step

                elif event.key == pygame.K_s and game.y + step + 50 <= height:
                    game.y += step

        pygame.display.flip()
        screen.fill((255, 255, 255))
        if menu.games_started:
            game.draw_opponent()
        else:
            menu.draw_menu()
        clock.tick(fps)
    pygame.quit()
