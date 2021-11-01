import sys
import pygame
import settings
from menu import Menu
# from states.game_over import GameOver
from splash import Splash
# from states.battle_pause import Pause
from game import Game
from characterselect import CharacterSelect
from region import Region
from battle2 import Battle
from map_bounds import MapBounds
from region_select import RegionSelect

# initialize the game
# create the screen
screen = pygame.display.set_mode((settings.X, settings.Y))

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
    #    "GAMEPLAY": Gameplay(),
    #    "GAME_OVER": GameOver(),
    #    "PAUSE": Pause(),
}

icon = settings.image_load('sword.png')
pygame.display.set_icon(icon)

# Title and Icon
pygame.display.set_caption("Neon Knights")

game = Game(screen, states, "SPLASH")
game.run()

pygame.quit()
sys.exit()
