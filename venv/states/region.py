import math
import random
import copy
import network_generator
import pygame
import settings
from base import BaseState


class Party(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 2 * settings.X
        self.y = 2 * settings.Y
        self.image = pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Region\D20_Party.png")
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 55, 202))

    def draw(self, surface):
        self.draw(surface)

    def update(self, x, y):
        self.rect = pygame.Rect(x - (self.image.get_width() / 4), y - (self.image.get_height() / 2),
                                self.image.get_width(),
                                self.image.get_height())


class Node(pygame.sprite.Sprite):
    def __init__(self, x, y, neighbors, edges, state, node_type, event_type):
        pygame.sprite.Sprite.__init__(self)
        self.index = state
        self.seen = False
        self.x = x
        self.y = y
        if state == 0:
            self.state = "Exit"
        elif state == 1:
            self.state = "Explored"
        else:
            self.state = "Unexplored"
        self.type = node_type
        self.event = event_type
        self.selected = False
        self.hover = False
        self.neighbors = neighbors
        self.edges = edges
        self.images_unexplored = []
        self.images_explored = []
        self.images_exit = []
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet1.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet2.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet3.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet4.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet5.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet6.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet7.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet8.png"))
        self.images_unexplored.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet9.png"))
        self.images_unexplored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet10.png"))
        self.images_unexplored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet11.png"))
        self.images_unexplored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet12.png"))
        self.images_unexplored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Sheet13.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored1.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored2.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored3.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored4.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored5.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored6.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored7.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored8.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored9.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored10.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored11.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored12.png"))
        self.images_explored.append(pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Node_Explored13.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node1.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node2.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node3.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node4.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node5.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node6.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node7.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node8.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node9.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node10.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node11.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node12.png"))
        self.images_exit.append(
            pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Node\Exit_Node13.png"))
        self.animation_index = 0
        self.image = self.images_unexplored[self.animation_index]
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        for i, value in enumerate(self.images_unexplored):
            self.images_unexplored[i].set_colorkey((255, 55, 202))
            self.images_explored[i].set_colorkey((255, 55, 202))
            self.images_exit[i].set_colorkey((255, 55, 202))

    def update(self, dt):
        if self.state == "Unexplored":
            if self.selected:
                self.animation_index += 0.375
                self.animation_index %= len(self.images_unexplored)
            else:
                self.animation_index = 0
            self.image = self.images_unexplored[math.floor(self.animation_index)]

        if self.state == "Explored":
            if self.selected:
                self.animation_index += 0.375
                self.animation_index %= len(self.images_explored)
            else:
                self.animation_index = 0
            self.image = self.images_explored[math.floor(self.animation_index)]

        if self.state == "Exit":
            if self.selected:
                self.animation_index += 0.375
                self.animation_index %= len(self.images_exit)
            else:
                self.animation_index = 0
            self.image = self.images_exit[math.floor(self.animation_index)]

    def draw(self):
        pass

    def cleanup(self):
        self.kill()


class Region(BaseState):
    def __init__(self):
        super(Region, self).__init__()
        self.group_index = 0
        self.equip_index = 0
        self.inventory_display_index = 0
        self.equipment_inventory_selection_index = 0
        self.inv_size = 0
        self.inventory_selection_index_relative = 0
        self.equipment_menu_horizontal_index = "Equip"
        self.equipment_selection_index = 0
        self.node_browse_index = 0
        self.shop_state = "Buy"
        self.next_state = "BATTLE"
        self.inventory_menu_player_index = 'player_a'
        self.alt_travel_index = 3
        self.nodes = []
        self.hover = False
        self.state = "Browse"
        self.state_options = ["Browse", "Event", "Equip_menu", "Skill_tree_menu", "Options_menu", "Shop",
                              "Alt_Travel_Confirm"]
        self.overlay_image = pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                               r"\Region\Region_Overlay.png").convert_alpha()
        self.overlay_rect = [0, 0, self.overlay_image.get_width(), self.overlay_image.get_height()]
        self.clock = pygame.time.Clock()

    def startup(self, persistent):
        self.persist = persistent
        if self.persist['region_generate']:
            self.region_generate()
        self.character_stat_update()
        self.character_ability_update()

    def handle_action(self, action):
        if self.state == "Browse":
            if action == "t":
                for node in self.persist['nodes'][self.persist['current_position']].neighbors:
                    if self.persist['nodes'][node].selected:
                        self.persist['current_position'] = node
                        self.handle_action("travel")
                        break
                if self.persist['party_abilities'].fly and self.persist['party_abilities'].fly_charges > 0:
                    for value in self.persist['nodes']:
                        if value.selected:
                            self.state = "Alt_Travel_Confirm"
                elif self.persist['party_abilities'].fast_travel:
                    for value in self.persist['nodes']:
                        if value.selected and value.state == "Explored":
                            self.state = "Alt_Travel_Confirm"
                elif self.persist['party_abilities'].teleport:
                    for value in self.persist['nodes']:
                        if value.selected:
                            self.state = "Alt_Travel_Confirm"
            if action == "travel":
                self.persist['nodes'][self.persist['current_position']].selected = False
                #  Conserve Supplies **************************************************************************
                if self.persist['party_abilities'].conserve_supplies and settings.random_int(0, 100) < 50:
                    pass
                else:
                    if self.persist['supplies'] > 0:
                        self.persist['supplies'] -= 1
                        self.party_regen()
                    else:
                        for player in self.persist['characters']:
                            self.persist['characters'][player].hp -= int(
                                0.1 * self.persist['characters'][player].max_hp)
                            if self.persist['characters'][player].hp < 0:
                                self.persist['characters'][player].hp = 0
                if self.persist['nodes'][self.persist['current_position']].state == "Unexplored":
                    self.persist['nodes'][self.persist['current_position']].state = "Explored"
                    self.node_event()
                    print(self.persist['nodes'][self.persist['current_position']].type)
                    print(self.persist['nodes'][self.persist['current_position']].event)
                    self.state = "Event"
            elif action == "tab":
                self.state = "Equip_menu"
            elif action == "click":
                print(pygame.mouse.get_pos())
                for node in self.persist['nodes']:
                    print(node.index, node.x, node.y)
                if settings.click_check(settings.REGION_MENUS['browser']['travel_rect']):
                    self.handle_action("t")
                else:
                    pos = pygame.mouse.get_pos()
                    for node in self.persist['node_group']:
                        node.selected = False
                        if node.rect.collidepoint(pos):
                            node.selected = True
                if 'player_a' in self.persist['characters']:
                    if settings.click_check(
                            settings.REGION_MENUS['browser']['resources']['player_a eq menu bg rect']):
                        self.state = "Equip_menu"
                    elif settings.click_check(
                            settings.REGION_MENUS['browser']['resources']['player_a st menu bg rect']):
                        self.state = "Skill_tree_menu"
                if settings.click_check(settings.REGION_MENUS['browser']['shop_toggle_rect']):
                    if hasattr(self.persist['nodes'][self.persist['current_position']], 'event_data'):
                        if hasattr(self.persist['nodes'][self.persist['current_position']], 'event'):
                            if self.persist['nodes'][self.persist['current_position']].event == "Shop":
                                self.state = "Shop"
                if self.persist['chargers'] > 2 and self.persist['elixirs'] > 2 and self.persist[
                    'party_abilities'].create_portal:
                    if settings.click_check(settings.REGION_MENUS['browser']['portal_rect']):
                        self.state = "Construct_Portal"

            elif action == "mouse_move":
                self.hover = False
                for node in self.persist['node_group']:
                    node.hover = False
                    if node.rect.collidepoint(pygame.mouse.get_pos()):
                        node.hover = True
                        self.hover = True

            elif action == "left" or action == "up":
                for node in self.persist['nodes']:
                    node.selected = False
                self.node_browse_index += 1
                self.node_browse_index %= len(self.persist['nodes'][self.persist['current_position']].neighbors)
                self.persist['nodes'][self.persist['nodes'][self.persist['current_position']].neighbors[
                    self.node_browse_index]].selected = True
            elif action == "right" or action == "down":
                for node in self.persist['nodes']:
                    node.selected = False
                self.node_browse_index -= 1
                self.node_browse_index %= len(self.persist['nodes'][self.persist['current_position']].neighbors)
                self.persist['nodes'][self.persist['nodes'][self.persist['current_position']].neighbors[
                    self.node_browse_index]].selected = True

        elif self.state == "Event":
            if action == "up":
                self.persist['nodes'][self.persist['current_position']].event_data.option_index += 1
                self.persist['nodes'][self.persist['current_position']].event_data.option_index %= \
                    len(self.persist['nodes'][self.persist['current_position']].event_data.options) + 1
            elif action == "down":
                self.persist['nodes'][self.persist['current_position']].event_data.option_index -= 1
                self.persist['nodes'][self.persist['current_position']].event_data.option_index %= \
                    len(self.persist['nodes'][self.persist['current_position']].event_data.options) + 1
            elif action == "return":
                options = self.persist['nodes'][self.persist['current_position']].event_data.weights[
                    self.persist['nodes'][self.persist['current_position']].event_data.option_index][0]
                weights = self.persist['nodes'][self.persist['current_position']].event_data.weights[
                    self.persist['nodes'][self.persist['current_position']].event_data.option_index][1]
                outcome = random.choices(options, weights)[0]
                if outcome == 'Battle':
                    self.done = True
                    self.next_state = "BATTLE"
                    self.state = "Browse"
                elif outcome == 'Shop':
                    self.state = "Shop"
                elif outcome == 'Escape':
                    self.state = "Browse"
            elif action == "mouse_move":
                options = getattr(self.persist['nodes'][self.persist['current_position']].event_data, 'options',
                                  ['none'])
                rects = settings.REGION_MENUS['event']['option rects']
                for i, node in enumerate(options[0]):
                    if settings.click_check(rects[i]):
                        self.persist['nodes'][self.persist['current_position']].event_data.option_index = i
            elif action == "click":
                options = getattr(self.persist['nodes'][self.persist['current_position']].event_data, 'options',
                                  ['none'])
                rects = settings.REGION_MENUS['event']['option rects']
                for i, node in enumerate(options[0]):
                    if settings.click_check(rects[i]):
                        if self.persist['nodes'][self.persist['current_position']].event_data.option_index == i:
                            self.handle_action("return")

        elif self.state == "Equip_menu":
            if action == "tab":
                self.state = "Skill_tree_menu"
            elif action == "backspace":
                self.state = "Browse"
            elif action == "up":
                if self.equipment_menu_horizontal_index == "Equip":
                    self.equipment_selection_index -= 1
                    self.equipment_selection_index %= \
                        len(self.persist['characters'][self.inventory_menu_player_index].equipment_options)
                elif self.equipment_menu_horizontal_index == "Inventory":
                    if self.inventory_selection_index_relative > 0:
                        self.equipment_inventory_selection_index -= 1
                        self.inventory_selection_index_relative -= 1
                    elif len(self.persist['inventory']) > 12 and self.inventory_display_index > 0:
                        self.inventory_display_index -= 1
            elif action == "down":
                if self.equipment_menu_horizontal_index == "Equip":
                    self.equipment_selection_index += 1
                    self.equipment_selection_index %= \
                        len(self.persist['characters'][self.inventory_menu_player_index].equipment_options)
                elif self.equipment_menu_horizontal_index == "Inventory":
                    if self.inventory_selection_index_relative == 12 and self.equipment_inventory_selection_index < len(self.persist['inventory']) - 1:
                        self.equipment_inventory_selection_index += 1
                        self.inventory_display_index += 1
                    elif self.inventory_selection_index_relative < 12:
                        self.equipment_inventory_selection_index += 1
                        self.inventory_selection_index_relative += 1
            elif action == "left":
                if self.equipment_menu_horizontal_index == "Equip":
                    self.equipment_menu_horizontal_index = "Inventory"
                else:
                    self.equipment_menu_horizontal_index = "Equip"
            elif action == "right":
                if self.equipment_menu_horizontal_index == "Inventory":
                    self.equipment_menu_horizontal_index = "Equip"
                else:
                    self.equipment_menu_horizontal_index = "Inventory"
            elif action == "return":
                self.equip_unequip()
                self.character_stat_update()
                self.character_ability_update()
            elif action == "mouse_move":
                for value in settings.REGION_MENUS['equip menu']['Top_Equip_Rect']:
                    if settings.click_check(settings.REGION_MENUS['equip menu']['Top_Equip_Rect'][value]):
                        self.equipment_selection_index = value
                        self.equipment_menu_horizontal_index = "Equip"
                        break
                    else:
                        self.equipment_selection_index = -1
                for key in settings.REGION_MENUS['equip menu']['inventory rects'].keys():
                    if settings.click_check(settings.REGION_MENUS['equip menu']['inventory rects'][key]):
                        self.equipment_inventory_selection_index = key + self.inventory_display_index
                        self.inventory_selection_index_relative = key
                        self.equipment_menu_horizontal_index = "Inventory"
                        break
                    else:
                        self.equipment_inventory_selection_index = -1
            elif action == "click":
                self.handle_action("mouse_move")
                self.equip_unequip()

        elif self.state == "Skill_tree_menu":
            if action == "tab":
                self.state = "Equip_menu"
            elif action == "backspace":
                self.state = "Browse"

        elif self.state == "Options_menu":
            pass

        elif self.state == "Shop":
            shop = self.persist['nodes'][self.persist['current_position']].event_data.shop
            if action == "backspace":
                self.state = "Browse"
            if action == "mouse_move":
                pos = pygame.mouse.get_pos()
                apos = (pos[0] * 100 / settings.X, pos[1] * 100 / settings.Y)
                print(apos)
            if self.shop_state == "Buy":
                if action == "tab":
                    self.shop_state = "Sell"
                elif action == "click":
                    if settings.click_check(settings.REGION_MENUS['shop']['supplies_label']):
                        if self.persist['gold'] > shop["Supplies"]["Price"] and shop["Supplies"]["Stock"] > 0:
                            self.persist['gold'] -= shop["Supplies"]["Price"]
                            self.persist['supplies'] += 1
                            shop["Supplies"]["Stock"] -= 1
                    elif settings.click_check(settings.REGION_MENUS['shop']['chargers_label']):
                        if self.persist['gold'] > shop["Charger"]["Price"] and shop["Charger"]["Stock"] > 0:
                            self.persist['gold'] -= shop["Charger"]["Price"]
                            self.persist['chargers'] += 1
                            shop["Charger"]["Stock"] -= 1
                    elif settings.click_check(settings.REGION_MENUS['shop']['elixirs_label']):
                        if self.persist['gold'] > shop["Elixir"]["Price"] and shop["Elixir"]["Stock"] > 0:
                            self.persist['gold'] -= shop["Elixir"]["Price"]
                            self.persist['elixirs'] += 1
                            shop["Elixir"]["Stock"] -= 1
                    elif settings.click_check(settings.REGION_MENUS['shop']['sell_button_top']):
                        self.shop_state = "Sell"
            elif self.shop_state == "Sell":
                if action == "tab":
                    self.shop_state = "Buy"
                elif action == "click":
                    if settings.click_check(settings.REGION_MENUS['shop']['buy_button_top']):
                        self.shop_state = "Buy"

        elif self.state == "Alt_Travel_Confirm":
            if action == "backspace":
                self.state = "Browse"
            elif action == "click":
                if settings.click_check(settings.REGION_MENUS[self.state]['FT_Rect']):
                    self.handle_action("fast_travel")
                elif settings.click_check(settings.REGION_MENUS[self.state]['Fly_Rect']):
                    self.handle_action("fly")
                elif settings.click_check(settings.REGION_MENUS[self.state]['Teleport_Rect']):
                    self.handle_action("teleport")
            elif action == "left":
                self.alt_travel_index -= 1
                if self.alt_travel_index < 0:
                    self.alt_travel_index = 2
            elif action == "right":
                self.alt_travel_index += 1
                self.alt_travel_index %= 3
            elif action == "return":
                if self.alt_travel_index == 1:
                    self.handle_action("fly")
                elif self.alt_travel_index == 0:
                    self.handle_action("fast_travel")
                elif self.alt_travel_index == 2:
                    self.handle_action("teleport")
            elif action == "mouse_move":
                self.alt_travel_index = 3
                if settings.click_check(settings.REGION_MENUS['Alt_Travel_Confirm']['FT_Rect']):
                    self.alt_travel_index = 0
                elif settings.click_check(settings.REGION_MENUS['Alt_Travel_Confirm']['Fly_Rect']):
                    self.alt_travel_index = 1
                elif settings.click_check(settings.REGION_MENUS['Alt_Travel_Confirm']['Teleport_Rect']):
                    self.alt_travel_index = 2
            elif action == "fly":
                if self.persist['party_abilities'].fly_charges > 0 and self.persist['party_abilities'].fly:
                    for node in self.persist['nodes']:
                        if node.selected:
                            self.persist['party_abilities'].fly_charges -= 1
                            self.persist['current_position'] = node.index
                            self.state = "Browse"
                            if self.persist['nodes'][self.persist['current_position']].state == "Unexplored":
                                self.persist['nodes'][self.persist['current_position']].state = "Explored"
                                self.node_event()
                                print(self.persist['nodes'][self.persist['current_position']].type)
                                print(self.persist['nodes'][self.persist['current_position']].event)
                                self.state = "Event"
            elif action == "fast_travel":
                if self.persist['elixirs'] > 1 and self.persist['party_abilities'].fast_travel:
                    for node in self.persist['nodes']:
                        if node.selected and node.state == "Explored":
                            self.persist['elixirs'] -= 1
                            self.persist['current_position'] = node.index
                            self.state = "Browse"
            elif action == "teleport":
                if self.persist['elixirs'] > 2 and self.persist['party_abilities'].teleport:
                    for node in self.persist['nodes']:
                        if node.selected:
                            self.persist['elixirs'] -= 2
                            self.persist['current_position'] = node.index
                            self.state = "Browse"
                            if self.persist['nodes'][self.persist['current_position']].state == "Unexplored":
                                self.persist['nodes'][self.persist['current_position']].state = "Explored"
                                self.node_event()
                                print(self.persist['nodes'][self.persist['current_position']].type)
                                print(self.persist['nodes'][self.persist['current_position']].event)
                                self.state = "Event"

        elif self.state == "Construct_Portal":
            if action == "click":
                if settings.click_check(settings.REGION_MENUS['browser']['portal_rect']):
                    for node in self.persist['nodes']:
                        if node.selected:
                            self.persist['nodes'][self.persist['current_position']].neighbors.append(node.index)
                            node.neighbors.append(self.persist['nodes'][self.persist['current_position']].index)
                            self.persist['portal'].append([(node.x, node.y), (
                                self.persist['nodes'][self.persist['current_position']].x,
                                self.persist['nodes'][self.persist['current_position']].y)])
                            self.persist['elixirs'] -= 2
                            self.persist['chargers'] -= 2
                            self.state = "Browse"
                else:
                    pos = pygame.mouse.get_pos()
                    for node in self.persist['node_group']:
                        node.selected = False
                        if node.rect.collidepoint(pos):
                            node.selected = True
            elif action == "mouse_move":
                self.hover = False
                for node in self.persist['nodes']:
                    node.hover = False
                    if node.rect.collidepoint(pygame.mouse.get_pos()):
                        node.hover = True
                        self.hover = True
            elif action == "left" or action == "up":
                for node in self.persist['nodes']:
                    node.selected = False
                self.node_browse_index += 1
                self.node_browse_index %= len(self.persist['nodes'][self.persist['current_position']].neighbors)
                self.persist['nodes'][self.persist['nodes'][self.persist['current_position']].neighbors[
                    self.node_browse_index]].selected = True
            elif action == "right" or action == "down":
                for node in self.persist['nodes']:
                    node.selected = False
                self.node_browse_index -= 1
                self.node_browse_index %= len(self.persist['nodes'][self.persist['current_position']].neighbors)
                self.persist['nodes'][self.persist['nodes'][self.persist['current_position']].neighbors[
                    self.node_browse_index]].selected = True
            elif action == "backspace":
                self.state = "Browse"

    def equip_unequip(self):
        if self.equipment_menu_horizontal_index == "Equip":
            slot = self.persist['characters'][self.inventory_menu_player_index].equipment_options[
                self.equipment_selection_index]
            if slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                self.persist['inventory'].append(
                    copy.deepcopy(self.persist['characters'][self.inventory_menu_player_index].equipment[slot]))
                del (self.persist['characters'][self.inventory_menu_player_index].equipment[slot])

        elif self.equipment_menu_horizontal_index == "Inventory" and 0 <= self.equipment_inventory_selection_index <= len(self.persist['inventory'])-1 :
            if hasattr(self.persist['inventory'][self.equipment_inventory_selection_index], 'slot'):
                slot = self.persist['inventory'][self.equipment_inventory_selection_index].slot
                if slot in self.persist['characters'][self.inventory_menu_player_index].equipment_options:
                    if slot in self.persist['characters'][self.inventory_menu_player_index].equipment:
                        self.persist['inventory'].append(
                            copy.deepcopy(self.persist['characters'][self.inventory_menu_player_index].equipment[slot]))
                        del (self.persist['characters'][self.inventory_menu_player_index].equipment[slot])
                    self.persist['characters'][self.inventory_menu_player_index].equipment[slot] = copy.deepcopy(
                        self.persist['inventory'][self.equipment_inventory_selection_index])
                    del self.persist['inventory'][self.equipment_inventory_selection_index]
        self.character_stat_update()
        self.character_ability_update()

    def update(self, dt):
        if self.state == "Browse":
            self.persist['node_group'].update(dt)
            self.mouse_hover()
            self.persist['party'].update(self.persist['nodes'][self.persist['current_position']].x,
                                         self.persist['nodes'][self.persist['current_position']].y)
        if self.state == "Event":
            if self.persist['nodes'][self.persist['current_position']].event_data.event_done:
                self.state = "Browse"
        if self.state == "Equip_menu":
            pass
        if self.state == "Skill_tree_menu":
            pass
        if self.state == "Options_menu":
            pass
        if self.state == "Shop":
            pass
        if self.state == "Construct_Portal":
            self.persist['node_group'].update(dt)
            self.mouse_hover()
            self.persist['party'].update(self.persist['nodes'][self.persist['current_position']].x,
                                         self.persist['nodes'][self.persist['current_position']].y)

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
                self.handle_action("backspace")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def party_regen(self):
        hp_regen = 0.1
        mp_regen = 0
        if self.persist['party_abilities'].mp_regen_travel:
            mp_regen = 0.1
        if self.persist['party_abilities'].boosted_regen_travel:
            mp_regen *= 2
            hp_regen *= 2
        for player in self.persist['characters']:
            self.persist['characters'][player].hp += int(
                hp_regen * self.persist['characters'][player].max_hp)
            if self.persist['characters'][player].hp > self.persist['characters'][player].max_hp:
                self.persist['characters'][player].hp = self.persist['characters'][player].max_hp
            self.persist['characters'][player].mp += int(
                mp_regen * self.persist['characters'][player].max_mp)
            if self.persist['characters'][player].mp > self.persist['characters'][player].max_mp:
                self.persist['characters'][player].mp = self.persist['characters'][player].max_mp

    def draw(self, surface):
        surface.fill(pygame.Color("green"))
        if 'region_layout' in self.persist:
            surface.blit(settings.REGION_LAYOUTS[self.persist['region_type']][self.persist['region_layout']]["Image"],
                         (0, 0))

        # PATH VISION **********************************************************************************************************

        if self.persist['party_abilities'].path_vision:
            if self.persist['party_abilities'].static_path:
                for node in self.persist['node_group']:
                    for i, value in enumerate(node.edges):
                        pygame.draw.line(surface, (0, 0, 0), (self.persist['nodes'][value[0]].x + 16,
                                                              self.persist['nodes'][value[0]].y + 16),
                                         (self.persist['nodes'][value[1]].x + 16, self.persist['nodes'][value[1]].y +
                                          16), 3)
            else:
                for node in self.persist['node_group']:
                    if node.hover:
                        for i, value in enumerate(node.edges):
                            pygame.draw.line(surface, (0, 0, 0), (self.persist['nodes'][value[0]].x + 16,
                                                                  self.persist['nodes'][value[0]].y + 16),
                                             (
                                                 self.persist['nodes'][value[1]].x + 16,
                                                 self.persist['nodes'][value[1]].y +
                                                 16), 3)
                        break
        else:
            if self.persist['party_abilities'].static_path:
                for i, value in enumerate(self.persist['nodes'][self.persist['current_position']].edges):
                    pygame.draw.line(surface, (0, 0, 0), (self.persist['nodes'][value[0]].x + 16,
                                                          self.persist['nodes'][value[0]].y + 16),
                                     (
                                         self.persist['nodes'][value[1]].x + 16, self.persist['nodes'][value[1]].y +
                                         16), 3)
            else:
                if self.persist['nodes'][self.persist['current_position']].hover:
                    for i, value in enumerate(self.persist['nodes'][self.persist['current_position']].edges):
                        pygame.draw.line(surface, (0, 0, 0), (self.persist['nodes'][value[0]].x + 16,
                                                              self.persist['nodes'][value[0]].y + 16),
                                         (
                                             self.persist['nodes'][value[1]].x + 16, self.persist['nodes'][value[1]].y +
                                             16), 3)

        # Node Group ***********************************************************************************************************
        self.persist['node_group'].draw(surface)

        # Node Labels **********************************************************************************************************
        for node in self.persist['nodes']:
            if node.index in self.persist['nodes'][self.persist['current_position']].neighbors:
                node.seen = True
            offset = (-settings.X * 4 / 100, -settings.Y * 2 / 100)
            if node.x < settings.X / 2 and node.y < settings.Y / 2:
                offset = (settings.X * 3 / 100, settings.Y * 3 / 100)
            elif node.x >= settings.X / 2 and node.y < settings.Y / 2:
                offset = (-settings.X * 4 / 100, settings.Y * 2 / 100)
            elif node.x < settings.X / 2 and node.y >= settings.Y / 2:
                offset = (settings.X * 2 / 100, -settings.Y * 2 / 100)
            if node.state == "Explored" or node.seen:
                if node.type == "Encounter" or node.type == "Dungeon":
                    text = node.type
                else:
                    text = node.event
                settings.tw(surface, text, (0, 0, 0),
                            [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                            settings.DETAIL_FONT)
            if self.persist['party_abilities'].scout_vision:
                if node.index in self.persist['nodes'][self.persist['current_position']].neighbors:
                    if node.type == "Encounter" or node.type == "Dungeon":
                        text = node.type
                    else:
                        text = node.event
                    settings.tw(surface, text, (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)
            if self.persist['party_abilities'].locate_shops or self.persist['party_abilities'].region_revealed:
                if node.event == "Shop":
                    settings.tw(surface, "Shop", (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)
            if self.persist['party_abilities'].locate_inn or self.persist['party_abilities'].region_revealed:
                if node.event == "Inn":
                    settings.tw(surface, "Inn", (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)
            if self.persist['party_abilities'].locate_tavern or self.persist['party_abilities'].region_revealed:
                if node.event == "Tavern":
                    settings.tw(surface, "Tavern", (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)
            if self.persist['party_abilities'].locate_dungeon or self.persist['party_abilities'].region_revealed:
                if node.type == "Dungeon":
                    settings.tw(surface, "Dungeon", (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)
            if self.persist['party_abilities'].locate_encounter or self.persist['party_abilities'].region_revealed:
                if node.type == "Encounter":
                    settings.tw(surface, "Encounter", (0, 0, 0),
                                [node.x + offset[0], node.y + offset[1], settings.X * 7 / 100, settings.Y * 5 / 100],
                                settings.DETAIL_FONT)

        # Party Icon ***************************************************************************************************
        self.persist['party_group'].draw(surface)

        # Overlay ******************************************************************************************************
        surface.blit(self.overlay_image, (0, 0))
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
        settings.tw(surface, str(self.persist['gold']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['coin data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.persist['supplies']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['supplies data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.persist['chargers']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['charge data rect'], settings.HEADING_FONT)
        settings.tw(surface, str(self.persist['elixirs']), (20, 150, 150), settings.REGION_MENUS
        ['browser']['resources']['elixir data rect'], settings.HEADING_FONT)

        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_a icon bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_a status bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_a eq menu bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_a st menu bg rect'], border_radius=6)

        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_b icon bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_b status bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_b eq menu bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_b st menu bg rect'], border_radius=6)

        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_c icon bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_c status bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_c eq menu bg rect'], border_radius=6)
        pygame.draw.rect(surface, (150, 150, 150),
                         settings.REGION_MENUS['browser']['resources']['player_c st menu bg rect'], border_radius=6)
        players = ['player_a', 'player_b', 'player_c']
        for name in players:
            if name in self.persist['characters']:
                icon = self.persist['characters'][name].current_class + "Icon"
                surface.blit(settings.REGION_STATIC_SPRITES[icon],
                             settings.REGION_MENUS['browser']['resources'][name + ' icon pos'])
                pygame.draw.rect(surface, (150, 0, 0),
                                 settings.REGION_MENUS['browser']['resources'][name + ' hp rect'])
                a = settings.REGION_MENUS['browser']['resources'][name + ' hp rect'][0]
                b = settings.REGION_MENUS['browser']['resources'][name + ' hp rect'][1]
                c = settings.REGION_MENUS['browser']['resources'][name + ' hp rect'][2]
                d = settings.REGION_MENUS['browser']['resources'][name + ' hp rect'][3]
                hp = self.persist['characters'][name].hp
                mhp = self.persist['characters'][name].max_hp
                pygame.draw.rect(surface, (0, 150, 0),
                                 [a + (c * (1 - hp / mhp)), b, (c * hp / mhp), d])
                pygame.draw.rect(surface, (0, 0, 50),
                                 settings.REGION_MENUS['browser']['resources'][name + ' hp rect'], 4)
                a = settings.REGION_MENUS['browser']['resources'][name + ' mp rect'][0]
                b = settings.REGION_MENUS['browser']['resources'][name + ' mp rect'][1]
                c = settings.REGION_MENUS['browser']['resources'][name + ' mp rect'][2]
                d = settings.REGION_MENUS['browser']['resources'][name + ' mp rect'][3]
                mp = self.persist['characters'][name].mp
                mmp = self.persist['characters'][name].max_mp
                pygame.draw.rect(surface, (0, 0, 150),
                                 [a + (c * (1 - mp / mmp)), b, (c * mp / mmp), d])
                pygame.draw.rect(surface, (0, 0, 0),
                                 settings.REGION_MENUS['browser']['resources'][name + ' mp rect'], 4)
                settings.tw(surface, 'hp', (0, 0, 0), settings.REGION_MENUS['browser']['resources'] \
                    [name + ' hp data rect'], settings.TEXT_FONT)
                settings.tw(surface, 'mp', (0, 0, 0), settings.REGION_MENUS['browser']['resources'] \
                    [name + ' mp data rect'], settings.TEXT_FONT)
                settings.tw(surface, 'equip', (0, 0, 0), settings.REGION_MENUS['browser'] \
                    ['resources'][name + ' eq menu bg rect'], settings.TEXT_FONT)
                settings.tw(surface, 'skills', (0, 0, 0), settings.REGION_MENUS['browser'] \
                    ['resources'][name + ' st menu bg rect'], settings.TEXT_FONT)

            else:
                x = settings.REGION_MENUS['browser']['resources'][name + ' icon bg rect'][0]
                y = settings.REGION_MENUS['browser']['resources'][name + ' icon bg rect'][1]
                a = settings.REGION_MENUS['browser']['resources'][name + ' icon bg rect'][2] + x
                b = settings.REGION_MENUS['browser']['resources'][name + ' icon bg rect'][3] + y
                pygame.draw.line(surface, (0, 0, 0), (x, y), (a, b), 5)
                pygame.draw.line(surface, (0, 0, 0), (x, b), (a, y), 5)

        if self.state == "Browse" or self.state == "Construct_Portal":
            if hasattr(self.persist['nodes'][self.persist['current_position']], 'event_data'):
                if hasattr(self.persist['nodes'][self.persist['current_position']], 'event'):
                    if self.persist['nodes'][self.persist['current_position']].event == "Shop":
                        pygame.draw.rect(surface, (150, 150, 50), settings.REGION_MENUS['browser']['shop_toggle_rect'],
                                         int(settings.X / 128), border_radius=int(settings.X / 64))
                        settings.tw(surface, "SHOP", (150, 150, 50), settings.REGION_MENUS['browser'] \
                            ['shop_toggle_text'], settings.TEXT_FONT)
            travel = False
            for value in self.persist['nodes'][self.persist['current_position']].neighbors:
                if self.persist['nodes'][value].selected:
                    travel = True
                    break
            if not travel:
                for node in self.persist['nodes']:
                    if self.persist['party_abilities'].fast_travel and self.persist['chargers'] > 0:
                        if node.state == "Explored" and node.selected:
                            travel = True
                            break
                    if self.persist['party_abilities'].fly and self.persist['party_abilities'].fly_charges > 0:
                        if node.selected:
                            travel = True
                            break
                    if self.persist['party_abilities'].teleport and self.persist['elixirs'] > 1:
                        if node.selected:
                            travel = True
                            break
            color = (100, 100, 100)
            if travel and self.state != "Construct_Portal":
                color = (200, 200, 150)
            pygame.draw.rect(surface, (50, 50, 50), settings.REGION_MENUS['browser']['travel_rect'],
                             border_radius=int(settings.X / 128))
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['browser']['travel_rect'],
                             int(settings.X / 128), border_radius=int(settings.X / 128))
            settings.tw(surface, "TRAVEL", color, settings.REGION_MENUS['browser'] \
                ['travel_text'], settings.TEXT_FONT)

            color = settings.TEXT_COLOR
            if self.persist['chargers'] > 2 and self.persist['elixirs'] > 2:
                color = settings.SELECTED_COLOR
            if self.persist['party_abilities'].create_portal:
                pygame.draw.rect(surface, (40, 40, 70), settings.REGION_MENUS['browser']['portal_rect'],
                                 border_radius=int(settings.X / 128))
                pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['browser']['portal_rect'],
                                 int(settings.X / 128), border_radius=int(settings.X / 128))
                settings.tw(surface, "CONSTRUCT PORTAL", color, settings.REGION_MENUS['browser'] \
                    ['portal_text'], settings.DETAIL_FONT)

            if self.persist['portal']:
                for portal in self.persist['portal']:
                    start = (portal[0][0] + settings.X * 2 / 100, portal[0][1] + settings.Y * 2 / 100)
                    end = (portal[1][0] + settings.X * 2 / 100, portal[1][1] + settings.Y * 2 / 100)

                    settings.draw_line_dashed(surface, (40, 40, 70), start, end, width=5)
            if self.state == "Construct_Portal":
                settings.tw(surface, settings.REGION_MENUS['browser']['portal_prompt'], settings.TEXT_COLOR,
                            settings.REGION_MENUS['browser']['portal_prompt_rect'], settings.DETAIL_FONT)

        elif self.state == "Event":
            pygame.draw.rect(surface, (150, 150, 150), settings.REGION_MENUS['event']['background 1 rect'])
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['event']['background 2 rect'])
            settings.tw(surface, self.persist['nodes'][self.persist['current_position']].event_data.prompt,
                        (20, 150, 150), settings.REGION_MENUS['event']['prompt rect'],
                        settings.TEXT_FONT)
            for i, value in enumerate(self.persist['nodes'][self.persist['current_position']].event_data.options[0]):
                if self.persist['nodes'][self.persist['current_position']].event_data.option_index == i:
                    settings.tw(surface,
                                self.persist['nodes'][self.persist['current_position']].event_data.options[
                                    0][i],
                                settings.SELECTED_COLOR,
                                settings.REGION_MENUS['event']['option rects'][i],
                                settings.TEXT_FONT)
                else:
                    settings.tw(surface,
                                self.persist['nodes'][self.persist['current_position']].event_data.options[
                                    0][i],
                                (20, 150, 150), settings.REGION_MENUS['event']['option rects'][i],
                                settings.TEXT_FONT)

        elif self.state == "Equip_menu":
            pygame.draw.rect(surface, (150, 150, 150), settings.REGION_MENUS['equip menu']['background 1 rect'],
                             border_radius=16)
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['equip menu']['background 2 rect'],
                             border_radius=12)

            # Display current equipment *******************************************************************
            r = settings.REGION_MENUS['equip menu']['Top_Slot_Rect']
            e = settings.REGION_MENUS['equip menu']['Top_Equip_Rect']
            for n, equip_slot in enumerate(
                    self.persist['characters'][self.inventory_menu_player_index].equipment_options):
                settings.tw(surface, equip_slot, settings.TEXT_COLOR, r[n], settings.TEXT_FONT)
                if equip_slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                    text = self.persist['characters'][self.inventory_menu_player_index].equipment[
                        equip_slot].name
                else:
                    text = '-'
                if self.equipment_selection_index == n and self.equipment_menu_horizontal_index == "Equip":
                    color = settings.SELECTED_COLOR
                else:
                    color = settings.TEXT_COLOR
                settings.tw(surface, text, color, e[n], settings.TEXT_FONT)

            # Display current equipment inventory ***********************************************************
            for i, item in enumerate(self.persist['inventory']):
                color = settings.TEXT_COLOR
                if not item.equipment:
                    color = (50, 50, 50)
                    if self.equipment_inventory_selection_index == i and self.equipment_menu_horizontal_index == "Inventory":
                        color = (100, 100, 100)
                elif self.equipment_inventory_selection_index == i and self.equipment_menu_horizontal_index == "Inventory":
                    color = settings.SELECTED_COLOR
                if 12 >= i - self.inventory_display_index >= 0:
                    settings.tw(surface, item.name, color, settings.REGION_MENUS['equip menu']['inventory rects'][i - self.inventory_display_index], settings.TEXT_FONT)
            if len(self.persist['inventory']) < 13:
                for i in range(len(self.persist['inventory']), 13):
                    color = (50, 50, 50)
                    if self.equipment_inventory_selection_index == i and self.equipment_menu_horizontal_index == "Inventory":
                        color = (100, 100, 100)
                    settings.tw(surface, '-'.center(12), color, settings.REGION_MENUS['equip menu']['inventory rects'][i], settings.TEXT_FONT)

            # Display current stats *************************************************************************
            potential = self.potential_stat()
            for key, value in enumerate(settings.REGION_MENUS['equip menu']['Stat_Rects']):
                stat = getattr(self.persist['characters'][self.inventory_menu_player_index], value)
                if value == 'hp':
                    stat2 = getattr(self.persist['characters'][self.inventory_menu_player_index], 'max_hp')
                    settings.tw(surface, value + ':' + str(stat).rjust(10 - len(value)) + '/' + str(stat2), settings.TEXT_COLOR,
                                settings.REGION_MENUS['equip menu']['Stat_Rects'][value], settings.TEXT_FONT)
                elif value == 'mp':
                    stat2 = getattr(self.persist['characters'][self.inventory_menu_player_index], 'max_mp')
                    settings.tw(surface, value + ':' + str(stat).rjust(11 - len(value)) + '/' + str(stat2), settings.TEXT_COLOR,
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

            # Display current player / menu *****************************************************************
            settings.tw(surface, "Equipment", settings.TEXT_COLOR,
                        settings.REGION_MENUS['equip menu']['title rect'], settings.HEADING_FONT)
            settings.tw(surface, self.persist['characters'][self.inventory_menu_player_index].name, settings.TEXT_COLOR,
                        settings.REGION_MENUS['equip menu']['player name rect'], settings.TEXT_FONT)

        elif self.state == "Skill_tree_menu":
            pygame.draw.rect(surface, (150, 150, 150), settings.REGION_MENUS['skill tree']['background 1 rect'],
                             border_radius=16)
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['skill tree']['background 2 rect'],
                             border_radius=12)
            proto = settings.REGION_MENUS['skill tree']['skill_rect_proto']
            skill_rects = []
            text_rects = []
            skill_offset = settings.REGION_MENUS['skill tree']['skill_offset']
            text_offset = settings.REGION_MENUS['skill tree']['text_offset']
            for c in range(6):
                for r in range(6):
                    skill_rects.append(
                        [skill_offset[0] * c + proto[0], skill_offset[1] * r + proto[1], proto[2], proto[3]])
                    text_rects.append([skill_offset[0] * c + proto[0] + text_offset[0],
                                       skill_offset[1] * r + proto[1] + text_offset[1], proto[2], proto[3]])
            for value in skill_rects:
                pygame.draw.rect(surface, (150, 150, 150), value, border_radius=8)
            for value in text_rects:
                settings.tw(surface, "Skill Long", settings.TEXT_COLOR, value, settings.DETAIL_FONT)
        elif self.state == "Options_menu":
            pass
        elif self.state == "Shop":
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS['shop']['background 1 rect'],
                             border_radius=int(settings.Y / 256))
            pygame.draw.rect(surface, (40, 40, 40), settings.REGION_MENUS['shop']['background 2 rect'],
                             border_radius=int(settings.Y / 256))
            if self.shop_state == "Buy":
                shop = self.persist['nodes'][self.persist['current_position']].event_data.shop
                settings.tw(surface, "Supplies: " + str(shop["Supplies"]["Stock"]), settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['supplies_label'], settings.TEXT_FONT)
                settings.tw(surface, "Charger: " + str(shop["Charger"]["Stock"]), settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['chargers_label'], settings.TEXT_FONT)
                settings.tw(surface, "Elixir: " + str(shop["Elixir"]["Stock"]), settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['elixirs_label'], settings.TEXT_FONT)
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_bottom'],
                                 settings.REGION_MENUS['shop']['buy_button_bottom'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_top'],
                                 settings.REGION_MENUS['shop']['buy_button_pressed'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                settings.tw(surface, "BUY", settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['buy_text_bottom'], settings.TEXT_FONT)
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_bottom'],
                                 settings.REGION_MENUS['shop']['sell_button_bottom'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_top'],
                                 settings.REGION_MENUS['shop']['sell_button_top'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                settings.tw(surface, "SELL", settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['sell_text_top'], settings.TEXT_FONT)

            elif self.shop_state == "Sell":
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_bottom'],
                                 settings.REGION_MENUS['shop']['buy_button_bottom'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_top'],
                                 settings.REGION_MENUS['shop']['buy_button_top'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                settings.tw(surface, "BUY", settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['buy_text_top'], settings.TEXT_FONT)
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_bottom'],
                                 settings.REGION_MENUS['shop']['sell_button_bottom'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                pygame.draw.rect(surface, settings.REGION_MENUS['shop']['button_color_top'],
                                 settings.REGION_MENUS['shop']['sell_button_pressed'],
                                 border_radius=settings.REGION_MENUS['shop']['button_radius'])
                settings.tw(surface, "SELL", settings.TEXT_COLOR,
                            settings.REGION_MENUS['shop']['sell_text_bottom'], settings.TEXT_FONT)

        elif self.state == "Alt_Travel_Confirm":
            pygame.draw.rect(surface, (100, 100, 100), settings.REGION_MENUS[self.state]['BG_Rect'],
                             border_radius=int(settings.Y / 128))
            pygame.draw.rect(surface, (0, 0, 0), settings.REGION_MENUS[self.state]['BG_Rect'], int(settings.Y / 128),
                             border_radius=int(settings.Y / 128))
            color = (40, 40, 40)
            if self.alt_travel_index == 0:
                color = (60, 60, 60)
            pygame.draw.rect(surface, color, settings.REGION_MENUS[self.state]['FT_Rect'],
                             border_radius=int(settings.Y / 128))
            color = (40, 40, 40)
            if self.alt_travel_index == 1:
                color = (60, 60, 60)
            pygame.draw.rect(surface, color, settings.REGION_MENUS[self.state]['Fly_Rect'],
                             border_radius=int(settings.Y / 128))
            color = (40, 40, 40)
            if self.alt_travel_index == 2:
                color = (60, 60, 60)
            pygame.draw.rect(surface, color, settings.REGION_MENUS[self.state]['Teleport_Rect'],
                             border_radius=int(settings.Y / 128))
            settings.tw(surface, "Fast Travel", settings.TEXT_COLOR, settings.REGION_MENUS[self.state]['FT_Text'],
                        settings.TEXT_FONT)
            settings.tw(surface, "Fly", settings.TEXT_COLOR, settings.REGION_MENUS[self.state]['Fly_Text'],
                        settings.TEXT_FONT)
            settings.tw(surface, "Teleport", settings.TEXT_COLOR, settings.REGION_MENUS[self.state]['Teleport_Text'],
                        settings.TEXT_FONT)

    def region_generate(self):
        # network_gen(num_nodes=30, knn=4, node_space=80, space_probability=95,
        # node_space_ll=0, node_space_ul=350, min_edge_angle=15)
        valid = False
        max_shop = settings.REGION_PARAMETERS_MAX_SHOP[
            self.persist['region_index']]  # (255, 159),(873, 172),(876, 569),(262, 530)
        self.persist['node_group'] = pygame.sprite.Group()
        self.persist['party_group'] = pygame.sprite.Group()
        self.persist['nodes'] = []
        self.persist['portal'] = []
        region_options = []
        for option in settings.REGION_LAYOUTS[self.persist['region_type']]:
            region_options.append(option)
        self.persist['region_layout'] = region_type = settings.choose_random(region_options)
        num_nodes = 30
        if 'num_nodes' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            num_nodes = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['num_nodes']
        knn = 4
        if 'knn' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            knn = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['knn']
        node_space = 100
        if 'node_space' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            node_space = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['node_space']
        space_probability = 100
        if 'space_probability' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            space_probability = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['space_probability']
        node_space_ll = 0
        if 'node_space_ll' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            node_space_ll = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['node_space_ll']
        node_space_ul = 350
        if 'node_space_ul' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            node_space_ul = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['node_space_ul']
        min_edge_angle = 15
        if 'min_edge_angle' in settings.REGION_LAYOUTS[self.persist['region_type']][region_type]:
            min_edge_angle = settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['min_edge_angle']
        while not valid:
            node_list, edge_list, neighbors_dict, edge_dict, valid_path = network_generator.network_gen(
                X=settings.X, Y=settings.Y, shapes=settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['Shapes'],
                start_rect=settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['Start'],
                end_rect=settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['End'],
                positive=settings.REGION_LAYOUTS[self.persist['region_type']][region_type]['Positive'],
                num_nodes=num_nodes, knn=knn, node_space=node_space, space_probability=space_probability,
                node_space_ll=node_space_ll, node_space_ul=node_space_ul, min_edge_angle=min_edge_angle)
            valid = valid_path
        for i, value in enumerate(node_list):
            if i == 0:
                self.persist['nodes'].append(Node(value[0], value[1], neighbors_dict[i], edge_dict[i], i, "Encounter",
                                                  "Boss"))
                self.persist['node_group'].add(self.persist['nodes'][i])
            elif i == 1:
                self.persist['nodes'].append(Node(value[0], value[1], neighbors_dict[i], edge_dict[i], i, "Empty",
                                                  "Region Entry"))
                self.persist['node_group'].add(self.persist['nodes'][i])
            else:
                node_type, event_type, event_id = settings.node_assign(self.persist)
                self.persist['nodes'].append(Node(value[0], value[1], neighbors_dict[i], edge_dict[i], i, node_type,
                                                  event_type))
                self.persist['node_group'].add(self.persist['nodes'][i])
        self.persist['party'] = Party()
        self.persist['party_group'].add(self.persist['party'])
        self.persist['current_position'] = 1
        self.persist['region_generate'] = False

    def node_event(self):
        node_event = self.persist['nodes'][self.persist['current_position']].event
        event_type = self.persist['nodes'][self.persist['current_position']].type
        region = self.persist['region_index']
        self.persist['nodes'][self.persist['current_position']].event_data = \
            settings.NodeEvent(node_event, event_type, self.persist)

    def mouse_hover(self):
        if self.state == "Browse":
            pass
        if self.state == "Event":
            pass
        if self.state == "Equip_menu":
            pass
        if self.state == "Skill_tree_menu":
            pass
        if self.state == "Options_menu":
            pass

    def character_stat_update(self):
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        for player in self.persist['characters']:
            for value in stats:
                if value == 'max_hp':
                    setattr(self.persist['characters'][player], value,
                            getattr(self.persist['characters'][player], 'base_hp'))
                elif value == 'max_mp':
                    setattr(self.persist['characters'][player], value,
                            getattr(self.persist['characters'][player], 'base_mp'))
                else:
                    setattr(self.persist['characters'][player], value,
                            getattr(self.persist['characters'][player], 'base_' + value))

            for slot in self.persist['characters'][player].equipment.keys():
                for value in stats:
                    if hasattr(self.persist['characters'][player].equipment[slot], value):
                        new_value = getattr(self.persist['characters'][player].equipment[slot], value) + \
                                    getattr(self.persist['characters'][player], value)
                        setattr(self.persist['characters'][player], value, new_value)
                    if value == 'strength':
                        if hasattr(self.persist['characters'][player].equipment[slot], 'attack'):
                            self.persist['characters'][player].strength += \
                                self.persist['characters'][player].equipment[slot].attack

    def character_ability_update(self):
        for player in self.persist['characters']:
            setattr(self.persist['characters'][player], 'techniques',
                getattr(self.persist['characters'][player], 'base_' + 'techniques'))
            for slot in self.persist['characters'][player].equipment.keys():
                if hasattr(self.persist['characters'][player].equipment[slot], 'techniques'):
                    for value in self.persist['characters'][player].equipment[slot].techniques:
                        if value not in self.persist['characters'][player].techniques:
                            self.persist['characters'][player].techniques.append(value)
        for player in self.persist['characters']:
            setattr(self.persist['characters'][player], 'attack_type',
                    getattr(self.persist['characters'][player], 'base_' + 'attack_type'))
            for slot in self.persist['characters'][player].equipment.keys():
                if hasattr(self.persist['characters'][player].equipment[slot], 'attack_type'):
                    setattr(self.persist['characters'][player], 'attack_type',
                            getattr(self.persist['characters'][player].equipment[slot], 'attack_type'))

    def potential_stat(self):
        stats = ['max_hp', 'max_mp', 'strength', 'magic', 'defense', 'spirit', 'speed', 'luck', 'crit_rate',
                 'crit_damage']
        potential = {}
        potential_value = 0
        current_value = 0
        if self.equipment_menu_horizontal_index == "Inventory" and self.persist['inventory'] and len(self.persist['inventory']) > self.equipment_inventory_selection_index >= 0:
            slot = self.persist['inventory'][self.equipment_inventory_selection_index].slot
            for value in stats:
                if value != 'strength':
                    if hasattr(self.persist['inventory'][self.equipment_inventory_selection_index], value):
                        potential_value = getattr(self.persist['inventory'][self.equipment_inventory_selection_index], value)
                    else:
                        potential_value = 0
                    if slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                        if hasattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value):
                            current_value = getattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value)
                        else:
                            current_value = 0
                    else:
                        current_value = 0
                    if potential_value - current_value != 0:
                        potential[value] = potential_value - current_value
                else:
                    if hasattr(self.persist['inventory'][self.equipment_inventory_selection_index], 'attack'):
                        potential_value = getattr(self.persist['inventory'][self.equipment_inventory_selection_index], 'attack')
                    else:
                        potential_value = 0
                    if slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                        if hasattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value):
                            current_value = getattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value)
                        else:
                            current_value = 0
                    else:
                        current_value = 0
                    if potential_value - current_value != 0:
                        potential[value] = potential_value - current_value
        elif self.equipment_menu_horizontal_index == "Equip":
            if len(self.persist['characters'][self.inventory_menu_player_index].equipment_options) - 1 >= \
                    self.equipment_selection_index >= 0:
                slot = self.persist['characters'][self.inventory_menu_player_index].equipment_options[self.equipment_selection_index]
                for value in stats:
                    if value != 'strength':
                        potential_value = 0
                        if slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                            if hasattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value):
                                current_value = getattr(
                                    self.persist['characters'][self.inventory_menu_player_index].equipment[slot], value)
                            else:
                                current_value = 0
                        else:
                            current_value = 0
                        if potential_value - current_value != 0:
                            potential[value] = potential_value - current_value
                    else:
                        potential_value = 0
                        if slot in self.persist['characters'][self.inventory_menu_player_index].equipment.keys():
                            if hasattr(self.persist['characters'][self.inventory_menu_player_index].equipment[slot],
                                       'attack'):
                                current_value = getattr(
                                    self.persist['characters'][self.inventory_menu_player_index].equipment[slot], 'attack')
                            else:
                                current_value = 0
                        else:
                            current_value = 0
                        if potential_value - current_value != 0:
                            potential[value] = potential_value - current_value
        return potential
