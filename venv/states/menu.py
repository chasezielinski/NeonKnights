import pygame
import settings

from base import BaseState


class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.options = ["Start Game", "Map Bounds", "Quit Game"]
        self.next_state = "CHARACTER_SELECT"
        self.rects = {0: [settings.X * 35 / 100, settings.Y / 3, settings.X * 30 / 100, settings.Y * 10 / 100],
                      1: [settings.X * 35 / 100, settings.Y / 3 + settings.Y * 10 / 100, settings.X * 30 / 100,
                          settings.Y * 10 / 100],
                      2: [settings.X * 35 / 100, settings.Y / 3 + settings.Y * 20 / 100, settings.X * 30 / 100,
                          settings.Y * 10 / 100],
                      3: [settings.X * 35 / 100, settings.Y / 3 + settings.Y * 30 / 100, settings.X * 30 / 100,
                          settings.Y * 10 / 100],
                      4: [settings.X * 35 / 100, settings.Y / 3 + settings.Y * 40 / 100, settings.X * 30 / 100,
                          settings.Y * 10 / 100],
                      }

    def startup(self, persistent):
        self.persist = persistent
        self.persist["Transition"].fade_in(500)
        self.persist["Music"].change_music("Title")

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self, action):
        if action == "return":
            if self.active_index == 0:
                self.done = True
                self.next_state = "CHARACTER_SELECT"
                self.persist['Music'].fade_out(1000)
            if self.active_index == 1:
                self.done = True
                self.next_state = "MAP_BOUNDS"
                self.persist['Music'].fade_out(1000)
            elif self.active_index == 2:
                self.quit = True
        elif action == "mouse_move":
            for i in range(len(self.options)):
                if settings.click_check(self.rects[i]):
                    self.active_index = i
                    break
                else:
                    self.active_index = -1
        elif action == "click":
            for i in range(len(self.options)):
                if settings.click_check(self.rects[i]):
                    self.active_index = i
                    self.handle_action("return")
                else:
                    self.active_index = -1

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.persist['SFX'].schedule_sfx("Toggle_2")
                self.active_index -= 1
                self.active_index %= len(self.options)
            elif event.key == pygame.K_DOWN:
                self.persist['SFX'].schedule_sfx("Toggle_2")
                self.active_index += 1
                self.active_index %= len(self.options)
            elif event.key == pygame.K_RETURN:
                self.persist['SFX'].schedule_sfx("Confirm_1")
                self.handle_action("return")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def update(self, dt):
        self.persist["Transition"].update(dt)
        self.persist['SFX'].update(dt)
        self.persist['FX'].update(dt)
        self.persist['Music'].update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        for index, option in enumerate(self.options):
            color = settings.TEXT_COLOR
            if index == self.active_index:
                color = settings.SELECTED_COLOR
            settings.tw(surface, option, color, self.rects[index], settings.HEADING_FONT, x_mode="center")
        self.persist["Transition"].draw(surface)
        self.persist['FX'].draw(surface)
