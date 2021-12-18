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
        self.battle_manager = BattleTestManager()

    def update(self, dt):
        if self.state == "detail":
            self.setup_options[self.setup_index].update(dt)
            if self.setup_options[self.setup_index].done:
                self.state = "setup"
                self.setup_options[self.setup_index].done = False
        elif self.state == "battle":
            self.battle_manager.update(dt)

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
        elif self.state == "battle":
            self.battle_manager.draw(surface)

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
                self.handle_action("Space")
            elif event.key == pygame.K_TAB:
                self.handle_action("Tab")
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
            elif action == "Tab":
                if not isinstance(self.setup_options[self.setup_index], str):
                    self.setup_options[self.setup_index].toggle_active()
        elif self.state == "detail":
            self.setup_options[self.setup_index].handle_action(action)
            if action == "Tab":
                self.change_option(self.setup_options)
                if isinstance(self.setup_options[self.setup_index], str):
                    self.setup_index = list(self.setup_options)[0]
        elif self.state == "battle":
            self.battle_manager.handle_action(action)

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
            self.state = "battle"
            team_1 = [self.setup_options["team_1_a"], self.setup_options["team_1_b"], self.setup_options["team_1_c"],
                      self.setup_options["team_1_d"], self.setup_options["team_1_e"]]
            team_2 = [self.setup_options["team_2_a"], self.setup_options["team_2_b"], self.setup_options["team_2_c"],
                      self.setup_options["team_2_d"], self.setup_options["team_2_e"]]
            self.battle_manager.set_battle(self.setup_options["battle_options"], team_1, team_2)
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
                        "active": [True, False],
                        "type": settings.CharacterGetter.get_list() + settings.EnemyGetter.get_list(),
                        "type option": ["set", "random"],
                        "level": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                        "level option": ["set", "random", "range"],
                        "level upper": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                        "level lower": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                        "equipment": None,  # get list of all equipment
                        "equipment option": ["set", "random"],
                        "abilities": settings.ActionGetter.get_actions_list(learnable=True),
                        "abilities option": ["set", "random"],
                        "items": None,  # get list of all battle items
                        "items option": ["set", "random"],
                        "return to menu": None
                        }
        self.settings = {"team": team,
                         "slot": slot,
                         "active": self.options["active"][0],
                         "type": self.options["type"][0],
                         "type option": self.options["type option"][0],
                         "level": self.options["level"][0],
                         "level option": self.options["level option"][0],
                         "level upper": self.options["level upper"][0],
                         "level lower": self.options["level lower"][0],
                         "equipment": None,
                         "equipment option": self.options["equipment option"][0],
                         "abilities": None,
                         "abilities option": self.options["abilities option"][0],
                         "items": None,
                         "items option": self.options["items option"][0],
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
        self.pick_from_list = None
        self.equipment_picker = EquipmentPicker()

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
        elif self.state == "pick_from_list":
            self.pick_from_list.draw(surface)
        elif self.state == "equipment":
            self.equipment_picker.draw(surface)

    def handle_action(self, action):
        if self.state == "overview":
            if action == "Up":
                self.change_option(self.settings, up=True)
            elif action == "Down":
                self.change_option(self.settings)
            elif action == "Return":
                self.menu_select()
        elif self.state == "pick_from_list":
            self.pick_from_list.handle_action(action)
        elif self.state == "equipment":
            self.equipment_picker.handle_action(action)

    def menu_select(self):
        if self.index == "return to menu":
            self.done = True
        elif self.index == "equipment":
            self.state = "equipment"
        elif self.index == "abilities":
            self.pick_from_list = ListPicker(self.options[self.index])
            self.state = "pick_from_list"
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
        if self.state == "pick_from_list":
            if self.pick_from_list.done:
                self.state = "overview"
                if self.pick_from_list.selection:
                    self.settings[self.index] = self.pick_from_list.selection
                else:
                    self.settings[self.index] = None
                self.pick_from_list.done = False

        elif self.state == "equipment":
            if self.equipment_picker.done:
                self.state = "overview"
                self.equipment_picker.done = False
            self.equipment_picker.update(dt)

    def toggle_active(self):
        self.settings["active"] = not self.settings["active"]


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
        elif self.index == "equipment":
            self.state = "equipment"
        elif self.index == "abilities":
            self.pick_from_list = ListPicker(self.options[self.index])
            self.state = "pick_from_list"
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

    def get_n_games(self):
        return self.settings["number of games"]

    def toggle_active(self):
        pass


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


class ListPicker:
    def __init__(self, list_):
        self.selection = []
        self.list_ = list_
        self.menu_dict = {x: False for x in self.list_}
        self.menu_dict["done"] = self.finish_select
        self.done = False
        self.index = list(self.menu_dict)[0]

    def update(self, dt):
        pass

    def draw(self, surface):
        for i, value in enumerate(list(self.menu_dict)):
            color = settings.TEXT_COLOR
            if self.index == value:
                color = settings.SELECTED_COLOR
            rect = [0, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100, settings.Y * 5 / 100]
            settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")
            if self.menu_dict[value] is not None:
                rect = [settings.X * 30 / 100, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100,
                        settings.Y * 5 / 100]
                settings.tw(surface, str(self.menu_dict[value]), color, rect, settings.TEXT_FONT, x_mode="ljust")

    def handle_action(self, action):
        if action == "Return":
            if isinstance(self.menu_dict[self.index], bool):
                self.menu_dict[self.index] = not self.menu_dict[self.index]
            elif self.index == "done":
                self.menu_dict[self.index]()
        elif action == "Up":
            self.change_option(self.menu_dict, up=True)
        elif action == "Down":
            self.change_option(self.menu_dict)

    def finish_select(self):
        self.selection = [x for x in self.menu_dict if self.menu_dict[x] and x != "done"]
        self.done = True

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


class PickOne:
    def __init__(self, list_):
        self.selection = None
        self.list_ = list_
        self.menu_dict = {x: False for x in self.list_}
        self.menu_dict["done"] = self.finish_select
        self.done = False
        self.index = list(self.menu_dict)[0]

    def update(self, dt):
        pass

    def draw(self, surface):
        for i, value in enumerate(list(self.menu_dict)):
            color = settings.TEXT_COLOR
            if self.index == value:
                color = settings.SELECTED_COLOR
            rect = [0, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100, settings.Y * 5 / 100]
            settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")
            if self.menu_dict[value] is not None:
                rect = [settings.X * 30 / 100, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100,
                        settings.Y * 5 / 100]
                settings.tw(surface, str(self.menu_dict[value]), color, rect, settings.TEXT_FONT, x_mode="ljust")

    def handle_action(self, action):
        if action == "Return":
            if self.index == "done":
                self.menu_dict[self.index]()
            elif isinstance(self.menu_dict[self.index], bool):
                for k in self.menu_dict:
                    if k == self.index:
                        self.menu_dict[k] = not self.menu_dict[k]
                    elif k != "done":
                        self.menu_dict[k] = False
        elif action == "Up":
            self.change_option(self.menu_dict, up=True)
        elif action == "Down":
            self.change_option(self.menu_dict)

    def finish_select(self):
        for k, v in self.menu_dict.items():
            if v:
                self.selection = k
                break
        else:
            self.selection = None
        self.done = True

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


class EquipmentPicker:
    def __init__(self):
        self.done = False
        self.menu_dict = {x.name: None for x in settings.EquipmentType}
        self.menu_dict["done"] = self.finish_select
        self.index = list(self.menu_dict)[0]
        self.picker = None
        self.state = "menu"

    def update(self, dt):
        if self.state == "pick":
            if self.picker.done:
                if self.picker.selection:
                    self.menu_dict[self.index] = self.picker.selection
                else:
                    self.menu_dict[self.index] = None
                self.picker.done = False
                self.state = "menu"

    def draw(self, surface):
        if self.state == "menu":
            for i, value in enumerate(list(self.menu_dict)):
                color = settings.TEXT_COLOR
                if self.index == value:
                    color = settings.SELECTED_COLOR
                rect = [0, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100, settings.Y * 5 / 100]
                settings.tw(surface, value, color, rect, settings.TEXT_FONT, x_mode="rjust")
                if self.menu_dict[value] is not None:
                    rect = [settings.X * 30 / 100, settings.Y * (5 / 100 + (i * 6 / 100)), settings.X * 25 / 100,
                            settings.Y * 5 / 100]
                    settings.tw(surface, str(self.menu_dict[value]), color, rect, settings.TEXT_FONT, x_mode="ljust")
        elif self.state == "pick":
            self.picker.draw(surface)

    def handle_action(self, action):
        if self.state == "menu":
            if action == "Return":
                if self.index == "done":
                    self.menu_dict[self.index]()
                else:
                    self.picker = PickOne(settings.ItemGetter.get_list_by_type(settings.EquipmentType[self.index]))
                    self.state = "pick"
            elif action == "Up":
                self.change_option(self.menu_dict, up=True)
            elif action == "Down":
                self.change_option(self.menu_dict)
        elif self.state == "pick":
            self.picker.handle_action(action)

    def finish_select(self):
        self.done = True

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


class BattleTestManager:
    def __init__(self):
        self.state = "pre_battle"
        self.done = False
        self.options = None
        self.team_1 = []
        self.team_1_score = 0
        self.team_2 = []
        self.team_2_score = 0
        self.team_1_call = None
        self.team_2_call = None
        self.options = None
        self.battle_actions = []

    def draw(self, surface):
        settings.tw(surface, f"team 1 {self.team_1_score}", settings.TEXT_COLOR,
                    [0, settings.Y * 2 / 100, settings.X / 2, settings.Y * 7 / 100], settings.HEADING_FONT,
                    x_mode="center")
        settings.tw(surface, f"team 2 {self.team_2_score}", settings.TEXT_COLOR,
                    [settings.X / 2, settings.Y * 2 / 100, settings.X / 2, settings.Y * 7 / 100], settings.HEADING_FONT,
                    x_mode="center")
        rect = [0, settings.Y * 90 / 100, settings.X, settings.Y * 7 / 100]
        settings.tw(surface, self.state, settings.TEXT_COLOR, rect, settings.HEADING_FONT, x_mode="center")
        for i, character in enumerate(self.team_1):
            n_rect = [settings.X * 2 / 100, settings.Y * (2 / 100 + i * 20 / 100), settings.X * 40 / 100,
                      settings.Y * 8 / 100]
            s_rect = [settings.X * 2 / 100, settings.Y * (10 / 100 + i * 20 / 100), settings.X * 40 / 100,
                      settings.Y * 8 / 100]
            settings.tw(surface, f"team_1 {i}", settings.TEXT_COLOR, n_rect, settings.TEXT_FONT)
            text_ = f"hp: {character.get_remaining_hp()} / {character.get_stat(settings.Stat.HP)}"
            settings.tw(surface, text_, settings.TEXT_COLOR, s_rect, settings.TEXT_FONT)
        for i, character in enumerate(self.team_2):
            n_rect = [settings.X * 52 / 100, settings.Y * (2 / 100 + i * 20 / 100), settings.X * 40 / 100,
                      settings.Y * 8 / 100]
            s_rect = [settings.X * 52 / 100, settings.Y * (10 / 100 + i * 20 / 100), settings.X * 40 / 100,
                      settings.Y * 8 / 100]
            settings.tw(surface, f"team_2 {i}", settings.TEXT_COLOR, n_rect, settings.TEXT_FONT, x_mode="rjust")
            text_ = f"hp: {character.get_remaining_hp()} / {character.get_stat(settings.Stat.HP)}"
            settings.tw(surface, text_, settings.TEXT_COLOR, s_rect, settings.TEXT_FONT, x_mode="rjust")

    def update(self, dt):
        if self.state in ["action", "post_turn"]:
            self.character_check()
            self.victory_check()
            self.match_check()
        if self.state == "pre_battle":
            if self.options.settings["step mode"] == "off":
                self.state = "pre_turn_team_1"

        elif self.state == "pre_turn_team_1":
            self.team_1_get_actions()
            self.state = "pre_turn_team_1_wait"

        elif self.state == "pre_turn_team_1_wait":
            pass

        elif self.state == "pre_turn_team_2":
            self.team_2_get_actions()
            self.state = "pre_turn_team_2_wait"

        elif self.state == "pre_turn_team_2_wait":
            self.battle_actions.sort(reverse=True)

        elif self.state == "pre_action":
            self.state = "action"

        elif self.state == "action":
            if self.battle_actions:
                self.state = "action_wait"
            else:
                self.state = "post_turn"

        elif self.state == "action_wait":
            self.battle_actions[0].do_action()
            del self.battle_actions[0]

        elif self.state == "post_turn":
            self.state = "post_turn_wait"

        elif self.state == "post_turn_wait":
            pass

    def handle_action(self, action):
        if action == "Space":
            self.increment_step()

    def increment_step(self):
        if self.state == "pre_turn_team_1_wait":
            self.state = "pre_turn_team_2"

        elif self.state == "pre_turn_team_2_wait":
            self.state = "pre_action"

        elif self.state == "action_wait":
            self.state = "pre_action"

        elif self.state == "post_turn_wait":
            self.state = "pre_turn_team_1"

    def set_battle(self, options, team_1, team_2):
        self.team_1_call = team_1
        self.team_2_call = team_2
        self.options = options
        self.team_1 = [TestCharacterGetter.get_character(x) for x in team_1 if x.settings["active"]]
        self.team_2 = [TestCharacterGetter.get_character(x) for x in team_2 if x.settings["active"]]

    def victory_check(self):
        if self.team_1 and not self.team_2:
            self.team_1_win()
        elif self.team_2 and not self.team_1:
            self.team_2_win()
        elif not self.team_1 and not self.team_2:
            self.draw_result()

    def team_1_win(self):
        self.team_1_score += 1
        self.state = "pre_battle"
        self.set_battle(self.options, self.team_1_call, self.team_2_call)

    def team_2_win(self):
        self.team_1_score += 1
        self.state = "pre_battle"
        self.set_battle(self.options, self.team_1_call, self.team_2_call)

    def draw_result(self):
        self.state = "pre_battle"
        self.set_battle(self.options, self.team_1_call, self.team_2_call)

    def character_check(self):
        self.team_1 = [x for x in self.team_1 if x.hp > 0]
        self.team_2 = [x for x in self.team_2 if x.hp > 0]

    def match_check(self):
        if self.team_1_score + self.team_2_score > self.options.get_n_games():
            self.match_done()

    def match_done(self):
        pass

    def team_1_get_actions(self):
        if self.options.settings["team 1 AI mode"] == "manual":
            pass
        elif self.options.settings["team 1 AI mode"] == "utility AI":
            actions = settings.UtilityAI.select_actions(self.team_1, self.team_2)
            for action_eval in actions.actions:
                self.battle_actions.append(TestActionCard(action_eval.user, action_eval.target, action_eval.action))

    def team_2_get_actions(self):
        if self.options.settings["team 2 AI mode"] == "manual":
            pass
        elif self.options.settings["team 2 AI mode"] == "utility AI":
            actions = settings.UtilityAI.select_actions(self.team_2, self.team_1)
            for action_eval in actions.actions:
                self.battle_actions.append(TestActionCard(action_eval.user, action_eval.target, action_eval.action))


class TestCharacterGetter:
    @staticmethod
    def get_character(character_data):
        class_ = TestCharacterGetter.get_type(character_data)
        if settings.CharacterGetter.class_exist(class_):
            character = settings.CharacterGetter.get_character(class_=class_)
        else:
            character = settings.EnemyGetter.get_enemy(class_=class_)
        character.level = TestCharacterGetter.get_level(character_data)
        # equip all equipment here
        # ************************

        character.abilities = TestCharacterGetter.get_abilities(character_data)

        # give all items here
        # ************************
        return character

    @staticmethod
    def get_type(data):
        if data.settings["type option"] == "set":
            return data.settings["type"]
        elif data.settings["type option"] == "random":
            return settings.choose_random(data.options["type"])

    @staticmethod
    def get_level(data):
        if data.settings["level option"] == "set":
            return data.settings["level"]
        elif data.settings["level option"] == "random":
            return settings.choose_random(data.options["level"])
        elif data.settings["level option"] == "range":
            return settings.random_int(data.settings["level lower"], data.settings["level upper"])

    @staticmethod
    def get_abilities(data):
        if data.settings["abilities option"] == "set":
            return [settings.ActionGetter.get_action(name=x) for x in data.settings["abilities"]]
        elif data.settings["abilities option"] == "random":
            n = settings.random_int(0, len(data.options["abilities"]) - 1)
            abilities = [x for x in data.options["abilities"]]
            while n > 0:
                x = settings.random_int(0, len(abilities) - 1)
                del abilities[x]
                n -= 1
            return {x: settings.ActionGetter.get_action(name=x) for x in abilities}


class TestActionCard:
    def __init__(self, source, target, action):
        self.source = source
        self.speed = source.get_stat(settings.Stat.SPEED)
        self.action = action
        self.target = target

    def __lt__(self, other):
        return self.speed < other.speed

    def do_action(self):
        self.action.do_action()


class StateEncoder:
    @staticmethod
    def encode(state):
        pass


class StateActionEncoder:
    @staticmethod
    def encode(state, action):
        pass
