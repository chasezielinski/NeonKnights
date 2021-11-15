import math
import random
import copy
import network_generator
import pygame
import pytweening
import settings
from base import BaseState
import pytweening as pt


class Node(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, neighbors, edges, state, node_type, node_event=None):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
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


class Path(object):
    def __init__(self, parent, node_1, node_2):
        self.parent = parent
        self.node_1 = node_1
        self.node_2 = node_2
        self.hover = False
        self.state = "Hidden"

    def update(self, dt):
        if self.parent.persist['party_abilities'].path_vision:
            self.state = "Visible"
        else:
            self.state = "Hidden"
            if self.node_1.state == "Explored" or self.node_2.state == "Explored":
                self.state = "Visible"

        self.hover = False
        if self.node_1.hover or self.node_2.hover:
            self.hover = True

    def draw(self, surface):
        if self.state == "Visible":
            if self.hover:
                pygame.draw.aaline(surface, (0, 0, 0), (self.node_1.x + 16, self.node_1.y + 16),
                                   (self.node_2.x + 16, self.node_2.y + 16), 8)
            else:
                pygame.draw.aaline(surface, (100, 100, 100), (self.node_1.x + 16, self.node_1.y + 16),
                                   (self.node_2.x + 16, self.node_2.y + 16), 5)


class Cursor(object):
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.parent = parent
        self.visible = False
        self.target_x = None
        self.target_y = None
        self.target_node = None
        self.position_queue = []
        self.move_speed = 0

    def snap(self):
        distance = 1000
        for node in self.parent.nodes.sprites():
            calc = math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)
            if calc < distance:
                self.target_node = node
                distance = calc
        for i in range(10):
            x = self.x - ((self.x - self.target_node.x) * pytweening.easeInExpo(i/10))
            y = self.y - ((self.y - self.target_node.y) * pytweening.easeInExpo(i/10))
            self.position_queue.append([x, y])

    def move(self, dt):
        flag = True
        if list(pygame.key.get_pressed())[79]:
            self.x += dt/5
            flag = False
        if list(pygame.key.get_pressed())[80]:
            self.x -= dt/5
            flag = False
        if list(pygame.key.get_pressed())[81]:
            self.y += dt/5
            flag = False
        if list(pygame.key.get_pressed())[82]:
            self.y -= dt/5
            flag = False
        if flag:
            self.parent.state = "Browse"
            self.snap()

    def update(self, dt):
        if not self.visible:
            self.move_speed += dt/15
            self.x = self.parent.party.x
            self.y = self.parent.party.y
        elif self.parent.state == "Browse":
            self.move_speed = 0
            if self.position_queue:
                self.x = self.position_queue[0][0]
                self.y = self.position_queue[0][1]
                del self.position_queue[0]
            else:
                self.x = self.target_node.x
                self.y = self.target_node.y

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, (0, 0, 0), [self.x, self.y, 32, 32], 4, border_radius=4)


class Party(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x = 2 * settings.X
        self.y = 2 * settings.Y
        self.images = []
        for image in settings.Party_Marker[0]:
            self.images.append(image.convert_alpha())
        self.image = self.images[0]
        self.times = settings.Party_Marker[1]
        self.timer = self.times[0]
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 55, 202))
        self.node = None
        self.animation_index = 0
        self.width = (self.image.get_width() * 24/100)
        self.height = (self.image.get_height() * 25/100)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.times[self.animation_index]:
            self.timer = 0
            self.animation_index += 1
            self.animation_index %= len(self.images)
            self.image = self.images[self.animation_index]
        if self.node is not None:
            self.x = self.node.x - self.width
            self.y = self.node.y - self.height

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))



class TravelButton(object):
    def __init__(self, parent):
        self.bg_rect = settings.REGION_MENUS['browser']['travel_rect']
        self.border_rect = settings.REGION_MENUS['browser']['travel_rect']
        self.text_rect = settings.REGION_MENUS['browser']['travel_text']
        self.state = "Active"
        self.hover = True
        self.parent = parent
        self.speed = 500
        self.time = 0
        self.dir = 1
        self.dim_color = (50, 50, 0)
        self.flash_color = (255, 255, 255)
        self.text_color = (150, 150, 0)
        self.color = (0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bg_rect, border_radius=8)
        settings.tw(surface, "TRAVEL", self.text_color, self.text_rect, settings.TEXT_FONT)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_rect, 8, border_radius=8)

    def update(self, dt):
        self.time += self.dir * dt
        if self.time > 500:
            self.time = 500
            self.dir *= -1
        elif self.time < 0:
            self.time = 0
            self.dir *= -1
        step = pt.easeInOutCubic(self.time / self.speed)
        color = (int(((self.flash_color[0] - self.dim_color[0]) * step) + self.dim_color[0]),
                 int(((self.flash_color[1] - self.dim_color[1]) * step) + self.dim_color[1]),
                 int(((self.flash_color[2] - self.dim_color[2]) * step) + self.dim_color[2]))
        for node in self.parent.nodes.sprites():
            if node.selected and node.travel:
                self.state = "Active"
                break
            else:
                self.state = "Dormant"
            self.hover = False
        if settings.click_check(self.bg_rect):
            self.hover = True
        if self.state == "Dormant":
            self.color = (50, 50, 50)
        elif self.state == "Active":
            if self.hover:
                self.color = (200, 200, 200)
            else:
                self.color = color

    def click(self):
        if settings.click_check(self.bg_rect):
            self.parent.travel()


class ShopButton(object):
    def __init__(self, parent):
        self.parent = parent
        self.state = "Hidden"
        self.bg_rect = [settings.X * 84 / 100, settings.Y * 2 / 100, settings.X * 13 / 100, settings.Y * 8 / 100]
        self.text_rect = [settings.X * 88 / 100, settings.Y * 4 / 100, settings.X * 9 / 100, settings.Y * 6 / 100]

    def draw(self, surface):
        if self.state == "Active":
            color = (40, 40, 40)
            if settings.click_check(self.bg_rect) and self.parent.state != "Event":
                color = (60, 60, 60)
            pygame.draw.rect(surface, color, self.bg_rect, border_radius=8)
            pygame.draw.rect(surface, (125, 125, 50), self.bg_rect, 5, border_radius=8)
            settings.tw(surface, "SHOP", (125, 125, 50), self.text_rect, settings.TEXT_FONT)

    def update(self, dt):
        if getattr(self.parent.party.node, 'type', None) == "Shop":
            self.state = "Active"
        else:
            self.state = "Hidden"

    def click(self):
        if self.state == "Active":
            if settings.click_check(self.bg_rect):
                self.parent.state = "Event"


class ExitButton(object):
    def __init__(self, parent):
        self.parent = parent
        self.state = "Hidden"
        self.bg_rect = [settings.X * 84 / 100, settings.Y * 2 / 100, settings.X * 13 / 100, settings.Y * 8 / 100]
        self.text_rect = [settings.X * 88 / 100, settings.Y * 4 / 100, settings.X * 9 / 100, settings.Y * 6 / 100]

    def draw(self, surface):
        if self.state == "Active":
            color = (40, 40, 40)
            if settings.click_check(self.bg_rect) and self.parent.state != "Event":
                color = (60, 60, 60)
            pygame.draw.rect(surface, color, self.bg_rect, border_radius=8)
            pygame.draw.rect(surface, (125, 50, 50), self.bg_rect, 5, border_radius=8)
            settings.tw(surface, "EXIT", (125, 50, 50), self.text_rect, settings.TEXT_FONT)

    def update(self, dt):
        if getattr(self.parent.party.node, 'type', None) == "Boss":
            self.state = "Active"
        else:
            self.state = "Hidden"

    def click(self):
        if self.state == "Active":
            if settings.click_check(self.bg_rect):
                self.parent.state = "Exit_Reqion"


class Resources(object):
    def __init__(self, parent):
        self.parent = parent

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['background 1 rect'], border_radius=6)
        pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['browser']['resources']['background 2 rect'],
                         border_radius=6)
        surface.blit(settings.REGION_STATIC_SPRITES['supplies icon'],
                     settings.REGION_MENUS['browser']['resources']['supplies icon pos'])
        surface.blit(settings.REGION_STATIC_SPRITES['elixir icon'],
                     settings.REGION_MENUS['browser']['resources']['elixir icon pos'])
        surface.blit(settings.REGION_STATIC_SPRITES['coin icon'],
                     settings.REGION_MENUS['browser']['resources']['coin icon pos'])
        surface.blit(settings.REGION_STATIC_SPRITES['charge icon'],
                     settings.REGION_MENUS['browser']['resources']['charge icon pos'])
        settings.tw(surface, str(self.parent.persist['gold']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['coin data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.parent.persist['supplies']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['supplies data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.parent.persist['chargers']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['charge data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.parent.persist['elixirs']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['elixir data rect'], settings.HEADING_FONT)

    def update(self, dt):
        pass

    def click(self):
        pass


class StatusBar(object):
    def __init__(self, parent):
        self.parent = parent
        self.party_population = 0
        self.offset = 17.5
        self.X = settings.X
        self.Y = settings.Y
        self.icon_pos = (self.X * 83 / 100, self.Y * 13 / 100)
        self.icon_bg_rect = [self.X * 82.5 / 100, self.Y * 12.5 / 100, self.X * 6 / 100, self.Y * 10 / 100]
        self.status_bg_rect = [self.X * 89 / 100, self.Y * 12.5 / 100, self.X * 10 / 100, self.Y * 10 / 100]
        self.hp_rect = [self.X * 91.75 / 100, self.Y * 13 / 100, self.X * 7 / 100, self.Y * 4 / 100]
        self.hp_data_rect = [self.X * 89 / 100, self.Y * 13 / 100, self.X * 8 / 100, self.Y * 4 / 100]
        self.mp_rect = [self.X * 91.75 / 100, self.Y * 18 / 100, self.X * 7 / 100, self.Y * 4 / 100]
        self.mp_data_rect = [self.X * 89 / 100, self.Y * 18 / 100, self.X * 8 / 100, self.Y * 4 / 100]
        self.equip_button = [self.X * 82.5 / 100, self.Y * 23.5 / 100, self.X * 8 / 100, self.Y * 5 / 100]
        self.skills_button = [self.X * 91 / 100, self.Y * 23.5 / 100, self.X * 8 / 100, self.Y * 5 / 100]
        self.color = (150, 150, 150)

    def update(self, dt):
        self.party_population = len(self.parent.persist['characters'])

    def draw(self, surface):
        for i, player in enumerate(self.parent.persist['characters']):
            pygame.draw.rect(surface, self.color,
                             [self.icon_bg_rect[0], self.icon_bg_rect[1] + (i * self.Y * self.offset),
                              self.icon_bg_rect[2], self.icon_bg_rect[3]], border_radius=6)
            pygame.draw.rect(surface, self.color,
                             [self.status_bg_rect[0], self.status_bg_rect[1] + (i * self.Y * self.offset),
                              self.status_bg_rect[2], self.status_bg_rect[3]], border_radius=6)
            pygame.draw.rect(surface, self.color,
                             [self.equip_button[0], self.equip_button[1] + (i * self.Y * self.offset),
                              self.equip_button[2], self.equip_button[3]], border_radius=6)
            pygame.draw.rect(surface, self.color,
                             [self.skills_button[0], self.skills_button[1] + (i * self.Y * self.offset),
                              self.skills_button[2], self.skills_button[3]], border_radius=6)
            surface.blit(settings.REGION_STATIC_SPRITES[player.current_class + "Icon"],
                         (self.icon_pos[0], self.icon_pos[1] + (i * self.Y * self.offset)))
            pygame.draw.rect(surface, (150, 0, 0),
                             [self.hp_rect[0], self.hp_rect[1] + (i * self.Y * self.offset), self.hp_rect[2],
                              self.hp_rect[3]])
            pygame.draw.rect(surface, (0, 150, 0),
                             [self.hp_rect[0] + (self.hp_rect[0] * (1 - player.hp / player.max_hp)),
                              self.hp_rect[1] + (i * self.Y * self.offset),
                              (self.hp_rect[2] * player.hp / player.max_hp), self.hp_rect[3]])
            pygame.draw.rect(surface, (0, 0, 0), self.hp_rect, 4)
            pygame.draw.rect(surface, (150, 0, 0),
                             [self.mp_rect[0], self.mp_rect[1] + (i * self.Y * self.offset), self.mp_rect[2],
                              self.mp_rect[3]])
            pygame.draw.rect(surface, (0, 150, 0),
                             [self.mp_rect[0] + (self.mp_rect[0] * (1 - player.mp / player.max_mp)),
                              self.mp_rect[1] + (i * self.Y * self.offset),
                              (self.mp_rect[2] * player.mp / player.max_mp), self.mp_rect[3]])
            pygame.draw.rect(surface, (0, 0, 0), self.mp_rect, 4)
            settings.tw(surface, 'hp', (0, 0, 0),
                        [self.hp_data_rect[0], self.hp_data_rect[1] + (i * self.Y * self.offset), self.hp_data_rect[2],
                         self.hp_data_rect[3]], settings.TEXT_FONT)
            settings.tw(surface, 'mp', (0, 0, 0),
                        [self.mp_data_rect[0], self.mp_data_rect[1] + (i * self.Y * self.offset), self.mp_data_rect[2],
                         self.mp_data_rect[3]], settings.TEXT_FONT)
            settings.tw(surface, 'equip', (0, 0, 0),
                        [self.equip_button[0], self.equip_button[1] + (i * self.Y * self.offset), self.equip_button[2],
                         self.equip_button[3]], settings.TEXT_FONT)
            settings.tw(surface, 'skills', (0, 0, 0),
                        [self.skills_button[0], self.skills_button[1] + (i * self.Y * self.offset),
                         self.skills_button[2], self.skills_button[3]], settings.TEXT_FONT)

    def click(self):
        for i, player in enumerate(self.parent.persist['characters']):
            if settings.click_check([self.equip_button[0], self.equip_button[1] + (i * self.Y * self.offset),
                                     self.equip_button[2], self.equip_button[3]]):
                self.parent.state = "Equip"
            if settings.click_check([self.skills_button[0], self.skills_button[1] + (i * self.Y * self.offset),
                                     self.skills_button[2], self.skills_button[3]]):
                self.parent.state = "Skill_Tree"


class Background(object):
    def __init__(self, parent, image):
        self.pos = (0, 0)
        self.parent = parent
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    def update(self, dt):
        pass


class Region(BaseState):
    def __init__(self):
        super(Region, self).__init__()
        self.next_state = "BATTLE"
        self.nodes = pygame.sprite.Group()
        self.selected_node = None
        self.party = Party(self)
        self.cursor = Cursor(self)
        self.buttons = [TravelButton(self), Resources(self), StatusBar(self), ShopButton(self), ExitButton(self)]
        self.equip_menu = settings.EquipMenu(self)
        self.skill_menu = settings.SkillTreeMenu(self)
        self.paths = []
        self.background = None
        self.state = "Browse"
        self.state_options = ["Browse", "Event", "Equip_menu", "Skill_tree_menu", "Options_menu", "Shop",
                              "Alt_Travel_Confirm"]
        self.overlay_image = pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                               r"\Region\Region_Overlay.png").convert_alpha()
        self.overlay_rect = [0, 0, self.overlay_image.get_width(), self.overlay_image.get_height()]

    def startup(self, persistent):
        self.persist = persistent
        if self.persist['region_generate']:
            self.region_generate()
        self.background = Background(self, settings.REGION_LAYOUTS[self.persist['region_type']][
            self.persist['region_layout']]["Image"])

    def handle_action(self, action):
        if self.state == "Browse":
            if action == "click":
                for button in self.buttons:
                    button.click()
                for node in self.nodes.sprites():
                    node.click()
            elif action == "mouse_move":
                pos = (int(pygame.mouse.get_pos()[0] * 100 / 1280), int(pygame.mouse.get_pos()[1] * 100 / 720))
                print(pos)
            elif action == "t":
                self.travel()
            elif action == "left" or action == "up" or action == "right" or action == "down":
                self.state = "Cursor_Move"
                self.cursor.visible = True

        elif self.state == "Event":
            if self.state == "Event":
                self.party.node.event.handle_action(action)

        elif self.state == "Equip":
            self.equip_menu.handle_action(action)

        elif self.state == "Skill_Tree":
            self.skill_menu.handle_action(action)

        elif self.state == "Options":
            pass

        elif self.state == "Inventory":
            pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.handle_action("up")
            elif event.key == pygame.K_DOWN:
                self.handle_action("down")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("right")
            elif event.key == pygame.K_LEFT:
                self.handle_action("left")
            elif event.key == pygame.K_RETURN:
                self.handle_action("return")
            elif event.key == pygame.K_t:
                self.handle_action("t")
            elif event.key == pygame.K_y:
                self.handle_action("y")
            elif event.key == pygame.K_TAB:
                self.handle_action("tab")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("backspace")
            elif event.key == pygame.K_ESCAPE:
                self.handle_action("escape")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
            elif event.button == 4:
                self.handle_action("wheel_up")
            elif event.button == 5:
                self.handle_action("wheel_down")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def update(self, dt):
        self.nodes.update(dt)
        self.party.update(dt)
        self.cursor.update(dt)
        for path in self.paths:
            path.update(dt)
        for button in self.buttons:
            button.update(dt)
        if self.state == "Event":
            self.party.node.event.update(dt)
        elif self.state == "Equip":
            self.equip_menu.update(dt)
        elif self.state == "Skill_Tree":
            self.skill_menu.update(dt)
        elif self.state == "Cursor_Move":
            self.cursor.move(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.background.draw(surface)
        for path in self.paths:
            path.draw(surface)
        self.nodes.draw(surface)
        #        for node in self.nodes.sprites():
        #            settings.tw(surface, node.type, (0, 0, 0), [node.x + 50, node.y + 50, 100, 100], settings.DETAIL_FONT)
        self.party.draw(surface)
        surface.blit(self.overlay_image, (0, 0))
        for button in self.buttons:
            button.draw(surface)
        self.cursor.draw(surface)
        if self.state == "Event":
            self.party.node.event.draw(surface)
        elif self.state == "Equip":
            self.equip_menu.draw(surface)
        elif self.state == "Skill_Tree":
            self.skill_menu.draw(surface)

    def region_generate(self):
        valid = False
        self.persist['node_group'] = pygame.sprite.Group()
        self.persist['party_group'] = pygame.sprite.Group()
        self.persist['nodes'] = []
        self.persist['portal'] = []
        region_options = []
        for option in settings.REGION_LAYOUTS[self.persist['region_type']]:
            region_options.append(option)
        self.persist['region_layout'] = region_layout = settings.choose_random(region_options)
        num_nodes = 30
        if 'num_nodes' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            num_nodes = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['num_nodes']
        knn = 4
        if 'knn' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            knn = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['knn']
        node_space = 100
        if 'node_space' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            node_space = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['node_space']
        space_probability = 100
        if 'space_probability' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            space_probability = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['space_probability']
        node_space_ll = 0
        if 'node_space_ll' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            node_space_ll = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['node_space_ll']
        node_space_ul = 350
        if 'node_space_ul' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            node_space_ul = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['node_space_ul']
        min_edge_angle = 15
        if 'min_edge_angle' in settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]:
            min_edge_angle = settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['min_edge_angle']
        node_list, edge_list, neighbors_dict, edge_dict, valid_path = None, None, None, None, None
        while not valid:
            node_list, edge_list, neighbors_dict, edge_dict, valid_path = network_generator.network_gen(
                X=settings.X, Y=settings.Y,
                shapes=settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['Shapes'],
                start_rect=settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['Start'],
                end_rect=settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['End'],
                positive=settings.REGION_LAYOUTS[self.persist['region_type']][region_layout]['Positive'],
                num_nodes=num_nodes, knn=knn, node_space=node_space, space_probability=space_probability,
                node_space_ll=node_space_ll, node_space_ul=node_space_ul, min_edge_angle=min_edge_angle)
            valid = valid_path
        for i, value in enumerate(node_list):
            if i == 0:
                self.nodes.add(Node(self, value[0], value[1], neighbors_dict[i], edge_dict[i], i, "Boss"))
            elif i == 1:
                self.nodes.add(Node(self, value[0], value[1], neighbors_dict[i], edge_dict[i], i, "Region Entry"))
            else:
                node_type = settings.node_assign_2(self)
                self.nodes.add(Node(self, value[0], value[1], neighbors_dict[i], edge_dict[i], i, node_type))
        for node in self.nodes.sprites():
            node.event = settings.event_caller(self, node)
            if node.index == 1:
                self.party.node = node
        self.persist['current_position'] = 1
        self.persist['region_generate'] = False
        for key in edge_dict.keys():
            for pair in edge_dict[key]:
                node_1 = None
                node_2 = None
                for node in self.nodes.sprites():
                    if node.index == key:
                        node_1 = node
                    if pair[1] == node.index:
                        node_2 = node
                    if node_2 is not None and node_1 is not None:
                        break
                if node_2 is not None and node_1 is not None:
                    self.paths.append(Path(self, node_1, node_2))

    def travel(self):
        if self.selected_node is not None:
            if self.selected_node.travel and self.selected_node.selected and self.party.node.index in \
                    self.selected_node.neighbors:
                self.party.node = self.selected_node
                self.selected_node.selected = False
                self.selected_node = None
                if self.party.node.state == "Unexplored":
                    self.state = "Event"
                    self.party.node.state = "Explored"
                    self.party.node.visited = True
