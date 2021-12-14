import pygame
import settings
from base import BaseState
import settings


class TestMenu(BaseState):
    def __init__(self):
        super(TestMenu, self).__init__()
        self.next_state = "MENU"
        self.menu_options = {
            0: "Return to Main Menu"
        }