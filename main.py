import sys
import pygame

# initialize the game
# create the screen
screen = pygame.display.set_mode((1280, 720))

from menu import Menu
# from states.game_over import GameOver
from splash import Splash
# from states.battle_pause import Pause
from game import Game
from characterselect import CharacterSelect
from region_2 import Region
from battle2 import Battle
from map_bounds import MapBounds
from region_select import RegionSelect
from test_menu import TestMenu
from battle_test import BattleTest

pygame.mixer.set_num_channels(16)
# enumerate states
states = {
    "MENU": Menu(),
    #    "SETUPMENU": SetupMenu(),
    "SPLASH": Splash(),
    "CHARACTER_SELECT": CharacterSelect(),
    "REGION": Region(),
    "BATTLE": Battle(),
    "MAP_BOUNDS": MapBounds(),
    "REGION_SELECT": RegionSelect(),
    "TEST_MENU": TestMenu(),
    "BATTLE_TEST": BattleTest(),
    #    "GAMEPLAY": Gameplay(),
    #    "GAME_OVER": GameOver(),
    #    "PAUSE": Pause(),
}

icon = pygame.image.load('sword.png')
pygame.display.set_icon(icon)

# Title and Icon
pygame.display.set_caption("Neon Knights")

game = Game(screen, states, "SPLASH")
game.run()

pygame.quit()
sys.exit()
