import pygame

from typing import Optional

from utils import *
from settings import *

vector = pygame.math.Vector2

def get_center(x: Optional[int] = SCREEN_WIDTH, y: Optional[int] = SCREEN_HEIGHT) -> vector:
    return vector(x/2, y/2)

def get_center(v: Optional[vector] = vector(SCREEN_WIDTH, SCREEN_HEIGHT)) -> vector:
    return vector(v.x/2, v.y/2)

def loadify(imgname: str) -> pygame.Surface:
    return pygame.image.load(imgname).convert_alpha()

def get_text_surface(
        text: str, 
        size: int, 
        color: pygame.Color, 
        font: Optional[pygame.font.Font] = None
        ) -> pygame.Surface:
    font = font or pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    return text_surface