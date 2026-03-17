from pygame import draw
from settings import WHITE, BLACK, GREY

def draw_key_effect(screen, rect, is_pressed=False):
    if is_pressed:
        key_color = GREY
    else:
        key_color = WHITE
    key_border_color = BLACK

    draw.rect(screen, key_color, rect, border_radius=8)
    draw.rect(screen, key_border_color,rect, 6, border_radius=8)