from pygame import *

import keys
from settings import *
from keys import create_key_rects, draw_keys
from sounds import load_sounds
from ui.settings_menu import SettingsMenu
from buttons import Button
from time import sleep
import threading

init()
font.init()
font1 = font.SysFont("Comic sans MS", 70, bold=False)
font2 = font.SysFont("Comic sans MS", 30, bold=False)


window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Piano")

clock = time.Clock()

screen_mode = "main"
settings_menu = None
current_volume = 0.5
num_keys = 7
recording = False

SETTINGS_BTN = transform.scale(image.load("assets/images/settings_btn/settings_btn.png"),
    (50,50)
)

SETTINGS_BTN_HOVER = transform.scale(image.load("assets/images/settings_btn/settings_btn_hover.png"),
    (50,50)
)

REC_BTN = transform.scale(image.load("assets/images/rec_btn/rec_btn.png"),
                          (50,50)
)

REC_BTN_HOVER = transform.scale(image.load("assets/images/rec_btn/rec_btn_hover.png"),
                          (50,50)
)

PLAY_BTN = transform.scale(image.load("assets/images/settings_btn/settings_btn.png"),
    (50,50)
)

STOP_REC_BTN = transform.scale(image.load("assets/images/rec_btn/stop_rec_btn.png"),
                          (50,50)
)

STOP_REC_BTN_HOVER = transform.scale(image.load("assets/images/rec_btn/stop_rec_hover_btn.png"),
                          (50,50)
)

PLAY_BTN = transform.scale(image.load("assets/images/play_btn/play_btn.png"),
    (50,50)
)

PLAY_BTN_HOVER = transform.scale(image.load("assets/images/play_btn/play_btn_hover.png"),
    (50, 50)
)

pressed_keys = set()
key_rects = create_key_rects(7)
keys_list = list(KEYS.keys())
sounds = load_sounds(KEYS)
main_txt = font1.render("Piano", True, (0, 0, 0))
recorded_keys = []

def apply_settings(volume:float, keys_count:int):
    global current_volume,num_keys,key_rects,pressed_keys
    current_volume = float(max(0.0, min(1.0, volume)))
    for s in sounds.values():
        try:
            s.set_volume(current_volume)
        except Exception:
            pass
    keys_count = max(1,min(len(KEYS),keys_count))
    if keys_count != num_keys:
        num_keys = keys_count
        keys_list = list(KEYS.keys())[:num_keys]
        key_rects = create_key_rects(num_keys)
        pressed_keys = {i for i  in pressed_keys if i < num_keys}

def open_settings():
    global screen_mode, settings_menu
    screen_mode = "settings"
    settings_menu = SettingsMenu(
        window.get_rect(),
        initial_value=current_volume,
        initial_keys=num_keys,
        min_key = 1,
        max_key =len(KEYS),
        on_change=apply_settings,
        on_back=lambda: back_to_main()
    )

def back_to_main():
    global screen_mode, settings_menu
    screen_mode = "main"
    settings_menu = None

def start_record_thread():
    global recorded_keys
    if not recording:
        threading.Thread(target=play_record, daemon=True).start()

def clear_record():
    global recorded_keys
    recorded_keys = []

def switch_recording():
    global  recording, rec_btn, play_btn
    if recording:
        rec_btn.img = REC_BTN
        rec_btn.img_hover = REC_BTN_HOVER
        recording = False
    else:
        clear_record()
        rec_btn.img = STOP_REC_BTN
        rec_btn.img_hover = STOP_REC_BTN_HOVER
        recording = True

def record(pressed_key):
    global recorded_keys
    recorded_keys.append(pressed_key)

def play_record():
    global  recorded_keys
    for key in recorded_keys:
        key.play()
        sleep(0.5)


settings_btn = Button(
    20,20,60,60,
    action = open_settings,
    img = SETTINGS_BTN,
    img_hover = SETTINGS_BTN_HOVER,
)

rec_btn = Button(
    920, 20, 60, 60,
    action = switch_recording,
    img = REC_BTN,
    img_hover = REC_BTN_HOVER,
)

play_btn = Button(
    860, 20, 60, 60,
    img = PLAY_BTN,
    img_hover = PLAY_BTN_HOVER,
    action=start_record_thread
)

game = True
while game:
    window.fill(WHITE)

    if screen_mode == "main":
        settings_btn.draw(window)
        rec_btn.draw(window)
        play_btn.draw(window)
        window.blit(main_txt, (400, 70))
        draw_keys(window, key_rects, pressed_keys)
    elif screen_mode == "settings" and settings_menu:
        settings_menu.draw(window, font2)

    for e in event.get():
        if e.type == QUIT:
            game = False

        if not settings_menu:
            settings_btn.handle_event(e)
            rec_btn.handle_event(e)
            play_btn.handle_event(e)

            if screen_mode == "main":
                if e.type == MOUSEBUTTONDOWN:
                    pos = e.pos
                    for i, r in enumerate(key_rects):
                        if r.collidepoint(e.pos):
                            sounds[keys_list[i]].play()
                            pressed_keys.add(i)
                            if recording:
                                record(sounds[keys_list[i]])
                if e.type == MOUSEBUTTONUP:
                    pos = e.pos
                    for i, r in enumerate(key_rects):
                        if i in pressed_keys and r.collidepoint(pos):
                            pressed_keys.remove(i)
        else:
            settings_menu.handle_event(e)

    display.update()
    clock.tick(FPS)