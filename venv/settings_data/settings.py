import copy
import math
import random
import numpy as np
import pygame
import names
import pytweening
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
MAX_NAME_LENGTH = 12

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

FIGHTER_LEFT_TREE = ["Brute",
                     [[0, 1, "Skill_1", 1, {"Name": "Skill_1",
                                            "Ability_Type": "Ability",
                                            "Description": "This is a skill. You can unlock it by clicking here, "
                                                           "if you have sufficient skill points.",
                                            "Cost": "1 Skill Point"}],
                      [0, 1, "Skill_2", 1, {"Name": "Skill_2",
                                            "Ability_Type": "Ability",
                                            "Description": "This is a skill. You can unlock it by clicking here, "
                                                           "if you have sufficient skill points.",
                                            "Cost": "1 Skill Point"}],
                      [1, 2, "Skill_3", 1, {"Name": "Skill_3",
                                            "Ability_Type": "Ability",
                                            "Description": "This is a skill. You can unlock it by clicking here, "
                                                           "if you have sufficient skill points.",
                                            "Cost": "1 Skill Point"}]]]

FIGHTER_CENTER_TREE = ["Knight",
                       [[0, 1, "Skill_1", 1, {"Name": "Skill_1",
                                              "Ability_Type": "Ability",
                                              "Description": "This is a skill. You can unlock it by clicking here, "
                                                             "if you have sufficient skill points.",
                                              "Cost": "1 Skill Point"}],
                        [0, 1, "Skill_2", 1, {"Name": "Skill_2",
                                              "Ability_Type": "Ability",
                                              "Description": "This is a skill. You can unlock it by clicking here, "
                                                             "if you have sufficient skill points.",
                                              "Cost": "1 Skill Point"}],
                        [1, 2, "Skill_3", 1, {"Name": "Skill_3",
                                              "Ability_Type": "Ability",
                                              "Description": "This is a skill. You can unlock it by clicking here, "
                                                             "if you have sufficient skill points.",
                                              "Cost": "1 Skill Point"}]]]

FIGHTER_RIGHT_TREE = ["Paladin",
                      [[0, 1, "Skill_1", 1, {"Name": "Skill_1",
                                             "Ability_Type": "Ability",
                                             "Description": "This is a skill. You can unlock it by clicking here, "
                                                            "if you have sufficient skill points.",
                                             "Cost": "1 Skill Point"}],
                       [0, 1, "Skill_2", 1, {"Name": "Skill_2",
                                             "Ability_Type": "Ability",
                                             "Description": "This is a skill. You can unlock it by clicking here, "
                                                            "if you have sufficient skill points.",
                                             "Cost": "1 Skill Point"}],
                       [1, 2, "Skill_3", 1, {"Name": "Skill_3",
                                             "Ability_Type": "Ability",
                                             "Description": "This is a skill. You can unlock it by clicking here, "
                                                            "if you have sufficient skill points.",
                                             "Cost": "1 Skill Point"}]]]


class TreeNode(object):
    def __init__(self, parent, prerequisite, branch, skill, cost=1, info=None):
        self.parent = parent
        self.prerequisite = prerequisite
        self.visible = False
        self.purchased = False
        self.hover = False
        self.branch = branch
        self.skill = skill
        self.cost = cost
        self.info = info
        self.order = 0
        self.width = 23
        self.y_pos = Y * (8 * (self.branch - 1)) / 100
        self.height = Y * 6 / 100
        self.x_pos = 0
        self.rect = [0, 0, 10, 10]
        self.text = [0, 0, 10, 10]
        self.player = self.parent.parent

    def update(self, dt):
        if self.parent.points >= self.prerequisite:
            self.visible = True
        if self.parent.structure[self.branch - 1] == 1:
            self.width = X * 23 / 100
            self.x_pos = 0
        elif self.parent.structure[self.branch - 1] == 2:
            self.width = X * 11 / 100
            self.x_pos = self.order * 12
        elif self.parent.structure[self.branch - 1] == 3:
            self.width = X * 7 / 100
            self.x_pos = self.order * 8

    def draw(self, surface, pos):
        self.rect = [pos[0] + (X * self.x_pos) / 100, self.y_pos + pos[1], self.width, self.height]
        self.text = [pos[0] + (X * self.x_pos + 2) / 100, self.y_pos + Y * 1.5 / 100 + pos[1], self.width, self.height]
        color = (40, 40, 40)
        if self.hover and self.visible and not self.purchased:
            color = (80, 80, 80)
        elif self.purchased:
            color = (80, 80, 120)
        if self.visible:
            pygame.draw.rect(surface, color, self.rect, border_radius=4)
            tw(surface, self.skill.center(int(self.width / 10) - (2 + len(self.skill))), SELECTED_COLOR, self.text,
               DETAIL_FONT)
        else:
            pygame.draw.rect(surface, (20, 20, 20), self.rect, border_radius=4)
            tw(surface, self.skill.center(int(self.width / 10) - (2 + len(self.skill))), TEXT_COLOR, self.text,
               DETAIL_FONT)

    def handle_action(self, action):
        if action == "mouse_move":
            self.hover = False
            if click_check(self.rect):
                self.hover = True
        elif action == "click":
            if click_check(self.rect) and not self.purchased and self.player.skill_points > self.cost and \
                    self.parent.points >= self.prerequisite:
                self.player.skill_points -= self.cost
                self.parent.points += self.cost
                self.purchased = True


class SkillTree(object):
    def __init__(self, character_class, tree, parent):
        self.character_class = character_class
        self.tree = tree
        self.parent = parent
        self.points = 0
        self.skill_nodes = []
        self.node_third_rect = []
        self.third_offset = None
        self.node_half_rect = []
        self.half_index = None
        self.node_rect = []
        self.y_offset = None
        self.structure = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.name = eval(self.character_class.upper() + "_" + self.tree.upper() + "_TREE")[0]
        for skill in eval(self.character_class.upper() + "_" + self.tree.upper() + "_TREE")[1]:
            self.skill_nodes.append(TreeNode(self, skill[0], skill[1], skill[2], skill[3], skill[4]))

    def update(self, dt):
        for branch in range(len(self.structure)):
            self.structure[branch] = 0
            for node in self.skill_nodes:
                if node.branch == branch + 1:
                    node.order = self.structure[branch]
                    self.structure[branch] += 1
        for node in self.skill_nodes:
            node.update(dt)

    def draw(self, surface, pos):
        tw(surface, (self.name + ": " + str(self.points)).center(18 - len(self.name)), TEXT_COLOR,
           [pos[0], pos[1] - (Y * 7 / 100), (X * 23 / 100), (Y * 7 / 100)], HEADING_FONT)
        for node in self.skill_nodes:
            node.draw(surface, pos)

    def handle_action(self, action):
        for node in self.skill_nodes:
            node.handle_action(action)


def character_initial(char, char_class):
    if char_class == "Fighter":
        char.equipment["Weapon"] = equipment_builder(equipment_type="Weapon")
        char.equipment["Armor"] = equipment_builder(equipment_type="Armor")
        char.equipment["Boots"] = equipment_builder(equipment_type="Boots")
        char.equipment["Helm"] = equipment_builder(equipment_type="Helm")
        char.equipment["Shield"] = equipment_builder(equipment_type="Shield")


def random_name():
    return names.get_last_name()


# Character Select


def image_load(path):
    image = pygame.image.load(path)
    image.set_colorkey(COLOR_KEY)
    return image


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: (filename)")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them aas a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey)


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
    "Savannah": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Savannah_Card_480p_1.png"),
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

UNEXPLORED_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet13.png")]

EXPLORED_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored13.png")]

EXIT_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node13.png")]

EVENT_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p8.png")]

DUNGEON_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p8.png")]

SHOP_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p8.png")]

ENCOUNTER_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p8.png")]

BOSS_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p8.png")]

Party_Marker = [
    [pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker1.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker2.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker3.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker4.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker5.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker6.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker7.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker8.png")],
    [65, 65, 65, 65, 65, 65, 65, 65]]


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
    def __init__(self, parent, name, supplies, elixirs, chargers, items, characters):
        self.parent = parent
        self.name = name
        self.name_rect = [X * 10 / 100, Y * 14 / 100, X * 75 / 100, Y * 7 / 100]
        self.supplies = supplies
        self.elixirs = elixirs
        self.chargers = chargers
        self.items = items
        self.characters = characters
        self.bg_1_rect = [X * 8 / 100, Y * 11 / 100, X * 76 / 100, Y * 85 / 100]
        self.bg_2_rect = [X * 8.5 / 100, Y * 12 / 100, X * 75 / 100, Y * 83 / 100]
        self.item_rects = [[X * 10 / 100, Y * 30 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 37 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 44 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 51 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 58 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 65 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 73 / 100, X * 20 / 100, Y * 7 / 100],
                           [X * 10 / 100, Y * 80 / 100, X * 20 / 100, Y * 7 / 100]]
        self.price_rects = [[X * 30 / 100, Y * 30 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 37 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 44 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 51 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 58 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 65 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 73 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 30 / 100, Y * 80 / 100, X * 12 / 100, Y * 7 / 100]]
        self.stock_rects = [[X * 42 / 100, Y * 30 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 37 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 44 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 51 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 58 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 65 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 73 / 100, X * 12 / 100, Y * 7 / 100],
                            [X * 42 / 100, Y * 80 / 100, X * 12 / 100, Y * 7 / 100]]
        self.price_rect = [X * 30 / 100, Y * 23 / 100, X * 12 / 100, Y * 7 / 100]
        self.stock_rect = [X * 42 / 100, Y * 23 / 100, X * 12 / 100, Y * 7 / 100]
        self.shop_inventory = []
        self.shop_index = -1
        self.shop_display_index = 0
        self.relative_index = -1

    def update(self, dt):
        inventory = []
        if self.supplies < 0:
            self.supplies = 0
        inventory.append(["supply", 3, self.supplies, 'common'])
        if self.elixirs < 0:
            self.elixirs = 0
        inventory.append(["elixir", 3, self.elixirs, 'common'])
        if self.chargers < 0:
            self.chargers = 0
        inventory.append(["charger", 3, self.chargers, 'common'])
        for item in self.items:
            inventory.append([item.name, item.buy_value, 1, 'item'])
        self.shop_inventory = inventory

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), self.bg_1_rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=8)
        tw(surface, self.name.rjust(25 - len(self.name)), TEXT_COLOR, self.name_rect, HEADING_FONT)
        tw(surface, "price", TEXT_COLOR, self.price_rect, TEXT_FONT)
        tw(surface, "stock", TEXT_COLOR, self.stock_rect, TEXT_FONT)
        for i in range(8):
            if len(self.shop_inventory) > i:
                color = TEXT_COLOR
                if i == self.relative_index:
                    color = SELECTED_COLOR
                tw(surface, self.shop_inventory[i + self.shop_display_index][0], color, self.item_rects[i], TEXT_FONT)
                tw(surface, str(self.shop_inventory[i + self.shop_display_index][1]), TEXT_COLOR, self.price_rects[i],
                   TEXT_FONT)
                tw(surface, str(self.shop_inventory[i + self.shop_display_index][2]), TEXT_COLOR, self.stock_rects[i],
                   TEXT_FONT)

    def handle_action(self, action):
        if action == "mouse_move":
            print((int(100 * pygame.mouse.get_pos()[0] / X), int(100 * pygame.mouse.get_pos()[1] / Y)))
            for i in range(8):
                if len(self.shop_inventory) > i:
                    if click_check(self.item_rects[i]):
                        self.relative_index = i
                        self.shop_index = self.relative_index + self.shop_display_index
                        break
            else:
                self.relative_index = -1
        elif action == "escape":
            self.parent.parent.state = "Browse"
        elif action == "click":
            for i in range(8):
                if len(self.shop_inventory) > i:
                    if click_check(self.item_rects[i]):
                        self.buy()
                        break

    def buy(self):
        if self.shop_inventory[self.shop_index][2] > 0 and self.parent.parent.persist['gold'] > \
                self.shop_inventory[self.shop_index][1]:
            self.parent.parent.persist['gold'] -= self.shop_inventory[self.shop_index][1]
            if self.shop_index == 0:
                self.parent.parent.persist['supplies'] += 1
                self.supplies -= 1
            elif self.shop_index == 1:
                self.parent.parent.persist['elixirs'] += 1
                self.elixirs -= 1
            elif self.shop_index == 2:
                self.parent.parent.persist['chargers'] += 1
                self.chargers -= 1
            elif self.shop_inventory[self.shop_index][3] == 'item':
                self.parent.parent.persist['inventory'].append(eval(self.items[self.shop_index - 3].name)())
                del self.shop_inventory[self.shop_index]
                del self.items[self.shop_index - 3]

    def sell(self):
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
            pass
        elif self.state == "Delay":
            if self.timer == 0:
                self.state = self.next_state
        elif self.state == "Reward":
            self.reward()
        elif self.state == "Exit":
            self.parent.event = shop_builder(self.parent)
            self.parent.parent.state = "Browse"
        elif self.state == "Battle":
            self.battle()
        elif self.state == "Shop":
            self.parent.event = shop_builder(self.parent)

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), self.bg_1_rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=8)
        if self.state == "Prompt":
            tw(surface, self.prompt, TEXT_COLOR, self.prompt_rect, TEXT_FONT)
            for index, option in enumerate(self.options):
                color = TEXT_COLOR
                if index == self.option_index:
                    color = SELECTED_COLOR
                tw(surface, str(index+1) + ". " + option[0], color, [self.option_rect[0], self.option_rect[1] +
                                                              (index * Y * 5 / 100), self.option_rect[2],
                                                              self.option_rect[3]], TEXT_FONT)

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

        elif action == "mouse_move":
            self.option_index = -1
            if len(self.options) > 0:
                for index, option in enumerate(self.options):
                    if click_check([self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                    self.option_rect[2], self.option_rect[3]]):
                        self.option_index = index

        elif action == "return":
            outcome = choose_random_weighted(self.options[self.option_index][1], self.options[self.option_index][2])
            if "state" in outcome.keys():
                setattr(self, "state", outcome["state"])
            if "prompt" in outcome.keys():
                setattr(self, "prompt", outcome["prompt"])
            if "options" in outcome.keys():
                setattr(self, "options", outcome["options"])

        elif action == "1":
            if len(self.options) >= 1:
                self.option_index = 0
                self.handle_action("return")

        elif action == "2":
            if len(self.options) >= 2:
                self.option_index = 1
                self.handle_action("return")

        elif action == "3":
            if len(self.options) >= 3:
                self.option_index = 2
                self.handle_action("return")

        elif action == "4":
            if len(self.options) >= 4:
                self.option_index = 3
                self.handle_action("return")

        elif action == "5":
            if len(self.options) >= 5:
                self.option_index = 4
                self.handle_action("return")

        elif action == "6":
            if len(self.options) >= 6:
                self.option_index = 5
                self.handle_action("return")

        elif action == "7":
            if len(self.options) >= 7:
                self.option_index = 6
                self.handle_action("return")

        elif action == "8":
            if len(self.options) >= 8:
                self.option_index = 7
                self.handle_action("return")

        elif action == "9":
            if len(self.options) >= 9:
                self.option_index = 8
                self.handle_action("return")

        elif action == "down":
            print(self.option_index)
            self.option_index += 1
            if len(self.options) != 0:
                self.option_index %= len(self.options)

        elif action == "up":
            print(self.option_index)
            self.option_index -= 1
            if len(self.options) != 0:
                self.option_index %= len(self.options)
        print(self.option_index)

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
        parameter_dictionary = choose_random_weighted(shop_dictionary["All"] + shop_dictionary[region_type],
                                                      shop_dictionary["All_Weights"] + shop_dictionary[
                                                          region_type + "_Weights"])
        return Event(node, parameter_dictionary)
    elif node.type == "Empty":
        return EmptyNode(node)
    else:
        return EmptyNode(node)
    # prompt, option_1, option_2 = None, option_3 = None, option_4 = None, enemies = None,
    # supply_reward = None, gold_reward = None, elixir_reward = None, charger_reward = None, item_reward = None


def shop_builder(node):
    region_index = node.parent.persist['region_index']
    region_type = node.parent.persist['region_type']
    supplies = random_int(3, 12)
    elixirs = random_int(1, 8)
    chargers = random_int(0, 8)
    item_number = random_int(2, 5)
    equipment_number = random_int(1, 5)
    items = []
    for i in range(item_number):
        items.append(eval(choose_random_weighted(ITEM_LIST["All"] + ITEM_LIST[region_type],
                                                 ITEM_LIST["All_Shop_Weights"] + ITEM_LIST[
                                                     region_type + "_Shop_Weights"]))())
    characters = None
    name_type = choose_random_weighted(["Adjective_Noun", "Name_Noun", "Title_Name_Noun"], [5, 5, 1])
    shop_name = "Name"
    if name_type == "Adjective_Noun":
        shop_name = choose_random(ADJECTIVES) + " " + choose_random(STORE_NAMES)
    elif name_type == "Name_Noun":
        shop_name = random_name() + "'s " + choose_random(STORE_NAMES)
    elif name_type == "Title_Name_Noun":
        shop_name = choose_random(TITLES) + " " + random_name() + "'s " + choose_random(STORE_NAMES)
    return Shop(node, shop_name, supplies, elixirs, chargers, items, characters)


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

shop_dictionary = {
    "All": [
        {"prompt": "A small shop that might have something useful.",
         "options": [["Check it out.", [{"state": "Shop"}], [1]],
                     ["Not interested.", [{"state": "Exit"}], [1]]],
         "enemies": ["Slime", "Slime"]}],
    "All_Weights": [1],
    "Desert": [],
    "Desert_Weights": [], }

P_NODE_TYPES = [10, 15, 20, 60]

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
            'hp': [X * 10 / 100, Y * 65 / 100, X * 35 / 100, Y * 5 / 100],
            'mp': [X * 10 / 100, Y * 70 / 100, X * 35 / 100, Y * 5 / 100],
            'strength': [X * 10 / 100, Y * 75 / 100, X * 50 / 100, Y * 5 / 100],
            'magic': [X * 10 / 100, Y * 80 / 100, X * 35 / 100, Y * 5 / 100],
            'defense': [X * 30 / 100, Y * 75 / 100, X * 35 / 100, Y * 5 / 100],
            'spirit': [X * 30 / 100, Y * 80 / 100, X * 35 / 100, Y * 5 / 100],
            'speed': [X * 10 / 100, Y * 85 / 100, X * 35 / 100, Y * 5 / 100],
            'luck': [X * 30 / 100, Y * 85 / 100, X * 35 / 100, Y * 5 / 100],
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

MUSIC = {'Title': r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\music\title.oga",
         'Desert': {'constant': pygame.mixer.Sound(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\music\Desert_Layer\constant-Constant.wav"),
                    'shop': pygame.mixer.Sound(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\music\Desert_Layer\shop-Shop.wav"),
                    'map': pygame.mixer.Sound(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\music\Desert_Layer\map-Map.wav"),
                    'battle': pygame.mixer.Sound(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\music\Desert_Layer\battle-Battle.wav"),
                    }
         }

SOUND_EFFECTS = {'Toggle_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\397604__nightflame__menu-fx-01.wav"),
        'Toggle_2': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\503340__tahutoa__clicky-accept-menu-sound.wav"),
        'Confirm_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\403019__inspectorj__ui-confirmation-alert-c4.wav"),
        'Blast_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\blast_1.wav"),
        'Attack_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\attack_1.wav"),
    'Menu': {
        'Toggle_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\397604__nightflame__menu-fx-01.wav"),
        'Toggle_2': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\503340__tahutoa__clicky-accept-menu-sound.wav"),
        'Confirm_1': pygame.mixer.Sound(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sfx\403019__inspectorj__ui-confirmation-alert-c4.wav"),
    },
}


class SFXManager(object):
    def __init__(self):
        self.sfx = []

    def schedule_sfx(self, sound, delay=0, play=1):
        self.sfx.append({'sound': sound, 'delay': delay, 'delay_reset': delay, 'play': play})

    def update(self, dt):
        for sfx in self.sfx:
            sfx['delay'] -= dt
            if sfx['delay'] <= 0:
                if sfx['sound'] in list(SOUND_EFFECTS.keys()):
                    SOUND_EFFECTS[sfx['sound']].play()
                sfx['play'] -= 1
                if sfx['play'] <= 0:
                    self.sfx.remove(sfx)
                else:
                    sfx['delay'] = sfx['delay_reset']


class Effect(pygame.sprite.Sprite):
    def __init__(self, sprites, frames, frame_times, delay, animation_type, pos):
        super().__init__()
        self.sprites = sprites[0]
        self.frames = frames
        self.frame_times = frame_times[0]
        self.delay = delay
        self.animation_type = animation_type
        self.timer = frame_times[0][0]
        self.frame_index = 0
        self.image = self.sprites[self.frames[0]]
        self.pos = pos
        self.state = "Hidden"

    def update(self, dt):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        if self.state == "Hidden":
            self.delay -= dt
            if self.delay <= 0:
                self.state = "Display"
        elif self.state == "Display":
            self.timer -= dt
            if self.timer <= 0:
                self.frame_index += 1
                if self.frame_index == len(self.frames):
                    self.state = "Done"
                else:
                    self.image = self.sprites[self.frames[self.frame_index]]
                    self.timer = self.frame_times[self.frame_index]

    def draw(self, surface):
        if self.state == "Display":
            surface.blit(self.image, self.pos)


class FXManager(object):
    def __init__(self):
        self.effects = pygame.sprite.Group()

    def update(self, dt):
        for effect in self.effects.sprites():
            effect.update(dt)
            if effect.state == "Done":
                effect.kill()

    def draw(self, surface):
        self.effects.draw(surface)

    def add_effect(self, sprites, frames, frame_times, delay, animation_type, pos=(0,0)):
        self.effects.add(Effect(sprites, frames, frame_times, delay, animation_type, pos))


class MusicManager(object):
    def __init__(self):
        self.channels = {}
        self.region = None
        self.mix_state = None
        self.game_state = None
        self.region_state = None
        self.fade_event = []
        self.music_schedule = []
        self.state = 'music'
        self.constant = pygame.mixer.Channel(0)
        self.map = pygame.mixer.Channel(1)
        self.shop = pygame.mixer.Channel(2)
        self.battle = pygame.mixer.Channel(3)
        self.event = pygame.mixer.Channel(4)
        self.dungeon = pygame.mixer.Channel(5)

    def update(self, dt, parent=None):
        if self.state is 'music':
            if not pygame.mixer.music.get_busy():
                if self.music_schedule:
                    self.music_schedule[0][0] -= dt
                    if self.music_schedule[0][0] <= 0:
                        pygame.mixer.music.load(self.music_schedule[0][1])
                        pygame.mixer.music.play(-1, fade_ms=self.music_schedule[0][2])
                        del self.music_schedule[0]
            if parent is not None:
                self.music_schedule.clear()
                self.state = 'layer'
                self.fade_out()
        elif self.state is 'layer':
            print('here')
            if self.region is not parent.persist['region_type']:
                self.layer_fade_out()
                self.set_region(parent.persist['region_type'])
            if parent.state == "Event":
                if isinstance(parent.party.node.event, Shop) and self.region_state != "Shop":
                    self.fade_to_shop()
                else:
                    self.fade_to_event()
            elif parent.state == "Browse" and self.region_state != "Browse":
                self.fade_to_map()

    def fade_to_shop(self):
        self.region_state = "Shop"
        self.constant.set_volume(1)
        self.map.set_volume(0)
        self.shop.set_volume(1)
        self.battle.set_volume(0)
        self.event.set_volume(0)
        self.dungeon.set_volume(0)

    def fade_to_map(self):
        self.region_state = "Map"
        self.constant.set_volume(1)
        self.map.set_volume(1)
        self.shop.set_volume(0)
        self.battle.set_volume(0)
        self.event.set_volume(0)
        self.dungeon.set_volume(0)

    def fade_to_event(self):
        self.region_state = "Event"
        self.constant.set_volume(1)
        self.map.set_volume(0)
        self.shop.set_volume(1)
        self.battle.set_volume(0)
        self.event.set_volume(0)
        self.dungeon.set_volume(0)

    def layer_fade_out(self):
        if self.constant.get_busy():
            self.constant.fadeout(2000)
        if self.map.get_busy():
            self.map.fadeout(2000)
        if self.shop.get_busy():
            self.shop.fadeout(2000)
        if self.battle.get_busy():
            self.battle.fadeout(2000)
        if self.event.get_busy():
            self.event.fadeout(2000)
        if self.dungeon.get_busy():
            self.dungeon.fadeout(2000)

    def set_region(self, region):
        self.region = region
        self.region_state = "Browse"
        self.constant.play(MUSIC[region]['constant'], -1, fade_ms=2000)
        self.constant.set_volume(1)
        self.map.play(MUSIC[region]['map'], -1, fade_ms=2000)
        self.map.set_volume(1)
        self.shop.play(MUSIC[region]['shop'], -1)
        self.shop.set_volume(0)
        self.battle.play(MUSIC[region]['battle'], -1)
        self.battle.set_volume(0)
        self.event.play(MUSIC[region]['constant'], -1)
        self.event.set_volume(0)
        self.dungeon.play(MUSIC[region]['constant'], -1)
        self.dungeon.set_volume(0)

    def set_state(self, region_state=None, game_state=None):
        if game_state is not None and game_state != self.game_state:
            self.game_state = game_state

    def change_music(self, track, delay=0, fade_ms=2000):
        if track in MUSIC.keys():
            if isinstance(MUSIC[track], str):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(delay)
                    self.music_schedule.append([delay, track, fade_ms])
                else:
                    pygame.mixer.music.load(MUSIC[track])
                    pygame.mixer.music.play(-1, fade_ms=fade_ms)
                    self.mix_state = "Single"
            elif isinstance(MUSIC[track], dict):
                self.channels = MUSIC[track]

    def fade_out(self, delay=2000):
        if self.mix_state == "Single":
            pygame.mixer.music.fadeout(delay)


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


def node_assign_2(parent):
    shops = 0
    n = 0
    n_max = len(parent.nodes.sprites())
    for node in parent.nodes.sprites():
        n += 1
        if node.type == "Shop":
            shops += 1
    if shops < 3 and random_int(0, 100) > (100 - (1.5 * n)):
        node_type = ["Shop"]
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
    def __init__(self):
        self.surface = pygame.Surface((X, Y))
        self.color = (0, 0, 0)
        self.surface.fill(self.color)
        self.alpha = 255
        self.surface.set_alpha(self.alpha)
        self.start = None
        self.timer = None
        self.delay = None
        self.state = "Black"
        self.next_state = "In"

    def update(self, dt):
        if self.delay is not None:
            self.delay -= dt
            if self.delay <= 0:
                self.delay = None
        elif self.timer is not None:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0
            if self.state == "In":
                self.alpha = int(255 * pytweening.easeInSine(self.timer / self.start))
                if self.timer < 0:
                    self.timer = None
                    self.state = "Clear"
            elif self.state == "Out":
                self.alpha = int(255 * pytweening.easeInSine(1 - self.timer / self.start))
                if self.timer < 0:
                    self.timer = None
                    self.state = "Black"
        self.surface.fill(self.color)
        self.surface.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))

    def fade_in(self, time=500, delay=None):
        self.state = "In"
        self.timer = self.start = time
        self.delay = delay

    def fade_out(self, time=500, delay=None):
        self.state = "Out"
        self.timer = self.start = time
        self.delay = delay

    def set_black(self):
        self.alpha = 255
        self.surface.set_alpha(self.alpha)
        self.state = "Black"

    def set_clear(self):
        self.alpha = 0
        self.surface.set_alpha(self.alpha)
        self.state = "Clear"


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
        self.relative_index = 0
        self.display_index = 0
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
            pos = (int(pygame.mouse.get_pos()[0] * 100 / 1280), int(pygame.mouse.get_pos()[1] * 100 / 720))
            print(pos)
            for n, equip_slot in enumerate(self.parent.persist['characters'][self.player_index].equipment_options):
                if click_check(self.equip_rects[n]):
                    self.equip_selection_index = n
                    self.menu_horizontal_index = "Equip"
                    break
            else:
                self.equip_selection_index = -1
                self.menu_horizontal_index = "None"
            for key in REGION_MENUS['equip menu']['inventory rects'].keys():
                if click_check(REGION_MENUS['equip menu']['inventory rects'][key]):
                    self.inventory_selection_index = key + self.display_index
                    self.relative_index = key
                    self.menu_horizontal_index = "Inventory"
                    break
                else:
                    self.inventory_selection_index = -1
        elif action == "tab":
            self.parent.state = "Skill_Tree"
        elif action == "click":
            self.equip_unequip()
            if not click_check(self.bg_1_rect):
                self.parent.state = "Browse"
        elif action == "wheel_up":
            if self.menu_horizontal_index == "Inventory":
                if self.scroll_index > 0:
                    self.scroll_index -= 1
                    self.display_index -= 1
        elif action == "wheel_down":
            if self.menu_horizontal_index == "Inventory":
                if self.scroll_index + 8 < len(self.parent.persist['inventory']):
                    self.scroll_index += 1
                    self.display_index += 1

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
            if not isinstance(item, Equipment):
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
        for key, value in enumerate(REGION_MENUS['equip menu']['Stat_Rects']):
            stat = getattr(self.parent.persist['characters'][self.player_index], value)
            if value == 'hp':
                stat2 = getattr(self.parent.persist['characters'][self.player_index], 'max_hp')
                tw(surface, value + ':' + str(stat).rjust(8 - len(value)) + '/' + str(stat2),
                   TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
            elif value == 'mp':
                stat2 = getattr(self.parent.persist['characters'][self.player_index], 'max_mp')
                tw(surface, value + ':' + str(stat).rjust(9 - len(value)) + '/' + str(stat2),
                   TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
            else:
                tw(surface, value + ':' + str(stat).rjust(12 - len(value)), TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                if value in potential.keys():
                    if value == 'defense' or value == 'spirit' or value == 'luck':
                        if potential[value] < 0:
                            tw(surface, str(potential[value]).rjust(22 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[value])).rjust(22
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                    elif value == 'magic' or value == 'speed':
                        if potential[value] < 0:
                            tw(surface, str(potential[value]).rjust(20 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[value])).rjust(20
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                    elif value == 'strength':
                        if potential[value] < 0:
                            tw(surface, str(potential[value]).rjust(23 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[value])).rjust(23
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)

    def potential_stat(self):
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        potential = {}
        if self.menu_horizontal_index == "Inventory" and self.parent.persist['inventory'] and len(
                self.parent.persist['inventory']) > self.inventory_selection_index >= 0:
            if hasattr(self.parent.persist['inventory'][self.inventory_selection_index], 'slot'):
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
            slot = type(self.parent.persist['inventory'][self.inventory_selection_index]).__name__
            if slot in self.parent.persist['characters'][self.player_index].equipment_options:
                if slot in self.parent.persist['characters'][self.player_index].equipment:
                    self.parent.persist['inventory'].append(
                        copy.deepcopy(self.parent.persist['characters'][self.player_index].equipment[slot]))
                    del (self.parent.persist['characters'][self.player_index].equipment[slot])
                self.parent.persist['characters'][self.player_index].equipment[slot] = copy.deepcopy(
                    self.parent.persist['inventory'][self.inventory_selection_index])
                del self.parent.persist['inventory'][self.inventory_selection_index]
        character_stat_update(self.parent.persist)
        character_ability_update(self.parent.persist)


class SkillTreeMenu(object):
    def __init__(self, parent):
        self.parent = parent
        self.player_index = 0
        self.bg_1_rect = [X * 8 / 100, Y * 11 / 100, X * 76 / 100, Y * 85 / 100]
        self.bg_2_rect = [X * 8.5 / 100, Y * 12 / 100, X * 75 / 100, Y * 83 / 100]
        self.left_pos = (X * 9 / 100, Y * 32 / 100)
        self.center_pos = (X * 35 / 100, Y * 32 / 100)
        self.right_pos = (X * 60 / 100, Y * 32 / 100)
        self.detail = SkillDetail(self)

    def update(self, dt):
        self.parent.persist['characters'][self.player_index].left_tree.update(dt)
        self.parent.persist['characters'][self.player_index].center_tree.update(dt)
        self.parent.persist['characters'][self.player_index].right_tree.update(dt)
        self.detail.update(dt)

    def handle_action(self, action):
        self.parent.persist['characters'][self.player_index].left_tree.handle_action(action)
        self.parent.persist['characters'][self.player_index].center_tree.handle_action(action)
        self.parent.persist['characters'][self.player_index].right_tree.handle_action(action)
        if action == "mouse_move":
            pass
        elif action == "escape":
            self.parent.state = "Browse"
        elif action == "click":
            if not click_check(self.bg_1_rect):
                self.parent.state = "Browse"
        elif action == "wheel_up":
            pass
        elif action == "wheel_down":
            pass
        elif action == "tab":
            self.parent.state = "Equip"

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.bg_1_rect, border_radius=int(X / 128))
        pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=int(X / 128))
        pygame.draw.line(surface, (40, 40, 40), (X * 33.5 / 100, Y * 30 / 100), (X * 33.5 / 100, Y * 90 / 100), 5)
        pygame.draw.line(surface, (40, 40, 40), (X * 59 / 100, Y * 30 / 100), (X * 59 / 100, Y * 90 / 100), 5)
        self.parent.persist['characters'][self.player_index].left_tree.draw(surface, self.left_pos)
        self.parent.persist['characters'][self.player_index].center_tree.draw(surface, self.center_pos)
        self.parent.persist['characters'][self.player_index].right_tree.draw(surface, self.right_pos)
        name = self.parent.persist['characters'][self.player_index].name
        tw(surface, name.center(18 - len(name)), TEXT_COLOR,
           [X * 11 / 100, Y * 16 / 100, (X * 23 / 100), (Y * 7 / 100)],
           TEXT_FONT)
        tw(surface, "Skill Tree".center(18 - len(name)), TEXT_COLOR,
           [X * 35 / 100, Y * 13 / 100, (X * 23 / 100), (Y * 7 / 100)],
           HEADING_FONT)
        self.detail.draw(surface)


class SkillDetail(object):
    def __init__(self, parent):
        self.parent = parent
        self.visible = False
        self.bg_1_rect = self.left_bg_1_rect = [X * 17 / 100, Y * 16 / 100, X * 35 / 100, Y * 70 / 100]
        self.bg_2_rect = self.left_bg_2_rect = [X * 18 / 100, Y * 17 / 100, X * 33 / 100, Y * 68 / 100]
        self.right_bg_1_rect = [X * 59 / 100, Y * 16 / 100, X * 35 / 100, Y * 70 / 100]
        self.right_bg_2_rect = [X * 60 / 100, Y * 17 / 100, X * 33 / 100, Y * 68 / 100]
        self.info = None
        self.name_rect = self.left_name = [X * 19 / 100, Y * 19 / 100, X * 32 / 100, Y * 7 / 100]
        self.ability_type_rect = self.left_type = [X * 19 / 100, Y * 25 / 100, X * 32 / 100, Y * 7 / 100]
        self.description_rect = self.left_description = [X * 19 / 100, Y * 31 / 100, X * 32 / 100, Y * 25 / 100]
        self.cost_rect = self.left_cost = [X * 19 / 100, Y * 80 / 100, X * 32 / 100, Y * 7 / 100]
        self.right_name = [X * 61 / 100, Y * 19 / 100, X * 32 / 100, Y * 7 / 100]
        self.right_type = [X * 61 / 100, Y * 25 / 100, X * 32 / 100, Y * 7 / 100]
        self.right_description = [X * 61 / 100, Y * 31 / 100, X * 32 / 100, Y * 25 / 100]
        self.right_cost = [X * 61 / 100, Y * 80 / 100, X * 32 / 100, Y * 7 / 100]

    def update(self, dt):
        self.visible = False
        for node in self.parent.parent.persist['characters'][self.parent.player_index].left_tree.skill_nodes:
            if node.hover:
                self.visible = True
                self.bg_1_rect = self.right_bg_1_rect
                self.bg_2_rect = self.right_bg_2_rect
                self.name_rect = self.right_name
                self.ability_type_rect = self.right_type
                self.description_rect = self.right_description
                self.cost_rect = self.right_cost
                self.info = node.info
                break
        if not self.visible:
            for node in self.parent.parent.persist['characters'][self.parent.player_index].center_tree.skill_nodes:
                if node.hover:
                    self.visible = True
                    self.bg_1_rect = self.right_bg_1_rect
                    self.bg_2_rect = self.right_bg_2_rect
                    self.name_rect = self.right_name
                    self.ability_type_rect = self.right_type
                    self.description_rect = self.right_description
                    self.cost_rect = self.right_cost
                    self.info = node.info
                    break
        if not self.visible:
            for node in self.parent.parent.persist['characters'][self.parent.player_index].right_tree.skill_nodes:
                if node.hover:
                    self.visible = True
                    self.bg_1_rect = self.left_bg_1_rect
                    self.bg_2_rect = self.left_bg_2_rect
                    self.name_rect = self.left_name
                    self.ability_type_rect = self.left_type
                    self.description_rect = self.left_description
                    self.cost_rect = self.left_cost
                    self.info = node.info
                    break

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, (50, 50, 50), self.bg_1_rect, border_radius=int(X / 128))
            pygame.draw.rect(surface, (0, 0, 0), self.bg_2_rect, border_radius=int(X / 128))
            if self.info is not None:
                for key in self.info.keys():
                    tw(surface, self.info[key], TEXT_COLOR, eval("self." + key.lower() + "_rect"), TEXT_FONT)


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
        self.region_revealed = False  # all region info revealed
        self.locate_shops = False  # see all shops in region
        self.locate_encounters = False  # see all encounters in region
        self.locate_inn = False  # see all inns in region
        self.locate_tavern = False  # see all taverns in region
        self.locate_events = False  # see all events in region
        self.locate_boss = False  # see boss node
        self.locate_dungeons = False  # see all dungeons in region
        self.mp_regen_travel = True  # regen some mp when traveling
        self.boosted_regen_travel = True  # regen more when traveling
        self.conserve_supplies = True  # chance to not use supplies when traveling
        self.fast_travel = True  # can travel to any previously visited node using elixir
        self.fly = True  # can travel to any node, usually just once
        self.fly_charges = 50  # paired to fly
        self.teleport = True  # can travel to any node, using multiple elixirs
        self.scout_vision = True  # can see details of neighboring nodes


def equipment_builder(region_index=None, region_type=None, equipment_type=None, name=None):
    types = ["Weapon", "Armor", "Boots", "Helm", "Shield", "Artifact", "Cape", "Medallion"]
    weights = [5, 5, 5, 5, 4, 4, 4, 4]
    if equipment_type is None:
        equipment_type = choose_random_weighted(types, weights)
    if name is not None:
        if name in eval(equipment_type.upper() + "_DICT").keys():
            dictionary = eval(equipment_type.upper() + "_DICT")[name]
        else:
            return equipment_builder(region_index, region_type, equipment_type)
    else:
        key = choose_random(list(eval(equipment_type.upper() + "_DICT").keys()))
        dictionary = eval(equipment_type.upper() + "_DICT")[key]
    return eval(equipment_type)(dictionary)


WEAPON_DICT = {"Coder Sword": {"name": "Coder Sword", "attack": 20, "energy": True, }, }
ARMOR_DICT = {"Iron Plate": {"name": "Iron Plate", "defense": 10, }, }
BOOTS_DICT = {"Leather Boots": {"name": "Leather Boots", "speed": 5, "defense": 3}, }
HELM_DICT = {"Iron Helm": {"name": "Iron Helm", "defense": 5, "spirit": 5, }, }
CAPE_DICT = {}
SHIELD_DICT = {"Spiked Shield": {"name": "Spiked Shield", "attack": 5, "defense": 5, }, }
MEDALLION_DICT = {}
ARTIFACT_DICT = {}


class Equipment(object):
    def __init__(self, dictionary):
        self.parent = None
        self.buy_value = 0
        self.sell_value = 0
        self.max_hp = 0
        self.max_mp = 0
        self.attack = 0
        self.magic = 0
        self.defense = 0
        self.spirit = 0
        self.speed = 0
        self.luck = 0
        self.crit_rate = 1
        self.crit_damage = 1
        self.level = 1
        self.max_level = 1
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])

    def equip(self, parent):
        self.parent = parent

    def unequip(self):
        self.parent = None

    def player_hit(self, action, damage=None):
        pass

    def ally_hit(self, action, damage=None):
        pass

    def player_action(self, action, damage=None):
        pass

    def player_miss(self, action, damage=None):
        pass

    def player_dodge(self, action, damage=None):
        pass

    def player_ko(self, action, damage=None):
        pass

    def ally_ko(self, action, damage=None):
        pass

    def player_ko_enemy(self, action, damage=None):
        pass

    def ally_ko_enemy(self, action, damage=None):
        pass

    def end_turn(self):
        pass

    def start_turn(self):
        pass


class Weapon(Equipment):
    def __init__(self, dictionary):
        self.energy = False
        super(Weapon, self).__init__(dictionary)
        self.attack = 0
        self.slot = "Weapon"
        self.attack_type = "Attack"
        self.target_type = "Single"
        self.hits = 1
        self.charge = 5
        self.max_charge = 30
        self.use_charge = 10

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


class Armor(Equipment):
    def __init__(self, dictionary):
        super(Armor, self).__init__(dictionary)


class Boots(Equipment):
    def __init__(self, dictionary):
        super(Boots, self).__init__(dictionary)


class Helm(Equipment):
    def __init__(self, dictionary):
        super(Helm, self).__init__(dictionary)


class Shield(Equipment):
    def __init__(self, dictionary):
        super(Shield, self).__init__(dictionary)


class Cape(Equipment):
    def __init__(self, dictionary):
        super(Cape, self).__init__(dictionary)


class Artifact(Equipment):
    def __init__(self, dictionary):
        super(Artifact, self).__init__(dictionary)


class Medallion(Equipment):
    def __init__(self, dictionary):
        super(Medallion, self).__init__(dictionary)


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
                if particle[6] <= 0:
                    tw(surface, str(particle[3]), particle[4], particle[0], TEXT_FONT)
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
                    particles_copy.append(
                        [new_rect, new_velocity, particle[2], particle[3], new_color, particle[5], particle[6]])
                else:
                    particles_copy.append(particle)
            self.particles = particles_copy
        self.delete_particles()

    def update(self, dt):
        if self.particles:
            for particle in self.particles:
                if particle[6] > 0:
                    particle[6] -= dt

    def add_particles(self, x, y, damage, critical=False, velocity=(1, 1), delay=0):
        rect = [x, y, 200, 100]
        f = random_int(1090, 1150) / 1000
        l = random_int(100, 120) / 100
        if (X * 3 / 8) - x < 0:
            velocity = (-X / 100 * velocity[0], (-Y / 720) * l * velocity[1])
            force = (f, 0)
        else:
            velocity = (X / 100 * velocity[0], (-Y / 720) * l * velocity[1])
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
        self.flip_state_on_hit = False
        self.flip_state_on_magic = False
        self.flip_state_on_physical = False
        self.shield_on_hit = 0
        self.ward_on_hit = 0
        self.slot = "None"
        self.parent = parent
        self.action = None
        self.hover = False
        self.selected = False
        self.current_sprite = 0
        self.dazed = 0  # can't use ability
        self.disabled = 0  # can't use attack
        self.stunned = 0  # can't act
        self.perplexed = 0  # can't use item
        self.vigilant = 0  # defense up
        self.smitten = 0
        self.faith = 0  # spirit up
        self.brave = 0  # attack up
        self.calm = 0  # magic up
        self.haste = 0  # extra turn
        self.turns = 0  # num turns
        self.quick = 0  # speed up
        self.lucky = 0  # luck up
        self.focus = 0  # crit rate up
        self.bleed = 5  # dot
        self.toxic = 5  # dot
        self.burn = 5  # dot
        self.curse = 0  # damage bonus
        self.spite = 0  # damage bonus
        self.invincible = 0  # damage immune
        self.shield = 0  # 1/2 damage physical or laser
        self.ward = 0  # 1/2 damage magical or laser
        self.frail = 0  # defense down
        self.terrify = 0  # spirit down
        self.weak = 0  # attack down
        self.distract = 0  # magic down
        self.slow = 0  # speed down
        self.hex = 0  # luck down
        self.dull = 0  # crit rate down
        self.savage = 0  # crit damage up
        self.gentle = 0  # crit damage down
        self.regen = 0  # regen over time
        self.speed = 0
        self.state = "Idle"
        self.action_options = []
        self.attack_action = Attack(self)
        self.battle_action = None
        self.tick_status = ['dazed', 'disabled', 'stunned', 'perplexed', 'vigilant', 'smitten', 'faith', 'brave',
                            'calm', 'haste', 'turns', 'quick', 'lucky', 'focus', 'bleed', 'burn', 'toxic', 'curse',
                            'spite', 'invincible', 'shield', 'ward', 'frail', 'terrify', 'weak', 'distract', 'slow',
                            'hex', 'dull', 'savage', 'gentle', 'regen', 'speed']

    #       self.defend_action = Attack(self)
    #       self.run_action = Attack(self)

    def update(self, dt):
        pass

    def damage(self, damage, action, delay=0):
        if damage == 'miss':
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, damage, delay=delay)
        elif damage == 'effect':
            pass
        elif damage < 0:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, -damage, delay=delay)
            self.hp += -damage
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        elif self.invincible > 0:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, "immune")
        else:
            if action.defend_stat == "defense" or action.defend_stat == "lowest":
                if self.shield > 0:
                    damage /= 2
            if action.defend_stat == "spirit" or action.defend_stat == "lowest":
                if self.ward > 0:
                    damage /= 2
            if self.spite > 0:
                damage += 10
            if self.curse > 0:
                damage *= 2
            damage = int(damage)
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, damage, delay=delay)
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0
        if damage != 'miss':
            if hasattr(action, 'effects'):
                for index, effect in enumerate(action.effects):
                    if random_int(0, 100) <= (action.parent.luck / self.luck) * effect[2]:
                        setattr(self, effect[0], getattr(self, effect[0]) + effect[1])
                        self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                                  effect[0] + '+' + str(effect[1]).rjust(3),
                                                                  delay=(index + 2) * 200)

    #        def call_effects(self):
    #            if self.current_action.target_type == "Single":
    #                if len(self.apply_effects) > 0:
    #                    status = self.apply_effects[0][0]
    #                    turns = self.apply_effects[0][1]
    #                    self.apply_effects = self.apply_effects[1:]
    #                    setattr(getattr(self, self.current_action.target), status, turns +
    #                            getattr(getattr(self, self.current_action.target), status))
    #                    self.damage_particle.add_particles(getattr(self, self.current_action.target).x +
    #                                                       getattr(self, self.current_action.target).rect[2] / 2,
    #                                                       getattr(self, self.current_action.target).y +
    #                                                       getattr(self, self.current_action.target).rect[3] / 2,
    #                                                       status + str(turns).rjust(3))

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

    def flip_state(self):
        pass

    def on_hit(self, action):
        if self.shield_on_hit > 0:
            if action.defend_stat == "defense" or action.defend_stat == "lowest":
                self.shield += self.shield_on_hit
                self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                          'shield +' + str(self.shield_on_hit).rjust(3), delay=100)
        if self.ward_on_hit > 0:
            if action.defend_stat == "spirit" or action.defend_stat == "lowest":
                self.shield += self.ward_on_hit
                self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                          'shield +' + str(self.ward_on_hit).rjust(3), delay=100)
        if self.flip_state_on_hit:
            self.flip_state()
        if self.flip_state_on_magic:
            if action.defend_stat == "defense" or action.defend_stat == "lowest":
                self.flip_state()
        if self.flip_state_on_physical:
            if action.defend_stat == "spirit" or action.defend_stat == "lowest":
                self.flip_state()

    def on_end_turn(self):
        for effect in self.tick_status:
            if getattr(self, effect) > 0:
                damage = None
                if effect == "bleed":
                    damage = int(self.hp * 5 / 100)
                elif effect == "burn":
                    damage = int(self.max_hp * 5 / 100)
                elif effect == "toxic":
                    damage = int((self.max_hp-self.hp) * 5 / 100)
                if damage is not None:
                    self.hp -= damage
                    self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                              damage, delay=500*self.parent.status_particle_index)
                    self.parent.status_particle_index += 1
                setattr(self, effect, getattr(self, effect) - 1)
                if getattr(self, effect) == 0:
                    self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                              effect + " has worn off", delay=500*self.parent.status_particle_index)
                    self.parent.status_particle_index += 1


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
        self.abilities = [KiBlast(self)]
        self.crit_rate = self.base_crit_rate = 1
        self.crit_damage = self.base_crit_damage = 1
        self.level = 1
        self.exp = 0
        self.skill_points = 10
        self.experience_to_level = 0
        self.battle_action = NoActionSelected(self)
        self.left_tree = SkillTree(char_class, "left", self)
        self.center_tree = SkillTree(char_class, "center", self)
        self.right_tree = SkillTree(char_class, "right", self)

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


class DesertWurm(BattleCharacter):
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
        self.hp = self.max_hp = [500, 700, 1000, 1400, 1900, 2500, 3100, 3700][region_index]
        self.mp = self.max_mp = [100, 110, 120, 130, 140, 150, 160, 180][region_index]
        self.strength = [20, 25, 30, 35, 40, 45, 50, 60][region_index]
        self.magic = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.defense = [20, 25, 30, 35, 40, 45, 50, 60][region_index]
        self.spirit = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.luck = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.speed = [10, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.crit_rate = [1, 1, 1, 1, 1, 1.1, 1.1, 1.1][region_index]
        self.crit_damage = [1, 1, 1, 1, 1, 1, 1, 1][region_index]
        self.exp_reward = [200, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.supply_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.elixir_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.charger_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.gold_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index],
                                      [10, 12, 14, 16, 18, 20, 22, 24][region_index])
        self.action_options = []
        self.item_reward = self.reward(region_index)
        self.state = "Main" # "Burrow", "Hidden"

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

        self.action_options = []
        if self.state == "Main":
            self.action_options = [Attack(self), SandBreath(self), Impale(self), Burrow(self), Bolster(self),
                                       DesertWrath(self)]

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

    def flip_state(self, state):
        self.action_options.clear()
        if state == "Main":
            self.action_options = [Attack(self), SandBreath(self), Impale(self), Burrow(self), Bolster(self),
                                       DesertWrath(self)]
            self.state = "Main"
        elif state == "Burrow":
            self.action_options = [TailSweep(self)]
            self.state = "Burrow"
        elif state == "Hidden":
            self.action_options = [Emerge(self)]
            self.state = "Hidden"

    def give_options(self):
        options = []
#        if hasattr(self, 'action'):
#            if getattr(self.action, 'name', "None") != "None":
#                return [(self.slot, "None", ["None"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]
#        for action in self.action_options:
#            if action.is_usable():
#                action_outcomes = action.expected_value()
#                for i in range(len(action_outcomes)):
#                    options.append(action_outcomes[i])
#        if options:
#            return options
#        else:
#            return [(self.slot, "None", ["None"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]


class BattleOverlay(object):
    def __init__(self, parent):
        # point to parent and persist dictionary
        self.skill_display_index = 0
        self.skill_relative = -1
        self.skill_index = -1
        self.parent = parent
        # target reticle flash variables
        self.reticle_color = None
        self.target_color = (255, 180, 180)
        self.target_speed = 500
        self.target_time = 0
        self.target_direction = 1
        self.item_index = -1
        self.item_display_index = 0
        self.item_relative = -1

    def handle_action(self, action):
        if self.parent.turn_sub_state == "Item":
            if action == "mouse_move":
                for key in range(5):
                    if click_check(BATTLE_MENUS['item_menu_rects'][key]):
                        self.item_relative = key
                        self.item_index = key + self.item_display_index
                        break
                    else:
                        self.item_relative = -1
                        self.item_index = -1
            elif action == "click":
                if self.item_index >= 0:
                    self.parent.selected_action = self.parent.persist['inventory'][self.item_index]
                    self.parent.turn_sub_state = "Target"
                else:
                    self.parent.turn_sub_state = "Browse"
            elif action == "up":
                if self.item_relative < 0 or self.item_relative > 4:
                    self.item_relative = 0
                if self.item_relative == 0 and self.item_display_index > 0:
                    self.item_display_index -= 1
                elif self.item_relative > 0:
                    self.item_relative -= 1
                self.item_index = self.item_relative + self.item_display_index
            elif action == "down":
                if self.item_relative < 0 or self.item_relative > 4:
                    self.item_relative = 0
                if self.item_relative == 4 and self.item_index < len(self.parent.persist['inventory']) - 1:
                    self.item_display_index += 1
                elif self.item_relative < 4:
                    self.item_relative += 1
                self.item_index = self.item_relative + self.item_display_index
            elif action == "backspace":
                pass
            elif action == "return":
                pass

        elif self.parent.turn_sub_state == "Skill":
            if action == "mouse_move":
                for key in range(5):
                    if click_check(BATTLE_MENUS['skill_menu_rects'][key]):
                        self.skill_relative = key
                        self.skill_index = key + self.skill_display_index
                        break
                    else:
                        self.skill_relative = -1
                        self.skill_index = -1
            elif action == "click":
                if self.skill_index >= 0:
                    self.parent.selected_action = self.parent.player_index.abilities[self.skill_index]
                    self.parent.turn_sub_state = "Target"
                else:
                    self.parent.turn_sub_state = "Browse"
            elif action == "up":
                if self.skill_relative < 0 or self.skill_relative > 4:
                    self.skill_relative = 0
                if self.skill_relative == 0 and self.skill_display_index > 0:
                    self.skill_display_index -= 1
                elif self.skill_relative > 0:
                    self.skill_relative -= 1
                self.skill_index = self.skill_relative + self.skill_display_index
            elif action == "down":
                if self.skill_relative < 0 or self.skill_relative > 4:
                    self.skill_relative = 0
                if self.skill_relative == 4 and self.skill_index < len(self.parent.player_index.abilities) - 1:
                    self.skill_display_index += 1
                elif self.skill_relative < 4:
                    self.skill_relative += 1
                self.skill_index = self.skill_relative + self.skill_display_index
            elif action == "backspace":
                pass
            elif action == "return":
                pass

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
                    option_text = option
                    if option == 'Attack':
                        if "Weapon" in self.parent.player_index.equipment.keys():
                            if self.parent.player_index.equipment["Weapon"].energy:
                                if self.parent.player_index.equipment["Weapon"].charge < \
                                        self.parent.player_index.equipment["Weapon"].use_charge:
                                    option_text = "Recharge"
                    color = TEXT_COLOR
                    if i == self.parent.action_type_index:
                        color = SELECTED_COLOR
                    tw(surface, option_text, color, BATTLE_MENUS['move_top_menu_rects'][option], TEXT_FONT)
                if self.parent.turn_sub_state == "Item":
                    for key in range(5):
                        if key+self.item_display_index + 1 > len(self.parent.persist['inventory']):
                            color = (50, 50, 50)
                            if key == self.item_relative:
                                color = (100, 100, 100)
                            tw(surface, "-".rjust(5), color, BATTLE_MENUS['item_menu_rects'][key], TEXT_FONT)
                        else:
                            color = TEXT_COLOR
                            if key == self.item_relative:
                                color = SELECTED_COLOR
                            tw(surface, self.parent.persist['inventory'][key+self.item_display_index].name, color,
                               BATTLE_MENUS['item_menu_rects'][key], TEXT_FONT)
                if self.parent.turn_sub_state == "Skill":
                    for key in range(5):
                        if key + self.skill_display_index + 1 > len(self.parent.player_index.abilities):
                            color = (50, 50, 50)
                            if key == self.skill_relative:
                                color = (100, 100, 100)
                            tw(surface, "-".rjust(5), color, BATTLE_MENUS['item_menu_rects'][key], TEXT_FONT)
                        else:
                            color = TEXT_COLOR
                            if key == self.skill_relative:
                                color = SELECTED_COLOR
                            tw(surface, self.parent.player_index.abilities[key + self.skill_display_index].name, color,
                               BATTLE_MENUS['item_menu_rects'][key], TEXT_FONT)

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
        if self.parent is not None:
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

    def target_set(self, source, battle_character):
        pass

    def cancel(self):
        self.kill()


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

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.kill()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Recharge(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)

    def is_usable(self):
        if self.parent.parent.persist['chargers'] > 0:
            return True

    def do_action(self):
        self.parent.equipment['Weapon'].charge = self.parent.equipment['Weapon'].max_charge
        self.parent.parent.persist['chargers'] -= 1
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
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
            self.parent.parent.persist['SFX'].schedule_sfx('Attack_1')
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class KiBlast(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.parent = parent
        self.target_type = "Team"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 40
        self.name = "Ki Blast"
        self.action_type = "Ability"
        self.animation_sprites = SpriteSheet(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\attack_all_enemy_animation_1_720p.png").load_strip([0, 0, 1280, 720], 19, (255, 55, 202)),
        self.animation_frames = [0, 1, 2, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        self.frame_times = [50, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 50, 50, 50, 150, 100],
        self.delay = 100
        self.animation_type = 'screen'
        self.mp_cost = 2

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
        if self.parent.dazed > 0 or self.parent.stunned > 0 or self.parent.mp < self.mp_cost:
            return False
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=2000)
        self.parent.parent.persist['FX'].add_effect(self.animation_sprites, self.animation_frames, self.frame_times, self.delay, self.animation_type)
        self.parent.parent.persist['SFX'].schedule_sfx('Blast_1')
        self.end_action_timer = 3000

    def target_set(self, source, battle_character):
        target = []
        if isinstance(battle_character, PlayerCharacter):
            for character in self.parent.parent.player_characters.sprites():
                target.append(character)
        else:
            for character in self.parent.parent.enemy_characters.sprites():
                target.append(character)
        self.target = target
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class SandBreath(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Team"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 30
        self.animation = "Slash_1"
        self.name = "Sand Breath"
        self.action_type = "Ability"
        self.effects = [("daze", 3, 50), ("frail", 3, 50)]

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
        if self.parent.dazed > 0 or self.parent.stunned > 0:
            return False
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Impale(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Single"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 60
        self.animation = "Slash_1"
        self.name = "Impale"
        self.action_type = "Ability"
        self.effects = [("stun", 2, 25), ("bleed", 3, 75)]

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
        if self.parent.dazed > 0 or self.parent.stunned > 0:
            return False
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Burrow(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "None"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 60
        self.animation = "Slash_1"
        self.name = "Burrow"
        self.action_type = "Ability"

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
        return True

    def do_action(self):
        self.parent.state = "Burrow"
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        pass


class TailSweep(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Team"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 60
        self.animation = "Slash_1"
        self.name = "Tail Sweep"
        self.action_type = "Ability"

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
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.parent.state = "Hidden"
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Emerge(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Team"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 20
        self.animation = "Slash_1"
        self.name = "Sand Breath"
        self.action_type = "Ability"
        self.effects = [("stun", 2, 100)]

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
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.parent.state = "Main"
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Bolster(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Single"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 0
        self.animation = "Slash_1"
        self.name = "Bolster"
        self.action_type = "Ability"
        self.effects = [("Vigilant", 3, 100), ("Faith", 3, 100)]

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
        if self.parent.dazed > 0 or self.parent.stunned > 0:
            return False
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class DesertWrath(BattleAction):
    def __init__(self, parent, target=None):
        super().__init__(parent, target=None)
        self.target_type = "Single"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 10
        self.animation = "Slash_1"
        self.name = "Desert's Wrath"
        self.action_type = "Ability"
        self.effects = [("bleed", 2, 10), ("toxic", 2, 10), ("burn", 2, 10), ("curse", 2, 10), ("spite", 2, 10),
                        ("hex", 2, 10), ("slow", 2, 10)]

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
        return True

    def do_action(self):
        for target in self.target:
            damage = attack_defense_calculate(self, self.parent, target)
            target.damage(damage, self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = battle_character
        if self.parent.battle_action:
            self.parent.battle_action.cancel()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


ITEM_LIST = {"All": ["StimPack"],
             "All_Shop_Weights": [1],
             "All_Reward_Weights": [1],
             "Desert": [],
             "Desert_Shop_Weights": [],
             "Desert_Reward_Weights": [],
             "Grasslands": [],
             "Grasslands_Shop_Weights": [],
             "Grasslands_Reward_Weights": [],
             "Badlands": [],
             "Badlands_Shop_Weights": [],
             "Badlands_Reward_Weights": [],
             "Valley": [],
             "Valley_Shop_Weights": [],
             "Valley_Reward_Weights": [],
             "Tundra": [],
             "Tundra_Shop_Weights": [],
             "Tundra_Reward_Weights": [], }

STORE_NAMES = ["Equipments", "Gear", "Stuff", "Things", "Trappings", "Paraphernalia", "Sundries", "Storehouse",
               "Stockhouse", "Surplus", "Oddments", "Bits", "Accoutraments", "Armaments", "Ordnance Supply",
               "Munitions", "Supplies", "Materials", "Necessities", "Outfitting", "Remedies"]

ADJECTIVES = ["accurate", "accessible", "adaptable", "advisable", "aesthetically pleasing", "agreeable", "available",
              "balanced", "bright", "calm", "candid", "capable", "certified", "clear", "compliant", "cooperative",
              "coordinated", "courageous", "credible", "cultured", "curious", "decisive", "deep", "delightful",
              "deployable", "descriptive", "detailed", "different", "diligent", "distinct", "dominant", "dramatic",
              "dry", "durable", "dynamic", "economical", "educated", "efficient", "elastic", "eloquent", "energetic",
              "entertaining", "enthusiastic", "familiar", "famous", "fast", "fearless", "festive", "fierce", "fine",
              "flawless", "flowing", "focused", "frequent", "fresh", "friendly", "functional", "funny", "futuristic",
              "gainful", "good", "grounded", "hard-to-find", "harmonious", "helpful", "holistic", "hybrid", "important",
              "inexpensive", "inquisitive", "instinctive", "intelligent", "interesting", "interoperable", "judicious",
              "knowledgeable", "known", "large", "lean", "learnable", "light", "likable", "literate", "logical",
              "long lasting", "long term", "lyrical", "magical", "maintainable", "makeshift", "material", "mature",
              "mixed", "momentous", "mysterious", "natural", "necessary", "new", "next", "nimble", "obtainable", "odd",
              "offbeat", "open", "operable", "optimal", "organic", "outstanding", "overt", "painstaking", "panoramic",
              "parallel", "peaceful", "perfect", "periodic", "perpetual", "physical", "plausible", "popular",
              "possible", "powerful", "precious", "premium", "present", "private", "productive", "protective", "proud",
              "public", "quick", "quiet", "rare", "ready", "real", "real time", "rebel", "receptive", "redundant",
              "regular", "relaxed", "relevant", "reliable", "remarkable", "resilient", "reusable", "ripe", "robust",
              "safe", "satisfying", "scalable", "scarce", "secure", "selective", "serious", "sharp", "silent", "simple",
              "sincere", "skillful", "small", "smart", "smooth", "solid", "sophisticated", "special", "spectacular",
              "spotless", "stable", "standard", "steadfast", "steady", "strategic", "strong", "sturdy", "stylish",
              "substantial", "subtle", "successful", "succinct", "sudden", "suitable", "superb", "supreme",
              "sustainable", "swanky", "talented", "tame", "tangible", "tasteful", "tasty", "tested", "thankful",
              "thin", "thinkable", "thoughtful", "threatening", "timely", "traceable", "truthful", "typical",
              "ubiquitous", "unbiased", "uncovered", "unique", "unknown", "upbeat", "upscale", "usable", "useful",
              "valuable", "vast", "well-made", "wide", "wise", "workable", "youthful", ]

TITLES = ["Sir", "Madam"]


class BattleConsumable(BattleAction):
    def __init__(self, parent=None, target=None):
        super().__init__(parent, target=None)
        self.action_type = "Item"


class StimPack(BattleConsumable):
    def __init__(self, parent=None, target=None):
        super().__init__(parent=None, target=None)
        self.parent = parent
        self.target = target
        self.target_type = "Single"
        self.animation = "Slash_1"
        self.name = "StimPack"
        self.buy_value = 50
        self.sell_value = 25
        self.effects = [("regen", 4, 100), ("quick", 4, 100)]

    def cancel(self):
        self.parent.parent.persist['inventory'].append(StimPack())
        self.kill()

    def do_action(self):
        for target in self.target:
            target.damage(-int(target.max_hp * 0.1), self, delay=100)
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        if hasattr(source, 'battle_action'):
            pass
        source.battle_action.cancel()
        source.battle_action = StimPack(source, battle_character)
        source.parent.battle_actions.add(source.battle_action)
        source.parent.battle_objects.add(source.battle_action)
        self.kill()
        source.parent.persist['inventory'].remove(self)


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
