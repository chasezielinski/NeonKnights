import copy
import random
import numpy as np
import pygame
import names

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
BASE_STATS = {
    "FIGHTER_BASE_STATS": {'FIGHTER_BASE_HP': 100,
                           'FIGHTER_BASE_MP': 10,
                           'FIGHTER_BASE_STRENGTH': 10,
                           'FIGHTER_BASE_DEFENSE': 10,
                           'FIGHTER_BASE_MAGIC': 10,
                           'FIGHTER_BASE_SPIRIT': 10,
                           'FIGHTER_BASE_SPEED': 10,
                           'FIGHTER_BASE_LUCK': 10,
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


def character_initial(persist, char, char_class):
    if char_class == "Fighter":
        persist['characters'][char].equipment["Weapon"] = Weapon("Coder Sword", 1)
        persist['characters'][char].equipment["Armor"] = Armor("Iron Plate", "common", '1')
        persist['characters'][char].equipment["Boots"] = Boots("Leather Boots", "common", '1')


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

REGION_BIOMES = ["Desert", "Forest", "Valley", "Grasslands", "Badlands", "Tundra",
                 "Savannah", "Rainforest", "Steppe", "Taiga"]

REGION_SHAPES = ["Land-Locked", "Coastal", "Archipelago", "Island", "Plateau",
                 "Lakeside", "Canyon", "River"]

NODE_TYPES = [["Empty", "Town", "Dungeon", "Lone Building", "Encounter"], [30, 15, 10, 10, 40]]

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
    'adept icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'artificer icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'rogue icon': image_load(
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
        'portal_prompt': 'Select a destination point and click "CONSTRUCT PORTAL to confirm. Cost: 2 Elixirs, 2 Chargers',
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
    'slot positions': {
        0: (X * 80 / 100, Y * 1 / 100),
        1: (X * 80 / 100, Y * 10 / 100),
        2: (X * 80 / 100, Y * 19 / 100),
        3: (X * 80 / 100, Y * 28 / 100),
        4: (X * 80 / 100, Y * 37 / 100),
        5: (X * 80 / 100, Y * 46 / 100),
        6: (X * 80 / 100, Y * 55 / 100),
        7: (X * 80 / 100, Y * 64 / 100),
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
    'action slot sprites': [image_load(
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
    'attack action': [0],
    'attack action weights': [1],
    'skill action': [1],
    'skill action weights': [1],
    'item action': [2],
    'item action weights': [1],
    'defend action': [3],
    'defend action weights': [1],
    'no action': [4, 5, 6, 7, 8, 9, 10, 11],
    'no action weights': [8, 1, 1, 1, 16, 1, 1, 1],
    'animation speed': 2000,
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


class PartyAbilityManager(object):
    def __init__(self):
        self.charger_travel = True  # can use charges instead of supplies **** NOT WORKING ****
        self.success_boost = True  # boost success rate for any choice **** NOT WORKING ****
        self.always_avoid_option = True  # always have an option to avoid event **** NOT WORKING ****
        self.create_portal = True  # create an edge using many resources
        self.less_empty_nodes = True  # less empty nodes spawn
        self.no_empty_nodes = True  # no empty nodes spawn
        self.path_vision = True  # see all paths in region
        self.static_path = True  # false = paths only visible when hovering over node
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


class PlayerCharacter(object):
    def __init__(self, char_class, name="bob"):
        char_class_upper = char_class.upper()
        self.attack_type = "Attack"
        self.name = name
        self.base_class = self.current_class = char_class
        self.hp = self.max_hp = self.base_hp = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_HP"]
        self.mp = self.max_mp = self.base_mp = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_MP"]
        self.strength = self.base_strength = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_STRENGTH"]
        self.defense = self.base_defense = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_DEFENSE"]
        self.magic = self.base_magic = BASE_STATS[char_class_upper + "_BASE_STATS"][char_class_upper + "_BASE_MAGIC"]
        self.spirit = self.base_spirit = BASE_STATS[char_class_upper + "_BASE_STATS"][char_class_upper + "_BASE_SPIRIT"]
        self.speed = self.base_speed = BASE_STATS[char_class_upper + "_BASE_STATS"][char_class_upper + "_BASE_SPEED"]
        self.luck = self.base_luck = BASE_STATS[char_class_upper + "_BASE_STATS"][char_class_upper + "_BASE_LUCK"]
        self.equipment_options = self.base_equipment_options = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_EQUIPMENT_OPTIONS"]
        self.base_attack_type = self.attack_type = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_ATTACK_TYPE"]
        self.equipment = {}
        self.techniques = self.base_techniques = BASE_STATS[char_class_upper + "_BASE_STATS"][
            char_class_upper + "_BASE_TECHNIQUES"]
        self.crit_rate = self.base_crit_rate = 1
        self.crit_damage = self.base_crit_damage = 1
        self.level = 1
        self.exp = 0
        self.skill_points = 0


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
               "bleed",  # hp loss based on remaining hp *** NOT WORKING
               "toxic",  # hp loss based on missing hp *** NOT WORKING
               "burn",  # flat hp loss *** NOT WORKING
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
               "gentle"]  # crit damage down *** NOT WORKING

STATUS_LIST_EOT = {
    "bleed": {'effect': 5, 'animation': 'none', },  # hp loss based on remaining hp *** NOT WORKING
    "toxic": {'effect': 5, 'animation': 'none', },  # hp loss based on missing hp *** NOT WORKING
    "burn": {'effect': 5, 'animation': 'none', },  # flat hp loss *** NOT WORKING]
}

bestiary = {
    "Slime": {'base_hp': [100, 120, 140, 160, 190, 220, 250, 300],
              'base_mp': [100, 110, 120, 130, 140, 150, 160, 180],
              'base_attack': [10, 12, 14, 16, 18, 20, 22, 28],
              'base_magic': [10, 12, 14, 16, 18, 20, 22, 28],
              'base_defense': [10, 12, 14, 16, 18, 20, 22, 28],
              'base_spirit': [10, 12, 14, 16, 18, 20, 22, 28],
              'base_luck': [10, 12, 14, 16, 18, 20, 22, 28],
              'base_speed': [10, 12, 14, 16, 18, 20, 22, 28],
              'exp_reward': [10, 12, 14, 16, 18, 20, 22, 28],
              'gold_reward': [20, 25, 30, 35, 40, 45, 50, 60],
              'supply_reward': [(0, 1), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 2)],
              'elixir_reward': [(0, 1), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 2)],
              'charger_reward': [(0, 1), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 2)],
              'crit_rate': [1, 1, 1, 1, 1, 1.1, 1.1, 1.1],
              'crit_damage': [1, 1, 1, 1, 1, 1, 1, 1],
              'item_reward': [['none', 'common', 'rare'], [60, 37, 3]],
              'attack_type': "Attack",
              'regions': {"Desert": True, "Forest": True, "Valley": True, "Grasslands": True, "Badlands": True,
                          "Tundra": True, "Savannah": True, "Rainforest": True, "Steppe": True, "Taiga": True},
              'sprites': [image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                     r"\Enemy\Slime\Slime128p1.png"),
                          image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                     r"\Enemy\Slime\Slime128p2.png"),
                          image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                     r"\Enemy\Slime\Slime128p3.png"),
                          image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                     r"\Enemy\Slime\Slime128p4.png")],
              'idle': [0, 1],  # frames of sprites associated with idle state
              'idle weights': [3, 1],  # time weights for idle frames
              'idle speed': 1000,  # ms to complete idle cycle
              'attack': [2],  # frames of sprites associated with attack state
              'cast': [3],  # frames of sprites associated with cast state
              'hit': [2],  # frames of sprites associated with hit state
              'miss': [3],  # frames of sprites associated with miss state
              'ai': {'ai_type': 'simple',
                     'actions': [["Attack", "Attack"], ["Skill", "Slime Ball"]],
                     'weights': [50, 50],
                     'target': 'random', }
              },
}
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

    }
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
