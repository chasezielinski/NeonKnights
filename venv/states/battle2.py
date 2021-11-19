import pygame
import math
import settings
import pytweening
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
        if action == "mouse_move":
            # mouse hover check
            for sprite in self.battle_objects.sprites():
                if hasattr(sprite, 'hover'):
                    sprite.hover = False
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.hover = True

        if self.state == "Turn":
            if self.turn_sub_state == "Browse":
                if action == "click":
                    # check for click on player character sprite or action queue sprite
                    for i, sprite in enumerate(self.battle_characters.sprites()):
                        if getattr(sprite, 'slot', 'none') in self.player_slots:
                            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                                self.player_index = sprite
                                print(self.player_index.speed)
                                self.turn_sub_state = "Move_Select"
                    # check for click on end turn button
                    if settings.click_check(settings.BATTLE_MENUS['turn_end_rect']):
                        self.turn_sub_state = "Confirm"
                if action == "t":
                    self.turn_sub_state = "Confirm"
            elif self.turn_sub_state == "Move_Select":
                if action == "mouse_move":
                    # check for mouse hover over move action types
                    flag = False
                    for i, option in enumerate(settings.actions_dict.keys()):
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            if self.action_type_index != i:
                                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                            self.action_type_index = i
                            flag = True
                    if not flag:
                        self.action_type_index = -1
                elif action == "up":
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    self.action_type_index -= 1
                    self.action_type_index %= len(settings.actions_dict.keys())
                elif action == "down":
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    self.action_type_index += 1
                    self.action_type_index %= len(settings.actions_dict.keys())
                elif action == "return":
                    if self.action_type_index == -1:
                        pass
                    elif settings.actions_dict.keys()[self.action_type_index] == "Skill":
                        if self.player_index.action_options:
                            if not self.player_index.dazed > 0 \
                                    and not self.player_index.stunned > 0:
                                for action in self.player_index.action_options:
                                    if action.is_usable():
                                        self.turn_sub_state = "Skill"
                                        break
                                else:
                                    pass
                    elif settings.actions_dict.keys()[self.action_type_index] == "Item":
                        if self.persist['inventory']:
                            if not self.player_index.perplexed > 0 \
                                    and not self.player_index.stunned > 0:
                                for item in self.persist['inventory']:
                                    if item.is_usable():
                                        self.turn_sub_state = "Item"
                                        break
                                else:
                                    pass
                    elif settings.actions_dict.keys()[self.action_type_index] == "Attack":
                        if hasattr(self.player_index, 'attack_action') \
                                and not self.player_index.disabled > 0 \
                                and not self.player_index.stunned > 0:
                            self.selected_action = self.player_index.attack_action
                            self.turn_sub_state = "Target"
                    elif settings.actions_dict.keys()[self.action_type_index] == "Defend":
                        if hasattr(self.player_index, 'defend_action') \
                                and not self.player_index.smitten > 0 \
                                and not self.player_index.stunned > 0:
                            self.selected_action = self.player_index.defend_action
                            self.turn_sub_state = "Target"
                    elif settings.actions_dict.keys()[self.action_type_index] == "Run":
                        if hasattr(self.player_index, 'run_action') \
                                and not self.player_index.trapped > 0 \
                                and not self.player_index.stunned > 0:
                            self.selected_action = self.player_index.run_action
                            self.turn_sub_state = "Target"
                elif action == "backspace":
                    self.turn_sub_state = "Browse"
                elif action == "click":
                    check = True
                    for i, option in enumerate(settings.actions_dict.keys()):
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            if option == "Skill":
                                print('here')
                                if self.player_index.abilities:
                                    print('here2')
                                    if not self.player_index.dazed > 0 \
                                            and not self.player_index.stunned > 0:
                                        print('here3')
                                        for action in self.player_index.abilities:
                                            print('here4')
                                            if action.is_usable():
                                                self.turn_sub_state = "Skill"
                                                check = False
                                                break
                                        else:
                                            pass
                            elif option == "Item":
                                if self.persist['inventory']:
                                    if not self.player_index.perplexed > 0 \
                                            and not self.player_index.stunned > 0:
                                        for item in self.persist['inventory']:
                                            if settings.BattleConsumable.__instancecheck__(item):
                                                self.turn_sub_state = "Item"
                                                check = False
                                                break
                            elif option == "Attack":
                                if hasattr(self.player_index, 'attack_action') \
                                        and not self.player_index.disabled > 0 \
                                        and not self.player_index.stunned > 0:
                                    self.selected_action = self.player_index.attack_action
                                    self.turn_sub_state = "Target"
                                    check = False
                            elif option == "Run":
                                if hasattr(self.player_index, 'run_action') \
                                        and not self.player_index.trapped > 0 \
                                        and not self.player_index.stunned > 0:
                                    self.selected_action = self.player_index.run_action
                                    self.turn_sub_state = "Target"
                                    check = False
                            elif option == "Defend":
                                if hasattr(self.player_index, 'defend_action') \
                                        and not self.player_index.smitten > 0 \
                                        and not self.player_index.stunned > 0:
                                    self.selected_action = self.player_index.defend_action
                                    self.turn_sub_state = "Target"
                                    check = False
                    if check:
                        self.turn_sub_state = "Browse"

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
                    player.exp += self.exp_reward/len(self.player_characters.sprites())
                self.persist['gold'] += self.gold_reward
                self.persist['supplies'] += self.supply_reward
                self.persist['chargers'] += self.charger_reward
                self.persist['elixirs'] += self.elixir_reward
        self.battle_objects.update(dt)
        self.battle_overlay.update(dt)
        self.damage_particle.update(dt)
        self.message.update(dt)
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
                if choice[1] != "None":
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
                self.delay(self.status_particle_index*500, "Pre_Turn")

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
