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
            if self.setup_options[self.setup_index].done:
                self.state = "setup"
                self.setup_options[self.setup_index].done = False

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        if self.state == "setup":
            for i, value in enumerate(list(self.setup_options)):
                color = settings.TEXT_COLOR
                if self.setup_index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5 / 100 + 7 / 100 * i), settings.X, settings.Y * 7 / 100]
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
            elif 0 <= event.key <= 122:
                print("{}".format(event.unicode))
                self.handle_action("{}".format(event.unicode))

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
        self.done = False
        self.state = "overview"
        team = "team_2"
        if slot in [0, 1, 2, 3, 4]:
            team = "team_1"
        self.options = {"team": team,
                        "slot": slot,
                        "type": settings.CharacterGetter.get_list() + settings.EnemyGetter.get_list() + ["random"],
                        "active": [True, False],
                        "level": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                        "equipment": None,  # get list of all equipment
                        "abilities": None,  # get list of all abilities
                        "items": None,  # get list of all battle items
                        "return to menu": None
                        }
        self.settings = {"team": team,
                         "slot": slot,
                         "type": self.options["type"][0],
                         "active": self.options["active"][0],
                         "level": self.options["level"][0],
                         "equipment": None,
                         "abilities": None,
                         "items": None,
                         "return to menu": None
                         }
        self.index = list(self.settings)[0]
        self.slot = slot
        self.type = "Fighter"
        self.active = True
        self.level = 1
        self.equipment = {}
        self.abilities = {}
        self.items = []
        self.get_input = GetInput()

    def draw(self, surface):
        if self.state == "overview":
            for i, value in enumerate(list(self.settings)):
                color = settings.TEXT_COLOR
                if self.index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100, settings.Y * 5 / 100]
                settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")
                if self.settings[value] is not None:
                    rect = [settings.X * 30 / 100, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100,
                            settings.Y * 5 / 100]
                    settings.tw(surface, str(self.settings[value]), color, rect, settings.TEXT_FONT, x_mode="ljust")

    def handle_action(self, action):
        if self.state == "overview":
            if action == "Up":
                self.change_option(self.settings, up=True)
            elif action == "Down":
                self.change_option(self.settings)
            elif action == "Return":
                self.menu_select()

    def menu_select(self):
        if self.index == "return to menu":
            self.done = True
        elif isinstance(self.options[self.index], list):
            self.increment_option()
        elif isinstance(self.options[self.index], int):
            self.state = "input"
            self.get_input.integer_input(self.index)

    def increment_option(self):
        index = self.options[self.index].index(self.settings[self.index]) + 1
        index %= len(self.options[self.index])
        self.settings[self.index] = self.options[self.index][index]

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

    def update(self, dt):
        pass


class BattleOptions:
    def __init__(self):
        self.done = False
        self.state = "overview"
        self.settings = {"number of games": 1,
                         "team 1 AI mode": "manual",
                         "team 2 AI mode": "manual",
                         "step mode": "off",
                         "return to menu": None
                         }
        self.options = {"number of games": 1,
                        "team 1 AI mode": ["manual", "utility AI"],
                        "team 2 AI mode": ["manual", "utility AI"],
                        "step mode": ["off", "turn", "battle"],
                        "return to menu": None
                        }
        self.index = list(self.settings)[0]
        self.get_input = GetInput()

    def draw(self, surface):
        if self.state == "overview":
            for i, value in enumerate(list(self.settings)):
                color = settings.TEXT_COLOR
                if self.index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100, settings.Y * 5 / 100]
                settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")
                if self.settings[value] is not None:
                    rect = [settings.X * 30 / 100, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100,
                            settings.Y * 5 / 100]
                    settings.tw(surface, str(self.settings[value]), color, rect, settings.TEXT_FONT, x_mode="ljust")
        elif self.state == "input":
            self.get_input.draw(surface)

    def handle_action(self, action):
        if self.state == "overview":
            if action == "Up":
                self.change_option(self.settings, up=True)
            elif action == "Down":
                self.change_option(self.settings)
            elif action == "Return":
                self.menu_select()
        elif self.state == "input":
            self.get_input.handle_action(action)

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
        if self.index == "return to menu":
            self.done = True
        elif isinstance(self.options[self.index], list):
            self.increment_option()
        elif isinstance(self.options[self.index], int):
            self.state = "input"
            self.get_input.integer_input(self.index)

    def increment_option(self):
        index = self.options[self.index].index(self.settings[self.index]) + 1
        index %= len(self.options[self.index])
        self.settings[self.index] = self.options[self.index][index]

    def update(self, dt):
        if self.state == "input":
            if self.get_input.done:
                self.get_input.done = False
                self.settings[self.index] = self.get_input.input
                self.state = "overview"


class GetInput:
    def __init__(self):
        self.input = ""
        self.prompt = None
        self.type = "int"
        self.done = False

    def update(self, dt):
        pass

    def draw(self, surface):
        rect = [settings.X * 40 / 100, settings.Y * 40 / 100, settings.X * 20 / 100, settings.Y * 20 / 100]
        pygame.draw.rect(surface, (20, 20, 20), rect)
        if self.prompt:
            rect = [settings.X * 40 / 100, settings.Y * 42 / 100, settings.X * 20 / 100, settings.Y * 20 / 100]
            settings.tw(surface, self.prompt, settings.TEXT_COLOR, rect, settings.TEXT_FONT, x_mode="center")
        if self.input:
            rect = [settings.X * 40 / 100, settings.Y * 50 / 100, settings.X * 20 / 100, settings.Y * 20 / 100]
            settings.tw(surface, self.input, settings.TEXT_COLOR, rect, settings.TEXT_FONT, x_mode="center")

    def handle_action(self, action):
        if self.type == "int" or self.type == "str":
            if action in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                self.input += action
        elif self.type == "str":
            if action in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                          "s", "t", "u", "v", "w", "x", "y", "z", "_"]:
                self.input += action
        if action == "Backspace" and len(self.input) > 0:
            self.input = self.input[:-1]
        elif action == "Return":
            if self.type == "int":
                try:
                    self.input = int(self.input)
                except:
                    print("integer input only")
                else:
                    self.done = True
                    self.input = str(self.input)
            elif self.type == "str":
                self.done = True

    def integer_input(self, prompt: str):
        self.type = "int"
        self.prompt = prompt

    def string_input(self, prompt: str):
        self.type = "str"
        self.prompt = prompt


class StateEncoder:
    @staticmethod
    def encode(state):
        pass


class StateActionEncoder:
    @staticmethod
    def encode(state, action):
        pass
