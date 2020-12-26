import pygame
import os
import sys
from random import randint


class Menu:
    def __init__(self):
        self.color = (0, 0, 0)
        self.games_started = False

    def draw_menu(self):
        pygame.draw.rect(screen, self.color, [
            (width // 2 - 50, height // 2 - 50),
            (100, 100)])

    def update(self, pos):
        # if user clicked to 'button'
        if width // 2 + 50 >= pos[0] >= width // 2 - 50 and \
                height // 2 + 50 >= pos[0] >= width // 2 - 50:
            self.games_started = True


class SettingsMenu:
    def __init__(self):
        pass


class MainGame:
    def __init__(self):
        self.opponent_pos = []
        self.color = 'yellow'
        self.color_opponent = 'red'
        self.x = width // 2
        self.y = height // 2
        self.size = 40
        self.res_car = [
            (self.x - self.size // 2, self.y - self.size // 2),
            (self.size, self.size)
        ]

    # draw user's car
    def draw_car(self):
        pygame.draw.rect(screen, self.color, self.res_car)

    # draw opponent car
    # this func doesnt work correctly yet
    def draw_opponent(self):
        if len(self.opponent_pos) < 2:
            self.opponent_pos.append(
                [
                    (randint(0, width - self.size),
                     height // 3),
                    (0, 0)
                ])
        for pos in self.opponent_pos:
            pygame.draw.rect(screen, self.color_opponent, pos)

    def update(self):
        # change pos of enemy's car
        for index, pos in enumerate(self.opponent_pos):
            if pos[0][1] + 1 >= height:
                self.opponent_pos.pop(index)
            else:
                self.opponent_pos[index] = [
                    (pos[0][0] - 0.2, pos[0][1] + 0.5),
                    (pos[1][0] + 0.2, pos[1][1] + 0.2)
                ]

        # change pos of user's car
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
    def load_image(self, name, color_key=None):
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
        # draw road
        pygame.draw.polygon(screen, 'brown', [
            (width // 3, 0),
            (width - width // 3, 0),
            (width, height),
            (0, height)
        ])

        # draw purple lines on road
        pygame.draw.line(screen, 'purple',
                         (width // 3, 0),
                         (0, height), 4)

        pygame.draw.line(screen, 'purple',
                         ((width // 2), 0),
                         (width // 4, height), 4)

        pygame.draw.line(screen, 'purple',
                         ((width // 2), 0),
                         (width // 4 * 3, height), 4)

        pygame.draw.line(screen, 'purple',
                         ((width - width // 3), 0),
                         (width // 4 * 4, height), 4)

        # draw white lines on road

        pygame.draw.line(screen, 'white',
                         (width // 3 + ((width // 2 - width // 3) // 2), 0),
                         ((width // 4 - 0) // 2, height), 4)

        pygame.draw.line(screen, 'white', (width // 2, 0),
                         (width // 2, height), 4)

        pygame.draw.line(screen, 'white',
                         (width // 2 + ((width - width // 3) - (width // 2)) // 2, 0),
                         (width - ((width // 4 * 4) - (width // 4 * 3)) // 2, height), 4)


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()

    # in future user can change this values in the settings,
    # but now i prefer use this values :)
    size = width, height = 600, 600

    screen = pygame.display.set_mode(size=size)
    menu = Menu()
    game = MainGame()
    background = LoadSprites()
    step_x = width // 4
    step_y = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started:
                menu.update(event.pos)

            elif event.type == pygame.KEYDOWN and menu.games_started:
                if (event.key == pygame.K_d or event.key == ord('в')) \
                        and game.x + step_x + game.size <= width:
                    if game.x < width // 2:
                        game.x = width // 2
                    else:
                        game.x += step_x

                elif (event.key == pygame.K_a or event.key == ord('ф')) \
                        and game.x - step_x - game.size >= 0:
                    if game.x > width // 2:
                        game.x = width // 2
                    else:
                        game.x -= step_x

                elif (event.key == pygame.K_w or event.key == ord('ц')) \
                        and game.y - step_y - game.size >= height // 3:
                    if game.x < width // 2:
                        game.x += 4
                    elif game.x > width // 2:
                        game.x -= 4
                    elif game.x == width:
                        game.x = width // 2
                    game.y -= step_y
                    game.size -= 1

                elif (event.key == pygame.K_s or event.key == ord('ы')) \
                        and game.y + step_y + game.size <= height:
                    if game.x > width // 2:
                        game.x += 4
                    elif game.x < width // 2:
                        game.x -= 4
                    elif game.x == width:
                        game.x = width // 2
                    game.y += step_y
                    game.size += 1

        pygame.display.flip()
        if menu.games_started:
            screen.fill('green')
            background.draw_ground()
            background.draw_sky()
            game.update()
        else:
            screen.fill('white')
            menu.draw_menu()
        clock.tick(fps)
    pygame.quit()
