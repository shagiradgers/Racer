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


class Scoreboard:
    def __init__(self):
        pass


class LoadSprites:
    def __init__(self):
        pass

    @staticmethod
    def load_image(name, color_key=None):
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
        screen.fill('brown', (
            (width // 4 - 20, 0),
            (width // 2 + 40, height)
        ))

        # draw lines on road

        pygame.draw.line(screen, 'black',
                         (width // 4, 0),
                         (width // 4, height),
                         5
                         )

        pygame.draw.line(screen, 'black',
                         (width // 2, 0),
                         (width // 2, height),
                         5
                         )

        pygame.draw.line(screen, 'black',
                         (width - width // 4, 0),
                         (width - width // 4, height),
                         5
                         )


class MainGame(pygame.sprite.Sprite):
    car_img = LoadSprites.load_image('car.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = self.car_img
        self.rect = self.car_img.get_rect()
        self.opponent_pos = []
        self.color_opponent = 'red'
        self.size = self.car_img.get_size()[0]
        self.rect.center = width // 2, height // 2

    # draw user's car
    def draw_car(self):
        pass

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
                    (pos[0][0] - 0.2, pos[0][1] + 0.2),
                    (pos[1][0] + 0.2, pos[1][1] + 0.2)
                ]
        self.image = pygame.transform.scale(self.image, self.rect.size)


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

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
                        and game.rect.x + step_x + game.size <= width:
                    game.rect.x += step_x

                elif (event.key == pygame.K_a or event.key == ord('ф')) \
                        and game.rect.x - step_x - game.size >= 0:
                    game.rect.x -= step_x

                elif (event.key == pygame.K_w or event.key == ord('ц')) \
                        and game.rect.y - step_y - game.size >= height // 3:
                    game.rect.y -= step_y
                    game.size -= 1

                elif (event.key == pygame.K_s or event.key == ord('ы')) \
                        and game.rect.y + step_y + game.size <= height:
                    game.rect.y += step_y
                    game.size += 1

        pygame.display.flip()
        if menu.games_started:
            screen.fill('green')
            background.draw_ground()
            background.draw_sky()
            game.update()
            game.draw_car()
            all_sprites.draw(screen)
            all_sprites.update()
        else:
            screen.fill('white')
            menu.draw_menu()
        clock.tick(fps)
    pygame.quit()
