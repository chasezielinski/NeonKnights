import math
import copy
import pygame
import pytweening
import settings
from base import BaseState
import pytweening as pt
from settings import X, Y, REGION_MENUS, click_check, tw, TEXT_COLOR, TEXT_FONT, SELECTED_COLOR, Equipment, Stat, \
    EquipmentType, SkillDetail, HEADING_FONT, NetworkGetter


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


class Path(object):
    def __init__(self, parent, node_1, node_2):
        self.parent = parent
        self.node_1 = self.get_node(node_1)
        self.node_2 = self.get_node(node_2)
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

    def get_node(self, index):
        for node in self.parent.nodes.sprites():
            if index == node.index:
                return node


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
        dir = [0, 0]
        if list(pygame.key.get_pressed())[79]:
            dir[0] += 1
            flag = False
        if list(pygame.key.get_pressed())[80]:
            dir[0] -= 1
            flag = False
        if list(pygame.key.get_pressed())[81]:
            dir[1] += 1
            flag = False
        if list(pygame.key.get_pressed())[82]:
            dir[1] -= 1
            flag = False
        if flag:
            self.move_speed = 0
            self.parent.state = "Browse"
            self.snap()
        else:
            if (dir[0]**2 + dir[1]**2) == 2:
                dir_factor = 1.41
            else:
                dir_factor = 1
            if dir[1] != 0:
                self.y += (dt * self.move_speed / (self.move_speed + 500))/(dir[1] * dir_factor * 2)
            if dir[0] != 0:
                self.x += (dt * self.move_speed / (self.move_speed + 500))/(dir[0] * dir_factor * 2)
            self.move_speed += dt

    def update(self, dt):
        if not self.visible:
            self.x = self.parent.party.x
            self.y = self.parent.party.y
        elif self.parent.state == "Browse":
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

    def handle_action(self, action):
        if action == 'return':
            if self.visible and self.target_node is not None:
                for node in self.parent.nodes.sprites():
                    node.selected = False
                self.target_node.selected = True
                self.parent.selected_node = self.target_node
                self.visible = False


class Party(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x = 2 * X
        self.y = 2 * Y
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
        self.bg_rect = [X * 14 / 100, Y * 2 / 100, X * 14 / 100, Y * 9 / 100]
        self.border_rect = [X * 14 / 100, Y * 2 / 100, X * 14 / 100, Y * 9 / 100]
        self.text_rect = [X * 17 / 100, Y * 5 / 100, X * 14 / 100, Y * 1 / 16]
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
        tw(surface, "TRAVEL", self.text_color, self.text_rect, TEXT_FONT)
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


class ResourceDisplay(object):
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
            surface.blit(player.status_icon, (self.icon_pos[0], self.icon_pos[1] + (i * self.Y * self.offset)))
            pygame.draw.rect(surface, (150, 0, 0),
                             [self.hp_rect[0], self.hp_rect[1] + (i * self.Y * self.offset), self.hp_rect[2],
                              self.hp_rect[3]])
            pygame.draw.rect(surface, (0, 150, 0),
                             [self.hp_rect[0] + (self.hp_rect[0] * (1 - player.hp / player.get_stat(settings.Stat.HP))),
                              self.hp_rect[1] + (i * self.Y * self.offset),
                              (self.hp_rect[2] * player.hp / player.get_stat(settings.Stat.HP)), self.hp_rect[3]])
            pygame.draw.rect(surface, (0, 0, 0), self.hp_rect, 4)
            pygame.draw.rect(surface, (150, 0, 0),
                             [self.mp_rect[0], self.mp_rect[1] + (i * self.Y * self.offset), self.mp_rect[2],
                              self.mp_rect[3]])
            pygame.draw.rect(surface, (0, 150, 0),
                             [self.mp_rect[0] + (self.mp_rect[0] * (1 - player.mp / player.get_stat(settings.Stat.MP))),
                              self.mp_rect[1] + (i * self.Y * self.offset),
                              (self.mp_rect[2] * player.mp / player.get_stat(settings.Stat.MP)), self.mp_rect[3]])
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
        self.buttons = [TravelButton(self), ResourceDisplay(self), StatusBar(self), ShopButton(self), ExitButton(self)]
        self.equip_menu = EquipMenu(self)
        self.skill_menu = SkillTreeMenu(self)
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
            elif action == 'return':
                self.cursor.handle_action(action)

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
            elif event.key == pygame.K_1:
                self.handle_action("1")
            elif event.key == pygame.K_2:
                self.handle_action("2")
            elif event.key == pygame.K_3:
                self.handle_action("3")
            elif event.key == pygame.K_4:
                self.handle_action("4")
            elif event.key == pygame.K_5:
                self.handle_action("5")
            elif event.key == pygame.K_6:
                self.handle_action("6")
            elif event.key == pygame.K_7:
                self.handle_action("7")
            elif event.key == pygame.K_8:
                self.handle_action("8")
            elif event.key == pygame.K_9:
                self.handle_action("9")
            elif event.key == pygame.K_0:
                self.handle_action("0")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")
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
        self.persist['Music'].update(dt, self)
        self.persist['SFX'].update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background, (0, 0))
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
        self.persist['node_group'] = pygame.sprite.Group()
        self.persist['party_group'] = pygame.sprite.Group()
        self.persist['nodes'] = []
        self.persist['portal'] = []
        data = settings.RegionBuilder().get_region(self.persist['region_type'])
        self.background = settings.ImageLoader().load_image(data["Image"])
        network, random_state = NetworkGetter().get_network(data)
        node_list, edge_list, neighbors_dict, edge_dict = network[0], network[1], network[2], network[3]

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
        for value in edge_dict:
            self.paths.append(Path(self, value[0], value[1]))

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


class EquipMenu(object):
    def __init__(self, parent):
        self.scroll_index = 0
        self.inventory_selection_index = -1
        self.equip_selection_index = -1
        self.menu_horizontal_index = "None"
        self.relative_index = 0
        self.display_index = 0
        self.parent = parent
        self.player_index = None
        self.bg_1_rect = [X * 8 / 100, Y * 11 / 100, X * 76 / 100, Y * 85 / 100]
        self.bg_2_rect = [X * 8.5 / 100, Y * 12 / 100, X * 75 / 100, Y * 83 / 100]
        self.slot_rects = REGION_MENUS['equip menu']['Top_Slot_Rect']
        self.equip_rects = REGION_MENUS['equip menu']['Top_Equip_Rect']
        self.inventory_rects = REGION_MENUS['equip menu']['inventory rects']

    def update(self, dt):
        if not self.player_index:
            self.player_index = self.parent.persist['characters'][0]

    def right_index(self):
        index = self.parent.persist['characters'].index(self.player_index)
        index += 1
        index %= len(self.parent.persist['characters'])
        self.player_index = self.parent.persist['characters'][index]

    def left_index(self):
        index = self.parent.persist['characters'].index(self.player_index)
        index -= 1
        index %= len(self.parent.persist['characters'])
        self.player_index = self.parent.persist['characters'][index]

    def handle_action(self, action):
        if action == "mouse_move":
            pos = (int(pygame.mouse.get_pos()[0] * 100 / 1280), int(pygame.mouse.get_pos()[1] * 100 / 720))
            print(pos)
            for n, equip_slot in enumerate(self.player_index.get_equipment_options()):
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
        for n, equip_slot in enumerate(self.player_index.get_equipment_options()):
            tw(surface, equip_slot, TEXT_COLOR, self.slot_rects[n], TEXT_FONT)
            if equip_slot in self.player_index.equipment.keys():
                text = self.player_index.equipment[equip_slot].name
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
        equipped = None
        selected = None
        if len(self.parent.persist['inventory']) > self.inventory_selection_index >= 0:
            selected = self.parent.persist['inventory'][self.inventory_selection_index]
        if type(selected).__name__ in self.player_index.equipment.keys():
            equipped = self.player_index.equipment[type(selected).__name__]
        potential = self.potential_stat(equipped=equipped, prospect=selected)
        for key, value in enumerate(REGION_MENUS['equip menu']['Stat_Rects']):
            stat = self.player_index.get_stat(Stat[value.upper()])
            if value == 'hp':
                stat2 = self.player_index.hp
                tw(surface, value + ':' + str(stat2).rjust(8 - len(value)) + '/' + str(stat), TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
            elif value == 'mp':
                stat2 = self.player_index.mp
                tw(surface, value + ':' + str(stat2).rjust(9 - len(value)) + '/' + str(stat), TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
            else:
                tw(surface, value + ':' + str(stat).rjust(12 - len(value)), TEXT_COLOR,
                   REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                if Stat[value.upper()] in potential.keys():
                    if value == 'defense' or value == 'spirit' or value == 'luck':
                        if potential[Stat[value.upper()]] < 0:
                            tw(surface, str(potential[Stat[value.upper()]]).rjust(22 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[Stat[value.upper()]])).rjust(22
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value], TEXT_FONT)
                    elif value == 'magic' or value == 'speed':
                        if potential[Stat[value.upper()]] < 0:
                            tw(surface, str(potential[Stat[value.upper()]]).rjust(20 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[Stat[value.upper()]])).rjust(20
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                    elif value == 'strength':
                        if potential[Stat[value.upper()]] < 0:
                            tw(surface, str(potential[Stat[value.upper()]]).rjust(23 - len(value)), (150, 0, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)
                        else:
                            tw(surface, ('+' + str(potential[Stat[value.upper()]])).rjust(23
                                                                            - len(value)), (0, 150, 0),
                               REGION_MENUS['equip menu']['Stat_Rects'][value],
                               TEXT_FONT)

    def potential_stat(self, equipped=None, prospect=None) -> dict:
        potential = {Stat.HP: 0, Stat.MP: 0, Stat.STRENGTH: 0, Stat.DEFENSE: 0, Stat.MAGIC: 0, Stat.SPIRIT: 0,
                     Stat.SPEED: 0, Stat.LUCK: 0, Stat.CRITICAL_RATE: 0, Stat.CRITICAL_DAMAGE: 0}

        if type(prospect).__name__.upper() in EquipmentType.__members__:
            for key in potential.keys():
                new = 0
                if prospect:
                    new = prospect.get_stat(key)
                old = 0
                if equipped:
                    old = equipped.get_stat(key)
                potential[key] = new - old

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