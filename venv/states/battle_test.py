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
        self.character_options = {
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
        }
        self.battle_options = BattleOptions()

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))

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
        pass


class PlayerOptions:
    def __init__(self, slot):
        self.team = "team_1"
        self.slot = slot
        self.type = "Fighter"
        self.active = True
        self.level = 1
        self.equipment = {}
        self.abilities = {}
        self.items = []


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

