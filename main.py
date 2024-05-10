import math
import os
import sys
import threading
import pygame

from settings import *
from sprite import *
from layout import *


class Game:

    def __init__(self):
        self.playing = True
        self.all_sprites = pygame.sprite.Group()
        pygame.init()
        # icon = pygame.image.load('data/icon.png')
        # pygame.display.set_icon(icon)
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        wall_surface = pygame.Surface([200, 200])
        pygame.draw.rect(wall_surface, pygame.Color(255, 255, 255), pygame.Rect(0, 0, 200, 200), 3)
        self.wall = Sprite(wall_surface, self, get_center() + vector(0, 50))

        self.fight = Button(self, get_center(), "Fight")
        self.act = Button(self, get_center(), "Act")
        self.item = Button(self, get_center(), "Item")
        self.mercy = Button(self, get_center(), "Mercy")

        vlayout = VerticalLayout(self.screen.get_rect())
        vlayout.add_abstract_stretch()
        vlayout.add_sprite(self.fight)
        vlayout.add_abstract_stretch()
        vlayout.add_sprite(self.act)
        vlayout.add_abstract_stretch()
        vlayout.add_sprite(self.item)
        vlayout.add_abstract_stretch()
        vlayout.add_sprite(self.mercy)
        vlayout.add_abstract_stretch()
        vlayout.render()

        wall_vlayout = VerticalLayout(self.screen.get_rect())
        wall_vlayout.add_abstract_stretch()
        wall_vlayout.add_sprite(self.wall)
        wall_vlayout.add_abstract_stretch()
        wall_vlayout.render()

        hlayout = HorizontalLayout(self.screen.get_rect())
        hlayout.add_abstract_stretch(5)
        hlayout.add_sprite(wall_vlayout)
        hlayout.add_abstract_stretch(2)
        hlayout.add_layout(vlayout)
        hlayout.add_abstract_stretch()
        hlayout.render()

        self.all_sprites.add(self.wall, self.fight, self.act, self.item, self.mercy)
        self.running = True

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            up_t = threading.Thread(target=self.update)
            up_t.start()
            up_t.join()
            dr_t = threading.Thread(target=self.draw)
            dr_t.start()
            dr_t.join()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_SPACE:
                    pass

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    while game.running:
        game.run()
    pygame.quit()
    sys.exit()