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
        self.color = 'yellow'
        self.color_opponent = 'red'
        self.x = self.width // 2
        self.y = self.height // 2
        self.size = 40
        self.res_car = [
            (self.x - self.size // 2, self.y - self.size // 2),
            (self.size, self.size)
        ]

    # draw user's car
    def draw_car(self):
        pygame.draw.rect(screen, self.color, self.res_car)

    # draw opponent car
    # this func doesnt work yet
    def draw_opponent(self):
        if len(self.opponent_pos) < 2:
            self.opponent_pos.append(
                [
                    (randint(0, self.width - self.size), self.height // 3),
                    (0, 0)
                ])
        for pos in self.opponent_pos:
            pygame.draw.rect(screen, self.color_opponent, pos)

    def update(self):
        for index, pos in enumerate(self.opponent_pos):
            if pos[0][1] + 1 >= height:
                self.opponent_pos.pop(index)
            else:
                self.opponent_pos[index] = [
                    (pos[0][0] - 0.2, pos[0][1] + 1),
                    (pos[1][0] + 0.2, pos[1][1] + 0.2)
                ]

        self.res_car = [
            (self.x - self.size // 2, self.y - self.size // 2),
            (self.size, self.size)
        ]

        pygame.draw.rect(screen, self.color, self.res_car)


class Scoreboard:
    def __init__(self):
        pass


class LoadSprites:
    def __init__(self):
        pass

    # I still this func from book :)
    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        return pygame.image.load(fullname)

    def draw_sky(self):
        pygame.draw.rect(screen, 'blue', [
            (0, 0),
            (width, height // 3)
        ])

    def draw_ground(self):
        pygame.draw.polygon(screen, 'brown', [
            (width // 3, 0),
            (width - width // 3, 0),
            (width, height),
            (0, height)
        ])


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
    background = LoadSprites()
    step = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not menu.games_started:
                menu.update(event.pos)

            elif event.type == pygame.KEYDOWN and menu.games_started:
                if event.key == pygame.K_d and game.x + step + game.size <= width:
                    game.x += step

                elif event.key == pygame.K_a and game.x - step - game.size >= 0:
                    game.x -= step

                elif event.key == pygame.K_w and game.y - step - game.size >= height // 3:
                    game.y -= step
                    game.size -= 1

                elif event.key == pygame.K_s and game.y + step + game.size <= height:
                    game.y += step
                    game.size += 1

        pygame.display.flip()
        screen.fill((255, 255, 255))
        if menu.games_started:
            background.draw_ground()
            background.draw_sky()
            game.update()
            game.draw_opponent()
        else:
            menu.draw_menu()
        clock.tick(fps)
    pygame.quit()
