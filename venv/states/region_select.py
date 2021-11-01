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

    def startup(self, persistent):
        self.persist = persistent
        self.options.append(self.persist['region_type'])
        while len(self.options) < 4:
            choice = settings.choose_random(settings.REGION_BIOMES)
            if choice not in self.options:
                self.options.append(choice)
        self.options = self.options[1:]

    def handle_action(self, action):
        if action == "return":
            if self.index == 0 or self.index == 1 or self.index == 2:
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.go_to_region()
        elif action == "mouse_move":
            if settings.click_check([75, 20, 330, 680]):
                if self.index != 0:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.index = 0
            elif settings.click_check([475, 20, 330, 680]):
                if self.index != 1:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.index = 1
            elif settings.click_check([875, 20, 330, 680]):
                if self.index != 2:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.index = 2
            else:
                self.index = -1
        elif action == "click":
            if self.index == 0 or self.index == 1 or self.index == 2:
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.go_to_region()
        elif action == "right":
            settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
            self.index +=1
            self.index %= len(self.options)
        elif action == "left":
            settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
            self.index -=1
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
        rect_color = (50, 50, 50)
        text_color = settings.TEXT_COLOR
        if self.index == 0:
            rect_color = (80, 80, 80)
            text_color = settings.SELECTED_COLOR
        pygame.draw.rect(surface, rect_color, [75, 20, 330, 680], border_radius=4)
        surface.blit(settings.REGION_CARDS[self.options[0]], (80, 120))
        settings.tw(surface, self.options[0].rjust(15 - len(self.options[0])), text_color,
                    [80, 60, 300, 50], settings.HEADING_FONT)
        rect_color = (50, 50, 50)
        text_color = settings.TEXT_COLOR
        if self.index == 1:
            rect_color = (80, 80, 80)
            text_color = settings.SELECTED_COLOR
        pygame.draw.rect(surface, rect_color, [475, 20, 330, 680], border_radius=4)
        surface.blit(settings.REGION_CARDS[self.options[1]], (480, 60))
        settings.tw(surface, self.options[1].rjust(15 - len(self.options[1])), text_color,
                    [480, 600, 300, 50], settings.HEADING_FONT)
        rect_color = (50, 50, 50)
        text_color = settings.TEXT_COLOR
        if self.index == 2:
            rect_color = (80, 80, 80)
            text_color = settings.SELECTED_COLOR
        pygame.draw.rect(surface, rect_color, [875, 20, 330, 680], border_radius=4)
        surface.blit(settings.REGION_CARDS[self.options[2]], (880, 180))
        settings.tw(surface, self.options[2].rjust(15 - len(self.options[2])), text_color,
                    [880, 80, 300, 50], settings.HEADING_FONT)
