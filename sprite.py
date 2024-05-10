import pygame

from typing import Any, Callable, Dict, Optional
from utils import *
from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, surface, game, pos=Optional[vector], vel=Optional[vector]):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = surface # pygame.transform.scale(loadify(f'data/{img}.png'), (int(self.radius * 2), int(self.radius * 2)))

        # self.image.set_colorkey((0, 255, 0))
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = pos or vector(0, 0)
        self.rect.center = pos
        self.vel = vel or vector(0, 0)

    def set_pos(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        pass

class Button(Sprite):
    def __init__(
            self, 
            game, 
            pos: vector,
            text: str, 
            onclick: Optional[Callable[[Sprite], Any]] = None,
            text_color: Optional[pygame.Color] = pygame.Color(255, 137, 3),
            size: Optional[Dict[int, None]] = [130, 50], 
            color: Optional[pygame.Color] = pygame.Color(255, 137, 3),
            stroke: Optional[int] = 3
            ):
        self.game = game
        self.pos = pos
        self.text = text
        self.onclick = onclick
        self.text_color = text_color
        self.size = size
        self.color = color
        self.stroke = stroke

        button_surface = pygame.Surface(self.size)
        pygame.draw.rect(button_surface, self.color, pygame.Rect(0, 0, size[0], size[1]), stroke)
        text_surface = get_text_surface(self.text, int(self.size[1]*0.7), self.text_color)
        rect = text_surface.get_rect()
        rect.center = button_surface.get_rect().center
        button_surface.blit(text_surface, rect)
        self.button = Sprite(button_surface, self, pos)

        super().__init__(button_surface, self.game, self.pos)

    def clicked(self):
        if self.onclick is not None:
            self.onclick(self)

    def reinit(self):
        self = Button(self.game, self.text, self.text_color, self.pos, self.size, self.color, self.stroke)

    def set_text(self, text):
        self.text = text
        self.reinit()
        return self

    def set_size(self, size):
        self.size = size
        self.reinit()
        return self

    def set_color(self, color):
        self.color = color
        self.reinit()
        return self

    def set_stroke(self, stroke):
        self.stroke = stroke
        self.reinit()
        return self