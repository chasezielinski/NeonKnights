import pygame
import math
import settings
import pytweening as pt
import numpy as np
from base import BaseState


class Battle(BaseState):
    def __init__(self):
        super(Battle, self).__init__()
        # instantiate battle Groups
        self.action_index = 0
        self.current_action = None
        self.battle_characters = pygame.sprite.Group()
        self.battle_characters_ko = pygame.sprite.Group()
        self.player_characters = pygame.sprite.Group()
        self.enemy_characters = pygame.sprite.Group()
        self.battle_objects = pygame.sprite.Group()
        self.battle_actions = pygame.sprite.Group()
        self.battle_animations = pygame.sprite.Group()
        self.damage_particle = settings.DamageParticle()
        self.action_card_manager = ActionCardManger(self)
        # instantiate state variables and menu index variables
        self.state = "Pre_Battle"
        self.turn_sub_state = "Browse"
        self.action_type_index = -1
        self.player_index = None
        self.enemy_slots = ['enemy_a', 'enemy_b', 'enemy_c', 'enemy_d', 'enemy_e']
        self.player_slots = ['player_a', 'player_b', 'player_c']
        self.name = "SlimeBall"
        self.selected_action = None
        self.supply_reward = 0
        self.elixir_reward = 0
        self.charger_reward = 0
        self.exp_reward = 0
        self.gold_reward = 0
        self.item_reward = []
        self.win_timer = 0
        # instantiate battle objects
        self.battle_overlay = settings.BattleOverlay(self)
        self.message = settings.BattleMessage()
        self.victory_display = settings.VictoryDisplay(self)
        self.status_particle_index = 0
        self.timer = None
        self.next_battle_state = None
        self.print_timer = 200

    def startup(self, persistent):
        self.persist = persistent
        self.victory_display = settings.VictoryDisplay(self)
        # point Battle to player character sprite objects and add them to proper Groups
        for player in self.persist['characters']:
            setattr(self, player.slot, player)
            setattr(getattr(self, player.slot), 'parent', self)
            self.battle_characters.add(getattr(self, player.slot))
            self.player_characters.add(getattr(self, player.slot))
            self.battle_objects.add(getattr(self, player.slot))
        # construct each enemy sprite object and add them to proper Groups
        for i, enemy in enumerate(self.persist['enemies']):
            slot = self.enemy_slots[i]
            population = len(self.persist['enemies'])
            setattr(self, slot, eval("settings." + enemy)(slot, self.persist['region_index'], population, self))
            self.battle_characters.add(getattr(self, slot))
            self.enemy_characters.add(getattr(self, slot))
            self.battle_objects.add(getattr(self, slot))

    def handle_action(self, action):
        if self.state != "Pointer":
            if action == ",":
                self.state = "Pointer"
        elif self.state == "Pointer":
            if action == ",":
                self.state = "Turn"
        if action == "mouse_move":
            # mouse hover check
            for sprite in self.battle_objects.sprites():
                if hasattr(sprite, 'hover'):
                    sprite.hover = False
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.hover = True

        if self.state == "Turn":
            self.action_card_manager.handle_action(action)
            if self.turn_sub_state == "Browse":
                if action == "click":
                    # check for click on player character sprite or action queue sprite
                    for i, sprite in enumerate(self.battle_characters.sprites()):
                        if isinstance(sprite, settings.PlayerCharacter):
                            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                                self.player_index = sprite
                                self.turn_sub_state = "Move_Select"
                                self.action_card_manager.set_main_actions()
                    # check for click on end turn button
                    if settings.click_check(settings.BATTLE_MENUS['turn_end_rect']):
                        self.turn_sub_state = "Confirm"
                if action == "t":
                    self.turn_sub_state = "Confirm"
            elif self.turn_sub_state == "Move_Select":
                pass
                # if action == "mouse_move":
                #     # check for mouse hover over move action types
                #     flag = False
                #     for i, option in enumerate(settings.actions_dict.keys()):
                #         if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                #             if self.action_type_index != i:
                #                 settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                #             self.action_type_index = i
                #             flag = True
                #     if not flag:
                #         self.action_type_index = -1
                # elif action == "up":
                #     settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                #     self.action_type_index -= 1
                #     self.action_type_index %= len(settings.actions_dict.keys())
                # elif action == "down":
                #     settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                #     self.action_type_index += 1
                #     self.action_type_index %= len(settings.actions_dict.keys())
                # elif action == "return":
                #     if self.action_type_index == -1:
                #         pass
                #     elif settings.actions_dict.keys()[self.action_type_index] == "Skill":
                #         if self.player_index.action_options:
                #             if not self.player_index.dazed > 0 \
                #                     and not self.player_index.stunned > 0:
                #                 for action in self.player_index.action_options:
                #                     if action.is_usable():
                #                         self.turn_sub_state = "Skill"
                #                         break
                #                 else:
                #                     pass
                #     elif settings.actions_dict.keys()[self.action_type_index] == "Item":
                #         if self.persist['inventory']:
                #             if not self.player_index.perplexed > 0 \
                #                     and not self.player_index.stunned > 0:
                #                 for item in self.persist['inventory']:
                #                     if item.is_usable():
                #                         self.turn_sub_state = "Item"
                #                         break
                #                 else:
                #                     pass
                #     elif settings.actions_dict.keys()[self.action_type_index] == "Attack":
                #         if hasattr(self.player_index, 'attack_action') \
                #                 and not self.player_index.disabled > 0 \
                #                 and not self.player_index.stunned > 0:
                #             self.selected_action = self.player_index.attack_action
                #             self.turn_sub_state = "Target"
                #     elif settings.actions_dict.keys()[self.action_type_index] == "Defend":
                #         if hasattr(self.player_index, 'defend_action') \
                #                 and not self.player_index.smitten > 0 \
                #                 and not self.player_index.stunned > 0:
                #             self.selected_action = self.player_index.defend_action
                #             self.turn_sub_state = "Target"
                #     elif settings.actions_dict.keys()[self.action_type_index] == "Run":
                #         if hasattr(self.player_index, 'run_action') \
                #                 and not self.player_index.trapped > 0 \
                #                 and not self.player_index.stunned > 0:
                #             self.selected_action = self.player_index.run_action
                #             self.turn_sub_state = "Target"
                # elif action == "backspace":
                #     self.turn_sub_state = "Browse"
                # elif action == "click":
                #     check = True
                #     for i, option in enumerate(settings.actions_dict.keys()):
                #         if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                #             if option == "Skill":
                #                 if self.player_index.abilities:
                #                     if not self.player_index.dazed > 0 \
                #                             and not self.player_index.stunned > 0:
                #                         for action in self.player_index.abilities:
                #                             if action.is_usable():
                #                                 self.turn_sub_state = "Skill"
                #                                 check = False
                #                                 break
                #                         else:
                #                             pass
                #             elif option == "Item":
                #                 if self.persist['inventory']:
                #                     if not self.player_index.perplexed > 0 \
                #                             and not self.player_index.stunned > 0:
                #                         for item in self.persist['inventory']:
                #                             if settings.BattleConsumable.__instancecheck__(item):
                #                                 self.turn_sub_state = "Item"
                #                                 check = False
                #                                 break
                #             elif option == "Attack":
                #                 if hasattr(self.player_index, 'attack_action') \
                #                         and not self.player_index.disabled > 0 \
                #                         and not self.player_index.stunned > 0:
                #                     self.selected_action = self.player_index.attack_action
                #                     self.turn_sub_state = "Target"
                #                     check = False
                #             elif option == "Run":
                #                 if hasattr(self.player_index, 'run_action') \
                #                         and not self.player_index.trapped > 0 \
                #                         and not self.player_index.stunned > 0:
                #                     self.selected_action = self.player_index.run_action
                #                     self.turn_sub_state = "Target"
                #                     check = False
                #             elif option == "Defend":
                #                 if hasattr(self.player_index, 'defend_action') \
                #                         and not self.player_index.smitten > 0 \
                #                         and not self.player_index.stunned > 0:
                #                     self.selected_action = self.player_index.defend_action
                #                     self.turn_sub_state = "Target"
                #                     check = False
                #     if check:
                #         self.turn_sub_state = "Browse"

            elif self.turn_sub_state == "Skill":
                self.battle_overlay.handle_action(action)
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"

            elif self.turn_sub_state == "Item":
                self.battle_overlay.handle_action(action)

            elif self.turn_sub_state == "Target":
                if action == "click":
                    for sprite in self.battle_characters:
                        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                            self.selected_action.target_set(self.player_index, [sprite])
                            self.sort_actions()
                        self.turn_sub_state = "Browse"

            elif self.turn_sub_state == "Confirm":
                if action == "y":
                    self.state = "Pre_Action"
                    self.sort_actions()
                elif action == "n" or action == "backspace":
                    self.state = "Browse"
                elif action == "click":
                    if settings.click_check(settings.BATTLE_MENUS['confirm_yes_rect']):
                        self.state = "Pre_Action"
                        self.sort_actions()
                    elif settings.click_check(settings.BATTLE_MENUS['confirm_no_rect']):
                        self.state = "Browse"

        elif self.state == "Pre_Action":
            pass

        elif self.state == "Victory_2":
            if action == "return" or action == "click":
                self.victory_display.handle_action()

        if action == "Clean_Up":
            self.next_state = "REGION"
            self.state = "Pre_Battle"
            for objects in self.battle_objects:
                objects.kill()
            del self.victory_display
            self.supply_reward = 0
            self.elixir_reward = 0
            self.charger_reward = 0
            self.exp_reward = 0
            self.gold_reward = 0
            self.item_reward = []
            self.win_timer = 0
            self.done = True

    def delay(self, time, return_state):
        self.timer = time
        self.next_battle_state = return_state
        self.state = "Delay"

    def update(self, dt):
        self.print_timer -= dt
        if self.print_timer <= 0:
            #print(pygame.mouse.get_pos())
            #print((pygame.mouse.get_pos()[0]*100/settings.X ,pygame.mouse.get_pos()[1]*100/settings.Y))
            self.print_timer = 200
        for sprite in self.battle_characters:
            if sprite.hp <= 0:
                sprite.ko()
        if self.state not in ["Victory_1", "Victory_2", "Defeat", "Clean_Up", "Delay", "Wait"]:
            if len(self.player_characters.sprites()) <= 0:
                self.state = "Defeat"
            elif len(self.enemy_characters.sprites()) <= 0:
                self.state = "Victory_1"
                self.win_timer = 2000
                for player in self.player_characters.sprites():
                    player.exp += self.exp_reward / len(self.player_characters.sprites())
                self.persist['gold'] += self.gold_reward
                self.persist['supplies'] += self.supply_reward
                self.persist['chargers'] += self.charger_reward
                self.persist['elixirs'] += self.elixir_reward
        self.battle_objects.update(dt)
        self.battle_overlay.update(dt)
        self.damage_particle.update(dt)
        self.message.update(dt)
        self.action_card_manager.update(dt)
        self.persist['Music'].update(dt, self)
        if self.state == "Pre_Battle":
            self.state = "Pre_Turn"
        elif self.state == "Pre_Turn":
            for player in self.player_characters.sprites():
                player.pre_turn(self)
            options = []
            for enemy in self.enemy_characters.sprites():
                options.append(enemy.give_options())
            choices = settings.utility_select(options)
            for choice in choices:
                choice[1].target_set(choice[0], choice[2])
            self.sort_actions()
            self.state = "Turn"
            self.turn_sub_state = "Browse"
            self.message.set_message("Select actions", state="Persist")
        elif self.state == "Turn":
            pass
        elif self.state == "Pre_Action":
            self.message.clear_message()
            for action in self.battle_actions:
                if action.queue == self.action_index:
                    self.current_action = action
                    self.state = "Action"
                    break
            else:
                if self.action_index > 9:
                    self.state = "End_Turn"
                    self.action_index = 0
                else:
                    self.action_index += 1
        elif self.state == "Action":
            self.current_action.do_action()
            self.state = "Wait"
        elif self.state == "Wait":
            pass
        elif self.state == "Check":
            if hasattr(self.current_action, 'hits'):
                if self.current_action.hits > 1:
                    self.current_action.hits -= 1
                    self.state = "Action"
                else:
                    self.state = "Pre_Action"
                    self.action_index += 1
                if self.action_index > 9:
                    self.state = "End_Turn"
                    self.action_index = 0
            else:
                self.state = "Pre_Action"
                self.action_index += 1
                if self.action_index > 9:
                    self.state = "End_Turn"
                    self.action_index = 0
        elif self.state == "End_Turn":
            self.status_particle_index = 0
            for character in self.battle_characters.sprites():
                character.on_end_turn()
                self.delay(self.status_particle_index * 500, "Pre_Turn")

        elif self.state == "Victory_1":
            self.win_timer -= dt
            if self.win_timer <= 0:
                self.state = "Victory_2"

        elif self.state == "Victory_2":
            self.victory_display.update(dt)

        elif self.state == "Victory_3":
            pass

        elif self.state == "Delay":
            self.timer -= dt
            if self.timer <= 0:
                self.timer = None
                self.state = self.next_battle_state
                self.next_battle_state = None
        self.persist['FX'].update(dt)
        self.persist['SFX'].update(dt)

    def stop_wait(self):
        if self.state == "Wait":
            self.state = "Check"

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.battle_characters.draw(surface)
        self.battle_characters_ko.draw(surface)
        self.battle_animations.draw(surface)
        self.damage_particle.draw(surface)
        self.battle_overlay.draw(surface)
        self.battle_actions.draw(surface)
        self.action_card_manager.draw(surface)
        self.message.draw(surface)
        for action in self.battle_actions.sprites():
            action.draw_text(surface)
        self.persist['FX'].draw(surface)
        if self.state == "Victory_2":
            self.victory_display.draw(surface)

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
            elif event.key == pygame.K_TAB:
                self.handle_action("tab")
            elif event.key == pygame.K_y:
                self.handle_action("y")
            elif event.key == pygame.K_n:
                self.handle_action("n")
            elif event.key == pygame.K_t:
                self.handle_action("t")
            elif event.key == pygame.K_COMMA:
                self.handle_action(",")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("backspace")
            elif event.key == pygame.K_ESCAPE:
                self.handle_action("escape")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
            elif event.button == 4:
                self.handle_action("wheel_up")
            elif event.button == 5:
                self.handle_action("wheel_down")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.handle_action("un-click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def sort_actions(self):
        for i, action in enumerate(self.battle_actions.sprites()):
            action.queue = i
        if len(self.battle_actions.sprites()) > 1:
            flag = True
            while flag:
                flag = False
                for sprite in self.battle_actions.sprites():
                    for sprite_2 in self.battle_actions.sprites():
                        a = (sprite.queue, sprite.parent.speed)
                        b = (sprite_2.queue, sprite_2.parent.speed)
                        if a[0] > b[0] and a[1] > b[1]:
                            sprite.queue = b[0]
                            sprite_2.queue = a[0]
                            flag = True
                        elif a[1] == b[1] and settings.random_int(0, 100) > 50:
                            sprite.queue = b[0]
                            sprite_2.queue = a[0]

    def ability_click(self):
        if self.player_index.abilities:
            if not self.player_index.dazed > 0 \
                    and not self.player_index.stunned > 0:
                for action in self.player_index.abilities:
                    if action.is_usable():
                        self.turn_sub_state = "Skill"
                        break

    def attack_click(self):
        pass

    def defend_click(self):
        pass

    def item_click(self):
        pass

    def run_click(self):
        pass


class ActionCardManger(object):
    def __init__(self, parent):
        self.parent = parent
        self.action_cards = []
        self.card_rect = (31*settings.X/100, 74*settings.Y/100, 66*settings.X/100, 26*settings.Y/100)
        self.timer = 200
        self.state = "Main"
        self.pointer = Pointer(self)
        self.pointer_states = ["Target"]
        self.selected_action = None

    def update(self, dt):
        if self.state in self.pointer_states:
            self.pointer.update(dt)
        if self.action_cards and self.state in ["Main", "Ability", "Item"]:
            self.determine_layering(dt)

    def draw(self, surface):
        if self.state in self.pointer_states:
            self.pointer.draw(surface)
        if self.action_cards:
            self.action_cards.sort(reverse=True)
            for action_card in self.action_cards:
                action_card.draw(surface)

    def determine_layering(self, dt):
        lowest = self.action_cards[0]
        for i, action_card in enumerate(self.action_cards):
            action_card.update(dt)
            if action_card.distance_x_mouse < lowest.distance_x_mouse:
                lowest = action_card
        if lowest.hover:
            lowest.layer = -1
            self.selected_action = lowest
        else:
            self.selected_action = None
        for i, action_card in enumerate(self.action_cards):
            action_card.toggle_position()

    def target(self):
        self.state = "Target"

    def set_main_actions(self):
        self.action_cards.clear()
        self.action_cards.append(ActionCard(self, "Attack", "self.parent.target()", 0, self.parent.player_index.attack_action))
        self.action_cards.append(ActionCard(self, "Defend", "self.parent.target()", 1, self.parent.player_index.defend_action))
        self.action_cards.append(ActionCard(self, "Ability", "self.parent.set_ability_actions()", 2))
        self.action_cards.append(ActionCard(self, "Item", "self.parent.set_item_actions()", 3))
        self.action_cards.append(ActionCard(self, "Run", "self.parent.target()", 4, self.parent.player_index.run_action))
        self.action_cards.append(ActionCard(self, "Back", "self.parent.menu_back()", 5))
        self.set_action_card_positions()

    def set_ability_actions(self):
        self.state = "Ability"
        self.action_cards.clear()
        for i, ability in enumerate(self.parent.player_index.abilities):
            self.action_cards.append(ActionCard(self, ability.name, "self.parent.target()", i, ability))
        self.action_cards.append(ActionCard(self, "Back", "self.parent.menu_back()", len(self.parent.player_index.abilities)))
        self.set_action_card_positions()

    def set_item_actions(self):
        pass

    def menu_back(self):
        if self.state in ["Target"]:
            self.state = "Main"
            self.set_main_actions()
            self.selected_action = None
        elif self.state == "Main":
            self.parent.turn_sub_state = "Browse"
            self.action_cards.clear()
        elif self.state == "Ability":
            self.state = "Main"
            self.set_main_actions()

    def set_action_card_positions(self):
        for action_card in self.action_cards:
            action_card.set_position(len(self.action_cards))

    def handle_action(self, action):
        if action == "click" and self.action_cards:
            for card in self.action_cards:
                card.handle_action(action)
        elif action == "un-click":
            if self.selected_action is not None and self.state == "Target":
                for sprite in self.parent.battle_characters.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        self.selected_action.battle_action.target_set(None, [sprite])
                        self.menu_back()
                        self.menu_back()
                        break
                else:
                    self.menu_back()


class ActionCard(object):
    def __init__(self, parent, name, function, index, battle_action=None):
        self.battle_action = battle_action
        self.parent = parent
        self.name = name
        self.function = function
        self.active = False
        self.hover = False
        self.name = name
        self.index = index
        self.layer = index
        self.selected = False
        self.pos = (0, 0)
        self.size = (15*settings.X/100, 26*settings.Y/100)
        self.distance_x_mouse = int

    def handle_action(self, action):
        if action == "click":
            if self.layer == -1 and settings.click_check(self.pos + self.size):
                self.select()

    def update(self, dt):
        self.distance_x_mouse = (self.pos[0] + self.size[0]/2) - pygame.mouse.get_pos()[0]
        if self.distance_x_mouse < 0:
            self.distance_x_mouse *= -1
        self.hover = False
        if settings.click_check(self.pos + self.size):
            self.hover = True
        self.layer = self.index

    def toggle_position(self):
        if self.hover and self.layer == -1:
            self.pos = self.pos[0], self.parent.card_rect[1] - 2*settings.Y/100
        else:
            self.pos = self.pos[0], self.parent.card_rect[1]

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.pos + self.size, border_radius=8)
        pygame.draw.rect(surface, (150, 150, 150), self.pos + self.size, width=5, border_radius=8)
        text_rect = [self.pos[0]+(1*settings.X/100), self.pos[1]+(1*settings.Y/100), self.size[0]-(2*settings.X/100), self.size[1]]
        settings.tw(surface, self.name, settings.TEXT_COLOR, text_rect, settings.TEXT_FONT)

    def select(self):
        eval(self.function)
        self.parent.pointer.set_anchor((self.pos[0] + self.size[0]/2, self.pos[1]))

    def set_position(self, number_cards):
        max_card_with_no_overlap = math.floor(self.parent.card_rect[2]/self.size[0])
        if number_cards <= max_card_with_no_overlap:
            self.pos = self.get_position()
        else:
            self.pos = self.get_overlap_position(number_cards)

    def get_position(self):
        return self.parent.card_rect[0] + self.index * self.size[0], self.parent.card_rect[1]

    def get_overlap_position(self, number_cards):
        offset = self.parent.card_rect[2]/number_cards
        return self.parent.card_rect[0] + self.index * offset, self.parent.card_rect[1]

    def __lt__(self, other):
        return self.layer < other.layer

    def __gt__(self, other):
        return self.layer > other.layer

    def __eq__(self, other):
        return self.layer == other.layer

    def __le__(self, other):
        return self.layer <= other.layer

    def __ge__(self, other):
        return self.layer >= other.layer

    def __ne__(self, other):
        return self.layer != other.layer


class Pointer(object):
    def __init__(self, parent):
        self.parent = parent
        self.point_1 = (200, 500)
        self.point_2 = (50, 400)
        self.pointer_spline_point = (100, 300)
        self.n_points = 10
        self.points = []
        self.triangle_pointer = Wireframe(self, [(0, 0), (40, 10), (40, -10)])

    def update(self, dt):
        self.points = bezier(np.arange(0, 1, 1/self.n_points), [self.point_1, self.point_2, self.pointer_spline_point, pygame.mouse.get_pos()])
        self.triangle_pointer.update(dt)
        self.pointer_spline_point = pygame.mouse.get_pos()[0] - 200, pygame.mouse.get_pos()[1]

    def draw(self, surface):
        if self.points:
            for point in self.points:
                pygame.draw.circle(surface, (100, 20, 20), point, 10, 4)
            self.triangle_pointer.draw(surface)

    def set_anchor(self, point):
        self.point_1 = point


def bezier(weights, points):
    bezier_points = []
    for weight in weights:
        bezier_points.append(lerp_recurse(weight, points))
    return bezier_points


def lerp_recurse(float_, points):
    new_points = []
    for i in range(1, len(points)):
        new_points.append(lerp(points[i], points[i-1], float_))
    if len(new_points) > 1:
        return lerp_recurse(float_, new_points)
    else:
        return new_points[0]


def lerp(point_1, point_2, float_):
    """give two points and a float in [0, 1] and return a point between proportional to the float"""
    return point_1[0] + (float_ * (point_2[0] - point_1[0])), point_1[1] + (float_ * (point_2[1] - point_1[1]))


class Wireframe(object):
    def __init__(self, parent, points):
        self.parent = parent
        self.theta = 0
        self.pos = (0, 0)
        self.points = points
        self.draw_points = points

    def update(self, dt):
        self.pos = pygame.mouse.get_pos()
        self.draw_points = []
        for point in self.points:
            self.draw_points.append(self.point_transform(point))
        self.theta = angle_find((-1, 0), difference_vector(self.pos, self.parent.pointer_spline_point))

    def draw(self, surface):
        draw_wireframe(surface, self.draw_points)

    def point_transform(self, point):
        rot = np.array([[math.cos(self.theta), -math.sin(self.theta)], [math.sin(self.theta), math.cos(self.theta)]])
        v = np.array([point[0], point[1]])
        v2 = np.dot(rot, v)
        return v2[0] + self.pos[0], v2[1] + self.pos[1]


def draw_wireframe(surface, points, width=4):
    for i, point in enumerate(points):
        pygame.draw.line(surface, (200, 200, 200), point, points[i-1], width)


def angle_find(v1, v2):
    cosine_theta = np.dot(v1, v2)
    sine_theta = np.cross(v1, v2)
    return np.arctan2(sine_theta, cosine_theta)


def difference_vector(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def length(v1):
    return math.sqrt(v1[0]**2 + v1[1]**2)
