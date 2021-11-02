import math
import random
import copy
import network_generator
import pygame
import settings
from base import BaseState
import pytweening as pt


class Node(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, neighbors, edges, state, node_type):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.index = state
        self.seen = False
        self.x = x
        self.y = y
        self.type = node_type
        if state == 1:
            self.state = "Explored"
        elif state == 0:
            self.state = "Exit"
        else:
            self.state = "Unexplored"
        self.event = None
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

        elif self.state == "Explored":
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

    def cleanup(self):
        self.kill()

    def hover(self):
        pass

    def click(self):
        self.selected = False
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.parent.persist['current_position'] != self.index:
            self.selected = True


class Party(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x = 2 * settings.X
        self.y = 2 * settings.Y
        self.image = pygame.image.load(
            r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites\Region\D20_Party.png")
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 55, 202))

    def update(self, dt):
        for sprite in self.parent.nodes.sprites():
            if self.parent.persist['current_position'] == sprite.index:
                self.x = sprite.x
                self.y = sprite.y
                break
        self.rect = pygame.Rect(self.x - (self.image.get_width() / 4), self.y - (self.image.get_height() / 2),
                                self.image.get_width(),
                                self.image.get_height())


class TravelButton(object):
    def __init__(self, parent):
        self.x = 200
        self.y = 200
        self.bg_rect = []
        self.border_rect = []
        self.text_rect = []
        self.state = "Dormant"
        self.hover = False
        self.parent = parent
        self.tween = pt.easeInOutExpo()

    def draw(self, surface):
        pass

    def update(self):
        if self.state == "Dormant":
            pass
        elif self.state == "Active":
            pass

    def click(self):
        if settings.click_check(self.bg_rect):
            self.parent.travel()


class Region(BaseState):
    def __init__(self):
        super(Region, self).__init__()
        self.next_state = "BATTLE"
        self.nodes = pygame.sprite.Group()
        self.party = pygame.sprite.Group()
        self.buttons = []
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
                for node in self.nodes.sprites():
                    node.click()

        elif self.state == "Event":
            pass

        elif self.state == "Equip":
            pass

        elif self.state == "Skill_Tree":
            pass

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
                self.handle_action("backspace")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def update(self, dt):
        self.nodes.update(dt)
        self.party.update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.nodes.draw(surface)
        self.party.draw(surface)
        surface.blit(self.overlay_image, (0,0))

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
        self.party.add(Party(self))
        self.persist['current_position'] = 1
        self.persist['region_generate'] = False
