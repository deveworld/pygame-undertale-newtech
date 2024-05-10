from __future__ import annotations
import pygame

from math import floor
from utils import *
from settings import *
from sprite import *

class Layout:
    def __init__(self, rect: pygame.Rect, sprites: Optional[pygame.sprite.Group] = None) -> None:
        self.rect = rect
        if sprites is None:
            self.layouts = []
        else:
            self.layouts = [sprite for sprite in sprites]
        self.rendered = True

    def add_sprite(self, sprite: Sprite):
        self.layouts.append(sprite)
        self.rendered = False

    def add_abstract_stretch(self, stretch: int = 1):
        [self.layouts.append(None) for _ in range(stretch)]
        self.rendered = False
    
    def add_stretch(self, size: int):
        if size != 0:
            self.layouts.append(size)
        self.rendered = False

    def add_layout(self, layout: Layout):
        self.layouts.append(layout)
        self.rendered = False

    def get_width(self) -> int:
        if not self.rendered:
            self.render()
        return self.rect.width
    
    def get_height(self) -> int:
        if not self.rendered:
            self.render()
        return self.rect.height

    def render(self):
        if self.rendered:
            return
        self.rendered = True


class HorizontalLayout(Layout):
    def __init__(self, rect: pygame.Rect, sprites: Optional[pygame.sprite.Group] = None) -> None:
        super().__init__(rect, sprites)

    def render(self):
        if self.rendered:
            return
        self.rendered = True
        rect_start = self.rect.top
        rect_end = self.rect.bottom
        rect_height = self.rect.height

        heights = []
        abstract_stretches = 0
        heights_sum = 0
        max_width = -1
        for layout in self.layouts:
            if isinstance(layout, Sprite):
                heights.append(layout.image.get_rect().height)
                heights_sum += layout.image.get_rect().height
                max_width = max(max_width, layout.image.get_rect().width)
            elif isinstance(layout, int):
                heights.append(layout)
                heights_sum += layout
            elif isinstance(layout, Layout):
                if isinstance(layout, VerticalLayout):
                    heights.append(layout.get_height())
                    heights_sum += layout.get_height()
                    max_width = max(max_width, layout.get_width())
                else:
                    raise RuntimeError("Only VerticalLayout can be in HorizonalLayout.")
            elif layout is None:
                abstract_stretches += 1

        self.rect = pygame.Rect(self.rect.left, self.rect.top, max_width, self.rect.height)
            
        if heights_sum > rect_height:
            raise RuntimeError("All sprites/stretches height sum are over rect height.")
        
        remain_height = rect_height - heights_sum
        if abstract_stretches != 0:
            abstract_stretch_height = int(floor(remain_height / abstract_stretches))

        now_height = rect_start
        i = 0

        for layout in self.layouts:
            if isinstance(layout, Sprite):
                pos = layout.pos
                pos.y = now_height
                layout.set_pos(pos)
                now_height += heights[i]
                i+=1
            elif isinstance(layout, int):
                now_height += layout
            elif isinstance(layout, Layout):
                for other_layout in layout.layouts:
                    if isinstance(other_layout, Sprite):
                        pos = other_layout.pos
                        pos.y = now_height
                        other_layout.set_pos(pos)
                now_height += heights[i]
                i+=1
            elif layout is None:
                now_height += abstract_stretch_height

        if now_height > rect_end:
            raise RuntimeError("Height calculation end over rect height.")


class VerticalLayout(Layout):
    def __init__(self, rect: pygame.Rect, sprites: Optional[pygame.sprite.Group] = None) -> None:
        super().__init__(rect, sprites)

    def render(self):
        if self.rendered:
            return
        self.rendered = True
        rect_start = self.rect.left
        rect_end = self.rect.right
        rect_width = self.rect.width

        widths = []
        abstract_stretches = 0
        widths_sum = 0
        max_height = -1
        for layout in self.layouts:
            if isinstance(layout, Sprite):
                widths.append(layout.image.get_rect().width)
                widths_sum += layout.image.get_rect().width
                max_height = max(max_height, layout.image.get_rect().height)
            elif isinstance(layout, int):
                widths.append(layout)
                widths_sum += layout
            elif isinstance(layout, Layout):
                if isinstance(layout, HorizontalLayout):
                    widths.append(layout.get_width())
                    widths_sum += layout.get_width()
                    max_height = max(max_height, layout.get_height())
                else:
                    raise RuntimeError("Only HorizontalLayout can be in VerticalLayout.")
            elif layout is None:
                abstract_stretches += 1

        self.rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, max_height)
            
        if widths_sum > rect_width:
            raise RuntimeError("All sprites/stretches width sum are over rect width.")
        
        remain_width = rect_width - widths_sum
        if abstract_stretches != 0:
            abstract_stretch_height = int(floor(remain_width / abstract_stretches))

        now_width = rect_start
        i = 0

        for layout in self.layouts:
            if isinstance(layout, Sprite):
                pos = layout.pos
                pos.x = now_width
                layout.set_pos(pos)
                now_width += widths[i]
                i+=1
            elif isinstance(layout, int):
                now_width += layout
            elif isinstance(layout, Layout):
                for other_layout in layout.layouts:
                    if isinstance(other_layout, Sprite):
                        pos = other_layout.pos
                        pos.x = now_width
                        other_layout.set_pos(pos)
                now_width += widths[i]
                i+=1
            elif layout is None:
                now_width += abstract_stretch_height

        if now_width > rect_end:
            raise RuntimeError("Width calculation end over rect width.")
