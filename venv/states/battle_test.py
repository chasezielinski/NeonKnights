import pygame
import settings
from base import BaseState
import settings
import unittest


class BattleTest(BaseState):
    def __init__(self):
        super(BattleTest, self).__init__()
        self.next_state = "TEST_MENU"
        self.state = "setup"
        self.setup_options = {
            "team_1_a": PlayerOptions(0),
            "team_1_b": PlayerOptions(1),
            "team_1_c": PlayerOptions(2),
            "team_1_d": PlayerOptions(3),
            "team_1_e": PlayerOptions(4),
            "team_2_a": PlayerOptions(5),
            "team_2_b": PlayerOptions(6),
            "team_2_c": PlayerOptions(7),
            "team_2_d": PlayerOptions(8),
            "team_2_e": PlayerOptions(9),
            "battle_options": BattleOptions(),
            "start": "start",
            "return": "return",
        }
        self.setup_index = list(self.setup_options)[0]

    def update(self, dt):
        if self.state == "detail":
            self.setup_options[self.setup_index].update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        if self.state == "setup":
            for i, value in enumerate(list(self.setup_options)):
                color = settings.TEXT_COLOR
                if self.setup_index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5/100 + 7/100 * i), settings.X, settings.Y * 7/100]
                settings.tw(surface, value, color, rect, settings.HEADING_FONT, x_mode="center")
        elif self.state == "detail":
            self.setup_options[self.setup_index].draw(surface)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.handle_action("Left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("Right")
            elif event.key == pygame.K_UP:
                self.handle_action("Up")
            elif event.key == pygame.K_DOWN:
                self.handle_action("Down")
            elif event.key == pygame.K_RETURN:
                self.handle_action("Return")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("Backspace")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")

    def handle_action(self, action):
        if self.state == "setup":
            if action == "Up":
                self.change_option(self.setup_options, up=True)
            elif action == "Down":
                self.change_option(self.setup_options)
            elif action == "Return":
                self.menu_select()
        elif self.state == "detail":
            self.setup_options[self.setup_index].handle_action(action)

    def change_option(self, options, up=False):
        if self.setup_index in list(options):
            dir = 1
            if up:
                dir = -1
            index = list(options).index(self.setup_index) + dir
            index %= len(options)
            self.setup_index = list(options)[index]
        else:
            self.setup_index = list(options)[0]

    def menu_select(self):
        if self.setup_index == "return":
            self.next_state = "TEST_MENU"
            self.done = True
        elif self.setup_index == "start":
            pass
        else:
            self.state = "detail"


class PlayerOptions:
    def __init__(self, slot):
        self.state = "overview"
        self.options = {"team": None,
                        "slot": None,
                        "type": None,
                        "active": None,
                        "level": None,
                        "equipment": None,
                        "abilities": None,
                        "items": None,
                        "return": None
                        }
        self.index = list(self.options)[0]
        self.team = "team_2"
        if slot in [0, 1, 2, 3, 4]:
            self.team = "team_1"
        self.slot = slot
        self.type = "Fighter"
        self.active = True
        self.level = 1
        self.equipment = {}
        self.abilities = {}
        self.items = []

    def draw(self, surface):
        if self.state == "overview":
            for i, value in enumerate(list(self.options)):
                color = settings.TEXT_COLOR
                if self.index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5/100 + (i * 6/100)), settings.X * 25/100, settings.Y * 5/100]
                settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")

    def handle_action(self, action):
        if self.state == "overview":
            if action == "Up":
                self.change_option(self.options, up=True)
            elif action == "Down":
                self.change_option(self.options)
            elif action == "Return":
                self.menu_select()

    def change_option(self, options, up=False):
        if self.index in list(options):
            dir = 1
            if up:
                dir = -1
            index = list(options).index(self.index) + dir
            index %= len(options)
            self.index = list(options)[index]
        else:
            self.index = list(options)[0]

    def menu_select(self):
        pass

    def update(self, dt):
        pass


class BattleOptions:
    def __init__(self):
        pass


class StateEncoder:
    @staticmethod
    def encode(state):
        pass


class StateActionEncoder:
    @staticmethod
    def encode(state, action):
        pass

