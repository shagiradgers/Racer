import pygame
import os
import sys


class Menu:
    def __init__(self):
        pass


class SettingsMenu:
    def __init__(self):
        pass


class MainGame:
    def __init__(self):
        pass


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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        screen.fill((255, 255, 255))
        clock.tick(fps)
