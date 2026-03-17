
import pygame
from buttons import Button
from ui.sliders import Slider

class SettingsMenu:
    def __init__(self, screen, initial_value, initial_keys, min_key, max_key, on_change, on_back):
        self.screen = screen
        self.on_change = on_change
        self.on_back = on_back

        cx = screen.centerx
        top = 140

        back_img = pygame.transform.scale(
            pygame.image.load('assets/images/back_btn/button.png') , (50,50)
        )
        back_img_hover = pygame.transform.scale(
            pygame.image.load('assets/images/back_btn/button_hovered.png') , (50,50)
        )
        self.back_btn = Button(
            20,20,50,50,
            self._back,
            img=back_img,
            img_hover=back_img_hover,
        )

        def volume_to_text(v):
            return f"{int(v * 100)}%"

        self.volume_slider = Slider(
            cx - 200, top, 400,
            0.0, 1.0, step = 0.01, initial = initial_value,
            label = "гучність",
            value_to_text = volume_to_text
        )
        self.volume_slider.set_on_change(self._on_volume)

        def  keys_to_text(v):
            return str(int(v))

        self.keys_slider = Slider(
            cx - 200, top + 120, 400,
            min_key, max_key, step = 1, initial = initial_keys,
            label = "кількість клавіш",
            value_to_text = keys_to_text
        )
        self.keys_slider.set_on_change(self._on_keys)
    def _on_change(self,v):
        if self.on_change:
            self.on_change(float(v), int(self.keys_slider.value))

    def _on_keys(self, v):
        if self.on_change:
            self.on_change(float(self.volume_slider.value), int(v))

    def _on_volume(self, v):
        if self.on_change:
            self.on_change(float(v), int(self.keys_slider.value))

    def _back(self):
        if self.on_back:
            self.on_back()

    def draw(self, screen, font):
        title = font.render("settings", True, (0, 0, 0,))
        screen.blit(title, title.get_rect(center=(self.screen.centerx, 80)))

        self.back_btn.draw(screen, font)
        self.volume_slider.draw(screen, font)
        self.keys_slider.draw(screen, font)

    def handle_event(self, event):
        self.back_btn.handle_event(event)
        self.volume_slider.handle_event(event)
        self.keys_slider.handle_event(event)


