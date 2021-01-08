import pygame
import os
import sys
from random import sample, randint
from time import time


class Menu:

    def __init__(self):
        self.color = (0, 0, 0)
        self.games_started = False
        self.button = LoadSprites.load_image('button.png')
        self.button_size = self.button.get_size()
        self.background = LoadSprites.load_image('menu_background.png')

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
        if width // 2 + self.button_size[0] >= pos[0] >= width // 2 - self.button_size[0] and \
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
    player_img = pygame.transform.scale(player_img, (110, 155))

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

    def __init__(self, x):
        super(Opponents, self).__init__(all_sprites)
        self.image = LoadSprites.load_image('enemy' +
                                            str(randint(1, 5)) +
                                            '.png')
        self.image = pygame.transform.scale(self.image, (90, 135))
        self.rect = self.image.get_rect()
        self.rect.center = x, -self.image.get_size()[1]
        self.speed = 1

    def update(self):
        if not self.rect.x >= height:
            self.rect.y += self.speed
        self.rect.y += self.speed


if __name__ == '__main__':
    running = True
    fps = 100
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    size = width, height = 600, 600

    screen = pygame.display.set_mode(size=size)
    menu = Menu()
    player = Player()
    background = LoadSprites()
    step_x = width // 4
    step_y = 10
    start = time()
    delay = 0.5

    pos_for_ops = [width // 4, width // 2, width - width // 4]
    opponents = []
    for pos in sample(pos_for_ops, 2):
        opponents.append(Opponents(pos))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and not menu.games_started:
                menu.update(event.pos)

            elif event.type == pygame.KEYDOWN and menu.games_started:
                end = time()

                if (event.key == pygame.K_d or event.key == ord('в') or
                    event.key == pygame.K_RIGHT) \
                        and player.rect.x + step_x + player.size['x'] // 2 <= width and \
                        end - start >= delay:
                    player.rect.x += step_x
                    start = time()

                elif (event.key == pygame.K_a or event.key == ord('ф') or
                        event.key == pygame.K_LEFT) \
                        and player.rect.x - step_x - player.size['x'] // 2 >= 0 and \
                        end - start >= delay:
                    player.rect.x -= step_x
                    start = time()

                elif (event.key == pygame.K_w or event.key == ord('ц') or
                      event.key == pygame.K_UP) \
                        and player.rect.y - step_y >= height // 3:
                    player.rect.y -= step_y
                    start = time()

                elif (event.key == pygame.K_s or event.key == ord('ы') or
                      event.key == pygame.K_DOWN) \
                        and player.rect.y + step_y <= height:
                    player.rect.y += step_y
                    start = time()

        pygame.display.flip()
        if menu.games_started:
            background.draw_ground()
            player.update()
            all_sprites.draw(screen)
            all_sprites.update()
        else:
            screen.fill('white')
            menu.draw_menu()

        # add new opponents
        if opponents[-1].rect.y >= height // 2 and opponents[-2].rect.y >= height // 2:
            for pos in sample(pos_for_ops, 2):
                opponents.append(Opponents(pos))

        # del opponents that was out of screen
        if opponents[0].rect.y >= height and opponents[0].rect.y >= height:
            opponents.pop(0) and opponents.pop(0)

        # rewrite this peace of code
        for opponent in opponents:
            if opponent.rect.center == player.rect.center:
                print('CRUSH')

        clock.tick(fps)
    pygame.quit()
