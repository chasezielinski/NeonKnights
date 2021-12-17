import pygame
import settings
from base import BaseState
import settings
import unittest


class TestMenu(BaseState):
    def __init__(self):
        super(TestMenu, self).__init__()
        self.next_state = "MENU"
        self.menu_options = {
            "Run Actions Test": self.run_actions_test,
            "To Battle Test Menu": self.to_battle_test_menu,
            "Return to Main Menu": self.return_to_main,
        }
        self.index = "Return to Main Menu"

    def startup(self, persistent):
        self.persist = persistent
        self.persist["Transition"].fade_in(500)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        for i, option in enumerate(self.menu_options):
            color = settings.TEXT_COLOR
            if option == self.index:
                color = settings.SELECTED_COLOR
            rect = [0, (settings.Y / 10) + (i * settings.Y * 7 / 100), settings.X, settings.Y * 7 / 100]
            settings.tw(surface, option, color, rect, settings.HEADING_FONT, x_mode="center")

    def handle_action(self, action):
        if action == "Return":
            self.select_option()
        elif action == "Up":
            self.option_decrement()
        elif action == "Down":
            self.option_increment()

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

    def option_increment(self):
        index = list(self.menu_options).index(self.index)
        index += 1
        index %= len(self.menu_options)
        self.index = list(self.menu_options)[index]

    def option_decrement(self):
        index = list(self.menu_options).index(self.index)
        index -= 1
        index %= len(self.menu_options)
        self.index = list(self.menu_options)[index]

    def select_option(self):
        self.menu_options[self.index]()

    def return_to_main(self):
        self.next_state = "MENU"
        self.done = True

    def run_actions_test(self):
        for action in ACTION_LIST:
            ACTION = action
            unittest.main(module='test_menu', defaultTest="TestActionCompleteness", exit=False)

    def to_battle_test_menu(self):
        self.next_state = "BATTLE_TEST"
        self.done = True


ACTION_LIST = settings.ActionGetter.get_actions_list()
ACTION = ACTION_LIST[0]


class TestActionCompleteness(unittest.TestCase):
    """Test each action in json file."""

    def setUp(self):
        self.action = settings.ActionGetter.get_action(name=ACTION)

    def test_target_type_getter(self):
        target_type = self.action.get_target_type()
        self.assertTrue(isinstance(target_type, settings.TargetType))

    def test_damage_type_getter(self):
        damage_type = self.action.get_damage_type()
        self.assertTrue(isinstance(damage_type, settings.DamageType))

    def test_damage_stat_getter(self):
        damage_stat = self.action.get_damage_stat()
        self.assertTrue(isinstance(damage_stat, settings.Stat))

    def test_power_getter(self):
        power = self.action.get_power()
        self.assertTrue(isinstance(power, int))


