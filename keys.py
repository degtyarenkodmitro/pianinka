from pygame import Rect
from effects import draw_key_effect

def draw_keys(screen, key_rects, keys_pressed):
    for i, key_rect in enumerate(key_rects):
        key_pressed = i in keys_pressed
        draw_key_effect(screen, key_rect, key_pressed)

def create_key_rects(num_keys, start_x=150, start_y=200, key_width=100, key_height=250):
    rects = []
    for i in range(num_keys):
        x = start_x + i * key_width
        rects.append(Rect(x, start_y, key_width, key_height))
    return rects