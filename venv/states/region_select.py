import pygame
import settings

from base import BaseState


class RegionSelect(BaseState):
    def __init__(self):
        super(RegionSelect, self).__init__()
        self.active_index = 0
        self.index = -1
        self.next_state = "REGION"
        self.options = []
        self.rects = {0: [75, 20, 330, 680],
                      1: [475, 20, 330, 680],
                      2: [875, 20, 330, 680], }
        self.text_rects = {0: [80, 60, 300, 50],
                           1: [480, 600, 300, 50],
                           2: [880, 60, 300, 50], }
        self.image_pos = {0: (80, 120),
                           1: (480, 60),
                           2: (880, 180),}

    def startup(self, persistent):
        self.persist = persistent
        self.options = self.persist["world"].get_options(self.persist["region_index"])

    def handle_action(self, action):
        if action == "return":
            if self.index == 0 or self.index == 1 or self.index == 2:
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.go_to_region()
        elif action == "mouse_move":
            for key, value in self.rects.items():
                if settings.click_check(value):
                    if self.index != key:
                        settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                    self.index = key
                    break
            else:
                self.index = -1
        elif action == "click":
            if self.index == 0 or self.index == 1 or self.index == 2:
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.go_to_region()
        elif action == "right":
            settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
            self.index += 1
            self.index %= len(self.options)
        elif action == "left":
            settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
            self.index -= 1
            self.index %= len(self.options)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.handle_action("left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("right")
            elif event.key == pygame.K_RETURN:
                self.handle_action("return")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def go_to_region(self):
        self.persist['region_type'] = self.options[self.index]
        self.persist['region_generate'] = True
        self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        for key, value in self.rects.items():
            rect_color = (50, 50, 50)
            text_color = settings.TEXT_COLOR
            if self.index == key:
                rect_color = (80, 80, 80)
                text_color = settings.SELECTED_COLOR
            pygame.draw.rect(surface, rect_color, value, border_radius=4)
            surface.blit(settings.REGION_CARDS[self.options[key]], self.image_pos[key])
            settings.tw(surface, self.options[key], text_color, self.text_rects[key], settings.HEADING_FONT,
                        x_mode="center")
