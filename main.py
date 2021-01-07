import pygame
import os
import sys
from random import sample


class Menu:

    def __init__(self):
        self.color = (0, 0, 0)
        self.games_started = False
        self.button = LoadSprites.load_image('button.png')
        self.button_size = self.button.get_size()

    def draw_menu(self):
        # button "start game"

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
        screen.blit(self.load_image('road.png'), (0, 0))


class MainGame:

    def __init__(self):
        pass

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    player_img = LoadSprites.load_image('car.png')

    def __init__(self):
        super(Player, self).__init__(all_sprites)
        self.image = self.player_img
        self.rect = self.image.get_rect()
        self.rect.center = width // 2, height // 2
        self.size = {'x': self.image.get_size()[0],
                     'y': self.image.get_size()[1]}

    def update(self):
        pass


class Opponents(pygame.sprite.Sprite):
    opponent_img = LoadSprites.load_image('opponent.png')

    def __init__(self, x):
        super(Opponents, self).__init__(all_sprites)
        self.image = self.opponent_img
        self.rect = self.image.get_rect()
        self.rect.center = x, -self.image.get_size()[1]
        print(self.rect.center)

    def update(self):
        if not self.rect.x >= height:
            self.rect.y += 1


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    size = width, height = 600, 600

    screen = pygame.display.set_mode(size=size)
    menu = Menu()
    game = Player()
    background = LoadSprites()
    step_x = width // 4
    step_y = 10

    pos_for_ops = [width // 4, width // 2, width - width // 4]
    ops = []
    for pos in sample(pos_for_ops, 2):
        ops.append(Opponents(pos))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started:
                menu.update(event.pos)

            elif event.type == pygame.KEYDOWN and menu.games_started:
                if (event.key == pygame.K_d or event.key == ord('в')) \
                        and game.rect.x + step_x + game.size['x'] <= width:
                    game.rect.x += step_x

                elif (event.key == pygame.K_a or event.key == ord('ф')) \
                        and game.rect.x - step_x - game.size['x'] >= 0:
                    game.rect.x -= step_x

                elif (event.key == pygame.K_w or event.key == ord('ц')) \
                        and game.rect.y - step_y - game.size['y'] >= height // 3:
                    game.rect.y -= step_y

                elif (event.key == pygame.K_s or event.key == ord('ы')) \
                        and game.rect.y + step_y + game.size['y'] <= height:
                    game.rect.y += step_y

        pygame.display.flip()
        if menu.games_started:
            screen.fill('green')
            background.draw_ground()
            game.update()
            all_sprites.draw(screen)
            all_sprites.update()
        else:
            screen.fill('white')
            menu.draw_menu()
        clock.tick(fps)
    pygame.quit()
