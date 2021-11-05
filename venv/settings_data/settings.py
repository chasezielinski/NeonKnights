import copy
import math
import random
import numpy as np
import pygame
import names
import pytweening
import settings
from threading import Timer

pygame.init()
pygame.mixer.init()

random.seed()

pygame.font.init()
# General Settings

X = 1280
SCREEN_RESOLUTION_X_OPTIONS = {
    "1280": 1280
}
Y = 720
SCREEN_RESOLUTION_Y_OPTIONS = {
    "720": 720
}

REGION_X = X * 5 / 8
REGION_X_OFFSET = X * 1 / 8
REGION_Y = Y * 3 / 4
REGION_Y_OFFSET = Y * 1 / 8

DETAIL_FONT = pygame.font.Font(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\fonts\manaspc.ttf", 16)
TEXT_FONT = pygame.font.Font(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\fonts\manaspc.ttf", 24)
HEADING_FONT = pygame.font.Font(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\fonts\manaspc.ttf", 36)
TEXT_COLOR = (20, 100, 100)
SELECTED_COLOR = (75, 225, 225)
COLOR_KEY = (255, 55, 202)
MAX_NAME_LENGTH = 20

# Player Characters
BASE_CLASSES = ["Fighter", "Adept", "Rogue", "Artificer"]
EXPERIENCE_CURVE = [100, 210, 320, 430, 540, 650, 760, 870, 980, 1090, 1200, 1310, 1420, 1530]
EXPERIENCE_CURVE_TOTAL = [100, 310, 630, 1060, 1600, 2250, 3010, 3880, 4860, 5950, 7150, 8460, 9880, 11410]
for i in range(len(EXPERIENCE_CURVE)):
    EXPERIENCE_CURVE_TOTAL.append(sum(EXPERIENCE_CURVE[:i + 1]))
BASE_STATS = {
    "FIGHTER_BASE_STATS": {'FIGHTER_BASE_HP': 100,
                           'FIGHTER_BASE_MP': 10,
                           'FIGHTER_BASE_STRENGTH': 100,
                           'FIGHTER_BASE_DEFENSE': 10,
                           'FIGHTER_BASE_MAGIC': 10,
                           'FIGHTER_BASE_SPIRIT': 10,
                           'FIGHTER_BASE_SPEED': 10,
                           'FIGHTER_BASE_LUCK': 10000,
                           'FIGHTER_BASE_ATTACK_TYPE': "Attack",
                           'FIGHTER_BASE_EQUIPMENT_OPTIONS': ["Weapon", "Helm", "Armor", "Boots", "Shield"],
                           'FIGHTER_BASE_TECHNIQUES': ["Bash", "Strike", "Impale", "Dash", "Fortify", "Magic Strike",
                                                       "True Strike"], },

    "ADEPT_BASE_STATS": {'ADEPT_BASE_HP': 100,
                         'ADEPT_BASE_MP': 10,
                         'ADEPT_BASE_STRENGTH': 10,
                         'ADEPT_BASE_DEFENSE': 10,
                         'ADEPT_BASE_MAGIC': 10,
                         'ADEPT_BASE_SPIRIT': 10,
                         'ADEPT_BASE_SPEED': 10,
                         'ADEPT_BASE_LUCK': 10,
                         'ADEPT_BASE_ATTACK_TYPE': "Attack",
                         'ADEPT_BASE_EQUIPMENT_OPTIONS': ["Weapon", "Helm", "Armor", "Boots", "Medallion"],
                         'ADEPT_BASE_TECHNIQUES': ["Fireball"]},

    "ROGUE_BASE_STATS": {'ROGUE_BASE_HP': 100,
                         'ROGUE_BASE_MP': 10,
                         'ROGUE_BASE_STRENGTH': 10,
                         'ROGUE_BASE_DEFENSE': 10,
                         'ROGUE_BASE_MAGIC': 10,
                         'ROGUE_BASE_SPIRIT': 10,
                         'ROGUE_BASE_SPEED': 10,
                         'ROGUE_BASE_LUCK': 10,
                         'ROGUE_BASE_ATTACK_TYPE': "Attack",
                         'ROGUE_BASE_EQUIPMENT_OPTIONS': ["Weapon", "Helm", "Armor", "Boots", "Cape"],
                         'ROGUE_BASE_TECHNIQUES': ["Double Strike"]},

    "ARTIFICER_BASE_STATS": {'ARTIFICER_BASE_HP': 100,
                             'ARTIFICER_BASE_MP': 10,
                             'ARTIFICER_BASE_STRENGTH': 10,
                             'ARTIFICER_BASE_DEFENSE': 10,
                             'ARTIFICER_BASE_MAGIC': 10,
                             'ARTIFICER_BASE_SPIRIT': 10,
                             'ARTIFICER_BASE_SPEED': 10,
                             'ARTIFICER_BASE_LUCK': 10,
                             'ARTIFICER_BASE_ATTACK_TYPE': "Attack",
                             'ARTIFICER_BASE_EQUIPMENT_OPTIONS': ["Weapon", "Helm", "Armor", "Boots", "Artifact"],
                             'ARTIFICER_BASE_TECHNIQUES': ["Construct"]},
}


def character_initial(char, char_class):
    if char_class == "Fighter":
        char.equipment["Weapon"] = Weapon("Coder Sword", 1)
        char.equipment["Armor"] = Armor("Iron Plate", "common", '1')
        char.equipment["Boots"] = Boots("Leather Boots", "common", '1')


# Character Select


def image_load(path):
    image = pygame.image.load(path)
    image.set_colorkey(COLOR_KEY)
    return image


MAIN_MENU_RECTS = {
    "options": {0: [X * 37 / 100, Y / 3, X / 4, Y * 10 / 100],
                1: [X * 37 / 100, Y / 3 + Y * 10 / 100, X / 4, Y * 10 / 100],
                2: [X * 37 / 100, Y / 3 + Y * 20 / 100, X / 4, Y * 10 / 100],
                3: [X * 37 / 100, Y / 3 + Y * 30 / 100, X / 4, Y * 10 / 100],
                4: [X * 37 / 100, Y / 3 + Y * 40 / 100, X / 4, Y * 10 / 100],
                },
}

CHARACTER_SELECT_MENU = {
    'class_option_rects': {
        "Fighter": [X * 15 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Adept": [X * 35 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Rogue": [X * 55 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Artificer": [X * 75 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
    },
    'name_entry_option_rects': {
        "random": [X * 75 / 100, Y * 30 / 100, X * 25 / 100, Y * 10 / 100],
        "select": [X * 75 / 100, Y * 40 / 100, X * 25 / 100, Y * 10 / 100],
        "back": [X * 75 / 100, Y * 50 / 100, X * 25 / 100, Y * 10 / 100],
    },
    'confirm_rects': {
        "confirm": [X * 75 / 100, Y * 40 / 100, X * 25 / 100, Y * 10 / 100],
        "back": [X * 75 / 100, Y * 50 / 100, X * 25 / 100, Y * 10 / 100],
    },
    'name_display_rect': [X * 50 / 100, Y * 70 / 100, X * 80 / 100, Y * 5 / 100],
    'class_display_rect': [X * 50 / 100, Y * 5 / 100, X * 80 / 100, Y * 5 / 100],
    'prompt_rect': [X * 1 / 8, Y * 13 / 16, X * 3 / 4, Y * 1 / 8],
    'fighter pos': (X * 1 / 10, Y * 8 / 100),
    'adept pos': (X * 3 / 10, Y * 8 / 100),
    'rogue pos': (X * 5 / 10, Y * 8 / 100),
    'artificer pos': (X * 7 / 10, Y * 8 / 100),
    'selected pos': (X * 4 / 10, Y * 2 / 8),
    'sprites': {
        "Fighter": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character "
                    r"Select\Fighter128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p12.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p12.png"),
            ],
            'idle_frames': [0, 1],
            'idle_weights': [5, 1],
            'idle_speed': 2000,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Rogue": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p12.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p12.png"),
            ],
            'idle_frames': [0, 1],
            'idle_weights': [11, 1],
            'idle_speed': 6000,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Adept": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p16.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p16.png"),
            ],
            'idle_frames': range(16),
            'idle_weights': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'idle_speed': 500,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Artificer": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p16.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p17.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p18.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p19.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p20.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p21.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p22.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p23.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p24.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p25.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p26.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p27.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p28.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p29.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p30.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p16.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p17.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p18.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p19.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p20.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p21.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p22.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p23.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p24.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p25.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p26.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p27.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p28.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p29.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p30.png"),
            ],
            'idle_frames': range(30),
            'idle_weights': [500, 100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100, 50, 50, 200, 50, 30, 30, 30,
                             100, 50, 50, 50, 50, 50, 50, 50, 50],
            'idle_speed': 2290,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        }
    },
}

# Regions

REGION_BIOMES = ["Desert", "Grasslands", "Valley"]  # , "Forest", "Savannah", "Badlands", "Tundra",
# "Rainforest", "Steppe", "Taiga"]
REGION_CARDS = {
    "Desert": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Desert_Card_480p_1.png"),
    "Grasslands": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Grasslands_Card_480p_1.png"),
    "Valley": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Valley_Card_480p_1.png"),
}

REGION_SHAPES = ["Land-Locked", "Coastal", "Archipelago", "Island", "Plateau",
                 "Lakeside", "Canyon", "River"]

REGION_LAYOUTS = {
    # num_nodes=30, knn=4, node_space=100, space_probability=100,
    # node_space_ll=0, node_space_ul=350, min_edge_angle=15
    'Badlands':
        {
            "Badlands_1":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Badlands_720_BG_2.png"),
                    'Start': [176, 424, 312, 592],
                    'End': [904, 496, 1024, 528],
                    'Shapes': [[(120, 224), (432, 264), (592, 184), (760, 176), (1048, 280), (1048, 680), (848, 680),
                                (776, 624), (712, 368), (560, 360), (328, 600), (120, 608)]],
                    'Positive': True,
                },
        },
    'Desert':
        {
            "Desert_1":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Desert_720_BG_1.png"),
                    'Start': [120, 264, 296, 440],
                    'End': [856, 344, 1032, 488],
                    'Shapes': [[(120, 96), (950, 96), (950, 504), (912, 528), (824, 432), (816, 288), (720, 232),
                                (536, 288), (480, 472), (376, 512), (120, 440)],
                               [(120, 512), (336, 600), (552, 528), (640, 392), (728, 432), (856, 584), (950, 580),
                                (950, 580), (120, 580)],
                               [(552, 424), (560, 344), (696, 280), (776, 320), (768, 350), (704, 300), (616, 300)]],
                    'Positive': True,
                },
            "Desert_2":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Desert_720_BG_2.png"),
                    'Start': [124, 94, 266, 418],
                    'End': [956, 244, 1022, 506],
                    'Shapes': [[(122, 92), (966, 90), (680, 369), (650, 588), (602, 606), (420, 476), (124, 428)],
                               [(792, 472), (1026, 164), (1032, 540), (904, 446), (790, 508)]],
                    'Positive': True,
                },
        }
}

NODE_TYPES = [["Empty", "Town", "Dungeon", "Lone Building", "Encounter"], [30, 15, 10, 10, 40]]

NODE_TYPES_2 = [["Shop", "Dungeon", "Encounter", "Event", "Empty"], [1, 2, 40, 27, 30]]


class EmptyNode(object):
    def __init__(self, parent):
        self.parent = parent

    def handle_action(self, action):
        pass

    def update(self, dt):
        self.parent.parent.state = "Browse"

    def draw(self, surface):
        pass


class Shop(object):
    def __init__(self):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def handle_action(self, action):
        pass


class Event(object):
    def __init__(self, parent, parameter_dictionary):
        self.parent = parent
        self.state = "Prompt"
        self.option_index = -1
        self.bg_1_rect = [X * 17 / 100, Y * 7 / 100, X * 60 / 100, Y * 88 / 100]
        self.bg_2_rect = [X * 17 / 100, Y * 8 / 100, X * 59 / 100, Y * 86 / 100]
        self.prompt_rect = [X * 18 / 100, Y * 9 / 100, X * 57 / 100, Y * 84 / 100]
        self.option_rect = [X * 18 / 100, Y * 55 / 100, X * 57 / 100, Y * 5 / 100]
        self.option_offset = 5
        self.timer = 0
        self.next_state = "Prompt"
        self.enemies = None
        self.prompt = None
        self.options = None
        self.supply_reward = None
        self.gold_reward = None
        self.elixir_reward = None
        self.charger_reward = None
        self.item_reward = None
        for key in parameter_dictionary.keys():
            setattr(self, key, parameter_dictionary[key])

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0
        if self.state == "Prompt":
            for index, option in enumerate(self.options):
                if click_check([self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                self.option_rect[2], self.option_rect[3]]):
                    self.option_index = index
                else:
                    self.option_index = -1
        elif self.state == "Delay":
            if self.timer == 0:
                self.state = self.next_state
        elif self.state == "Reward":
            self.reward()
        elif self.state == "Exit":
            self.parent.parent.state = "Browse"
        elif self.state == "Battle":
            self.battle()

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), self.bg_1_rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=8)
        if self.state == "Prompt":
            tw(surface, self.prompt, TEXT_COLOR, self.prompt_rect, TEXT_FONT)
            for index, option in enumerate(self.options):
                color = TEXT_COLOR
                if click_check([self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                self.option_rect[2], self.option_rect[3]]):
                    color = SELECTED_COLOR
                tw(surface, "1. " + option[0], color, [self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                                       self.option_rect[2], self.option_rect[3]], TEXT_FONT)

    def handle_action(self, action):
        if action == "click":
            if self.state == "Prompt":
                for index, option in enumerate(self.options):
                    if click_check([self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                    self.option_rect[2], self.option_rect[3]]):
                        outcome = choose_random_weighted(self.options[index][1], self.options[index][2])
                        if "state" in outcome.keys():
                            setattr(self, "state", outcome["state"])
                        if "prompt" in outcome.keys():
                            setattr(self, "prompt", outcome["prompt"])
                        if "options" in outcome.keys():
                            setattr(self, "options", outcome["options"])

        if action == "return":
            outcome = choose_random_weighted(self.options[self.option_index][1], self.options[self.option_index][2])
            if "state" in outcome.keys():
                setattr(self, "state", outcome["state"])
            if "prompt" in outcome.keys():
                setattr(self, "prompt", outcome["prompt"])
            if "options" in outcome.keys():
                setattr(self, "options", outcome["options"])

    def battle(self):
        self.parent.parent.persist['enemies'] = self.enemies
        self.parent.parent.state = "Browse"
        self.parent.parent.next_state = "BATTLE"
        self.parent.parent.done = True

    def reward(self):
        if self.gold_reward is not None:
            self.parent.parent.persist['gold'] += self.gold_reward
        if self.charger_reward is not None:
            self.parent.parent.persist['chargers'] += self.charger_reward
        if self.elixir_reward is not None:
            self.parent.parent.persist['elixirs'] += self.elixir_reward
        if self.supply_reward is not None:
            self.parent.parent.persist['supplies'] += self.supply_reward
        if self.item_reward is not None:
            if isinstance(self.item_reward, list):
                for item in self.item_reward:
                    self.parent.parent.persist['inventory'].append(item)
            else:
                self.parent.parent.persist['inventory'].append(self.item_reward)
        self.exit()

    def exit(self):
        self.timer = 250
        self.state = "Delay"
        self.next_state = "Exit"


class Dungeon(object):
    def __init__(self):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def handle_action(self, action):
        pass


class Empty(object):
    def __init__(self):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def handle_action(self, action):
        pass


def event_caller(parent, node):
    region_index = parent.persist['region_index']
    region_type = parent.persist['region_type']
    if node.type == "Encounter":
        parameter_dictionary = choose_random_weighted(encounter_dictionary["All"] + encounter_dictionary[region_type],
                                                      encounter_dictionary["All_Weights"] + encounter_dictionary[
                                                          region_type + "_Weights"])
        return Event(node, parameter_dictionary)
    elif node.type == "Event":
        return EmptyNode(node)
    elif node.type == "Dungeon":
        return EmptyNode(node)
    elif node.type == "Shop":
        return EmptyNode(node)
    elif node.type == "Empty":
        return EmptyNode(node)
    else:
        return EmptyNode(node)
    # prompt, option_1, option_2 = None, option_3 = None, option_4 = None, enemies = None,
    # supply_reward = None, gold_reward = None, elixir_reward = None, charger_reward = None, item_reward = None


encounter_dictionary = {
    "All": [
        {"prompt": "A pair of aggressive slime monsters try to block your path.",
         "options": [["Prepare to fight.", [{"state": "Battle"}], [1]],
                     ["Try to run around them.", [{"prompt": "The slimes cut you off and block your escape.",
                                                   "options": [["Prepare to fight.", [{"state": "Battle"}], [1]]]},
                                                  {"prompt": "You manage to run by and escape.",
                                                   "options": [["Continue on.", [{"state": "Exit"}], [1]]]}], [1, 1]]],
         "enemies": ["Slime", "Slime"]}],
    "All_Weights": [1],
    "Desert": [],
    "Desert_Weights": [], }

NODE_EVENT_TYPES = {"Empty": [["Nothing", "Investigate", "Region Entry"], [60, 40, 0]],
                    "Town": [["Shop", "Tavern", "Academy"], [45, 45, 10]],
                    "Dungeon": [["Cave", "Fortress"], [50, 50]],
                    "Lone Building": [["Witch's Hut", "Shop"], [10, 90]],
                    "Encounter": [["Regular", "Inescapable", "Thieves", "Boss"], [80, 10, 10, 0]]}

P_NODE_TYPES = [10, 15, 20, 60]

REGION_PARAMETERS_MAX_SHOP = [4, 4, 4, 3, 3, 3, 2, 2]

REGION_STATIC_SPRITES = {
    'coin icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Coin Icon.png"),
    'supplies icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Supplies Icon.png"),
    'elixir icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Elixir Icon.png"),
    'heart icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Heart Icon.png"),
    'charge icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Charge Icon.png"),
    "FighterIcon": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'AdeptIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'ArtificerIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'RogueIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png")
}

REGION_MENUS = {
    'browser': {
        'shop_toggle_rect': [X * 84 / 100, Y * 2 / 100, X * 14 / 100, Y * 9 / 100],
        'shop_toggle_text': [X * 88 / 100, Y * 5 / 100, X * 14 / 100, Y * 1 / 16],
        'travel_rect': [X * 14 / 100, Y * 2 / 100, X * 14 / 100, Y * 9 / 100],
        'travel_text': [X * 17 / 100, Y * 5 / 100, X * 14 / 100, Y * 1 / 16],
        'portal_rect': [X * 1 / 100, Y * 2 / 100, X * 14 / 100, Y * 9 / 100],
        'portal_text': [X * 4 / 100, Y * 5 / 100, X * 8 / 100, Y * 1 / 16],
        'portal_prompt_rect': [X * 83 / 100, Y * 70 / 100, X * 17 / 100, Y * 30 / 100],
        'portal_prompt': 'Select a destination point and click "CONSTRUCT PORTAL to confirm. Cost: 2 Elixirs, '
                         '2 Chargers',
        'resources': {
            'background 1 rect': [X * 30 / 100, Y * 1 / 100, X * 52 / 100, Y * 11 / 100],
            'background 2 rect': [X * 31 / 100, Y * 2 / 100, X * 50 / 100, Y * 9 / 100],
            'supplies icon pos': (X * 31 / 100, Y * 2 / 100),
            'supplies data rect': [X * 36 / 100, Y * 5 / 100, X * 10 / 100, Y * 10 / 100],
            'elixir icon pos': (X * 43 / 100, Y * 2 / 100),
            'elixir data rect': [X * 47 / 100, Y * 5 / 100, X * 10 / 100, Y * 10 / 100],
            'charge icon pos': (X * 55 / 100, Y * 2 / 100),
            'charge data rect': [X * 60 / 100, Y * 5 / 100, X * 10 / 100, Y * 10 / 100],
            'coin icon pos': (X * 67 / 100, Y * 2 / 100),
            'coin data rect': [X * 72 / 100, Y * 5 / 100, X * 10 / 100, Y * 10 / 100],
            'player_a icon pos': (X * 83 / 100, Y * 13 / 100),
            'player_a icon bg rect': [X * 82.5 / 100, Y * 12.5 / 100, X * 6 / 100, Y * 10 / 100],
            'player_a status bg rect': [X * 89 / 100, Y * 12.5 / 100, X * 10 / 100, Y * 10 / 100],
            'player_a hp rect': [X * 91.75 / 100, Y * 13 / 100, X * 7 / 100, Y * 4 / 100],
            'player_a hp data rect': [X * 89 / 100, Y * 13 / 100, X * 8 / 100, Y * 4 / 100],
            'player_a mp rect': [X * 91.75 / 100, Y * 18 / 100, X * 7 / 100, Y * 4 / 100],
            'player_a mp data rect': [X * 89 / 100, Y * 18 / 100, X * 8 / 100, Y * 4 / 100],
            'player_a eq menu bg rect': [X * 82.5 / 100, Y * 23.5 / 100, X * 8 / 100, Y * 5 / 100],
            'player_a st menu bg rect': [X * 91 / 100, Y * 23.5 / 100, X * 8 / 100, Y * 5 / 100],
            'player_b icon pos': (X * 83 / 100, Y * 30 / 100),
            'player_b icon bg rect': [X * 82.5 / 100, Y * 30 / 100, X * 6 / 100, Y * 10 / 100],
            'player_b status bg rect': [X * 89 / 100, Y * 30 / 100, X * 10 / 100, Y * 10 / 100],
            'player_b hp rect': [X * 91.75 / 100, Y * 30.5 / 100, X * 7 / 100, Y * 4 / 100],
            'player_b hp data rect': [X * 89 / 100, Y * 30.5 / 100, X * 8 / 100, Y * 4 / 100],
            'player_b mp rect': [X * 91.75 / 100, Y * 35.5 / 100, X * 7 / 100, Y * 4 / 100],
            'player_b mp data rect': [X * 89 / 100, Y * 35.5 / 100, X * 8 / 100, Y * 4 / 100],
            'player_b eq menu bg rect': [X * 82.5 / 100, Y * 41 / 100, X * 8 / 100, Y * 5 / 100],
            'player_b st menu bg rect': [X * 91 / 100, Y * 41 / 100, X * 8 / 100, Y * 5 / 100],
            'player_c icon pos': (X * 67 / 100, Y * 47.5 / 100),
            'player_c icon bg rect': [X * 82.5 / 100, Y * 47.5 / 100, X * 6 / 100, Y * 10 / 100],
            'player_c status bg rect': [X * 89 / 100, Y * 47.5 / 100, X * 10 / 100, Y * 10 / 100],
            'player_c hp rect': [X * 91.75 / 100, Y * 48 / 100, X * 7 / 100, Y * 4 / 100],
            'player_c hp data rect': [X * 89 / 100, Y * 48 / 100, X * 8 / 100, Y * 4 / 100],
            'player_c mp rect': [X * 91.75 / 100, Y * 53 / 100, X * 7 / 100, Y * 4 / 100],
            'player_c mp data rect': [X * 89 / 100, Y * 53 / 100, X * 8 / 100, Y * 4 / 100],
            'player_c eq menu bg rect': [X * 82.5 / 100, Y * 58.5 / 100, X * 8 / 100, Y * 5 / 100],
            'player_c st menu bg rect': [X * 91 / 100, Y * 58.5 / 100, X * 8 / 100, Y * 5 / 100],
        }
    },
    'event': {
        'background 1 rect': [X * 17 / 100, Y * 7 / 100, X * 60 / 100, Y * 88 / 100],
        'background 2 rect': [X * 17 / 100, Y * 8 / 100, X * 59 / 100, Y * 86 / 100],
        'prompt rect': [X * 18 / 100, Y * 9 / 100, X * 57 / 100, Y * 84 / 100],
        'option rects': [[X * 18 / 100, Y * 75 / 100, X * 57 / 100, Y * 5 / 100],
                         [X * 18 / 100, Y * 70 / 100, X * 57 / 100, Y * 5 / 100],
                         [X * 18 / 100, Y * 65 / 100, X * 57 / 100, Y * 5 / 100],
                         [X * 18 / 100, Y * 60 / 100, X * 57 / 100, Y * 5 / 100],
                         [X * 18 / 100, Y * 55 / 100, X * 57 / 100, Y * 5 / 100]]
    },
    'equip menu': {
        'background 1 rect': [X * 5 / 100, Y * 5 / 100, X * 90 / 100, Y * 90 / 100],
        'background 2 rect': [X * 6 / 100, Y * 7 / 100, X * 88 / 100, Y * 86 / 100],
        'title rect': [X * 40 / 100, Y * 10 / 100, X * 20 / 100, Y * 10 / 100],
        'equip menu indices': {
            'character index': 'player_a',
            'equip selection index': 0,
            'inventory selection index': 0,
            'relative selection index': 0,
            'inventory display index': 0,
            'inventory display max': 14,
            'item group index': 0},
        'player name rect': [X * 10 / 100, Y * 11 / 100, X * 40 / 100, Y * 10 / 100],
        'Top_Slot_Rect': {
            0: [X * 10 / 100, Y * 20 / 100, X * 10 / 100, Y * 5 / 100],
            1: [X * 10 / 100, Y * 25 / 100, X * 10 / 100, Y * 5 / 100],
            2: [X * 10 / 100, Y * 30 / 100, X * 10 / 100, Y * 5 / 100],
            3: [X * 10 / 100, Y * 35 / 100, X * 10 / 100, Y * 5 / 100],
            4: [X * 10 / 100, Y * 40 / 100, X * 10 / 100, Y * 5 / 100],
            5: [X * 10 / 100, Y * 45 / 100, X * 10 / 100, Y * 5 / 100],
            6: [X * 10 / 100, Y * 50 / 100, X * 10 / 100, Y * 5 / 100],
            7: [X * 10 / 100, Y * 55 / 100, X * 10 / 100, Y * 5 / 100],
            8: [X * 10 / 100, Y * 60 / 100, X * 10 / 100, Y * 5 / 100], },
        'Top_Equip_Rect': {
            0: [X * 30 / 100, Y * 20 / 100, X * 20 / 100, Y * 5 / 100],
            1: [X * 30 / 100, Y * 25 / 100, X * 20 / 100, Y * 5 / 100],
            2: [X * 30 / 100, Y * 30 / 100, X * 20 / 100, Y * 5 / 100],
            3: [X * 30 / 100, Y * 35 / 100, X * 20 / 100, Y * 5 / 100],
            4: [X * 30 / 100, Y * 40 / 100, X * 20 / 100, Y * 5 / 100],
            5: [X * 30 / 100, Y * 45 / 100, X * 20 / 100, Y * 5 / 100],
            6: [X * 30 / 100, Y * 50 / 100, X * 20 / 100, Y * 5 / 100],
            7: [X * 30 / 100, Y * 55 / 100, X * 20 / 100, Y * 5 / 100],
            8: [X * 30 / 100, Y * 60 / 100, X * 20 / 100, Y * 5 / 100], },
        'Stat_Rects': {
            'hp': [X * 10 / 100, Y * 60 / 100, X * 35 / 100, Y * 5 / 100],
            'mp': [X * 10 / 100, Y * 65 / 100, X * 35 / 100, Y * 5 / 100],
            'strength': [X * 10 / 100, Y * 70 / 100, X * 50 / 100, Y * 5 / 100],
            'magic': [X * 10 / 100, Y * 75 / 100, X * 35 / 100, Y * 5 / 100],
            'defense': [X * 34 / 100, Y * 70 / 100, X * 35 / 100, Y * 5 / 100],
            'spirit': [X * 34 / 100, Y * 75 / 100, X * 35 / 100, Y * 5 / 100],
            'speed': [X * 10 / 100, Y * 80 / 100, X * 35 / 100, Y * 5 / 100],
            'luck': [X * 34 / 100, Y * 80 / 100, X * 35 / 100, Y * 5 / 100],
        },
        'inventory rects': {0: [X * 60 / 100, Y * 20 / 100, X * 20 / 100, Y * 5 / 100],
                            1: [X * 60 / 100, Y * 25 / 100, X * 20 / 100, Y * 5 / 100],
                            2: [X * 60 / 100, Y * 30 / 100, X * 20 / 100, Y * 5 / 100],
                            3: [X * 60 / 100, Y * 35 / 100, X * 20 / 100, Y * 5 / 100],
                            4: [X * 60 / 100, Y * 40 / 100, X * 20 / 100, Y * 5 / 100],
                            5: [X * 60 / 100, Y * 45 / 100, X * 20 / 100, Y * 5 / 100],
                            6: [X * 60 / 100, Y * 50 / 100, X * 20 / 100, Y * 5 / 100],
                            7: [X * 60 / 100, Y * 55 / 100, X * 20 / 100, Y * 5 / 100],
                            8: [X * 60 / 100, Y * 60 / 100, X * 20 / 100, Y * 5 / 100],
                            9: [X * 60 / 100, Y * 65 / 100, X * 20 / 100, Y * 5 / 100],
                            10: [X * 60 / 100, Y * 70 / 100, X * 20 / 100, Y * 5 / 100],
                            11: [X * 60 / 100, Y * 75 / 100, X * 20 / 100, Y * 5 / 100],
                            12: [X * 60 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
                            13: [X * 60 / 100, Y * 85 / 100, X * 20 / 100, Y * 5 / 100]
                            }
    },
    'skill tree': {
        'background 1 rect': [X * 5 / 100, Y * 5 / 100, X * 90 / 100, Y * 90 / 100],
        'background 2 rect': [X * 6 / 100, Y * 7 / 100, X * 88 / 100, Y * 86 / 100],
        'skill_rect_proto': [X * 8.25 / 100, Y * 29 / 100, X * 12 / 100, Y * 7 / 100],
        'text_offset': [X * 1 / 100, Y * 2 / 100],
        'skill_offset': [14.25 * X / 100, 9 * Y / 100],
    },
    'shop': {
        'button_radius': int(X / 320),
        'background 1 rect': [X / 16 - 10, Y / 8 - 10, X * 7 / 8 + 20, Y * 3 / 4 + 20],
        'background 2 rect': [X / 16, Y / 8, X * 7 / 8, Y * 3 / 4],
        'supplies_label': [X * 10 / 100, Y * 40 / 100, X * 15 / 100, Y * 5 / 100],
        'chargers_label': [X * 10 / 100, Y * 45 / 100, X * 15 / 100, Y * 5 / 100],
        'elixirs_label': [X * 10 / 100, Y * 50 / 100, X * 15 / 100, Y * 5 / 100],
        'buy_button_top': [X * 37 / 100, Y * 13 / 100, X * 10 / 100, Y * 5.5 / 100],
        'buy_button_pressed': [X * 37 / 100, Y * 14 / 100, X * 10 / 100, Y * 5.5 / 100],
        'buy_button_bottom': [X * 37 / 100, Y * 15 / 100, X * 10 / 100, Y * 5 / 100],
        'buy_text_top': [X * 39.5 / 100, Y * 13.5 / 100, X * 10 / 100, Y * 5 / 100],
        'buy_text_bottom': [X * 39.5 / 100, Y * 14.5 / 100, X * 10 / 100, Y * 5 / 100],
        'sell_button_top': [X * 53 / 100, Y * 13 / 100, X * 10 / 100, Y * 5.5 / 100],
        'sell_button_pressed': [X * 53 / 100, Y * 14 / 100, X * 10 / 100, Y * 5.5 / 100],
        'sell_button_bottom': [X * 53 / 100, Y * 15 / 100, X * 10 / 100, Y * 5 / 100],
        'sell_text_top': [X * 55.5 / 100, Y * 13.5 / 100, X * 10 / 100, Y * 5 / 100],
        'sell_text_bottom': [X * 55.5 / 100, Y * 14.5 / 100, X * 10 / 100, Y * 5 / 100],
        'button_color_top': (120, 120, 150),
        'button_color_bottom': (10, 0, 40),

    },
    'Alt_Travel_Confirm': {
        'BG_Rect': [X * 30 / 100, Y * 30 / 100, X * 40 / 100, Y * 40 / 100],
        'FT_Rect': [X * 31 / 100, Y * 50 / 100, X * 12 / 100, Y * 19 / 100],
        'Fly_Rect': [X * 44 / 100, Y * 50 / 100, X * 12 / 100, Y * 19 / 100],
        'Teleport_Rect': [X * 57 / 100, Y * 50 / 100, X * 12 / 100, Y * 19 / 100],
        'FT_Text': [X * 32 / 100, Y * 51 / 100, X * 10 / 100, Y * 17 / 100],
        'Fly_Text': [X * 45 / 100, Y * 51 / 100, X * 10 / 100, Y * 17 / 100],
        'Teleport_Text': [X * 58 / 100, Y * 51 / 100, X * 10 / 100, Y * 17 / 100],
    },
}
# self.persist['region menus']['event'] = {}
# self.persist['region menus']['equip menu'] = {}
# self.persist['region menus']['skill tree menu'] = {}
BATTLE_MENUS = {
    'enemy positions': {
        1: {'enemy_a': (600, 300)},
        2: {'enemy_a': (600, 100),
            'enemy_b': (600, 300)},
        3: {'enemy_a': (500, 100),
            'enemy_b': (500, 100),
            'enemy_c': (500, 200)},
        4: {'enemy_a': (500, 100),
            'enemy_b': (500, 100),
            'enemy_c': (500, 200),
            'enemy_d': (500, 100)},
        5: {'enemy_a': (500, 100),
            'enemy_b': (500, 100),
            'enemy_c': (500, 200),
            'enemy_d': (500, 100),
            'enemy_e': (500, 200)},
    },
    'hero positions': {
        1: {'player_a': (600, 300)},
        2: {'player_b': (600, 100),
            'player_a': (600, 300)},
        3: {'player_a': (500, 100),
            'player_b': (500, 100),
            'player_c': (500, 200)}
    },
    'slot_positions': {
        0: (X * 80 / 100, Y * 1 / 100),
        1: (X * 80 / 100, Y * 10 / 100),
        2: (X * 80 / 100, Y * 19 / 100),
        3: (X * 80 / 100, Y * 28 / 100),
        4: (X * 80 / 100, Y * 37 / 100),
        5: (X * 80 / 100, Y * 46 / 100),
        6: (X * 80 / 100, Y * 55 / 100),
        7: (X * 80 / 100, Y * 64 / 100),
    },
    'battle_slot_index': {
        "player_a": 0,
        "player_b": 1,
        "player_c": 2,
        "player_summon_a": 3,
        "player_summon_b": 4,
        "enemy_a": 5,
        "enemy_b": 6,
        "enemy_c": 7,
        "enemy_d": 8,
        "enemy_e": 9,
    },
    'player_status_rects': {
        'player_a': {
            'hp': [X * 20 / 100, Y * 76 / 100, X * 20 / 100, Y * 7 / 100],
            'mp': [X * 20 / 100, Y * 80 / 100, X * 20 / 100, Y * 7 / 100],
            'name': [X * 1 / 100, Y * 76 / 100, X * 20 / 100, Y * 7 / 100]
        },
        'player_b': {
            'hp': [X * 20 / 100, Y * 84 / 100, X * 20 / 100, Y * 7 / 100],
            'mp': [X * 20 / 100, Y * 88 / 100, X * 20 / 100, Y * 7 / 100],
            'name': [X * 1 / 100, Y * 84 / 100, X * 20 / 100, Y * 7 / 100]
        },
        'player_c': {
            'hp': [X * 20 / 100, Y * 92 / 100, X * 20 / 100, Y * 7 / 100],
            'mp': [X * 20 / 100, Y * 96 / 100, X * 20 / 100, Y * 7 / 100],
            'name': [X * 1 / 100, Y * 92 / 100, X * 20 / 100, Y * 7 / 100]
        }
    },
    'move_top_menu_rects': {
        'border': [X * 30 / 100, Y * 75.5 / 100, X * 13 / 100, Y * 24 / 100],
        "Attack": [X * 31 / 100, Y * 77 / 100, X * 12 / 100, Y * 4 / 100],
        "Defend": [X * 31 / 100, Y * 81 / 100, X * 12 / 100, Y * 4 / 100],
        "Skill": [X * 31 / 100, Y * 85 / 100, X * 12 / 100, Y * 4 / 100],
        "Item": [X * 31 / 100, Y * 89 / 100, X * 12 / 100, Y * 4 / 100],
        "Run": [X * 31 / 100, Y * 93 / 100, X * 12 / 100, Y * 4 / 100],
    },
    'skill_menu_rects': {
        'border': [X * 44 / 100, Y * 75.5 / 100, X * 13 / 100, Y * 24 / 100],
        0: [X * 45 / 100, Y * 77 / 100, X * 12 / 100, Y * 4 / 100],
        1: [X * 45 / 100, Y * 81 / 100, X * 12 / 100, Y * 4 / 100],
        2: [X * 45 / 100, Y * 85 / 100, X * 12 / 100, Y * 4 / 100],
        3: [X * 45 / 100, Y * 89 / 100, X * 12 / 100, Y * 4 / 100],
        4: [X * 45 / 100, Y * 93 / 100, X * 12 / 100, Y * 4 / 100],
    },
    'item_menu_rects': {
        'border': [X * 44 / 100, Y * 75.5 / 100, X * 13 / 100, Y * 24 / 100],
        0: [X * 45 / 100, Y * 77 / 100, X * 12 / 100, Y * 4 / 100],
        1: [X * 45 / 100, Y * 81 / 100, X * 12 / 100, Y * 4 / 100],
        2: [X * 45 / 100, Y * 85 / 100, X * 12 / 100, Y * 4 / 100],
        3: [X * 45 / 100, Y * 89 / 100, X * 12 / 100, Y * 4 / 100],
        4: [X * 45 / 100, Y * 93 / 100, X * 12 / 100, Y * 4 / 100],
    },
    'turn_end_rect': [X * 1 / 100, Y * 60 / 100, X * 10 / 100, Y * 10 / 100],
    'confirm_rect': [X * 35 / 100, Y * 30 / 100, X * 20 / 100, Y * 20 / 100],
    'confirm_prompt_rect': [X * 36 / 100, Y * 31 / 100, X * 20 / 100, Y * 20 / 100],
    'confirm_yes_rect': [X * 36 / 100, Y * 45 / 100, X * 20 / 100, Y * 20 / 100],
    'confirm_no_rect': [X * 45 / 100, Y * 45 / 100, X * 20 / 100, Y * 20 / 100]
}

BATTLE_MENU_SPRITES = {
    'action_slot_sprites': [image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p1.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p2.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p3.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p4.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p5.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p6.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p7.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p8.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p9.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p10.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p11.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p12.png")
    ],
    'attack_action': [0],
    'attack_action_weights': [1],
    'ability_action': [1],
    'ability_action_weights': [1],
    'item_action': [2],
    'item_action_weights': [1],
    'defend_action': [3],
    'defend_action_weights': [1],
    'no_action': [4, 5, 6, 7, 8, 9, 10, 11],
    'no_action_weights': [8, 1, 1, 1, 16, 1, 1, 1],
    'animation_speed': 2000,
    'target_reticules': {
        'target': image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Target Rets128p2.png"),
        'source': image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Target Rets128p1.png"),
    }

}

SOUND_EFFECTS = {
    'Menu': {
        'Toggle_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\397604__nightflame__menu-fx-01.wav"),
        'Toggle_2': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\503340__tahutoa__clicky-accept-menu-sound.wav"),
        'Confirm_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\403019__inspectorj__ui-confirmation-alert-c4.wav"),
    },
}


def draw_line_dashed(surface, color, start_pos, end_pos, width=1, dash_length=10, exclude_corners=True):
    # convert tuples to numpy arrays
    start_pos = np.array(start_pos)
    end_pos = np.array(end_pos)

    # get euclidian distance between start_pos and end_pos
    length = np.linalg.norm(end_pos - start_pos)

    # get amount of pieces that line will be split up in (half of it are amount of dashes)
    dash_amount = int(length / dash_length)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

    return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n + 1]), width)
            for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]


def item_generate(item):
    return 'none'


def random_int(a, b):
    return random.randint(a, b)


def click_check(rect):
    pos = pygame.mouse.get_pos()
    if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
        return True
    else:
        return False


def tw(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


def node_assign(persist):
    node_type = random.choices(NODE_TYPES[0], weights=NODE_TYPES[1])
    event_type = random.choices(NODE_EVENT_TYPES[node_type[0]][0],
                                weights=NODE_EVENT_TYPES[node_type[0]][1])
    event_id = event_assign(node_type, event_type, persist)
    return node_type[0], event_type[0], event_id[0]


def node_assign_2(parent):
    shops = 0
    n = 0
    n_max = len(parent.nodes.sprites())
    for node in parent.nodes.sprites():
        n += 1
        if node.type == "Shop":
            shops += 1
    if shops < 3 and random_int(0, 100) > (100 - (1.5 * n)):
        node_type = "Shop"
    else:
        node_type = random.choices(NODE_TYPES_2[0], weights=NODE_TYPES_2[1])
    return node_type[0]


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def choose_random_weighted(options, weights):
    return random.choices(options, weights)[0]


def choose_random(options):
    return random.choice(options)


def event_assign(node_type, event_type, persist):
    event_id = "NULL"
    return event_id


def event_parse(node_event, region):
    pass


NODE_EVENT_IDS = {"Empty": {"Nothing": "Null"}}


class ScreenTransition(object):
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.color = (0, 0, 0)
        self.alpha = 0


class NodeEvent(object):
    def __init__(self, event_type, node_type, persist):
        #        region = persist['region_index']
        self.event_done = True
        self.option_index = 0
        # Less Empty Nodes *****************************************************
        if node_type == "Empty":
            if persist['party_abilities'].no_empty_nodes:
                node_type = persist['nodes'][persist['current_position']].type = choose_random_weighted(
                    NODE_TYPES[0][1:], NODE_TYPES[1][1:])
                if node_type == "Encounter":
                    event_type = persist['nodes'][persist['current_position']].event = choose_random_weighted(
                        NODE_EVENT_TYPES[node_type][0][:-1], NODE_EVENT_TYPES[node_type][1][:-1])
                else:
                    event_type = persist['nodes'][persist['current_position']].event = choose_random_weighted(
                        NODE_EVENT_TYPES[node_type][0], NODE_EVENT_TYPES[node_type][1])
            elif persist['party_abilities'].less_empty_nodes and random_int(0, 100) > 50:
                node_type = persist['nodes'][persist['current_position']].type = choose_random_weighted(
                    NODE_TYPES[0][1:], NODE_TYPES[1][1:])
                if node_type == "Encounter":
                    event_type = persist['nodes'][persist['current_position']].event = choose_random_weighted(
                        NODE_EVENT_TYPES[node_type][0][:-1], NODE_EVENT_TYPES[node_type][1][:-1])
                else:
                    event_type = persist['nodes'][persist['current_position']].event = choose_random_weighted(
                        NODE_EVENT_TYPES[node_type][0], NODE_EVENT_TYPES[node_type][1])
        if node_type in Event_Dictionary:
            if event_type in Event_Dictionary[node_type]:
                event_list = []
                self.event_done = False
                for event in Event_Dictionary[node_type][event_type]:
                    if str(persist['region_index']) in Event_Dictionary[node_type][event_type][event]["Region"] \
                            or "All" in Event_Dictionary[node_type][event_type][event]["Region"]:
                        if persist['region_type'] in Event_Dictionary[node_type][event_type][event]["Region Type"] \
                                or "All" in Event_Dictionary[node_type][event_type][event]["Region Type"]:
                            event_list.append(Event_Dictionary[node_type][event_type][event])
                event = choose_random(event_list)
                if "Prompt" in event:
                    self.prompt = event["Prompt"]
                if "Options" in event:
                    self.options = event["Options"]
                if "Battle" in event:
                    self.battle = event["Battle"]
                if "Weights" in event:
                    self.weights = event["Weights"]
                if event_type == "Shop":
                    self.shop = shop_builder(persist['region_index'])


Event_Dictionary = {
    "Encounter": {
        "Regular": {
            "Single Slime": {
                "Prompt": "A lone slime is preventing your continuation. While not very threatening, there is no "
                          "reasoning with this monster.",
                "Options": [["Fight it.", "Try and run around it"]],
                "Weights": [[["Battle"], [100]], [["Battle", "Escape"], [50, 1050]]],
                "Battle": ["Slime", "Slime"],
                "Region": ["All"],
                "Region Type": ["All"],
            },
            "Double Slime": {
                "Prompt": "A couple of slimes are preventing your continuation. While not very threatening, there is "
                          "no reasoning with these monsters.",
                "Options": [["Fight them.", "Try and run around them"]],
                "Weights": [[["Battle"], [100]], [["Battle", "Escape"], [50, 1050]]],
                "Battle": ["Slime", "Slime"],
                "Region": ["All"],
                "Region Type": ["All"],
            },

        },
    },

    "Town": {
        "Shop": {
            "Desolate Town Shop": {
                "Prompt": "You come across a desolate town. There's not much here but you see a shop that may have "
                          "some useful items.",
                "Options": [["Check out the shop.", "Leave."]],
                "Weights": [[["Shop"], [100]], [["Escape"], [100]]],
                "Region": ["All"],
                "Region Type": ["All"],
            },
        },
    },
}


def random_name():
    return names.get_last_name()


def character_stat_update(persist):
    stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
             'crit_damage']
    for player in persist['characters']:
        for value in stats:
            if value == 'max_hp':
                setattr(player, value, player.base_hp)
            elif value == 'max_mp':
                setattr(player, value, player.base_mp)
            else:
                setattr(player, value, getattr(player, 'base_' + value))
        for slot in player.equipment.keys():
            for value in stats:
                if hasattr(player.equipment[slot], value):
                    new_value = getattr(player.equipment[slot], value) + getattr(player, value)
                    setattr(player, value, new_value)
                if value == 'strength':
                    if hasattr(player.equipment[slot], 'attack'):
                        player.strength += player.equipment[slot].attack


def character_ability_update(persist):
    for player in persist['characters']:
        setattr(player, 'techniques',
                getattr(player, 'base_' + 'techniques'))
        for slot in player.equipment.keys():
            if hasattr(player.equipment[slot], 'techniques'):
                for value in player.equipment[slot].techniques:
                    if value not in player.techniques:
                        player.techniques.append(value)
    for player in persist['characters']:
        setattr(player, 'attack_type',
                getattr(player, 'base_' + 'attack_type'))
        for slot in player.equipment.keys():
            if hasattr(player.equipment[slot], 'attack_type'):
                setattr(player, 'attack_type',
                        getattr(player.equipment[slot], 'attack_type'))


class EquipMenu(object):
    def __init__(self, parent):
        self.scroll_index = 0
        self.inventory_selection_index = -1
        self.equip_selection_index = -1
        self.menu_horizontal_index = "None"
        self.parent = parent
        self.player_index = 0
        self.bg_1_rect = [X * 8 / 100, Y * 11 / 100, X * 76 / 100, Y * 85 / 100]
        self.bg_2_rect = [X * 8.5 / 100, Y * 12 / 100, X * 75 / 100, Y * 83 / 100]
        self.slot_rects = REGION_MENUS['equip menu']['Top_Slot_Rect']
        self.equip_rects = REGION_MENUS['equip menu']['Top_Equip_Rect']
        self.inventory_rects = REGION_MENUS['equip menu']['inventory rects']

    def update(self, dt):
        pass

    def handle_action(self, action):
        if action == "mouse_move":
            for n, equip_slot in enumerate(self.parent.persist['characters'][self.player_index].equipment_options):
                if click_check(self.equip_rects[n]):
                    self.equip_selection_index = n
                    self.menu_horizontal_index = "Equip"
                    break
            else:
                self.equip_selection_index = -1
        elif action == "click":
            if not click_check(self.bg_1_rect):
                self.parent.state = "Browse"

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.bg_1_rect, border_radius=int(X / 128))
        pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=int(X / 128))
        for n, equip_slot in enumerate(self.parent.persist['characters'][self.player_index].equipment_options):
            tw(surface, equip_slot, TEXT_COLOR, self.slot_rects[n], TEXT_FONT)
            if equip_slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                text = self.parent.persist['characters'][self.player_index].equipment[
                    equip_slot].name
            else:
                text = '-'
            if self.equip_selection_index == n and self.menu_horizontal_index == "Equip":
                color = SELECTED_COLOR
            else:
                color = TEXT_COLOR
            tw(surface, text, color, self.equip_rects[n], TEXT_FONT)
        for i, item in enumerate(self.parent.persist['inventory']):
            color = TEXT_COLOR
            if not item.equipment:
                color = (50, 50, 50)
                if self.inventory_selection_index == i and self.menu_horizontal_index == "Inventory":
                    color = (100, 100, 100)
            elif self.inventory_selection_index == i and self.menu_horizontal_index == "Inventory":
                color = SELECTED_COLOR
            if 7 >= i - self.scroll_index >= 0:
                tw(surface, item.name, color, self.inventory_rects[i - self.scroll_index], TEXT_FONT)
        if len(self.parent.persist['inventory']) < 8:
            for j in range(len(self.parent.persist['inventory']), 8):
                color = (50, 50, 50)
                if self.inventory_selection_index == j and self.menu_horizontal_index == "Inventory":
                    color = (100, 100, 100)
                tw(surface, '-'.center(12), color, self.inventory_rects[j], TEXT_FONT)
        potential = self.potential_stat()
        for key, value in enumerate(settings.REGION_MENUS['equip menu']['Stat_Rects']):
            stat = getattr(self.parent.persist['characters'][self.inventory_selection_index], value)
            if value == 'hp':
                stat2 = getattr(self.parent.persist['characters'][self.inventory_selection_index], 'max_hp')
                settings.tw(surface, value + ':' + str(stat).rjust(10 - len(value)) + '/' + str(stat2),
                            settings.TEXT_COLOR,
                            settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
            elif value == 'mp':
                stat2 = getattr(self.parent.persist['characters'][self.inventory_selection_index], 'max_mp')
                settings.tw(surface, value + ':' + str(stat).rjust(11 - len(value)) + '/' + str(stat2),
                            settings.TEXT_COLOR,
                            settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
            else:
                settings.tw(surface, value + ':' + str(stat).rjust(14 - len(value)), settings.TEXT_COLOR,
                            settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
                if value in potential.keys():
                    if value == 'defense' or value == 'spirit' or value == 'luck':
                        if potential[value] < 0:
                            settings.tw(surface, str(potential[value]).rjust(24 - len(value)), (150, 0, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
                        else:
                            settings.tw(surface, ('+' + str(potential[value])).rjust(24
                                                                                     - len(value)), (0, 150, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
                    elif value == 'magic' or value == 'speed':
                        if potential[value] < 0:
                            settings.tw(surface, str(potential[value]).rjust(22 - len(value)), (150, 0, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value],
                                        settings.TEXT_FONT)
                        else:
                            settings.tw(surface, ('+' + str(potential[value])).rjust(22
                                                                                     - len(value)), (0, 150, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value],
                                        settings.TEXT_FONT)
                    elif value == 'strength':
                        if potential[value] < 0:
                            settings.tw(surface, str(potential[value]).rjust(25 - len(value)), (150, 0, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value],
                                        settings.TEXT_FONT)
                        else:
                            settings.tw(surface, ('+' + str(potential[value])).rjust(25
                                                                                     - len(value)), (0, 150, 0),
                                        settings.REGION_MENUS['equip menu']['Stat_Rects'][value],
                                        settings.TEXT_FONT)

    def potential_stat(self):
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        potential = {}
        if self.menu_horizontal_index == "Inventory" and self.parent.persist['inventory'] and len(
                self.parent.persist['inventory']) > self.inventory_selection_index >= 0:
            slot = self.parent.persist['inventory'][self.inventory_selection_index].slot
            for value in stats:
                if value != 'strength':
                    if hasattr(self.parent.persist['inventory'][self.inventory_selection_index], value):
                        potential_value = getattr(self.parent.persist['inventory'][self.inventory_selection_index],
                                                  value)
                    else:
                        potential_value = 0
                    if slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                        if hasattr(self.parent.persist['characters'][self.player_index].equipment[slot], value):
                            current_value = getattr(
                                self.parent.persist['characters'][self.player_index].equipment[slot], value)
                        else:
                            current_value = 0
                    else:
                        current_value = 0
                    if potential_value - current_value != 0:
                        potential[value] = potential_value - current_value
                else:
                    if hasattr(self.parent.persist['inventory'][self.inventory_selection_index], 'attack'):
                        potential_value = getattr(self.parent.persist['inventory'][self.inventory_selection_index],
                                                  'attack')
                    else:
                        potential_value = 0
                    if slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                        if hasattr(self.parent.persist['characters'][self.player_index].equipment[slot], value):
                            current_value = getattr(
                                self.parent.persist['characters'][self.player_index].equipment[slot], value)
                        else:
                            current_value = 0
                    else:
                        current_value = 0
                    if potential_value - current_value != 0:
                        potential[value] = potential_value - current_value
        elif self.menu_horizontal_index == "Equip":
            if len(self.parent.persist['characters'][self.player_index].equipment_options) - 1 >= \
                    self.equip_selection_index >= 0:
                slot = self.parent.persist['characters'][self.player_index].equipment_options[
                    self.equip_selection_index]
                for value in stats:
                    if value != 'strength':
                        potential_value = 0
                        if slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                            if hasattr(self.parent.persist['characters'][self.player_index].equipment[slot], value):
                                current_value = getattr(
                                    self.parent.persist['characters'][self.player_index].equipment[slot], value)
                            else:
                                current_value = 0
                        else:
                            current_value = 0
                        if potential_value - current_value != 0:
                            potential[value] = potential_value - current_value
                    else:
                        potential_value = 0
                        if slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                            if hasattr(self.parent.persist['characters'][self.player_index].equipment[slot],
                                       'attack'):
                                current_value = getattr(
                                    self.parent.persist['characters'][self.player_index].equipment[slot], 'attack')
                            else:
                                current_value = 0
                        else:
                            current_value = 0
                        if potential_value - current_value != 0:
                            potential[value] = potential_value - current_value
        return potential

    def equip_unequip(self):
        if self.menu_horizontal_index == "Equip":
            slot = self.parent.persist['characters'][self.player_index].equipment_options[self.equip_selection_index]
            if slot in self.parent.persist['characters'][self.player_index].equipment.keys():
                self.parent.persist['inventory'].append(
                    copy.deepcopy(self.parent.persist['characters'][self.player_index].equipment[slot]))
                del (self.parent.persist['characters'][self.player_index].equipment[slot])

        elif self.menu_horizontal_index == "Inventory" and 0 <= self.inventory_selection_index <= len(
                self.parent.persist['inventory']) - 1:
            if hasattr(self.parent.persist['inventory'][self.inventory_selection_index], 'slot'):
                slot = self.parent.persist['inventory'][self.inventory_selection_index].slot
                if slot in self.parent.persist['characters'][self.player_index].equipment_options:
                    if slot in self.parent.persist['characters'][self.player_index].equipment:
                        self.parent.persist['inventory'].append(
                            copy.deepcopy(self.parent.persist['characters'][self.player_index].equipment[slot]))
                        del (self.parent.persist['characters'][self.player_index].equipment[slot])
                    self.parent.persist['characters'][self.player_index].equipment[slot] = copy.deepcopy(
                        self.parent.persist['inventory'][self.inventory_selection_index])
                    del self.parent.persist['inventory'][self.inventory_selection_index]
        settings.character_stat_update(self.parent.persist)
        settings.character_ability_update(self.parent.persist)


class PartyAbilityManager(object):
    def __init__(self):
        self.charger_travel = True  # can use charges instead of supplies **** NOT WORKING ****
        self.success_boost = True  # boost success rate for any choice **** NOT WORKING ****
        self.always_avoid_option = True  # always have an option to avoid event **** NOT WORKING ****
        self.create_portal = True  # create an edge using many resources
        self.less_empty_nodes = True  # less empty nodes spawn
        self.no_empty_nodes = True  # no empty nodes spawn
        self.path_vision = False  # see all paths in region
        self.static_path = False  # false = paths only visible when hovering over node
        self.region_revealed = True  # all region info revealed
        self.locate_shops = True  # see all shops in region
        self.locate_encounter = True  # see all encounters in region
        self.locate_inn = True  # see all inns in region
        self.locate_tavern = True  # see all taverns in region
        self.locate_dungeon = True  # see all dungeons in region
        self.mp_regen_travel = True  # regen some mp when traveling
        self.boosted_regen_travel = True  # regen more when traveling
        self.conserve_supplies = True  # chance to not use supplies when traveling
        self.fast_travel = True  # can travel to any previously visited node using elixir
        self.fly = True  # can travel to any node, usually just once
        self.fly_charges = 50  # paired to fly
        self.teleport = True  # can travel to any node, using multiple elixirs
        self.scout_vision = True  # can see details of neighboring nodes


def shop_builder(region):
    shop_inventory = {
        "Supplies": {},
        "Elixir": {},
        "Charger": {},
        "Items": {},
        "Equipment": {}, }
    supplies_price = [3, 3, 3, 4, 4, 4, 5, 5]
    supplies_quantity = random_int(3, 12)
    shop_inventory["Supplies"]["Price"] = supplies_price[region]
    shop_inventory["Supplies"]["Stock"] = supplies_quantity
    elixir_price = [3, 3, 3, 4, 4, 4, 5, 5]
    elixir_quantity = random_int(3, 12)
    shop_inventory["Elixir"]["Price"] = elixir_price[region]
    shop_inventory["Elixir"]["Stock"] = elixir_quantity
    charger_price = [3, 3, 3, 4, 4, 4, 5, 5]
    charger_quantity = random_int(3, 12)
    shop_inventory["Charger"]["Price"] = charger_price[region]
    shop_inventory["Charger"]["Stock"] = charger_quantity
    return shop_inventory


class Weapon(object):
    def __init__(self, weapon, level):
        self.name = weapon
        self.level = level
        self.max_level = weapon_dict[self.name]["max_level"]
        self.attack = weapon_dict[self.name]["attack"][self.level - 1]
        self.slot = "Weapon"
        self.equipment = True
        self.attack_type = weapon_dict[self.name]['attack_type']
        self.buy_value = weapon_dict[self.name]['buy_value']
        self.sell_value = weapon_dict[self.name]['sell_value']
        if 'hits' in weapon_dict[self.name].keys():
            self.hits = weapon_dict[self.name]['hits'][self.level - 1]
        else:
            self.hits = 1
        if 'status' in weapon_dict[self.name].keys():
            for effect in weapon_dict[self.name]['status'].keys():
                setattr(self, effect, [weapon_dict[self.name]['status'][effect][0][self.level - 1],
                                       weapon_dict[self.name]['status'][effect][1][self.level - 1]])
        if 'techniques' in weapon_dict[self.name].keys():
            self.techniques = []
            for technique in weapon_dict[self.name]['status'].keys():
                self.techniques.append(weapon_dict[self.name]['techniques'][technique])
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        for stat in stats:
            if stat in weapon_dict[self.name].keys():
                setattr(self, stat, weapon_dict[self.name][stat][self.level - 1])
        if 'charge' in weapon_dict[self.name].keys():
            self.max_charge = self.charge = weapon_dict[self.name]['charge'][0]
            self.charge_cost = weapon_dict[self.name]['charge'][1]

    def recharge(self):
        if hasattr(self, 'charge') and hasattr(self, 'max_charge'):
            self.charge = self.max_charge

    def stat_update(self):
        self.attack = weapon_dict[self.name]["attack"][self.level - 1]
        if 'hits' in weapon_dict[self.name].keys():
            self.hits = weapon_dict[self.name]['hits'][self.level - 1]
        else:
            self.hits = 1
        if 'status' in weapon_dict[self.name].keys():
            for effect in weapon_dict[self.name]['status'].keys():
                setattr(self, effect, [weapon_dict[self.name]['status'][effect][0][self.level - 1],
                                       weapon_dict[self.name]['status'][effect][1][self.level - 1]])
        if 'techniques' in weapon_dict[self.name].keys():
            self.techniques = []
            for technique in weapon_dict[self.name]['status'].keys():
                self.techniques.append(weapon_dict[self.name]['techniques'][technique])
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        for stat in stats:
            if stat in weapon_dict[self.name].keys():
                setattr(self, stat, weapon_dict[self.name][stat][self.level - 1])

    def can_upgrade(self):
        if self.level < self.max_level:
            return True
        return False

    def upgrade(self):
        if self.can_upgrade():
            self.level += 1
        self.stat_update()


class Armor(object):
    def __init__(self, armor, tier, level):
        self.name = armor
        self.tier = tier
        self.level = level
        self.defense = armor_dict[armor]["defense"][int(level) - 1] + armor_dict[armor]["tier mod"][tier]
        self.slot = "Armor"
        self.equipment = True


class Boots(object):
    def __init__(self, boots, tier, level):
        self.name = boots
        self.tier = tier
        self.level = level
        self.defense = boots_dict[boots]["defense"][int(level) - 1] + boots_dict[boots]["tier mod"][tier]
        self.speed = boots_dict[boots]["speed"][int(level)] + boots_dict[boots]["tier mod"][tier]
        self.slot = "Boots"
        self.equipment = True


class InventoryManager(object):
    def __init__(self, persist):
        self.persist = persist
        self.players = ['player_a', 'player_b', 'player_c']
        self.player = {'player_a': {'head': 'none', 'body': 'none', 'right': 'none', 'hip': 'none', 'back': 'none',
                                    'left': 'none', 'neck': 'none', 'feet': 'none'},
                       'player_b': {'head': 'none', 'body': 'none', 'right': 'none', 'hip': 'none', 'back': 'none',
                                    'left': 'none', 'neck': 'none', 'feet': 'none'},
                       'player_c': {'head': 'none', 'body': 'none', 'right': 'none', 'hip': 'none', 'back': 'none',
                                    'left': 'none', 'neck': 'none', 'feet': 'none'},
                       }
        self.does_exist = {'player_a': False,
                           'player_b': False,
                           'player_c': False,
                           }
        self.is_class = {'player_a': 'none',
                         'player_b': 'none',
                         'player_c': 'none',
                         }
        self.allowable = {'player_a': [],
                          'player_b': [],
                          'player_c': [],
                          }
        self.inventory = []


battle_characters = {
    "Fighter": {'sprites': [image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p1.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p2.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p3.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p4.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p5.png")
                            ],
                'idle': [0, 1, 2, 3],  # frames of sprites associated with idle state
                'idle weights': [10, 1, 3, 1],  # time weights for idle frames
                'idle speed': 2000,  # ms to complete idle cycle
                'attack': [4],  # frames of sprites associated with attack state
                'cast': [4],  # frames of sprites associated with cast state
                'hit': [0],  # frames of sprites associated with hit state
                'miss': [2],  # frames of sprites associated with miss state
                },
}

BATTLE_ANIMATIONS = {
    "Slash_1": {
        'sprites': [image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p1.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p2.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p3.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p4.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p5.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p6.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p7.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p8.png"),
                    ],
        'weights': [1, 1, 1, 1, 1, 1, 1, 10],  # time weights for idle frames
        'speed': 500,  # ms to complete idle cycle
        'delay': 100,
        'screen': False,
    },
}

STATUS_LIST = ["dazed",  # can't use abilities *** NOT WORKING
               "disabled",  # can't attack *** NOT WORKING
               "stunned",  # can't act *** NOT WORKING
               "perplexed",  # can't use items *** NOT WORKING
               "vigilant",  # defense up *** NOT WORKING
               "smitten",  # can't defend *** NOT WORKING
               "faith",  # spirit up *** NOT WORKING
               "brave",  # strength up *** NOT WORKING
               "calm",  # magic up *** NOT WORKING
               "haste",  # extra action each turn *** NOT WORKING
               "turns",  # number of extra actions, maybe not needed *** NOT WORKING
               "quick",  # speed up *** NOT WORKING
               "lucky",  # luck up *** NOT WORKING
               "focus",  # crit rate up *** NOT WORKING
               "curse",  # damage multiplied after calulation *** NOT WORKING
               "spite",  # damage added after calculation *** NOT WORKING
               "invincible",  # immune to damage *** NOT WORKING
               "shield",  # half physical/laser damage *** NOT WORKING
               "ward",  # half magical/laser damage *** NOT WORKING
               "frail",  # defense down *** NOT WORKING
               "terrify",  # spirit down *** NOT WORKING
               "weak",  # strength down *** NOT WORKING
               "distract",  # magic down *** NOT WORKING
               "slow",  # speed down *** NOT WORKING
               "hex",  # luck down *** NOT WORKING
               "dull",  # crit rate down *** NOT WORKING
               "savage",  # crit damage up *** NOT WORKING
               "gentle",  # crit damage down *** NOT WORKING
               "bleed",  # hp loss based on remaining hp
               "toxic",  # hp loss based on missing hp
               "burn"]  # flat hp loss

STATUS_LIST_EOT = {
    "bleed": {'effect': 5, 'animation': 'none', },  # hp loss based on remaining hp
    "toxic": {'effect': 5, 'animation': 'none', },  # hp loss based on missing hp
    "burn": {'effect': 5, 'animation': 'none', },  # flat hp loss
}


def weights_convert(idle_speed, idle_weights):
    weight_sum = 0
    for value in idle_weights:
        weight_sum += value
    for i, value in enumerate(idle_weights):
        idle_weights[i] = value * idle_speed / weight_sum
    return idle_weights


def vector_sum(v1=None, v2=None, v3=None, v4=None, v5=None):
    vector = []
    if v1:
        vector = copy.deepcopy(v1)
        print(vector)
    if v2:
        for i in range(len(vector)):
            vector[i] = vector[i] + v2[i]
        print(vector)
    if v3:
        for i in range(len(vector)):
            vector[i] = vector[i] + v3[i]
    if v4:
        for i in range(len(vector)):
            vector[i] = vector[i] + v4[i]
    if v5:
        for i in range(len(vector)):
            vector[i] = vector[i] + v5[i]
    return vector


def flip_sign(vector):
    if not len(vector) == 10:
        return vector
    else:
        vector[5] *= -1
        vector[6] *= -1
        vector[7] *= -1
        vector[8] *= -1
        vector[9] *= -1
        return vector


def normalize_ultity(vector):
    for i in range(len(vector)):
        if vector[i] > 1:
            vector[i] = math.log10(vector[i]) + 1
    return vector


def utility_select(options):
    n = len(options)
    max_utility = 0
    choices = []
    enemy_1_choice = None
    enemy_2_choice = None
    enemy_3_choice = None
    enemy_4_choice = None
    enemy_5_choice = None

    if n > 0:
        for option_enemy_1 in options[0]:
            if n > 1:
                for option_enemy_2 in options[1]:
                    if n > 2:
                        for option_enemy_3 in options[2]:
                            if n > 3:
                                for option_enemy_4 in options[3]:
                                    if n > 4:
                                        for option_enemy_5 in options[3]:
                                            if n == 4:
                                                outcome_total = vector_sum(option_enemy_1[3], option_enemy_2[3],
                                                                           option_enemy_3[3], option_enemy_4[3])
                                                outcome_total = flip_sign(outcome_total)
                                                outcome_total = normalize_ultity(outcome_total)
                                                if sum(outcome_total) > max_utility:
                                                    max_utility = sum(outcome_total)
                                                    enemy_1_choice = option_enemy_1
                                                    enemy_2_choice = option_enemy_2
                                                    enemy_3_choice = option_enemy_3
                                                    enemy_4_choice = option_enemy_4
                                    else:
                                        outcome_total = vector_sum(option_enemy_1[3], option_enemy_2[3],
                                                                   option_enemy_3[3], option_enemy_4[3])
                                        outcome_total = flip_sign(outcome_total)
                                        outcome_total = normalize_ultity(outcome_total)
                                        if sum(outcome_total) > max_utility:
                                            max_utility = sum(outcome_total)
                                            enemy_1_choice = option_enemy_1
                                            enemy_2_choice = option_enemy_2
                                            enemy_3_choice = option_enemy_3
                                            enemy_4_choice = option_enemy_4
                            else:
                                outcome_total = vector_sum(option_enemy_1[3], option_enemy_2[3], option_enemy_3[3])
                                outcome_total = flip_sign(outcome_total)
                                outcome_total = normalize_ultity(outcome_total)
                                if sum(outcome_total) > max_utility:
                                    max_utility = sum(outcome_total)
                                    enemy_1_choice = option_enemy_1
                                    enemy_2_choice = option_enemy_2
                                    enemy_3_choice = option_enemy_3
                    else:
                        outcome_total = vector_sum(option_enemy_1[3], option_enemy_2[3])
                        outcome_total = flip_sign(outcome_total)
                        outcome_total = normalize_ultity(outcome_total)
                        if sum(outcome_total) > max_utility:
                            max_utility = sum(outcome_total)
                            enemy_1_choice = option_enemy_1
                            enemy_2_choice = option_enemy_2
            else:
                outcome_total = option_enemy_1[3]
                outcome_total = flip_sign(outcome_total)
                outcome_total = normalize_ultity(outcome_total)
                if sum(outcome_total) > max_utility:
                    max_utility = sum(outcome_total)
                    enemy_1_choice = option_enemy_1
    if enemy_1_choice:
        choices.append(enemy_1_choice)
    if enemy_2_choice:
        choices.append(enemy_2_choice)
    if enemy_3_choice:
        choices.append(enemy_3_choice)
    if enemy_4_choice:
        choices.append(enemy_4_choice)
    if enemy_5_choice:
        choices.append(enemy_5_choice)

    return choices


class VictoryDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.bg_rect_1 = [X * 2 / 100, Y * 2 / 100, X * 80 / 100, Y * 80 / 100]
        self.bg_rect_2 = [X * 4 / 100, Y * 4 / 100, X * 76 / 100, Y * 76 / 100]
        self.timer = 0
        self.state = "Blank"
        self.exp_animation_time = 4000

    def update(self, dt):
        self.timer += dt
        if self.state == "Blank":
            if self.timer >= 1000:
                self.timer = 0
                self.state = "Gold"
        elif self.state == "Gold":
            if self.timer >= 500:
                self.timer = 0
                self.state = "Supply"
        elif self.state == "Supply":
            if self.timer >= 500:
                self.timer = 0
                self.state = "Elixir"
        elif self.state == "Elixir":
            if self.timer >= 500:
                self.timer = 0
                self.state = "Charger"
        elif self.state == "Charger":
            if self.timer >= 500:
                self.timer = 0
                self.state = "Item"
        elif self.state == "Item":
            pass
        elif self.state == "Exp":
            if self.timer >= 500:
                self.timer = 0
                self.state = "Exp_Animate"
        elif self.state == "Exp_Animate":
            if self.timer >= self.exp_animation_time:
                self.timer = 0
                self.state = "Done"
        elif self.state == "Done":
            pass

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), self.bg_rect_1, border_radius=12)
        pygame.draw.rect(surface, (50, 50, 50), self.bg_rect_2, border_radius=12)

        if self.state == "Gold" or self.state == "Supply" or self.state == "Elixir" or self.state == "Charger" or \
                self.state == "Item":
            tw(surface, "Gold:" + str(self.parent.gold_reward).rjust(15), TEXT_COLOR,
               [X * 6 / 100, Y * 6 / 100, X * 40 / 100, Y * 8 / 100], HEADING_FONT)
        if self.state == "Supply" or self.state == "Elixir" or self.state == "Charger" or self.state == "Item":
            tw(surface, "Supply:" + str(self.parent.supply_reward).rjust(13), TEXT_COLOR,
               [X * 6 / 100, Y * 14 / 100, X * 40 / 100, Y * 8 / 100], HEADING_FONT)
        if self.state == "Elixir" or self.state == "Charger" or self.state == "Item":
            tw(surface, "Elixir:" + str(self.parent.elixir_reward).rjust(13), TEXT_COLOR,
               [X * 6 / 100, Y * 22 / 100, X * 40 / 100, Y * 8 / 100], HEADING_FONT)
        if self.state == "Charger" or self.state == "Item":
            tw(surface, "Charger:" + str(self.parent.charger_reward).rjust(12), TEXT_COLOR,
               [X * 6 / 100, Y * 30 / 100, X * 40 / 100, Y * 8 / 100], HEADING_FONT)
        if self.state == "Item":
            tw(surface, "Item:", TEXT_COLOR,
               [X * 6 / 100, Y * 38 / 100, X * 40 / 100, Y * 8 / 100], HEADING_FONT)
        if self.state == "Exp" or self.state == "Exp_Animate" or self.state == "Done":
            for i, player in enumerate(self.parent.player_characters.sprites()):
                surface.blit(REGION_STATIC_SPRITES[player.current_class + "Icon"],
                             (X * 6 / 100, (Y * 14 / 100) + i * Y * 30 / 100))
                tw(surface, player.name, TEXT_COLOR,
                   [X * 6 / 100, Y * 6 / 100 + (i * Y * 30 / 100), X * 40 / 100, Y * 8 / 100], HEADING_FONT)
                exp_bar = (EXPERIENCE_CURVE[player.level - 1] - player.experience_to_level) / EXPERIENCE_CURVE[
                    player.level - 1]
                if self.state == "Exp":
                    start_exp = player.exp - int(self.parent.exp_reward / len(self.parent.player_characters.sprites()))
                    current_exp = start_exp
                    k = 0
                    for j, value in enumerate(EXPERIENCE_CURVE_TOTAL):
                        if current_exp < EXPERIENCE_CURVE_TOTAL[j]:
                            k = j
                            break
                    else:
                        k = len(EXPERIENCE_CURVE_TOTAL)
                    if k == 0:
                        bar_progress = current_exp / EXPERIENCE_CURVE_TOTAL[0]
                    elif k == len(EXPERIENCE_CURVE_TOTAL):
                        bar_progress = 1
                    else:
                        bar_progress = (current_exp - EXPERIENCE_CURVE_TOTAL[k - 1]) / (
                                EXPERIENCE_CURVE_TOTAL[k] - EXPERIENCE_CURVE_TOTAL[k - 1])
                    if k < len(EXPERIENCE_CURVE_TOTAL):
                        to_next = str(int(EXPERIENCE_CURVE_TOTAL[k] - current_exp))
                    else:
                        to_next = "0"
                    tw(surface, "level: " + str(k + 1), TEXT_COLOR,
                       [X * 5 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    tw(surface, "next: " + to_next, TEXT_COLOR,
                       [X * 72 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    pygame.draw.rect(surface, (150, 150, 50),
                                     [X * 20 / 100, Y * 20 / 100 + (i * Y * 30 / 100), bar_progress * (X * 50 / 100),
                                      Y * 10 / 100], border_radius=4)
                elif self.state == "Exp_Animate":
                    animate_exp = (self.timer / self.exp_animation_time)
                    start_exp = player.exp - int(self.parent.exp_reward / len(self.parent.player_characters.sprites()))
                    finish_exp = player.exp
                    current_exp = start_exp + (animate_exp * (finish_exp - start_exp))
                    k = 0
                    for j, value in enumerate(EXPERIENCE_CURVE_TOTAL):
                        if current_exp < EXPERIENCE_CURVE_TOTAL[j]:
                            k = j
                            break
                    else:
                        k = len(EXPERIENCE_CURVE_TOTAL)
                    if k == 0:
                        bar_progress = current_exp / EXPERIENCE_CURVE_TOTAL[0]
                    elif k == len(EXPERIENCE_CURVE_TOTAL):
                        bar_progress = 1
                    else:
                        bar_progress = (current_exp - EXPERIENCE_CURVE_TOTAL[k - 1]) / (
                                EXPERIENCE_CURVE_TOTAL[k] - EXPERIENCE_CURVE_TOTAL[k - 1])
                    if k < len(EXPERIENCE_CURVE_TOTAL):
                        to_next = str(int(EXPERIENCE_CURVE_TOTAL[k] - current_exp))
                    else:
                        to_next = "0"
                    tw(surface, "level: " + str(k + 1), TEXT_COLOR,
                       [X * 5 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    tw(surface, "next: " + to_next, TEXT_COLOR,
                       [X * 72 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    pygame.draw.rect(surface, (150, 150, 50),
                                     [X * 20 / 100, Y * 20 / 100 + (i * Y * 30 / 100), bar_progress * (X * 50 / 100),
                                      Y * 10 / 100], border_radius=4)
                elif self.state == "Done":
                    finish_exp = player.exp
                    current_exp = finish_exp
                    k = 0
                    for j, value in enumerate(EXPERIENCE_CURVE_TOTAL):
                        if current_exp < EXPERIENCE_CURVE_TOTAL[j]:
                            k = j
                            break
                    else:
                        k = len(EXPERIENCE_CURVE_TOTAL)
                    if k == 0:
                        bar_progress = current_exp / EXPERIENCE_CURVE_TOTAL[0]
                    elif k == len(EXPERIENCE_CURVE_TOTAL):
                        bar_progress = 1
                    else:
                        bar_progress = (current_exp - EXPERIENCE_CURVE_TOTAL[k - 1]) / (
                                EXPERIENCE_CURVE_TOTAL[k] - EXPERIENCE_CURVE_TOTAL[k - 1])
                    if k < len(EXPERIENCE_CURVE_TOTAL):
                        to_next = str(int(EXPERIENCE_CURVE_TOTAL[k] - current_exp))
                    else:
                        to_next = "0"
                    tw(surface, "level: " + str(k + 1), TEXT_COLOR,
                       [X * 5 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    tw(surface, "next: " + to_next, TEXT_COLOR,
                       [X * 72 / 100, Y * 22 / 100 + (i * Y * 30 / 100), X * 20 / 100, Y * 10 / 100], TEXT_FONT)
                    pygame.draw.rect(surface, (150, 150, 50),
                                     [X * 20 / 100, Y * 20 / 100 + (i * Y * 30 / 100), bar_progress * (X * 50 / 100),
                                      Y * 10 / 100], border_radius=4)
                pygame.draw.rect(surface, (0, 0, 0), [X * 19.5 / 100, Y * 19 / 100 + (i * Y * 30 / 100), (X * 51 / 100),
                                                      Y * 12 / 100], 8, border_radius=8)

    def handle_action(self):
        if self.state == "Blank" or self.state == "Gold" or self.state == "Supply" or self.state == "Elixir" or \
                self.state == "Charger":
            self.state = "Item"
        elif self.state == "Item":
            self.state = "Exp"
            self.timer = 0
        elif self.state == "Exp":
            self.state = "Done"
        elif self.state == "Exp_Animate":
            self.state = "Done"
        elif self.state == "Done":
            self.parent.handle_action("Clean_Up")


class BattleMessage:
    def __init__(self):
        self.timer = None
        self.message = None
        self.rect = [X * 2 / 100, Y * 2 / 100, X * 60 / 100, Y * 10 / 100]
        self.state = "Idle"

    def set_message(self, message, time=2000, state="Display"):
        self.message = message
        self.timer = time
        self.state = state

    def update(self, dt):
        if self.state == "Display" and self.timer:
            self.timer -= dt
            if self.timer <= 0:
                self.state = "Idle"
                self.message = None
                self.timer = None

    def draw(self, surface):
        if self.state == "Display" or self.state == "Persist":
            pygame.draw.rect(surface, (150, 150, 150), self.rect, border_radius=8)
            tw(surface, self.message, TEXT_COLOR, [self.rect[0] + 5, self.rect[1] + 2, self.rect[2] -
                                                   10, self.rect[3] - 4], TEXT_FONT)

    def clear_message(self):
        self.state = "Idle"
        self.message = None
        self.timer = None


class DamageParticle:
    def __init__(self):
        self.particles = []

    def draw(self, surface):
        if self.particles:
            particles_copy = []
            for particle in self.particles:
                if particle[5] <= 0:
                    settings.tw(surface, str(particle[3]), particle[4], particle[0], settings.TEXT_FONT)
                    new_x = int(particle[0][0] + particle[1][0])
                    new_y = int(particle[0][1] + particle[1][1])
                    new_vx = particle[1][0] / particle[2][0]
                    if -1 < new_vx < 1:
                        new_vx = 0
                    new_vy = particle[2][1] + particle[1][1]
                    new_velocity = (new_vx, new_vy)
                    new_rect = [new_x, new_y, particle[0][2], particle[0][3]]
                    if not particle[5]:
                        r = particle[4][0] + 5
                        if r > 255:
                            r = 255
                        g = particle[4][1] + 4
                        if g > 255:
                            g = 255
                        b = particle[4][2] + 5
                        if b > 255:
                            b = 255
                    else:
                        r = particle[4][0] + 5
                        r %= 255
                        g = particle[4][1] + 7
                        g %= 255
                        b = particle[4][2] + 11
                        b %= 255
                    new_color = (r, g, b)
                    particles_copy.append([new_rect, new_velocity, particle[2], particle[3], new_color, particle[5]])
                else:
                    particles_copy.append(particle)
            self.particles = particles_copy
        self.delete_particles()

    def update(self, dt):
        if self.particles:
            for particle in self.particles:
                if particle[5] > 0:
                    particle[5] -= dt

    def add_particles(self, x, y, damage, critical=False, velocity=(1, 1), delay=0):
        rect = [x, y, 200, 100]
        f = settings.random_int(1090, 1150) / 1000
        l = settings.random_int(100, 120) / 100
        if (settings.X * 3 / 8) - x < 0:
            velocity = (-settings.X / 100 * velocity[0], (-settings.Y / 720) * l * velocity[1])
            force = (f, 0)
        else:
            velocity = (settings.X / 100 * velocity[0], (-settings.Y / 720) * l * velocity[1])
            force = (f, 0)
        color = (20, 100, 20)
        particle = [rect, velocity, force, damage, color, critical, delay]
        self.particles.append(particle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[4] != (255, 255, 255)]
        self.particles = particle_copy
        particle_copy = [particle for particle in self.particles if particle[0][1] > 0]
        self.particles = particle_copy


class BattleCharacter(pygame.sprite.Sprite):
    def __init__(self, parent="None"):
        super().__init__()
        self.slot = "None"
        self.parent = parent
        self.action = None
        self.hover = False
        self.selected = False
        self.current_sprite = 0
        self.dazed = 0
        self.disabled = 0
        self.stunned = 0
        self.perplexed = 0
        self.vigilant = 0
        self.smitten = 0
        self.faith = 0
        self.brave = 0
        self.calm = 0
        self.haste = 0
        self.turns = 0
        self.quick = 0
        self.lucky = 0
        self.focus = 0
        self.bleed = 0
        self.toxic = 0
        self.burn = 0
        self.curse = 0
        self.spite = 0
        self.invincible = 0
        self.shield = 0
        self.ward = 0
        self.frail = 0
        self.terrify = 0
        self.weak = 0
        self.distract = 0
        self.slow = 0
        self.hex = 0
        self.dull = 0
        self.savage = 0
        self.gentle = 0
        self.speed = 0
        self.state = "Idle"
        self.action_options = []
        self.attack_action = Attack(self)
        self.battle_action = None

    #       self.defend_action = Attack(self)
    #       self.run_action = Attack(self)

    def update(self, dt):
        pass

    def damage(self, damage, action, delay=0):
        damage_total = damage
        if damage_total == 'miss':
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, damage_total, delay=delay)
        elif self.invincible > 0:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, "immune")
        else:
            if action.defend_stat == "defense" or action.defend_stat == "lowest":
                if self.shield > 0:
                    damage_total /= 2
            if action.defend_stat == "spirit" or action.defend_stat == "lowest":
                if self.ward > 0:
                    damage_total /= 2
            if self.spite > 0:
                damage_total += 10
            if self.curse > 0:
                damage_total *= 2
            damage_total = int(damage_total)
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, damage_total, delay=delay)
            self.hp -= damage_total
            if self.hp < 0:
                self.hp = 0

    def give_options(self):
        options = []
        if hasattr(self, 'action'):
            if getattr(self.action, 'name', "None") != "None":
                return [(self.slot, "None", ["None"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]
        for action in self.action_options:
            if action.is_usable():
                action_outcomes = action.expected_value()
                for i in range(len(action_outcomes)):
                    options.append(action_outcomes[i])
        #        self.action = eval(choice[0])(self, choice[1])
        #        self.parent.battle_actions.add(self.action)
        #        self.parent.battle_objects.add(self.action)
        if options:
            return options
        else:
            return [(self.slot, "None", ["None"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]

    def ko(self):
        self.kill()
        self.parent.battle_characters_ko.add(self)
        self.parent.battle_objects.add(self)
        self.battle_action.kill()


class PlayerCharacter(BattleCharacter):
    def __init__(self, char_class, player_holder, parent="None", name="bob"):
        super().__init__(parent="None")
        self.slot = player_holder
        self.move_selected = False
        self.sprites = battle_characters[char_class]['sprites']
        self.idle_frames = battle_characters[char_class]['idle']
        self.idle_speed = battle_characters[char_class]['idle speed']
        self.idle_weights = battle_characters[char_class]['idle weights']
        self.idle_weights = weights_convert(self.idle_speed, self.idle_weights)
        self.idle_time = random_int(0, self.idle_speed)
        self.idle_index = 0
        self.attack_frames = battle_characters[char_class]['attack']
        self.cast_frames = battle_characters[char_class]['cast']
        self.hit_frames = battle_characters[char_class]['hit']
        self.miss_frames = battle_characters[char_class]['miss']
        self.base_x = 300
        self.x = self.base_x
        self.base_y = 300
        self.y = self.base_y
        self.image = self.sprites[self.idle_frames[self.idle_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.attack_type = "Attack"
        self.name = name
        self.base_class = self.current_class = char_class
        self.hp = self.max_hp = self.base_hp = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_HP"]
        self.mp = self.max_mp = self.base_mp = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_MP"]
        self.strength = self.base_strength = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_STRENGTH"]
        self.defense = self.base_defense = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_DEFENSE"]
        self.magic = self.base_magic = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_MAGIC"]
        self.spirit = self.base_spirit = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_SPIRIT"]
        self.speed = self.base_speed = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_SPEED"]
        self.luck = self.base_luck = BASE_STATS[char_class.upper() + "_BASE_STATS"][char_class.upper() + "_BASE_LUCK"]
        self.equipment_options = self.base_equipment_options = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_EQUIPMENT_OPTIONS"]
        self.base_attack_type = self.attack_type = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_ATTACK_TYPE"]
        self.equipment = {}
        self.techniques = self.base_techniques = BASE_STATS[char_class.upper() + "_BASE_STATS"][
            char_class.upper() + "_BASE_TECHNIQUES"]
        self.crit_rate = self.base_crit_rate = 1
        self.crit_damage = self.base_crit_damage = 1
        self.level = 1
        self.exp = 0
        self.skill_points = 0
        self.experience_to_level = 0
        self.battle_action = NoActionSelected(self)

    def update(self, dt):
        if self.level < len(EXPERIENCE_CURVE) + 1:
            self.experience_to_level = sum(EXPERIENCE_CURVE[:self.level]) - self.exp
            if self.exp > sum(EXPERIENCE_CURVE[:self.level]):
                self.level += 1
                self.skill_points += 1
        if self.state == "Idle":
            self.idle_time += random_int(15, 20)
            if self.idle_time > self.idle_weights[self.idle_index]:
                self.idle_time -= self.idle_weights[self.idle_index]
                self.idle_index += 1
                if self.idle_index >= len(self.idle_frames):
                    self.idle_index = 0
            self.image = self.sprites[self.idle_frames[self.idle_index]]
        elif self.state == "Attack":
            self.image = self.sprites[self.attack_frames[0]]
        elif self.state == "Cast":
            self.image = self.sprites[self.cast_frames[0]]
        elif self.state == "Hit":
            self.image = self.sprites[self.hit_frames[0]]
        elif self.state == "Miss":
            self.image = self.sprites[self.miss_frames[0]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def pre_turn(self, parent):
        if not hasattr(self, 'battle_action'):
            setattr(self, 'battle_action', NoActionSelected(self))
            parent.battle_actions.add(self.battle_action)
            parent.battle_objects.add(self.battle_action)
        elif self.battle_action.turns == 0:
            if self.battle_action == "None":
                return
            else:
                self.battle_action.kill()
                setattr(self, 'battle_action', NoActionSelected(self))
                parent.battle_actions.add(self.battle_action)
                parent.battle_objects.add(self.battle_action)


class Slime(BattleCharacter):
    def __init__(self, enemy_slot, region_index, n_enemy, parent):
        super().__init__(parent)
        self.name = "Slime" + enemy_slot[5:]
        self.hover = False
        self.slot = enemy_slot
        self.sprites = [image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                   r"\Enemy\Slime\Slime128p1.png"),
                        image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                   r"\Enemy\Slime\Slime128p2.png"),
                        image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                   r"\Enemy\Slime\Slime128p3.png"),
                        image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                   r"\Enemy\Slime\Slime128p4.png")]
        self.idle_frames = [0, 1]
        self.idle_weights = [3, 1]
        self.idle_speed = 1000
        self.idle_time = random_int(0, self.idle_speed)
        self.idle_index = 0
        self.idle_weights = weights_convert(self.idle_speed, self.idle_weights)
        self.attack_frames = [2]
        self.cast_frames = [3]
        self.hit_frames = [2]
        self.miss_frames = [3]
        self.x = self.base_x = BATTLE_MENUS['enemy positions'][n_enemy][enemy_slot][0]
        self.y = self.base_y = BATTLE_MENUS['enemy positions'][n_enemy][enemy_slot][1]
        self.image = self.sprites[self.idle_frames[self.idle_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hp = self.max_hp = [100, 120, 140, 160, 190, 220, 250, 300][region_index]
        self.mp = self.max_mp = [100, 110, 120, 130, 140, 150, 160, 180][region_index]
        self.strength = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.magic = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.defense = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.spirit = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.luck = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.speed = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.crit_rate = [1, 1, 1, 1, 1, 1.1, 1.1, 1.1][region_index]
        self.crit_damage = [1, 1, 1, 1, 1, 1, 1, 1][region_index]
        self.ai = {'ai_type': 'simple',
                   'actions': [["Attack", "Attack"], ["Skill", "Slime Ball"]],
                   'weights': [50, 50],
                   'target': 'random', }
        self.exp_reward = [200, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.supply_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.elixir_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.charger_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.gold_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index],
                                      [10, 12, 14, 16, 18, 20, 22, 24][region_index])
        self.action_options = []
        self.action_options.append(Attack(self))
        self.action_options.append(SlimeBall(self))
        self.action_options.append(NoActionSelected(self))
        self.item_reward = self.reward(region_index)

    def reward(self, region_index):
        if len([['none', 'common', 'rare'], [60, 37, 3]][region_index]) == 1:
            if [['none', 'common', 'rare'], [60, 37, 3]][region_index][0] != 'none':
                item = item_generate([['none', 'common', 'rare'], [60, 37, 3]][region_index])
            else:
                item = 'none'
        else:
            n = random_int(0, len([['none', 'common', 'rare'], [60, 37, 3]][region_index]))
            if [['none', 'common', 'rare'], [60, 37, 3]][region_index][n - 1] != 'none':
                item = item_generate([['none', 'common', 'rare'], [60, 37, 3]][region_index])
            else:
                item = 'none'
        return item

    def update(self, dt):
        if self.state == "Idle":
            self.idle_time += random_int(15, 20)
            if self.idle_time > self.idle_weights[self.idle_index]:
                self.idle_time -= self.idle_weights[self.idle_index]
                self.idle_index += 1
                if self.idle_index >= len(self.idle_frames):
                    self.idle_index = 0
            self.image = self.sprites[self.idle_frames[self.idle_index]]
        elif self.state == "Attack":
            self.image = self.sprites[self.attack_frames[0]]
        elif self.state == "Cast":
            self.image = self.sprites[self.cast_frames[0]]
        elif self.state == "Hit":
            self.image = self.sprites[self.hit_frames[0]]
        elif self.state == "Miss":
            self.image = self.sprites[self.miss_frames[0]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def ko(self):
        self.kill()
        self.parent.battle_characters_ko.add(self)
        self.parent.battle_objects.add(self)
        self.battle_action.kill()
        self.parent.supply_reward += self.supply_reward
        self.parent.charger_reward += self.charger_reward
        self.parent.elixir_reward += self.elixir_reward
        self.parent.exp_reward += self.exp_reward
        self.parent.gold_reward += self.gold_reward


class BattleOverlay(object):
    def __init__(self, parent):
        # point to parent and persist dictionary
        self.parent = parent
        # target reticle flash variables
        self.reticle_color = None
        self.target_color = (255, 180, 180)
        self.target_speed = 500
        self.target_time = 0
        self.target_direction = 1

    def update(self, dt):
        self.reticle_color_update(dt)

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), [0, Y * 75 / 100, X, Y * 25 / 100])
        pygame.draw.rect(surface, (50, 50, 50), [X * 80 / 100, 0, X * 20 / 100, Y])
        if self.parent.state == "Turn":
            if self.parent.turn_sub_state == "Move_Select" or self.parent.turn_sub_state == "Item" or \
                    self.parent.turn_sub_state == "Skill":
                pygame.draw.rect(surface, (150, 0, 150), BATTLE_MENUS['move_top_menu_rects']['border'], 2)
                for i, option in enumerate(actions_dict.keys()):
                    color = TEXT_COLOR
                    if i == self.parent.action_type_index:
                        color = SELECTED_COLOR
                    tw(surface, option, color, BATTLE_MENUS['move_top_menu_rects'][option], TEXT_FONT)
            elif self.parent.turn_sub_state == "Browse":
                pygame.draw.rect(surface, (150, 150, 20), BATTLE_MENUS['turn_end_rect'], 5, 12)
                tw(surface, "END TURN", TEXT_COLOR, BATTLE_MENUS['turn_end_rect'],
                   HEADING_FONT)
            elif self.parent.turn_sub_state == "Target":
                target_type = getattr(self.parent.selected_action, 'target_type')
                target = None
                for sprite in self.parent.battle_characters.sprites():
                    if getattr(sprite, 'hover', False):
                        target = sprite
                if target_type == "Single" and target is not None:
                    pygame.draw.rect(surface, self.reticle_color, [target.rect.left - 4, target.rect.top - 4,
                                                                   target.rect.width + 8, target.rect.height + 8], 2)
                elif target_type == "Team" and target is not None:
                    if target.slot[:5] == "enemy":
                        for sprite in self.parent.enemy_characters.sprites():
                            pygame.draw.rect(surface, self.reticle_color, [sprite.rect.left - 4, sprite.rect.top - 4,
                                                                           sprite.rect.width + 8,
                                                                           sprite.rect.height + 8], 2)
                    else:
                        for sprite in self.parent.player_characters.sprites():
                            pygame.draw.rect(surface, self.reticle_color, [sprite.rect.left - 4, sprite.rect.top - 4,
                                                                           sprite.rect.width + 8,
                                                                           sprite.rect.height + 8], 2)

                elif target_type == "All" and target is not None:
                    for sprite in self.parent.battle_characters.sprites():
                        pygame.draw.rect(surface, self.reticle_color, [sprite.rect.left - 4, sprite.rect.top - 4,
                                                                       sprite.rect.width + 8, sprite.rect.height + 8],
                                         2)
            elif self.parent.turn_sub_state == "Confirm":
                pygame.draw.rect(surface, (50, 50, 50), BATTLE_MENUS['confirm_rect'], border_radius=12)
                pygame.draw.rect(surface, (150, 150, 20), BATTLE_MENUS['confirm_rect'], 5, 12)
                tw(surface, "End the turn?", TEXT_COLOR, BATTLE_MENUS['confirm_prompt_rect'], HEADING_FONT)
                color = TEXT_COLOR
                if click_check(BATTLE_MENUS['confirm_yes_rect']):
                    color = SELECTED_COLOR
                tw(surface, "YES", color, BATTLE_MENUS['confirm_yes_rect'], HEADING_FONT)
                color = TEXT_COLOR
                if click_check(BATTLE_MENUS['confirm_no_rect']):
                    color = SELECTED_COLOR
                tw(surface, "NO", color, BATTLE_MENUS['confirm_no_rect'], HEADING_FONT)
        elif self.parent.turn_sub_state == "Victory_1":
            pass
        elif self.parent.turn_sub_state == "Victory_2":
            pass
        elif self.parent.turn_sub_state == "Victory_3":
            pass
        elif self.parent.turn_sub_state == "Victory":
            pygame.draw.rect(surface, (20, 20, 20), [X * 30 / 100, Y * 30 / 100, X * 40 / 100, Y * 40 / 100],
                             border_radius=12)
            tw(surface, "VICTORY!", TEXT_COLOR, [X * 30 / 100, Y * 30 / 100, X * 40 / 100, Y * 40 / 100],
               HEADING_FONT)
            tw(surface, "Press enter to continue.", TEXT_COLOR, [X * 30 / 100, Y * 60 / 100, X * 20 / 100,
                                                                 Y * 20 / 100], TEXT_FONT)
        elif self.parent.turn_sub_state == "Defeat":
            pygame.draw.rect(surface, (20, 20, 20), [X * 30 / 100, Y * 30 / 100, X * 40 / 100, Y * 40 / 100],
                             border_radius=12)
            tw(surface, "Defeat!", TEXT_COLOR, [X * 30 / 100, Y * 30 / 100, X * 40 / 100, Y * 40 / 100],
               HEADING_FONT)
            tw(surface, "Press enter to continue.", TEXT_COLOR, [X * 30 / 100, Y * 60 / 100, X * 20 / 100,
                                                                 Y * 20 / 100], TEXT_FONT)
        for sprite in self.parent.player_characters.sprites():
            tw(surface, "hp: " + str(sprite.hp) + "/" + str(sprite.max_hp), TEXT_COLOR,
               BATTLE_MENUS['player_status_rects'][sprite.slot]['hp'], DETAIL_FONT)
            tw(surface, "mp: " + str(sprite.mp) + "/" + str(sprite.max_mp), TEXT_COLOR,
               BATTLE_MENUS['player_status_rects'][sprite.slot]['mp'], DETAIL_FONT)
            tw(surface, sprite.name, TEXT_COLOR,
               BATTLE_MENUS['player_status_rects'][sprite.slot]['name'], TEXT_FONT)

    def reticle_color_update(self, dt):
        self.target_time += dt * self.target_direction
        if self.target_time <= 0:
            self.target_time = 0
            self.target_direction *= -1
        elif self.target_time >= self.target_speed:
            self.target_time = self.target_speed
            self.target_direction *= -1
        step = pytweening.easeInOutSine(self.target_time / self.target_speed)
        self.reticle_color = (self.target_color[0] * step, self.target_color[1] * step, self.target_color[2] * step)


class BattleAction(pygame.sprite.Sprite):
    def __init__(self, parent, target=None):
        super().__init__()
        if target is None:
            target = ['None']
        self.state = "Idle"
        self.target = target
        self.hover = False
        self.parent = parent
        self.source = self.parent.slot
        self.speed = self.parent.speed
        self.queue = 0
        self.priority = False
        self.x = 0
        self.y = 0
        self.action_type = "None"
        self.name = "None"
        self.animation_speed = BATTLE_MENU_SPRITES['animation_speed']
        self.sprites = BATTLE_MENU_SPRITES['action_slot_sprites']
        self.attack_frames = BATTLE_MENU_SPRITES['attack_action']
        self.attack_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['attack_action_weights'])
        self.ability_frames = BATTLE_MENU_SPRITES['ability_action']
        self.ability_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['ability_action_weights'])
        self.item_frames = BATTLE_MENU_SPRITES['item_action']
        self.item_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['item_action_weights'])
        self.defend_frames = BATTLE_MENU_SPRITES['defend_action']
        self.defend_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['defend_action_weights'])
        self.skill_frames = BATTLE_MENU_SPRITES['ability_action']
        self.skill_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['ability_action_weights'])
        self.none_frames = BATTLE_MENU_SPRITES['no_action']
        self.none_weights = weights_convert(self.animation_speed, BATTLE_MENU_SPRITES['no_action_weights'])
        self.image = self.sprites[4]
        self.timer = self.animation_speed
        self.animation_index = 0
        self.turns = 0
        self.hits = 0
        self.mp_cost = 0
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.end_action_timer = None
        self.animation_start_timer = None
        self.damage_timer = None
        self.accuracy = 100
        self.crit_rate = 1
        self.action_time = 1000

    def delete_action(self):
        self.kill()

    def update(self, dt):
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.timer -= dt
        if self.timer <= 0:
            self.animation_index += 1
            self.animation_index %= len(getattr(self, self.action_type.lower() + "_frames"))
            self.timer = getattr(self, self.action_type.lower() + "_weights")[self.animation_index]
            self.image = self.sprites[getattr(self, self.action_type.lower() + "_frames")[self.animation_index]]
        if self.state == "Idle":
            self.x, self.y = BATTLE_MENUS['slot_positions'][self.queue]
        if self.end_action_timer:
            if self.end_action_timer > 0:
                self.end_action_timer -= dt
                if self.end_action_timer <= 0:
                    self.end_action_timer = None
                    self.action_done()

    def action_done(self):
        self.parent.parent.stop_wait()
        self.kill()

    def draw_text(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), [self.rect[0] + 17, self.rect[1] + 10, self.rect[2] - 34, self.rect[3] -
                                              20], border_radius=5)
        tw(surface, self.parent.name + ':' + self.name.rjust(5), TEXT_COLOR,
           [self.rect[0] + 26, self.rect[1] + 20, self.rect[2] - 14, self.rect[3] - 24], DETAIL_FONT)

    def is_usable(self):
        pass

    def do_action(self):
        self.end_action_timer = 1000

    def target_set(self, battle_character):
        pass


class NoActionSelected(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)

    def expected_value(self):
        value_set = []
        outcome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        value_set.append((self.parent, self, self, outcome))
        return value_set

    def is_usable(self):
        return True

    def do_action(self):
        self.end_action_timer = 1000

    def target_set(self, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.kill()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class SlimeBall(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Single"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 10
        self.mp_cost = 10
        self.accuracy = 90
        self.effect = [("frail", 100)]
        self.name = "SlimeBall"
        self.action_type = "Skill"
        self.action_time = 1000

    def situational_value(self):
        value_set = []
        for player in self.parent.parent.player_characters.sprites():
            if self.parent.mp < self.mp_cost:
                value = 0
            elif player.frail == 0:
                value = player.defense
            else:
                value = player.defense / 2
            value_set.append((self.name, player.slot, value))
        return value_set

    def do_action(self):
        damage_roll = random_int(85, 100)
        critical_roll = random_int(0, 100)
        effect_roll = random_int(0, 100)
        miss_roll = random_int(0, 100)
        source_luck = getattr(self.parent, 'luck')
        target_luck = getattr(self.parent.parent, self.target[0]).luck
        attack = getattr(self.parent, 'attack')
        defense = getattr(self.parent.parent, self.target[0]).defense
        if self.parent.brave > 0:
            attack *= 1.5
        if self.parent.weak > 0:
            attack /= 1.5
        if getattr(self.parent.parent, self.target).vigilant > 0:
            defense *= 1.5
        if getattr(self.parent.parent, self.target).frail > 0:
            defense /= 1.5
        if self.parent.lucky > 0:
            source_luck *= 1.5
        if self.parent.hex > 0:
            source_luck /= 1.5
        if getattr(self.parent.parent, self.target).lucky > 0:
            target_luck *= 1.5
        if getattr(self.parent.parent, self.target).hex > 0:
            target_luck /= 1.5
        if miss_roll * source_luck / target_luck < self.accuracy:
            damage = 'miss'
        else:
            critical = 1
            if critical_roll * self.parent.crit_rate * target_luck / source_luck <= self.crit_rate:
                critical = 1.5 * self.parent.crit_damage
            damage = int((self.power * attack / defense) * critical * damage_roll / 100)
        self.parent.state = "Attack"
        # animation class needed
        getattr(self.parent.parent, self.target[0]).damage(damage, self, self.action_time / 1000)
        for i, status in enumerate(self.effect):
            if effect_roll <= status[1]:
                getattr(self.parent.parent, self.target[0]).status(status[0], self,
                                                                   (self.action_time + (100 * i)) / 1000)
        self.end_action_timer = Timer(int(self.action_time / 1000), self.action_done())
        self.end_action_timer.start()

    def action_done(self):
        self.parent.parent.stop_wait()
        self.kill()


class Attack(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Single"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 20
        self.animation = "Slash_1"
        self.name = "Attack"
        self.action_type = "Attack"

    def expected_value(self):
        value_set = []
        for character in self.parent.parent.battle_characters.sprites():
            outcome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            damage_low, damage_high, p_hit, critical_low, critical_high, p_critical = \
                attack_defense_calculate(self, self.parent, character, ev=True)
            outcome[BATTLE_MENUS['battle_slot_index'][character.slot]] = \
                ((damage_low + damage_high) * p_hit * (1 - p_critical) / (2 * character.hp)) + \
                ((critical_low + critical_high) * p_hit * p_critical / (2 * character.hp))
            value_set.append((self.parent, self, [character], outcome))
        return value_set

    def is_usable(self):
        if self.parent.disabled > 0 or self.parent.stunned > 0:
            return False
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.kill()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


def attack_defense_calculate(action, source, target, estimate=False, ev=False):
    critical_roll = random_int(0, 100)
    miss_roll = random_int(0, 100)
    damage_roll = random_int(85, 100)
    attack = source.strength
    defense = target.defense
    source_luck = source.luck
    target_luck = target.luck
    if source.brave > 0:
        attack *= 1.5
    if source.weak > 0:
        attack /= 1.5
    if target.vigilant > 0:
        defense *= 1.5
    if target.frail > 0:
        defense /= 1.5
    if source.lucky > 0:
        source_luck *= 1.5
    if source.hex > 0:
        source_luck /= 1.5
    if target.lucky > 0:
        target_luck *= 1.5
    if target.hex > 0:
        target_luck /= 1.5
    if estimate or ev:
        low_end = (action.power * attack / defense) * 85 / 100
        high_end = (action.power * attack / defense)
        critical_low = (action.power * attack / defense) * 1.5 * 85 / 100
        critical_high = (action.power * attack / defense) * 1.5
        if target.shield > 0:
            low_end /= 2
            high_end /= 2
            critical_low /= 2
            critical_high /= 2
        if target.invincible > 0:
            low_end = 0
            high_end = 0
            critical_low = 0
            critical_high = 0
        if target.spite > 0:
            low_end += 10
            high_end += 10
            critical_low += 10
            critical_high += 10
        if target.curse > 0:
            low_end *= 2
            high_end *= 2
            critical_low *= 2
            critical_high *= 2
        p_hit = (source_luck / target_luck) * action.accuracy / 100
        p_critical = 1 - (0.95 / ((source_luck / target_luck) * source.crit_rate * action.crit_rate))
        if p_critical < 0:
            p_critical = 0
        if ev:
            return low_end, high_end, p_hit, critical_low, critical_high, p_critical
        elif estimate:
            return low_end, high_end, p_hit
    if miss_roll * target_luck / source_luck > action.accuracy:
        damage = 'miss'
    else:
        critical = 1
        if critical_roll * source.crit_rate * action.crit_rate * target_luck / source_luck >= 95:
            critical = 1.5 * source.crit_damage
        damage = (action.power * attack / defense) * critical * damage_roll / 100
    return damage


actions_dict = {
    "Attack": {
        "Attack": {
            "Target": "Single",
            "Attack_Stat": "strength",
            "Defend_Stat": "defense",
            "Animation": "Slash_1",
        },
        "Magic_Attack": {
            "Target": "Single",
            "Attack_Stat": "magic",
            "Defend_Stat": "spirit",
            "Animation": "Slash_1",
        },
        "Defense_Attack": {
            "Target": "Single",
            "Attack_Stat": "defense",
            "Defend_Stat": "defense",
            "Animation": "Slash_1",
        },
        "Energy_Attack": {
            "Target": "Single",
            "Attack_Stat": "strength",
            "Defend_Stat": "lowest",
            "Animation": "Slash_1",
        },
        "True_Attack": {
            "Target": "Single",
            "Attack_Stat": "strength",
            "Defend_Stat": "none",
            "Animation": "Slash_1",
        },
        "Wide_Attack": {
            "Target": "Team",
            "Attack_Stat": "strength",
            "Defend_Stat": "defense",
            "Animation": "Slash_1",
        },
        "Wide_Magic_Attack": {
            "Target": "Team",
            "Attack_Stat": "magic",
            "Defend_Stat": "spirit",
            "Animation": "Slash_1",
        },
        "Wide_Energy_Attack": {
            "Target": "Team",
            "Attack_Stat": "strength",
            "Defend_Stat": "lowest",
            "Animation": "Slash_1",
        },
        "Wide_True_Attack": {
            "Target": "Team",
            "Attack_Stat": "strength",
            "Defend_Stat": "none",
            "Animation": "Slash_1",
        },
        "Chaotic_Attack": {
            "Target": "All",
            "Attack_Stat": "strength",
            "Defend_Stat": "defense",
            "Animation": "Slash_1",
        },
        "Chaotic_Magic_Attack": {
            "Target": "All",
            "Attack_Stat": "magic",
            "Defend_Stat": "spirit",
            "Animation": "Slash_1",
        },
        "Chaotic_Energy_Attack": {
            "Target": "All",
            "Attack_Stat": "strength",
            "Defend_Stat": "lowest",
            "Animation": "Slash_1",
        },
        "Chaotic_True_Attack": {
            "Target": "All",
            "Attack_Stat": "strength",
            "Defend_Stat": "none",
            "Animation": "Slash_1",
        },
    },
    "Defend": {
    },
    "Skill": {
        "Slime Ball": {
            "Target": "Single",
            "Attack_Stat": "strength",
            "Defend_Stat": "defense",
            "Power": 10,
            "MP Cost": 10,
            "Effect": [("Corrode", 100)],
        },
    },
    "Item": {

    },
    "Run": {

    },
}
weapon_dict = {
    "Short Sword": {
        "attack": [6, 8, 10, 12, 14]
    },

    "Coder Sword": {
        "max_level": 5,
        "attack": [6, 8, 10, 12, 14],
        "hits": [2, 2, 3, 3, 3],
        "status": {
            "bleed": [[100, 100, 100, 100, 100], [2, 2, 2, 3, 3]],
        },
        "attack_type": "Magic_Attack",
        'buy_value': 999,
        'sell_value': 999,

    },
}
armor_dict = {
    "Iron Plate": {
        "tier": ["common", "rare"],
        "tier mod": {"common": 0, "rare": 2},
        "defense": [2, 5, 8]
    }
}
boots_dict = {
    "Leather Boots": {
        "tier": ["common", "rare"],
        "tier mod": {"common": 0, "rare": 2},
        "defense": [1, 2, 3],
        "speed": [1, 3, 5]
    }
}
