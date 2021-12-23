import copy
import math
import random

import network_generator
import numpy as np
import pygame
import names
import pytweening
from threading import Timer
import json
from enum import Enum, unique, auto
from itertools import product
from typing import List, Type, Union

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

DETAIL_FONT = pygame.font.Font(r"venv\resources\fonts\manaspc.ttf", 16)
TEXT_FONT = pygame.font.Font(r"venv\resources\fonts\manaspc.ttf", 24)
HEADING_FONT = pygame.font.Font(r"venv\resources\fonts\manaspc.ttf", 36)
TEXT_COLOR = (20, 100, 100)
SELECTED_COLOR = (75, 225, 225)
COLOR_KEY = (255, 55, 202)
MAX_NAME_LENGTH = 12


@unique
class Status(Enum):
    DAZED = auto()  # can't use ability
    DISABLED = auto()  # can't use attack
    STUNNED = auto()  # can't act
    PERPLEXED = auto()  # CAN'T USE ITEM
    TRAPPED = auto()  # CAN'T RUN
    VIGILANT = auto()  # DEFENSE UP
    SMITTEN = auto()  # CAN'T DEFEND
    FAITH = auto()  # SPIRIT UP
    BRAVE = auto()  # ATTACK UP
    CALM = auto()  # MAGIC UP
    HASTE = auto()  # EXTRA TURN
    TURNS = auto()  # NUM TURNS
    QUICK = auto()  # SPEED UP
    LUCKY = auto()  # LUCK UP
    FOCUS = auto()  # CRIT RATE UP
    BLEED = auto()  # DOT
    TOXIC = auto()  # DOT
    BURN = auto()  # DOT
    CURSE = auto()  # DAMAGE BONUS
    SPITE = auto()  # DAMAGE BONUS
    INVINCIBLE = auto()  # DAMAGE IMMUNE
    SHIELD = auto()  # 1/2 DAMAGE PHYSICAL OR LASER
    WARD = auto()  # 1/2 DAMAGE MAGICAL OR LASER
    FRAIL = auto()  # DEFENSE DOWN
    TERRIFY = auto()  # SPIRIT DOWN
    WEAK = auto()  # ATTACK DOWN
    DISTRACT = auto()  # MAGIC DOWN
    SLOW = auto()  # SPEED DOWN
    HEX = auto()  # LUCK DOWN
    DULL = auto()  # CRIT RATE DOWN
    SAVAGE = auto()  # CRIT DAMAGE UP
    GENTLE = auto()  # CRIT DAMAGE DOWN
    REGEN = auto()  # REGEN OVER TIME


@unique
class Stat(Enum):
    HP = auto()
    MP = auto()
    STRENGTH = auto()
    DEFENSE = auto()
    MAGIC = auto()
    SPIRIT = auto()
    SPEED = auto()
    LUCK = auto()
    CRITICAL_RATE = auto()
    CRITICAL_DAMAGE = auto()


@unique
class DamageType(Enum):
    MAGICAL = auto()
    PHYSICAL = auto()
    LASER = auto()
    TRUE = auto()


@unique
class TargetType(Enum):
    SINGLE = auto()
    TEAM = auto()
    ALL = auto()
    NONE = auto()
    SELF = auto()


@unique
class EquipmentType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    HELM = auto()
    BOOTS = auto()
    SHIELD = auto()
    CAPE = auto()
    MEDALLION = auto()
    ARTIFACT = auto()


@unique
class CharacterClass(Enum):
    FIGHTER = auto()
    ROGUE = auto()
    ADEPT = auto()
    ARTIFICER = auto()


@unique
class ActionType(Enum):
    ATTACK = auto()
    ABILITY = auto()
    ITEM = auto()
    RUN = auto()
    DEFEND = auto()


# Player Characters
BASE_CLASSES = ["Fighter", "Adept", "Rogue", "Artificer"]
EXPERIENCE_CURVE = [100, 210, 320, 430, 540, 650, 760, 870, 980, 1090, 1200, 1310, 1420, 1530]
EXPERIENCE_CURVE_TOTAL = [100, 310, 630, 1060, 1600, 2250, 3010, 3880, 4860, 5950, 7150, 8460, 9880, 11410]
for i in range(len(EXPERIENCE_CURVE)):
    EXPERIENCE_CURVE_TOTAL.append(sum(EXPERIENCE_CURVE[:i + 1]))

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
    image = pygame.image.load(path).convert()
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
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey)


# Regions

REGION_BIOMES = ["Desert", "Grasslands", "Valley"]  # , "Forest", "Savannah", "Badlands", "Tundra",
# "Rainforest", "Steppe", "Taiga"]
REGION_CARDS = {
    "Desert": image_load(
        r"venv\resources\sprites\Region\Cards\Desert_Card_480p_1.png"),
    "Grasslands": image_load(
        r"venv\resources\sprites\Region\Cards\Grasslands_Card_480p_1.png"),
    "Valley": image_load(
        r"venv\resources\sprites\Region\Cards\Valley_Card_480p_1.png"),
    "Savannah": image_load(
        r"venv\resources\sprites\Region\Cards\Savannah_Card_480p_1.png"),
}

REGION_SHAPES = ["Land-Locked", "Coastal", "Archipelago", "Island", "Plateau",
                 "Lakeside", "Canyon", "River"]

REGION_LAYOUTS = {
    # num_nodes=30, knn=4, node_space=100, space_probability=100,
    # node_space_ll=0, node_space_ul=350, min_edge_angle=15
    "Badlands":
        {
            "Badlands_1":
                {
                    "Image": image_load(r"venv\resources\sprites\Region\BGs\Badlands_1_720p.png"),
                    "Start": [176, 424, 312, 592],
                    "End": [904, 496, 1024, 528],
                    "Shapes": [[(120, 224), (432, 264), (592, 184), (760, 176), (1048, 280), (1048, 680), (848, 680),
                                (776, 624), (712, 368), (560, 360), (328, 600), (120, 608)]],
                    "Positive": True,
                },
        },
    "Desert":
        {
            "Desert_1":
                {
                    "Image": image_load(r"venv\resources\sprites\Region\BGs"
                                        r"\Desert_1_720p.png"),
                    "Start": [120, 264, 296, 440],
                    "End": [856, 344, 1032, 488],
                    "Shapes": [[(120, 96), (950, 96), (950, 504), (912, 528), (824, 432), (816, 288), (720, 232),
                                (536, 288), (480, 472), (376, 512), (120, 440)],
                               [(120, 512), (336, 600), (552, 528), (640, 392), (728, 432), (856, 584), (950, 580),
                                (950, 580), (120, 580)],
                               [(552, 424), (560, 344), (696, 280), (776, 320), (768, 350), (704, 300), (616, 300)]],
                    "Positive": True,
                },
            "Desert_2":
                {
                    "Image": image_load(r"venv\resources\sprites\Region\BGs"
                                        r"\Desert_2_720p.png"),
                    "Start": [124, 94, 266, 418],
                    "End": [956, 244, 1022, 506],
                    "Shapes": [[(122, 92), (966, 90), (680, 369), (650, 588), (602, 606), (420, 476), (124, 428)],
                               [(792, 472), (1026, 164), (1032, 540), (904, 446), (790, 508)]],
                    "Positive": True,
                },
        }
}

NODE_TYPES = [["Empty", "Town", "Dungeon", "Lone Building", "Encounter"], [30, 15, 10, 10, 40]]

NODE_TYPES_2 = [["Shop", "Dungeon", "Encounter", "Event", "Empty"], [1, 2, 40, 27, 30]]

UNEXPLORED_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet8.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet9.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet10.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet11.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet12.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Sheet13.png")]

EXPLORED_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored8.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored9.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored10.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored11.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored12.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Node_Explored13.png")]

EXIT_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node8.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node9.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node10.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node11.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node12.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Exit_Node13.png")]

EVENT_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Event_Node32p8.png")]

DUNGEON_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Dungeon_Node32p8.png")]

SHOP_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Shop_Node32p8.png")]

ENCOUNTER_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Encounter_Node32p8.png")]

BOSS_NODE = [
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p1.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p2.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p3.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p4.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p5.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p6.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p7.png"),
    pygame.image.load(r"venv\resources\sprites\Node\Boss_Node32p8.png")]

Party_Marker = [
    [pygame.image.load(r"venv\resources\sprites\Region\Party_Marker1.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker2.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker3.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker4.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker5.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker6.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker7.png"),
     pygame.image.load(r"venv\resources\sprites\Region\Party_Marker8.png")],
    [65, 65, 65, 65, 65, 65, 65, 65]]

BATTLE_BGS = {"Desert": {0: pygame.image.load(r"venv\resources\sprites"
                                              r"\Battle\BGs\Desert_Battle_720p.png")}}


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
                        self.parent.parent.persist['SFX'].schedule_sfx('Shop_Buy_1')
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
        self.bg_2_rect = [X * 18 / 100, Y * 8 / 100, X * 59 / 100, Y * 86 / 100]
        self.pos = [X * 17 / 100, Y * 7 / 100]
        self.pos_origin = (X * 17 / 100, Y * 7 / 100)
        self.prompt_rect = [X * 18 / 100, Y * 9 / 100, X * 57 / 100, Y * 84 / 100]
        self.option_rect = [X * 18 / 100, Y * 55 / 100, X * 57 / 100, Y * 5 / 100]
        self.option_offset = 5
        self.timer = 0
        self.next_state = "Prompt"
        self.enemies = None
        self.prompt = None
        self.options = None
        self.rewards = None
        self.cost = None
        self.item_reward = None
        self.display_cost_reward = False
        self.shake_queue = []
        for key in parameter_dictionary.keys():
            if key == "cost":
                self.cost = {}
                for k in parameter_dictionary[key].keys():
                    self.cost[k] = eval(parameter_dictionary[key][k])
            elif key == "rewards":
                self.rewards = {}
                for k in parameter_dictionary[key].keys():
                    self.rewards[k] = eval(parameter_dictionary[key][k])
            else:
                setattr(self, key, parameter_dictionary[key])

    def restore_position(self):
        if self.pos[0] != self.pos_origin[0]:
            if -0.001 > self.pos[0] - self.pos_origin[0] > 0.001:
                self.pos[0] = self.pos_origin[0]
            else:
                self.pos[0] = self.pos[0] + (0.1 * (self.pos_origin[0] - self.pos[0]))
        if self.pos[1] != self.pos_origin[1]:
            if -0.001 > self.pos[1] - self.pos_origin[1] > 0.001:
                self.pos[1] = self.pos_origin[1]
            else:
                self.pos[1] = self.pos[1] + (0.1 * (self.pos_origin[1] - self.pos[1]))

    def update_position(self):
        self.bg_1_rect = [self.pos[0], self.pos[1], X * 60 / 100, Y * 88 / 100]
        self.bg_2_rect = [self.pos[0] + (X * 1 / 100), self.pos[1] + (Y * 1 / 100), X * 58 / 100, Y * 86 / 100]
        self.prompt_rect = [self.pos[0] + (X * 1 / 100), self.pos[1] + (Y * 2 / 100), X * 57 / 100, Y * 84 / 100]
        self.option_rect = [self.pos[0] + (X * 1 / 100), self.pos[1] + (Y * 48 / 100), X * 57 / 100, Y * 5 / 100]

    def update_timer(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.timer = 0

    def shake(self, n=6, delay=150, magnitude=15):
        for i in range(n):
            x = random_int(-1, 1) * magnitude
            y = random_int(-1, 1) * magnitude
            self.shake_queue.append([(x, y), delay])
            self.parent.parent.persist['SFX'].schedule_sfx("Thump_1", 100)

    def shake_tick(self, dt):
        self.shake_queue[0][1] -= dt
        if self.shake_queue[0][1] <= 0:
            self.pos[0] += self.shake_queue[0][0][0]
            self.pos[1] += self.shake_queue[0][0][1]
            del self.shake_queue[0]

    def update(self, dt):
        self.update_position()
        if self.pos[0] != self.pos_origin[0] or self.pos[1] != self.pos_origin[1]:
            self.restore_position()
        if self.timer > 0:
            self.update_timer(dt)
        if self.shake_queue:
            self.shake_tick(dt)
        if self.state == "Prompt":
            pass
        elif self.state == "Delay":
            if self.timer == 0:
                self.state = self.next_state
        elif self.state == "Reward":
            self.reward()
            self.pay_cost()
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
                tw(surface, str(index + 1) + ". " + option[0], color, [self.option_rect[0], self.option_rect[1] +
                                                                       (index * Y * 5 / 100), self.option_rect[2],
                                                                       self.option_rect[3]], TEXT_FONT)
        if self.display_cost_reward:
            index = int(len(self.prompt) / 45)
            cost_keys = list(self.cost.keys())
            rewards_keys = list(self.rewards.keys())
            cost_text1 = ''
            cost_text2 = ''
            cost_text3 = ''
            cost_text4 = ''
            cost_text5 = ''
            if len(cost_keys) > 0:
                cost_text1 = f'Give:    {cost_keys[0]}: {self.cost[cost_keys[0]]}'
                if len(cost_keys) > 1:
                    cost_text2 = f' {cost_keys[1]}: {self.cost[cost_keys[1]]}'
                    if len(cost_keys) > 2:
                        cost_text3 = f' {cost_keys[2]}: {self.cost[cost_keys[2]]}'
                        if len(cost_keys) > 3:
                            cost_text4 = f' {cost_keys[3]}: {self.cost[cost_keys[3]]}'
                            if len(cost_keys) > 4:
                                cost_text5 = f' {cost_keys[4]}: {self.cost[cost_keys[4]]}'
            cost_text = cost_text1 + cost_text2 + cost_text3 + cost_text4 + cost_text5  # [X * 17/100, Y * 7/100]
            tw(surface, cost_text, TEXT_COLOR,
               [self.pos[0] + (X * 1 / 100), (Y * 10 / 100) + Y * 5 * index / 100 + self.pos[1], X * 60 / 100,
                Y * 15 / 100], TEXT_FONT)
            rewards_text1 = rewards_text2 = rewards_text3 = rewards_text4 = rewards_text5 = ''
            if len(rewards_keys) > 0:
                rewards_text1 = f'Recieve:    {rewards_keys[0]}: {self.rewards[rewards_keys[0]]}'
                if len(rewards_keys) > 1:
                    rewards_text2 = f' {rewards_keys[1]}: {self.rewards[rewards_keys[1]]}'
                    if len(rewards_keys) > 2:
                        rewards_text3 = f' {rewards_keys[2]}: {self.rewards[rewards_keys[2]]}'
                        if len(rewards_keys) > 3:
                            rewards_text4 = f' {rewards_keys[3]}: {self.rewards[rewards_keys[3]]}'
                            if len(rewards_keys) > 4:
                                rewards_text5 = f' {rewards_keys[4]}: {self.rewards[rewards_keys[4]]}'
            rewards_text = rewards_text1 + rewards_text2 + rewards_text3 + rewards_text4 + rewards_text5
            print(rewards_text)
            tw(surface, rewards_text, TEXT_COLOR,
               [self.pos[0] + (X * 1 / 100), (Y * 10 / 100) + self.pos[1] + Y * 5 * (index + 2) / 100, X * 60 / 100,
                Y * 15 / 100], TEXT_FONT)

    def handle_action(self, action):
        if action == "click":
            if self.state == "Prompt":
                for index, option in enumerate(self.options):
                    if click_check([self.option_rect[0], self.option_rect[1] + (index * Y * 5 / 100),
                                    self.option_rect[2], self.option_rect[3]]):
                        if len(option) > 3:
                            for key in self.cost.keys():
                                if self.parent.parent.persist[key] < self.cost[key]:
                                    break
                            else:
                                outcome = choose_random_weighted(self.options[index][1], self.options[index][2])
                                if "state" in outcome.keys():
                                    setattr(self, "state", outcome["state"])
                                if "prompt" in outcome.keys():
                                    setattr(self, "prompt", outcome["prompt"])
                                if "options" in outcome.keys():
                                    setattr(self, "options", outcome["options"])
                                if self.display_cost_reward:
                                    self.display_cost_reward = False

                        else:
                            outcome = choose_random_weighted(self.options[index][1], self.options[index][2])
                            if "state" in outcome.keys():
                                setattr(self, "state", outcome["state"])
                            if "prompt" in outcome.keys():
                                setattr(self, "prompt", outcome["prompt"])
                            if "options" in outcome.keys():
                                setattr(self, "options", outcome["options"])
                            if self.display_cost_reward:
                                self.display_cost_reward = False

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
            self.option_index += 1
            if len(self.options) != 0:
                self.option_index %= len(self.options)

        elif action == "up":
            self.option_index -= 1
            if len(self.options) != 0:
                self.option_index %= len(self.options)

        elif action == "space":
            self.shake()

    def battle(self):
        self.parent.parent.persist['enemies'] = self.enemies
        self.parent.parent.state = "Browse"
        self.parent.parent.next_state = "BATTLE"
        self.parent.parent.done = True

    def reward(self):
        if self.rewards is not None:
            for key in self.rewards.keys():
                self.parent.parent.persist[key] += self.rewards[key]
        if self.item_reward is not None:
            if isinstance(self.item_reward, list):
                for item in self.item_reward:
                    self.parent.parent.persist['inventory'].append(item)
            else:
                self.parent.parent.persist['inventory'].append(self.item_reward)
        self.exit()

    def pay_cost(self):
        if self.cost is not None:
            for key in self.cost.keys():
                self.parent.parent.persist[key] -= self.cost[key]

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


def event_caller(node, region_type, region_index):
    region_type = region_type
    region_index = region_index
    if node.type == "Encounter":
        parameter_dictionary = choose_random_weighted(encounter_dictionary["All"] + encounter_dictionary[region_type],
                                                      encounter_dictionary["All_Weights"] + encounter_dictionary[
                                                          region_type + "_Weights"])
        return Event(node, parameter_dictionary)
    elif node.type == "Event":
        parameter_dictionary = choose_random_weighted(event_dictionary["All"] + event_dictionary[region_type],
                                                      event_dictionary["All_Weights"] + event_dictionary[
                                                          region_type + "_Weights"])
        return Event(node, parameter_dictionary)
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


class Dialogue(object):
    def __init__(self, info):
        """valid info entries:
            id: unique identifier for use of linking dialog trees by options
            prompt: text to be printed to describe, instruct, or otherwise inform the player about their options
            options: dict of options given to the player, value is a list of possible outcomes and probabilities
            cost/2/3/n: if an option requires a cost, describe it in a dict here
            reward/2/3/n: dict of rewards for an outcome
            enemies: list of enemies for a battle outcome
            character: if a character will join as reward, put it here
            option_flag: if an option has a requirement to be displayed, put it here"""
        for key, value in info.items():
            setattr(self, key, value)


class DialogueBranch(Dialogue):
    def __init__(self, info):
        super().__init__(info)


class DialogueTree(Dialogue):
    def __init__(self, info):
        super().__init__(info)


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
                     ["Not interested.", [{"state": "Exit"}], [1]]], }],
    "All_Weights": [1],
    "Desert": [],
    "Desert_Weights": [], }

event_dictionary = {
    "All": [
        {"prompt": "You come across a small camp. The inhabitants explain that they're in need of chargers and are "
                   "willing to trade for them.",
         "cost": {"chargers": 'random.randint(1, 3)'},
         "rewards": {"supplies": 'random.randint(1, 3)', "elixirs": 'random.randint(1, 3)',
                     "gold": 'random.randint(0, 50)'},
         "options": [["Seems like a fair deal.", [{"state": "Reward"}], [1], "cost"],
                     ["Not interested.",
                      [{"prompt": "The group grumble among themselves as they head back to their camp.",
                        "options": [["Continue on.", [{"state": "Exit"}], [1]]]}], [1]]],
         "display_cost_reward": True}],
    "All_Weights": [1],
    "Desert": [],
    "Desert_Weights": [], }

P_NODE_TYPES = [10, 15, 20, 60]

REGION_STATIC_SPRITES = {
    'coin icon': image_load(
        r"venv\resources\sprites\Region\Coin Icon.png"),
    'supplies icon': image_load(
        r"venv\resources\sprites\Region\Supplies Icon.png"),
    'elixir icon': image_load(
        r"venv\resources\sprites\Region\Elixir Icon.png"),
    'heart icon': image_load(
        r"venv\resources\sprites\Region\Heart Icon.png"),
    'charge icon': image_load(
        r"venv\resources\sprites\Region\Charge Icon.png"),
    "FighterIcon": image_load(
        r"venv\resources\sprites\Region\Fighter Icon 64.png"),
    'AdeptIcon': image_load(
        r"venv\resources\sprites\Region\Fighter Icon 64.png"),
    'ArtificerIcon': image_load(
        r"venv\resources\sprites\Region\Fighter Icon 64.png"),
    'RogueIcon': image_load(
        r"venv\resources\sprites\Region\Fighter Icon 64.png")
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
        1: {0: (600, 300)},
        2: {0: (600, 100),
            1: (600, 300)},
        3: {0: (500, 100),
            1: (500, 100),
            2: (500, 200)},
        4: {0: (500, 100),
            1: (500, 100),
            2: (500, 200),
            3: (500, 100)},
        5: {0: (500, 100),
            1: (500, 100),
            2: (500, 200),
            3: (500, 100),
            4: (500, 200)},
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
        '0': {
            'hp': [X * 20 / 100, Y * 76 / 100, X * 20 / 100, Y * 7 / 100],
            'mp': [X * 20 / 100, Y * 80 / 100, X * 20 / 100, Y * 7 / 100],
            'name': [X * 1 / 100, Y * 76 / 100, X * 20 / 100, Y * 7 / 100]
        },
        '1': {
            'hp': [X * 20 / 100, Y * 84 / 100, X * 20 / 100, Y * 7 / 100],
            'mp': [X * 20 / 100, Y * 88 / 100, X * 20 / 100, Y * 7 / 100],
            'name': [X * 1 / 100, Y * 84 / 100, X * 20 / 100, Y * 7 / 100]
        },
        '2': {
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
        r"venv\resources\sprites\Battle\Menus\Action Slot720p1.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p2.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p3.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p4.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p5.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p6.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p7.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p8.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p9.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p10.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p11.png"),
        image_load(
            r"venv\resources\sprites\Battle\Menus\Action Slot720p12.png")
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
            r"venv\resources\sprites\Battle\Menus\Target Rets128p2.png"),
        'source': image_load(
            r"venv\resources\sprites\Battle\Menus\Target Rets128p1.png"),
    }

}

MUSIC = {'Title': r"venv\resources\music\title.oga",
         'Desert': {'constant': pygame.mixer.Sound(
             r"venv\resources\music\Desert_Layer\constant-Constant.wav"),
             'shop': pygame.mixer.Sound(
                 r"venv\resources\music\Desert_Layer\shop-Shop.wav"),
             'map': pygame.mixer.Sound(
                 r"venv\resources\music\Desert_Layer\map-Map.wav"),
             'battle': pygame.mixer.Sound(
                 r"venv\resources\music\Desert_Layer\battle-Battle.wav"),
             'event': pygame.mixer.Sound(
                 r"venv\resources\music\Desert_Layer\event-Event.wav"),
         }
         }

SOUND_EFFECTS = {'Toggle_1': pygame.mixer.Sound(
    r"venv\resources\sfx\397604__nightflame__menu-fx-01.wav"),
    'Toggle_2': pygame.mixer.Sound(
        r"venv\resources\sfx\503340__tahutoa__clicky-accept-menu-sound.wav"),
    'Confirm_1': pygame.mixer.Sound(
        r"venv\resources\sfx\403019__inspectorj__ui-confirmation-alert-c4.wav"),
    'Shop_Buy_1': pygame.mixer.Sound(
        r"venv\resources\sfx\shop_buy_1.wav"),
    'Blast_1': pygame.mixer.Sound(
        r"venv\resources\sfx\blast_1.wav"),
    'Attack_1': pygame.mixer.Sound(
        r"venv\resources\sfx\attack_1.wav"),
    'Thump_1': pygame.mixer.Sound(
        r"venv\resources\sfx\thump_1.wav"),
    'Menu': {
        'Toggle_1': pygame.mixer.Sound(
            r"venv\resources\sfx\397604__nightflame__menu-fx-01.wav"),
        'Toggle_2': pygame.mixer.Sound(
            r"venv\resources\sfx\503340__tahutoa__clicky-accept-menu-sound.wav"),
        'Confirm_1': pygame.mixer.Sound(
            r"venv\resources\sfx\403019__inspectorj__ui-confirmation-alert-c4.wav"),
    },
}


class SFXManager(object):
    def __init__(self):
        self.sfx = []
        self.sfx_channels = [pygame.mixer.Channel(0), pygame.mixer.Channel(1), pygame.mixer.Channel(2),
                             pygame.mixer.Channel(3), pygame.mixer.Channel(4), pygame.mixer.Channel(5)]

    def schedule_sfx(self, sound, delay=0, play=1):
        self.sfx.append({'sound': sound, 'delay': delay, 'delay_reset': delay, 'play': play})

    def update(self, dt):
        for sfx in self.sfx:
            sfx['delay'] -= dt
            if sfx['delay'] <= 0:
                if sfx['sound'] in list(SOUND_EFFECTS.keys()):
                    for channel in self.sfx_channels:
                        if not channel.get_busy():
                            channel.play(SOUND_EFFECTS[sfx['sound']])
                            break
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

    def add_effect(self, sprites, frames, frame_times, delay, animation_type, pos=(0, 0)):
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
        self.constant = pygame.mixer.Channel(6)
        self.map = pygame.mixer.Channel(7)
        self.shop = pygame.mixer.Channel(8)
        self.battle = pygame.mixer.Channel(9)
        self.event = pygame.mixer.Channel(10)
        self.dungeon = pygame.mixer.Channel(11)
        self.map.set_volume(0)
        self.event.set_volume(0)
        self.battle.set_volume(0)
        self.shop.set_volume(0)
        self.dungeon.set_volume(0)
        self.constant.set_volume(0)
        self.map_sound = None
        self.shop_sound = None
        self.battle_sound = None
        self.event_sound = None
        self.dungeon_sound = None
        self.constant_sound = None
        self.channel_fade = []

    def update(self, dt, parent=None):
        if parent is not None:
            if self.game_state != type(parent).__name__:
                self.game_state = type(parent).__name__
                eval('self.fade_to_' + self.game_state.lower())()
        if self.state == 'music':
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
        elif self.state == 'layer':
            if self.channel_fade:
                for event in self.channel_fade:
                    event[3] -= dt
                    if event[3] <= 0:
                        event[3] = 0
                    new_volume = event[2] - (event[3] / event[4])
                    if new_volume < 0:
                        new_volume *= -1
                    event[0].set_volume(new_volume)
                    if event[3] <= 0:
                        self.channel_fade.remove(event)
            if self.game_state == "Region":
                if self.region is not parent.persist['region_type']:
                    self.set_region(parent.persist['region_type'])
                if parent.state == "Event":
                    if isinstance(parent.party.node.event, Shop) and self.region_state != "Shop":
                        self.fade_to_shop()
                    elif self.region_state != "Event" and not isinstance(parent.party.node.event, Shop):
                        self.fade_to_event()
                elif parent.state == "Browse" and self.region_state != "Browse":
                    self.fade_to_region()

    def set_fade_event(self, channel, target, time=1000, delay=0):
        start_volume = channel.get_volume()
        if start_volume != target:
            self.channel_fade.append([channel, start_volume, target, time, time, delay])

    def fade_to_shop(self):
        self.region_state = "Shop"
        self.set_fade_event(self.constant, 1)
        self.set_fade_event(self.map, 0)
        self.set_fade_event(self.shop, 1)
        self.set_fade_event(self.battle, 0)
        self.set_fade_event(self.event, 0)
        self.set_fade_event(self.dungeon, 0)

    def fade_to_region(self):
        self.region_state = "Browse"
        self.set_fade_event(self.constant, 1)
        self.set_fade_event(self.map, 1)
        self.set_fade_event(self.shop, 0)
        self.set_fade_event(self.battle, 0)
        self.set_fade_event(self.event, 0)
        self.set_fade_event(self.dungeon, 0)

    def fade_to_event(self):
        self.region_state = "Event"
        self.set_fade_event(self.constant, 1)
        self.set_fade_event(self.map, 1)
        self.set_fade_event(self.shop, 0)
        self.set_fade_event(self.battle, 0)
        self.set_fade_event(self.event, 1)
        self.set_fade_event(self.dungeon, 0)

    def fade_to_battle(self):
        self.set_fade_event(self.constant, 1)
        self.set_fade_event(self.map, 0)
        self.set_fade_event(self.shop, 0)
        self.set_fade_event(self.battle, 1)
        self.set_fade_event(self.event, 0)
        self.set_fade_event(self.dungeon, 0)

    def layer_fade_out(self):
        self.set_fade_event(self.constant, 0)
        self.set_fade_event(self.map, 0)
        self.set_fade_event(self.shop, 0)
        self.set_fade_event(self.battle, 0)
        self.set_fade_event(self.event, 0)
        self.set_fade_event(self.dungeon, 0)

    def set_region(self, region):
        self.region = region
        self.region_state = "Browse"
        self.map_sound = MUSIC[region]['map']
        self.shop_sound = MUSIC[region]['shop']
        self.battle_sound = MUSIC[region]['battle']
        self.event_sound = MUSIC[region]['event']
        self.dungeon_sound = MUSIC[region]['constant']
        self.constant_sound = MUSIC[region]['constant']
        self.map.play(self.map_sound, -1, fade_ms=2000)
        self.event.play(self.event_sound, -1, fade_ms=2000)
        self.battle.play(self.battle_sound, -1, fade_ms=2000)
        self.shop.play(self.shop_sound, -1, fade_ms=2000)
        self.dungeon.play(self.dungeon_sound, -1, fade_ms=2000)
        self.constant.play(self.constant_sound, -1, fade_ms=2000)
        self.fade_to_region()

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


def tw(surface, text, color, rect, font, x_mode=None, y_mode=None, buffer=0, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    linesize = font.get_linesize()
    font_height = font.size("Tg")[1]
    y = buffer * font_height + rect.top
    text_lines = 0
    if y_mode is not None:
        text_lines = find_lines(text, font, rect)
        total_height = (text_lines - 1) * linesize + font_height

    if y_mode == "bjust":
        y = rect.bottom - total_height - (buffer * font_height)

    if y_mode == "center":
        y = rect.center[1] - total_height / 2
        buffer = 0

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
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
        image_rect = pygame.Rect((rect.left, y), (image.get_size()))
        if x_mode == "rjust":
            image_rect.right = rect.right - (buffer * font_height)
        elif x_mode == "center":
            image_rect.center = rect.center[0], image_rect.center[1]
        else:
            image_rect.left = rect.left + (buffer * font_height)
        surface.blit(image, image_rect)
        y += linesize

        # remove the text we just blitted
        text = text[i:]

    return text


def find_lines(text, font, rect):
    text_lines = 0
    while text:
        text_lines += 1
        i = 1

        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        text = text[i:]

    return text_lines


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


def node_assign_3():
    node_type = random.choices(NODE_TYPES_2[0], weights=NODE_TYPES_2[1])[0]
    return node_type


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
        self.alpha = 255
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
    def __init__(self):
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
    def __init__(self, properties, behaviors):
        self.energy = False
        super(Weapon, self).__init__()
        self.attack = 0
        self.slot = "Weapon"
        self.attack_type = "Attack"
        self.target_type = "Single"
        self.hits = 1
        self.charge = 5
        self.max_charge = 30
        self.use_charge = 10
        for key, value in properties.items():
            setattr(self, key, value)
        for k, v in behaviors.items():
            pass

    def recharge(self):
        if hasattr(self, 'charge') and hasattr(self, 'max_charge'):
            self.charge = self.max_charge

    def stat_update(self):
        pass

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


BATTLE_ANIMATIONS = {
    "Slash_1": {
        'sprites': [image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p1.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p2.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p3.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p4.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p5.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p6.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p7.png"),
                    image_load(r"venv\resources\sprites\Battle\Effects\slash1animation64p8.png"),
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
                                        for option_enemy_5 in options[4]:
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
                                                    enemy_5_choice = option_enemy_5
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
                surface.blit(REGION_STATIC_SPRITES[player.__class__.__name__ + "Icon"],
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
    def __init__(self, data, level, parent=None):
        super().__init__()
        self.sprites = SpriteSheet(data["sprites"]).load_strip(data["sprite_rect"], data["sprite_count"],
                                                               data["color_key"])
        self.status_icon = ImageLoader.load_image(data["status_icon"], data["color_key"])
        self.level = level
        self.level = 1
        self.flip_state_on_hit = False
        self.flip_state_on_magic = False
        self.flip_state_on_physical = False
        self.shield_on_hit = 0
        self.ward_on_hit = 0
        self.battle_slot = "None"
        self.parent = parent
        self.action = None
        self.hover = False
        self.selected = False
        self.current_sprite = 0
        self.status = {}
        self.equipment = {}
        self.abilities = {}
        self.ability_tree = None
        self.stats = {}
        self.speed = 0
        self.defend = 0
        self.state = "Idle"
        self.action_options = []
        self.attack_action = ActionGetter.get_action(name="Attack")
        self.battle_action = None
        self.defend_action = ActionGetter.get_action(name="Defend")
        self.run_action = ActionGetter.get_action(name="Run")
        self.timer = 0
        self.animation_index = 0
        self.state = "Idle"
        self.pos = 0, 0
        for k, v in data["attributes"].items():
            setattr(self, k, v)
        for k, v in data["stats"].items():
            self.stats[Stat[k.upper()]] = v

        self.equipment_options = []
        if "equipment_options" in data.keys():
            self.equipment_options = data["equipment_options"]

        self.animation_index = 0
        self.image = self.sprites[0]
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.hp = self.stats[Stat.HP][self.level]
        self.mp = self.stats[Stat.MP][self.level]
        self.class_ = data["attributes"]["class_type"]

    def get_class(self):
        return self.class_

    def update(self, dt):
        """Increment animation state, flip image, set new rect if necessary"""
        self.timer += dt * random_int(90, 110) / 100
        if self.timer > getattr(self, f"{self.state.lower()}_speed")[self.animation_index]:
            self.timer = 0
            self.animation_index += 1
            self.animation_index %= len(getattr(self, f"{self.state.lower()}_frames"))
        self.image = self.sprites[getattr(self, f"{self.state.lower()}_frames")[self.animation_index]]
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

    def get_equipment_options(self):
        options = self.equipment_options

        return options

    def set_pos_by_center(self, pos):
        """ Set position of sprite by center"""
        self.rect.center = pos
        self.pos = self.rect.topleft

    def change_hp(self, damage, delay, test=False):
        """Provide damage to BC, spawn particle and check for hp < min and hp > max"""
        damage = int(damage)
        if not test:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, damage, delay=delay)
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.get_stat(Stat.HP):
            self.hp = self.get_stat(Stat.HP)

    def get_stat(self, stat: Stat) -> int:
        """proper way to get stat"""
        value = self.stats[stat][self.level - 1]
        if self.equipment:
            for key, equipment in self.equipment.items():
                value += equipment.get_stat(stat)
        if self.abilities:
            for key, ability in self.abilities.items():
                value += ability.get_stat(stat)
        value *= self.get_status_multiplier(stat)
        return int(value)

    def get_status(self, status) -> int:
        if status in self.status:
            return self.status[status]
        else:
            return 0

    def get_status_multiplier(self, stat: Stat) -> float or int:
        value = 1
        if stat == Stat.HP or stat == Stat.MP:
            return value
        elif stat == Stat.STRENGTH:
            if Status.BRAVE in self.status.keys():
                value *= 1.5
            if Status.WEAK in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.MAGIC:
            if Status.CALM in self.status.keys():
                value *= 1.5
            if Status.DISTRACT in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.DEFENSE:
            if Status.VIGILANT in self.status.keys():
                value *= 1.5
            if Status.FRAIL in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.SPIRIT:
            if Status.FAITH in self.status.keys():
                value *= 1.5
            if Status.TERRIFY in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.LUCK:
            if Status.LUCKY in self.status.keys():
                value *= 1.5
            if Status.HEX in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.SPEED:
            if Status.QUICK in self.status.keys():
                value *= 1.5
            if Status.SLOW in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.CRITICAL_RATE:
            if Status.FOCUS in self.status.keys():
                value *= 1.5
            if Status.DULL in self.status.keys():
                value /= 1.5
            return value
        elif stat == Stat.CRITICAL_DAMAGE:
            if Status.SAVAGE in self.status.keys():
                value *= 1.5
            if Status.GENTLE in self.status.keys():
                value /= 1.5
            return value

    def check_status(self, status: Status) -> bool:
        return status in self.status

    def spend_mp(self, cost):
        self.mp -= cost
        if self.mp < 0:
            self.mp = 0

    def apply_status(self, status: Status, turns: int, delay, test=False):
        self.status[status] += turns
        if not test:
            self.status_particle(status, turns, delay)

    def damage(self, damage, action, delay=0, test=False):
        """Provide damage amount, action ref, and optional delay to for particle, to deliver damage or healing to BC"""
        # print(damage)
        if damage < 0:
            self.change_hp(damage, delay)
        elif Status.INVINCIBLE in self.status:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, "immune")
        else:
            if action.get_damage_type() == DamageType.PHYSICAL or action.get_damage_type() == DamageType.LASER:
                if Status.SHIELD in self.status:
                    damage /= 2
            if action.get_damage_type() == DamageType.MAGICAL or action.get_damage_type() == DamageType.LASER:
                if Status.WARD in self.status:
                    damage /= 2
            if Status.SPITE in self.status:
                damage += 10
            if Status.CURSE in self.status.keys():
                damage *= 2
            self.change_hp(damage, delay, test)

    def give_options(self):  # can be removed once in-game battle system is updated
        options = []
        if hasattr(self, 'action'):
            if getattr(self.action, 'name', "None") != "None":
                return [(self.battle_slot, "None", ["None"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]
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

    def ko(self):
        self.kill()
        self.parent.battle_characters_ko.add(self)
        self.parent.battle_objects.add(self)
        self.battle_action.kill()

    def flip_state(self):
        """hook for subclass"""
        pass

    def on_hit(self, action):
        """trigger for on hit effects"""
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

    def on_end_turn(self, test=False):
        """called after all actions on each turn, tick down status effects and trigger any other desired effects"""
        status_keys = list(self.status)
        delay_index = 0
        for status in status_keys:
            damage = 0
            if status == Status.BLEED:
                damage = int(self.get_remaining_hp() * 5 / 100)
            elif status == Status.BURN:
                damage = int(self.get_stat(Stat.HP) * 5 / 100)
            elif status == Status.TOXIC:
                damage = int(self.get_missing_hp() * 5 / 100)
            if damage:
                self.change_hp(damage, 500 * delay_index, test)
                delay_index += 1
            self.status[status] -= 1
            if self.status[status] <= 0:
                del self.status[status]
                if not test:
                    self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                              f"{status.name} has worn off", delay=500 * delay_index)

    def status_damage(self, status, damage):
        pass

    def get_remaining_hp(self):
        return self.hp

    def get_remaining_mp(self):
        return self.mp

    def get_missing_hp(self):
        return self.stats[Stat.HP] - self.hp

    def get_actions(self, useable=False) -> list:
        actions = []

        for key, ability in self.abilities.items():
            if useable:
                if ability.is_useable(self):
                    actions.append(ability)
            else:
                actions.append(ability)

        if self.attack_action.is_useable(self):
            actions.append(self.attack_action)

        if self.defend_action.is_useable(self):
            actions.append(self.defend_action)

        # also get from equipment, ability_tree

        return actions

    def get_action_options(self, ai_characters, enemy_characters, user, useable=False) -> list:
        actions = self.get_actions(useable)
        options = []

        for action in actions:
            if action.get_target_type() == TargetType.SINGLE:
                for character in ai_characters + enemy_characters:
                    options.append({"action": action, "target": character})
            elif action.get_target_type() == TargetType.TEAM:
                options.append({"action": action, "target": ai_characters})
                options.append({"action": action, "target": enemy_characters})
            elif action.get_target_type() == TargetType.NONE:
                options.append({"action": action, "target": ai_characters + enemy_characters})
            elif action.get_target_type() == TargetType.ALL:
                options.append({"action": action, "target": ai_characters + enemy_characters})
            elif action.get_target_type() == TargetType.SELF:
                options.append({"action": action, "target": user})

        return options

    def status_particle(self, status, turns, delay):
        self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery,
                                                  f"{status.name} +{turns}", delay=delay)

    def miss(self, delay=0, test=False):
        if not test:
            self.parent.damage_particle.add_particles(self.rect.centerx, self.rect.centery, "MISS", delay=delay)

    def encode(self) -> List[int]:
        encoding = [self.get_stat(x) for x in list(Stat)]
        encoding.append(self.get_remaining_hp())
        encoding.append(self.get_remaining_mp())
        encoding += [self.get_status(x) for x in list(Status)]
        return encoding


class PlayerCharacter(BattleCharacter):
    def __init__(self, data, name, level, class_):
        super().__init__(data, level, parent="None")
        self.move_selected = False
        self.attack_type = "Attack"
        self.name = name
        self.crit_rate = self.base_crit_rate = 1
        self.crit_damage = self.base_crit_damage = 1
        self.level = level
        self.exp = 0
        self.skill_points = level
        self.experience_to_level = 0
        self.timer = 0
        self.equipment = {}
        self.abilities = []
        self.class_ = class_

    def level_check(self):
        if self.level < len(EXPERIENCE_CURVE) + 1:
            self.experience_to_level = sum(EXPERIENCE_CURVE[:self.level]) - self.exp
            if self.exp > sum(EXPERIENCE_CURVE[:self.level]):
                self.level += 1
                self.skill_points += 1

    def pre_turn(self, parent):
        if not hasattr(self, 'battle_action'):
            setattr(self, 'battle_action', NoActionCardSelected(self))
            parent.battle_actions.add(self.battle_action)
            parent.battle_objects.add(self.battle_action)
        elif self.battle_action.turns == 0:
            if self.battle_action:
                return
            else:
                self.battle_action.kill()
                setattr(self, 'battle_action', NoActionCardSelected(self))
                parent.battle_actions.add(self.battle_action)
                parent.battle_objects.add(self.battle_action)

    def get_class(self):
        return self.class_


class Fighter(PlayerCharacter):
    def __init__(self, name):
        super(Fighter, self).__init__(name)
        self.sprites = SpriteSheet(
            r"venv\resources\sprites\Character\Battle\Fighter\Fighter_Battle128p.png").load_strip([0, 0, 128, 128], 6,
                                                                                                  (255, 55, 202))
        self.idle_frames = [0, 1, 2, 3]
        self.idle_speed = [1331, 134, 400, 134]
        self.attack_frames = [4]
        self.attack_speed = [1000]
        self.cast_frames = [4]
        self.cast_speed = [1000]
        self.hit_frames = [0]

        self.hit_speed = [1000]
        self.miss_frames = [2]
        self.miss_speed = [1000]
        self.pos = 0, 0
        self.image = self.sprites[0]
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.equipment_options = self.base_equipment_options = ["Weapon", "Helm", "Armor", "Boots", "Shield"]
        self.base_attack_type = self.attack_type = "Attack"
        self.equipment = {}
        self.abilities = self.base_abilities = ["Bash", "Strike", "Impale", "Dash", "Fortify", "Magic Strike",
                                                "True Strike"]
        self.abilities = [KiBlast(self)]
        self.left_tree = SkillTree("Fighter", "left", self)
        self.center_tree = SkillTree("Fighter", "center", self)
        self.right_tree = SkillTree("Fighter", "right", self)


class Slime(BattleCharacter):
    def __init__(self, enemy_slot, region_index, n_enemy, parent):
        super().__init__(parent)
        self.name = "Slime"
        self.hover = False
        self.battle_slot = enemy_slot
        self.sprites = SpriteSheet(r"venv\resources\sprites\Enemy\Slime"
                                   r"\Slime128p.png").load_strip([0, 0, 128, 128], 4, (255, 55, 202))
        self.idle_frames = [0, 1]
        self.idle_speed = [750, 250]
        self.attack_frames = [2]
        self.attack_speed = [1000]
        self.cast_frames = [3]
        self.cast_speed = [1000]
        self.hit_frames = [2]
        self.hit_speed = [1000]
        self.miss_frames = [3]
        self.miss_speed = [1000]
        self.pos = self.base_pos = BATTLE_MENUS['enemy positions'][n_enemy][self.battle_slot - 5]
        self.image = self.sprites[0]
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
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
        self.exp_reward = [200, 12, 14, 16, 18, 20, 22, 28][region_index]
        self.supply_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.elixir_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.charger_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index], [1, 1, 1, 1, 2, 2, 2, 2][region_index])
        self.gold_reward = random_int([0, 0, 0, 0, 0, 0, 0, 0][region_index],
                                      [10, 12, 14, 16, 18, 20, 22, 24][region_index])
        self.action_options = [Attack(self), SlimeBall(self)]
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
        self.sprites = [image_load(r"venv\resources\sprites\Enemy\Slime\Slime128p1.png"),
                        image_load(r"venv\resources\sprites\Enemy\Slime\Slime128p2.png"),
                        image_load(r"venv\resources\sprites\Enemy\Slime\Slime128p3.png"),
                        image_load(r"venv\resources\sprites\Enemy\Slime\Slime128p4.png")]
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
        self.state = "Main"  # "Burrow", "Hidden"

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

    def update(self, dt):
        self.reticle_color_update(dt)

    def draw(self, surface):
        if self.parent.state == "Turn":

            if self.parent.turn_sub_state == "Target":
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


class BattleActionCard(pygame.sprite.Sprite):
    def __init__(self, parent, target=None):
        super().__init__()
        if target is None:
            target = ['None']
        self.state = "Idle"
        self.target = target
        self.hover = False
        self.parent = parent
        if self.parent is not None:
            self.source = self.parent.battle_slot
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

    def __lt__(self, other):
        if self.priority and not other.priority:
            return False
        elif not self.priority and other.priority:
            return True
        else:
            return self.speed < other.speed

    def __gt__(self, other):
        if self.priority and not other.priority:
            return True
        elif not self.priority and other.priority:
            return False
        else:
            return self.speed > other.speed

    def __le__(self, other):
        if self.priority and not other.priority:
            return False
        elif not self.priority and other.priority:
            return True
        else:
            return self.speed <= other.speed

    def __ge__(self, other):
        if self.priority and not other.priority:
            return True
        elif not self.priority and other.priority:
            return False
        else:
            return self.speed >= other.speed


class NoActionCardSelected(BattleActionCard):
    def __init__(self, parent, target=None):
        super(NoActionCardSelected, self).__init__(parent, target=None)

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


class Run(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Run, self).__init__(parent, target=None)

    def is_usable(self):
        return True

    def do_action(self):
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = None
        if self.parent.battle_action:
            self.parent.battle_action.kill()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Defend(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Defend, self).__init__(parent, target=None)
        self.priority = True

    def is_usable(self):
        return True

    def do_action(self):
        self.parent.defend += 1
        self.end_action_timer = 1000

    def target_set(self, source, battle_character):
        self.target = None
        if self.parent.battle_action:
            self.parent.battle_action.kill()
        self.parent.battle_action = self
        self.parent.parent.battle_actions.add(self)
        self.parent.parent.battle_objects.add(self)


class Recharge(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Recharge, self).__init__(parent, target=None)

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


class SlimeBall(BattleActionCard):
    def __init__(self, parent, target=None):
        super(SlimeBall, self).__init__(parent, target=None)
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
            value_set.append((self.name, player.battle_slot, value))
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


class Attack(BattleActionCard):
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
            outcome[character.battle_slot] = ((damage_low + damage_high) * p_hit * (1 - p_critical) / (
                    2 * character.hp)) + ((critical_low + critical_high) * p_hit * p_critical / (2 * character.hp))
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


class KiBlast(BattleActionCard):
    def __init__(self, parent, target=None):
        super(KiBlast, self).__init__(parent, target=None)
        self.parent = parent
        self.target_type = "Team"
        self.attack_stat = "strength"
        self.defend_stat = "defense"
        self.power = 40
        self.name = "Ki Blast"
        self.action_type = "Ability"
        self.animation_sprites = SpriteSheet(
            r"venv\resources\sprites\Battle\Effects"
            r"\attack_all_enemy_animation_1_720p.png").load_strip([0, 0, 1280, 720], 19, (255, 55, 202)),
        self.animation_frames = [0, 1, 2, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        self.frame_times = [50, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 50, 50, 50,
                            150, 100],
        self.delay = 100
        self.animation_type = 'screen'
        self.mp_cost = 2

    def expected_value(self):
        value_set = []
        for character in self.parent.parent.battle_characters.sprites():
            outcome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            damage_low, damage_high, p_hit, critical_low, critical_high, p_critical = \
                attack_defense_calculate(self, self.parent, character, ev=True)
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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
        self.parent.parent.persist['FX'].add_effect(self.animation_sprites, self.animation_frames, self.frame_times,
                                                    self.delay, self.animation_type)
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


class SandBreath(BattleActionCard):
    def __init__(self, parent, target=None):
        super(SandBreath, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class Impale(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Impale, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class Burrow(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Burrow, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class TailSweep(BattleActionCard):
    def __init__(self, parent, target=None):
        super(TailSweep, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class Emerge(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Emerge, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class Bolster(BattleActionCard):
    def __init__(self, parent, target=None):
        super(Bolster, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class DesertWrath(BattleActionCard):
    def __init__(self, parent, target=None):
        super(DesertWrath, self).__init__(parent, target=None)
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
            outcome[BATTLE_MENUS['battle_slot_index'][character.battle_slot]] = \
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


class BattleConsumableCard(BattleActionCard):
    def __init__(self, parent=None, target=None):
        super().__init__(parent, target=None)
        self.action_type = "Item"


class StimPack(BattleConsumableCard):
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


class SettingsManager(object):
    def __init__(self):
        super(SettingsManager, self).__init__()
        self.load = True
        self.top_left = 0, 0
        self.top_center = 640, 0
        self.top_right = 1280, 0
        self.center_left = 0, 360
        self.center = 640, 360
        self.center_right = 1280, 360
        self.bottom_left = 0, 720
        self.bottom_center = 640, 720
        self.bottom_right = self.screen = 1280, 720
        self.music_volume = 0.5
        self.effects_volume = 0.5
        self.static_paths = True
        self.battle_messages = True
        self.size_options = {"720p": (1280, 720), "1080p": (1920, 1080), "1440p": (2560, 1440)}
        self.music_volume_options = {"0": 0, "1": 0.1, "2": 0.2, "3": 0.3, "4": 0.4, "5": 0.5, "6": 0.6, "7": 0.7,
                                     "8": 0.8, "9": 0.9, "10": 1}
        self.effects_volume_options = {"0": 0, "1": 0.1, "2": 0.2, "3": 0.3, "4": 0.4, "5": 0.5, "6": 0.6, "7": 0.7,
                                       "8": 0.8, "9": 0.9, "10": 1}
        self.static_path_options = {"Yes": True, "No": False}
        self.battle_messages_options = {"Yes": True, "No": False}

    def update(self, dt):
        if self.load:
            self.load = False

    def draw(self, surface):
        pass

    def handle_action(self, action):
        pass

    def exit_menu(self):
        self.load = True

    def set_screen_size(self, size: tuple):
        self.top_center = size[0] / 2, 0
        self.top_right = size[0], 0
        self.center_left = 0, size[0] / 2
        self.center = size[0] / 2, size[0] / 2
        self.center_right = size[0],
        self.bottom_left = 0, size[0]
        self.bottom_center = size[0] / 2, size[0]
        self.bottom_right = self.screen = size


class PauseMenu(object):
    def __init__(self):
        super(PauseMenu, self).__init__()

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def handle_action(self, action):
        pass


class JsonReader:
    @staticmethod
    def read_json(file):
        with open(file) as f:
            data = json.load(f)
        return data


class ImageLoader:
    @staticmethod
    def load_image(file_path, color_key=COLOR_KEY):
        image = pygame.image.load(file_path).convert()
        image.set_colorkey(color_key)
        return image


class ItemGetter:
    item_dict = JsonReader().read_json("venv/settings_data/Items.json")

    @staticmethod
    def get_item(**kwargs):
        kwargs_list = list(kwargs.keys())
        if "name" in kwargs_list:
            pass
        elif "names" in kwargs_list:
            pass
        elif "type" in kwargs_list:
            pass
        else:
            type = choose_random(ItemGetter.item_dict.keys())
            pass

    @staticmethod
    def construct_by_name(name):
        type = ItemGetter.get_type_by_name(name)
        pass

    @staticmethod
    def get_type_by_name(name: str):
        for key, value in ItemGetter.item_dict.times():
            if name in value.keys():
                return key

    @staticmethod
    def get_list_by_type(type_) -> list:
        return list(ItemGetter.item_dict[type_.name])


class WorldBuilder:
    def __init__(self):
        self.region_dict = JsonReader().read_json("venv/settings_data/Region_Maps.json")

    def get_region(self, region_type: str):
        region = choose_random([i for i in list(self.region_dict[region_type].keys())])
        return self.region_dict[region_type][region]

    def get_region_by_name(self, name: str):
        region = None
        for key, region_type in self.region_dict.items():
            for i, value in region_type.items():
                if name == i:
                    return value

    def get_name_list(self):
        name_list = []
        for key, region_type in self.region_dict.items():
            for k, value in region_type.items():
                name_list.append(k)
        return name_list


class CharacterGetter:
    data = JsonReader.read_json("venv/settings_data/Class_Data.json")

    @staticmethod
    def get_character(**kwargs):
        level = 1
        if "level" in kwargs.keys():
            level = kwargs["level"]

        class_ = choose_random(list(CharacterGetter.data.keys()))
        if "class_" in kwargs.keys():
            class_ = kwargs["class_"]

        name = random_name()
        if "name" in kwargs.keys():
            name = kwargs["name"]

        return PlayerCharacter(CharacterGetter.data[class_], name, level, class_)

    @staticmethod
    def get_list() -> list:
        return [x for x in list(CharacterGetter.data)]

    @staticmethod
    def class_exist(class_):
        return class_ in CharacterGetter.data


class EnemyGetter:
    data = JsonReader.read_json("venv/settings_data/Enemy_Data.json")

    @staticmethod
    def get_enemy(**kwargs):
        level = 1
        if "level" in kwargs.keys():
            level = kwargs["level"]

        class_ = choose_random(list(EnemyGetter.data))
        if "class" in kwargs.keys():
            class_ = kwargs["class"]

        return BattleCharacter(EnemyGetter.data[class_], level)

    @staticmethod
    def get_list() -> list:
        return [x for x in list(EnemyGetter.data)]


class ActionGetter:
    data = JsonReader.read_json("venv/settings_data/Battle_Actions.json")

    @staticmethod
    def get_action(**kwargs):
        if "name" in kwargs.keys():
            if kwargs["name"] in ActionGetter.data.keys():
                return Action(ActionGetter.data[kwargs["name"]])

        if "random" in kwargs.keys():
            if kwargs["random"]:
                return Action(ActionGetter.data[choose_random(list(ActionGetter.data.keys()))])

    @staticmethod
    def get_actions_list(learnable=False):
        if learnable:
            return [x for x in ActionGetter.data if ActionGetter.data[x]["learnable"]]
        return [x for x in ActionGetter.data]


class Action:
    def __init__(self, data):
        fields = ["name", "hits", "modify_character_attack",
                  "damage_delay", "mp_cost", "turn_delay", "power"]
        for key, value in data.items():
            if key in fields:
                setattr(self, key, value)
            elif key == "target_type":
                setattr(self, key, TargetType[value.upper()])
            elif key == "damage_type":
                setattr(self, key, DamageType[value.upper()])
            elif key == "damage_stat":
                setattr(self, key, Stat[value.upper()])
            elif key == "status":
                self.status = {}
                for k, v in data["status"].items():
                    self.status[Status[k.upper()]] = (v[0], v[1])
            elif key == "action_type":
                setattr(self, key, ActionType[value.upper()])
        self.parent = None
        self.target = None

    def get_target_type(self):
        return getattr(self, "target_type", TargetType.SINGLE)

    def get_damage_type(self):
        return getattr(self, "damage_type", DamageType.PHYSICAL)

    def get_damage_stat(self):
        return getattr(self, "damage_stat", Stat.STRENGTH)

    def get_power(self):
        return getattr(self, "power", 0)

    def is_useable(self, user) -> bool:
        if user.check_status(Status.DAZED) and self.action_type == ActionType.ABILITY:
            return False

        elif user.check_status(Status.DISABLED) and self.action_type == ActionType.ATTACK:
            return False

        elif user.check_status(Status.TRAPPED) and self.action_type == ActionType.RUN:
            return False

        elif user.check_status(Status.PERPLEXED) and self.action_type == ActionType.ITEM:
            return False

        elif user.check_status(Status.SMITTEN) and self.action_type == ActionType.DEFEND:
            return False

        elif user.check_status(Status.STUNNED):
            return False

        elif user.get_remaining_mp() < self.get_mp_cost():
            return False

        # if self.parent.dazed > 0 or self.parent.stunned > 0 or self.parent.mp < self.mp_cost:
        return True

    def do_action(self, test=False):
        self.parent.spend_mp(self.get_mp_cost())

        if isinstance(self.target, BattleCharacter):
            self.single_action(test=test)
        elif isinstance(self.target, list):
            self.multi_action(test=test)

    def single_action(self, test=False):
        for hits in range(self.hits):
            if not MissRoll.hit_or_miss(self, self.parent, self.target):
                damage = DamageCalculator.calculate(self, self.parent, self.target)
                self.target.damage(damage, self, self.damage_delay, test)
            else:
                self.target.miss(test=test)

    def multi_action(self, test=False):
        for hits in range(self.hits):
            miss_list = MissRoll.hit_or_miss(self, self.parent, self.target)
            for i, target in enumerate(self.target):
                if not miss_list[i]:
                    damage = DamageCalculator.calculate(self, self.parent, target)
                    target.damage(damage, self, self.damage_delay, test)
                else:
                    target.miss(test=test)

    def get_stat(self, stat) -> int:
        return 0

    def set_target(self, user, target):
        self.parent = user
        self.target = target

    def get_accuracy(self) -> int:
        return getattr(self, "accuracy", 100)

    def get_mp_cost(self) -> int:
        return getattr(self, "mp_cost", 0)

    def get_hits(self):
        return getattr(self, "hits", 1)

    def encode(self, ai_characters, enemy_characters):
        if not self.target and self.get_target_type() != TargetType.NONE:
            raise AttributeError('No valid target')
        if not self.parent:
            raise AttributeError('No action user')
        properties = [self.get_power(), self.get_mp_cost(), self.get_accuracy(), self.get_hits()]
        damage_type_one_hot = [1 if x == self.get_damage_type() else 0 for x in list(DamageType)]
        damage_stat_one_hot = [1 if x == self.get_damage_stat() else 0 for x in list(Stat)]
        character_map = self.get_character_map(ai_characters, enemy_characters)
        target_multi_hot = [1 if character_map[i] in self.target or character_map[i] == self.target else 0 for i in
                            range(10)]
        status_turns_multi_hot = [x[1] if x in self.status else 0 for x in list(Status)]
        status_chance_one_hot = [x[0] if x in self.status else 0 for x in list(Status)]
        return properties + damage_type_one_hot + damage_stat_one_hot + target_multi_hot + status_turns_multi_hot + status_chance_one_hot

    def get_character_map(self, ai_characters, enemy_characters):
        ai = ai_characters + [None for i in range(5 - len(ai_characters))]
        enemy = enemy_characters + [None for i in range(5 - len(enemy_characters))]
        return ai + enemy


class SkillTreeGetter:
    def __init__(self):
        self.data = JsonReader.read_json("venv/settings_data/Tree_Nodes.json")


class DamageCalculator:
    min_critical_roll = 0
    max_critical_roll = 100
    min_damage_roll = 85
    max_damage_roll = 100

    @staticmethod
    def calculate(action, user: BattleCharacter, target: BattleCharacter or [BattleCharacter], **kwargs) -> int or list:
        """take an action, user, target; determine proper damage formula and return damage"""
        if type(target) == list:
            return [DamageCalculator.calculate(action, user, target_, **kwargs) for target_ in target]
        else:
            critical_roll = DamageCalculator.get_critical_roll(**kwargs)
            damage_roll = DamageCalculator.get_damage_roll(**kwargs)
            if action.get_damage_type() == DamageType.PHYSICAL:
                return DamageCalculator.physical_calculate(action, user, target, damage_roll, critical_roll)
            elif action.get_damage_type() == DamageType.MAGICAL:
                return DamageCalculator.physical_calculate(action, user, target, damage_roll, critical_roll)
            elif action.get_damage_type() == DamageType.LASER:
                return DamageCalculator.physical_calculate(action, user, target, damage_roll, critical_roll)
            elif action.get_damage_type() == DamageType.TRUE:
                return DamageCalculator.physical_calculate(action, user, target, damage_roll, critical_roll)

    @staticmethod
    def get_damage_roll(**kwargs):
        if "damage_roll" in kwargs.keys():
            return kwargs["damage_roll"]
        if "damage_min_roll" in kwargs.keys():
            min_ = kwargs["damage_min_roll"]
        else:
            min_ = DamageCalculator.min_damage_roll
        if "damage_max_roll" in kwargs.keys():
            max_ = kwargs["damage_max_roll"]
        else:
            max_ = DamageCalculator.max_damage_roll
        if "average_roll" in kwargs.keys():
            if kwargs["average_roll"]:
                return (min_ + max_) / 2
        return random_int(min_, max_)

    @staticmethod
    def get_critical_roll(**kwargs):
        if "critical_roll" in kwargs.keys():
            return kwargs["critical_roll"]
        if "critical_min_roll" in kwargs.keys():
            min_ = kwargs["critical_min_roll"]
        else:
            min_ = DamageCalculator.min_critical_roll
        if "critical_max_roll" in kwargs.keys():
            max_ = kwargs["critical_max_roll"]
        else:
            max_ = DamageCalculator.max_critical_roll
        return random_int(min_, max_)

    @staticmethod
    def physical_calculate(action, user, target, damage_roll, critical_roll):
        defense = target.get_stat(Stat.DEFENSE)
        attack = user.get_stat(action.get_damage_stat())
        power = action.get_power()
        return (power * attack / defense) * damage_roll / 100

    @staticmethod
    def magical_calculate(action, user, target, damage_roll, critical_roll):
        defense = target.get_stat(Stat.SPIRIT)
        attack = user.get_stat(action.get_damage_stat())
        power = action.get_power()
        return (power * attack / defense) * damage_roll / 100

    @staticmethod
    def laser_calculate(action, user, target, damage_roll, critical_roll):
        defense = min(target.get_stat(Stat.DEFENSE), target.get_stat(Stat.SPIRIT))
        attack = user.get_stat(action.get_damage_stat())
        power = action.get_power()
        return (power * attack / defense) * damage_roll / 100

    @staticmethod
    def true_calculate(action, user, target, damage_roll, critical_roll):
        power = action.get_power()
        return power * damage_roll / 100


class CriticalRoll:
    critical_threshold = 95

    @staticmethod
    def critical_roll(action, user: Type[BattleCharacter],
                      target: Union[Type[BattleCharacter], List[Type[BattleCharacter]]]) -> bool or [bool]:
        """check for critical hit or not on a single target or a list of targets; return True = CRITICAL"""
        if type(target) == list:
            return [CriticalRoll.critical_roll(action, user, target_) for target_ in target]
        else:
            crit_roll = random_int(0, 100)
            crit_factor = user.get_stat(Stat.CRITICAL_RATE) * user.get_stat(Stat.LUCK) / target.get_stat(Stat.LUCK)
            return crit_roll * crit_factor > CriticalRoll.critical_threshold

    @staticmethod
    def get_crit_chance(action, user, target) -> Union[float, int]:
        crit_factor = user.get_stat(Stat.CRITICAL_RATE) * user.get_stat(Stat.LUCK) / target.get_stat(Stat.LUCK)
        p = CriticalRoll.critical_threshold / (100 * crit_factor)
        if 1 - p < 0:
            return 0
        elif 1 - p > 1:
            return 1
        else:
            return 1 - p


class MissRoll:
    @staticmethod
    def hit_or_miss(action, user: Type[BattleCharacter],
                    target: Union[Type[BattleCharacter], List[Type[BattleCharacter]]]) -> bool or [bool]:
        """check for hit or miss on a single target or a list of targets; return True = MISS; return False = HIT"""
        if type(target) == list:
            return [MissRoll.hit_or_miss(action, user, target_) for target_ in target]
        else:
            miss_roll = random_int(0, 100)
            return miss_roll * target.get_stat(Stat.LUCK) / user.get_stat(Stat.LUCK) > action.get_accuracy()

    @staticmethod
    def effect_hit_or_miss(accuracy, user: Type[BattleCharacter],
                           target: Union[Type[BattleCharacter], List[Type[BattleCharacter]]]) -> bool or [bool]:
        """check for hit or miss on a single target or a list of targets; return True = MISS; return False = HIT"""
        if type(target) == list:
            return [MissRoll.hit_or_miss(accuracy, user, target_) for target_ in target]
        else:
            miss_roll = random_int(0, 100)
            return miss_roll * target.get_stat(Stat.LUCK) / user.get_stat(Stat.LUCK) > accuracy()

    @staticmethod
    def get_hit_chance(action, user, target) -> float:
        return action.get_accuracy() * (user.get_stat(Stat.LUCK) / target.get_stat(Stat.LUCK)) / 100


class ActionEvaluator:
    """Class for determining the expected value of an action, given a user and target or targets."""

    @staticmethod
    def evaluate_action(action, user: Type[BattleCharacter],
                        target: Union[Type[BattleCharacter], List[Type[BattleCharacter]]],
                        character_map: dict) -> list:
        """take an action, user, and all battle characters;
        return a list of options with [user, action, target, outcome]"""
        outcome = np.zeros(len(character_map))

        if type(target) == list:
            for character in target:
                outcome[character_map[character]] = ActionEvaluator.single_evaluate(action, user, character)
        elif isinstance(target, BattleCharacter):
            outcome[character_map[target]] = ActionEvaluator.single_evaluate(action, user, target)

        return outcome

    @staticmethod
    def single_evaluate(action, user, target) -> Union[int, float]:
        value = 0
        # get damage value
        value += ActionEvaluator.get_damage_value(action, user, target)

        # get effect value
        value += ActionEvaluator.get_effect_value(action, user, target)

        # get auxiliary value
        value += ActionEvaluator.get_auxiliary_value(action, user, target)

        return value

    @staticmethod
    def get_damage_value(action, user, target) -> Union[int, float]:
        damage = DamageCalculator.calculate(action, user, target, average_roll=True)
        if damage >= 0:
            return damage / target.get_remaining_hp()
        elif damage < 0:
            return damage / target.get_missing_hp()
        else:
            return 0

    @staticmethod
    def get_effect_value(action, user, target) -> Union[int, float]:
        return 0

    @staticmethod
    def get_auxiliary_value(action, user, target) -> Union[int, float]:
        return 0


class ActionEval:
    """Object to hold the action, user, target or targets, and expected outcome of an action-option."""

    def __init__(self, action, user: Type[BattleCharacter],
                 target: Union[Type[BattleCharacter], List[Type[BattleCharacter]]], character_map):
        self.action = action
        self.user = user
        self.target = target
        self.evaluation = ActionEvaluator.evaluate_action(action, user, target, character_map)


class ActionSet:
    """Holds a combination of actions for one or more enemies. self.value is for use as a comparitor with higher value
    meaning better option."""

    def __init__(self, action_set: List[ActionEval], character_map, ai_characters):
        self.ai_characters = ai_characters
        self.actions = action_set
        self.character_map = character_map
        self.value = self.get_value()

    def get_value(self) -> float:
        """Combine expected values into a normalized comparitor float value"""

        # vector sum all evaluations
        # eval_sum = self.actions[0].evaluation
        # if len(self.actions) > 1:
        #     for i in range(len(self.actions) - 1):
        #         eval_sum = self.vector_add(eval_sum, self.actions[i + 1].evaluation)

        list_of_evals = [x.evaluation for x in self.actions]
        eval_sum = np.sum(list_of_evals, axis=1)

        # flip values on enemy outcome
        eval_sum = self.sign_flip(eval_sum)
        eval_sum = self.normalize(eval_sum)
        value = sum(eval_sum)
        return value

    def vector_add(self, v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]

    def normalize(self, eval_sum: List[float]) -> List[float]:
        """squash values above 1"""
        return [math.log(i, 10) + 1 if i > 1 else i for i in eval_sum]

    def sign_flip(self, eval_sum):
        """Flips sign on enemy target evaluations to reward healing of allies and damaging of enemies."""
        for key, value in self.character_map.items():
            if value in self.ai_characters:
                eval_sum[value] *= -1
            else:
                pass
        return eval_sum

    def __lt__(self, other):
        return self.value < other.value

    def get_number_of_actions(self):
        return len(self.actions)


class UtilityAI:
    """For use in battle at the start of turn to select enemy actions. Call UtilityAI.select_actions(),
    then use selected ActionSet object to set actions. Model an action-outcome as a list of floats mapped to each
    BattleCharacter where 1.0 equates to killing or fully healing a BattleCharacter."""

    @staticmethod
    def select_actions(ai_characters: Union[Type[BattleCharacter], List[Type[BattleCharacter]]],
                       enemy_characters: List[Type[BattleCharacter]]) -> ActionSet:

        character_map = {}
        for i, character in enumerate(ai_characters + enemy_characters):
            character_map[character] = i

        n_ai = 1
        if isinstance(ai_characters, list):
            n_ai = len(ai_characters)
        n_enemy = 1
        if isinstance(enemy_characters, list):
            n_enemy = len(enemy_characters)
        if len(character_map) != n_ai + n_enemy:
            raise ValueError(f"Character map is wrong size. Expected {n_ai + n_enemy}, but "
                             f"recieved {len(character_map)}.")

        # get an evaluation object for each action-option for each ai character
        evals = UtilityAI.get_actions_evaluations(ai_characters, ai_characters + enemy_characters, character_map)
        if not len(evals) == len(ai_characters):
            raise ValueError(f"worng amount of eval sets Expected {len(ai_characters)}, but recieved {len(evals)}.")

        # get a list of action-option combinations
        if len(ai_characters) == 1:
            action_options = product(evals[0])
        else:
            action_options = list(product(*evals))

        # combine each combination into an actionSet object and sort according to the expected value
        actions_sets = [ActionSet(option, character_map, ai_characters) for option in action_options]
        actions_sets.sort(reverse=True)

        # return the ActionSet with the highest expected value
        if len(ai_characters) == actions_sets[0].get_number_of_actions():
            return actions_sets[0]
        else:
            raise ValueError(f"Wrong number of actions returned. Expected {len(ai_characters)}, but recieved "
                             f"{actions_sets[0].get_number_of_actions()}.")

    @staticmethod
    def get_actions_evaluations(ai_characters: Union[List[Type[BattleCharacter]], Type[BattleCharacter]],
                                enemy_characters: List[Type[BattleCharacter]], character_map) -> List[
        List[ActionEval]]:
        evals_list = []

        # force type: List[BattleCharacter]
        if not type(ai_characters) == list:
            ai_characters = [ai_characters]

        # list options while evaluating, filter for usable actions
        for character in ai_characters:
            evals = [ActionEval(action["action"], character, action["target"], character_map) for action in
                     character.get_action_options(ai_characters, enemy_characters, character, useable=True)]
            evals_pos = [x for x in evals if ActionSet([x], character_map, ai_characters).value > 0]

            # if evals_pos:
            #     evals_list.append(evals_pos)
            # else:
            #     evals_neg = [(x, ActionSet([x], character_map, ai_characters).value) for x in evals]
            #     evals_neg.sort(key=lambda x: x[1], reverse=True)
            #     evals_list.append([evals_neg[0][0]])
            cull_factor = int(60 / len(ai_characters + enemy_characters))

            evals_cull_list = [(x, ActionSet([x], character_map, ai_characters).value) for x in evals]
            evals_cull_list.sort(key=lambda x: x[1], reverse=True)
            evals_cull_list = evals_cull_list[:cull_factor]
            survive_list = [x[0] for x in evals_cull_list]
            evals_list.append(survive_list)

        # return a list of lists: [[enemy_a_option_eval_1, enemy_a_option_eval_2, ...], [enemy_b_option_eval_1, ...]]
        return evals_list


class World:
    def __init__(self, map_, graph) -> None:
        self.map = map_
        self.graph = graph

    def get_next_options(self, current) -> list:
        pass


class RegionMapGetter:
    data = JsonReader.read_json("venv/settings_data/Region_Maps.json")

    @staticmethod
    def get_region_map(region_type):
        options = RegionMapGetter.data[region_type]
        return choose_random(options)


class WorldBuild:
    region_types = ["Badlands", "Taiga", "Desert", "Savannah", "Tundra", "Valley"]

    @staticmethod
    def choose_3() -> list:
        choice = set()
        choice.add(random.choice(WorldBuild.region_types))
        new_options = [x for x in WorldBuild.region_types if x not in choice]
        choice.add(random.choice(new_options))
        new_options = [x for x in WorldBuild.region_types if x not in choice]
        choice.add(random.choice(new_options))
        return list(choice)

    @staticmethod
    def extract_keys(dict_) -> list:
        keys = []
        for key, value in dict_:
            keys.append(key)
            if isinstance(value, dict):
                keys += WorldBuild.extract_keys(value)
        return keys

    @staticmethod
    def create_world(seed="zzzzzzzz") -> Type[World]:
        if seed:
            random.seed(seed)
        region_types = {i: WorldBuild.choose_3() for i in range(8)}

    @staticmethod
    def region_generate(region_type, region_index):
        data = RegionMapGetter.get_region_map(region_type)
        data["random_state"] = random.getstate()
        network, random_state = NetworkGetter().get_network(data)
        random.setstate(random_state)
        data["nodes"] = []
        data["node_list"] = network[0]
        data["edge_list"] = network[1]
        data["neighbors_dict"] = network[2]
        data["edge_dict"] = network[3]

        for i, value in enumerate(network[0]):
            if i == 0:
                data["nodes"].append(Node(value[0], value[1], network[2][i], network[3][i], i, "Boss"))
            elif i == 1:
                data["nodes"].append(Node(value[0], value[1], network[2][i], network[3][i], i, "Region Entry"))
            else:
                node_type = node_assign_3()
                data["nodes"].append(Node(value[0], value[1], network[2][i], network[3][i], i, node_type))
        for node in data["nodes"]:
            node.event = event_caller(node, region_type, region_index)
        return data


class NetworkGetter:
    def get_network(self, data):
        valid = False
        network, new_data = network_generator.network_gen(X, Y, data)
        valid = network[4]

        if valid:
            return network, new_data["random_state"]
        else:
            return NetworkGetter.get_network(new_data)


class Node(pygame.sprite.Sprite):
    def __init__(self, x, y, neighbors, edges, state, node_type, node_event=None):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.parent = None
        self.index = state
        self.seen = False
        self.visited = False
        self.x = x
        self.y = y
        self.type = node_type
        self.travel = False
        if state == 1:
            self.state = "Explored"
        elif state == 0:
            self.state = "Exit"
        else:
            self.state = "Unexplored"
        self.event = node_event
        self.selected = False
        self.hover = False
        self.neighbors = neighbors
        self.edges = edges
        self.images = settings.UNEXPLORED_NODE
        self.animation_index = 0
        self.image = self.images[0]
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.animation_speed = 0.25
        self.quick_speed = 0.25
        self.slow_speed = 0.375

    def update(self, dt):
        if self.type == "Shop":
            if (self.parent.persist['party_abilities'].scout_vision and self.seen) or \
                    self.parent.persist['party_abilities'].region_revealed or \
                    self.parent.persist['party_abilities'].locate_shops:
                self.images = settings.SHOP_NODE
                self.animation_speed = self.quick_speed
            elif self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        elif self.type == "Dungeon":
            if (self.parent.persist['party_abilities'].scout_vision and self.seen) or \
                    self.parent.persist['party_abilities'].region_revealed or \
                    self.parent.persist['party_abilities'].locate_dungeons:
                self.images = settings.DUNGEON_NODE
                self.animation_speed = self.quick_speed
            elif self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        elif self.type == "Encounter":
            if (self.parent.persist['party_abilities'].scout_vision and self.seen) or \
                    self.parent.persist['party_abilities'].region_revealed or \
                    self.parent.persist['party_abilities'].locate_encounters:
                self.images = settings.ENCOUNTER_NODE
                self.animation_speed = self.quick_speed
            elif self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        elif self.type == "Event":
            if (self.parent.persist['party_abilities'].scout_vision and self.seen) or \
                    self.parent.persist['party_abilities'].region_revealed or \
                    self.parent.persist['party_abilities'].locate_events:
                self.images = settings.EVENT_NODE
                self.animation_speed = self.quick_speed
            elif self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        elif self.type == "Empty":
            if self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        elif self.type == "Boss":
            if (self.parent.persist['party_abilities'].scout_vision and self.seen) or \
                    self.parent.persist['party_abilities'].region_revealed or \
                    self.parent.persist['party_abilities'].locate_boss:
                self.images = settings.BOSS_NODE
                self.animation_speed = self.quick_speed
            elif self.visited:
                self.images = settings.EXPLORED_NODE
                self.animation_speed = self.slow_speed
            else:
                self.images = settings.UNEXPLORED_NODE
                self.animation_speed = self.slow_speed
        if self.selected:
            self.animation_index += self.animation_speed
            self.animation_index %= len(self.images)
        else:
            if self.visited:
                self.animation_index = -1
            else:
                self.animation_index = 0
        self.image = self.images[math.floor(self.animation_index)]

        if self.parent.party.node is not None:
            if self.index in self.parent.party.node.neighbors:
                self.travel = True
            else:
                self.travel = False
        else:
            self.travel = False
        self.hover = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        if self.parent.party.node is not None:
            if self.index in self.parent.party.node.neighbors:
                self.seen = True

    def cleanup(self):
        self.kill()

    def hover(self):
        pass

    def click(self):
        self.selected = False
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.parent.party.node.index != self.index:
            self.selected = True
            self.parent.selected_node = self