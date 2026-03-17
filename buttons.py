import pygame
from pygame import *

class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        action=None,
        text: str = "",
        img: Surface = None,
        img_hover: Surface = None,
        center: bool = False
    ):
        self.text = text
        self.img = img
        self.img_hover = img_hover
        self.action = action
        self.center = center
        self.width = width
        self.height = height

        if self.center:
            self.rect = Rect(0, 0, width, height)
            self.rect.center = (x, y)
        else:
            self.rect = Rect(x, y, width, height)

    def draw(self, screen, font="Arial"):
        pos = mouse.get_pos()
        hovered = self.rect.collidepoint(pos)

        if hovered and self.img_hover:
            surf = self.img_hover
        else:
            surf = self.img

        img_w, img_h = surf.get_size()
        if img_w != self.width or img_h != self.height:
            surf = transform.scale(surf, (self.rect.width, self.rect.height))

        screen.blit(surf, self.rect.topleft)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()












