import pygame
import math
import settings
import pytweening
from base import BaseState


class BattleMessage:
    def __init__(self):
        self.message = None
        self.timer = 0

    def draw(self, surface):
        if self.message is not None:
            pygame.draw.rect(surface, (100, 100, 100), [200, 50, 880, 100], border_radius=12)
            settings.tw(surface, self.message, settings.TEXT_COLOR, [200, 50, 880, 100], settings.TEXT_FONT)
            pass

    def update(self, dt):
        if self.timer != -1:
            if self.timer > 0:
                self.timer -= dt
            if self.dt <= 0:
                self.message = None

    def set_message(self, message, duration):
        self.message = message
        self.timer = duration

class DamageParticle:
    def __init__(self):
        self.particles = []

    def draw(self, surface):
        if self.particles:
            particles_copy = []
            for particle in self.particles:
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
            self.particles = particles_copy
        self.delete_particles()

    def add_particles(self, x, y, damage, critical=False, velocity=(1, 1)):
        rect = [x, y, 200, 100]
        f = settings.random_int(1090, 1150) / 1000
        l = settings.random_int(100, 120) / 100
        if (settings.X*3/8) - x < 0:
            velocity = (-settings.X/100 * velocity[0], (-settings.Y/720)*l * velocity[1])
            force = (f, 0)
        else:
            velocity = (settings.X/100 * velocity[0], (-settings.Y/720)*l * velocity[1])
            force = (f, 0)

        color = (20, 100, 20)
        particle = [rect, velocity, force, damage, color, critical]
        self.particles.append(particle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[4] != (255, 255, 255)]
        self.particles = particle_copy
        particle_copy = [particle for particle in self.particles if particle[0][1] > 0]
        self.particles = particle_copy


class BattleEffect(pygame.sprite.Sprite):
    def __init__(self, animation, pos):
        super().__init__()
        self.sprites = settings.BATTLE_ANIMATIONS[animation]['sprites']
        self.image = self.sprites[0]
        self.rect = pygame.rect.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.x = pos[0]
        self.y = pos[1]
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.weights = settings.BATTLE_ANIMATIONS[animation]['weights']
        self.speed = settings.BATTLE_ANIMATIONS[animation]['speed']
        sum_weights = sum(self.weights)
        for i in range(len(self.weights)):
            self.weights[i] = int(self.speed * self.weights[i] / sum_weights)
        self.time = 0
        self.animation_index = 0

    def update(self, dt):
        self.time += dt
        if self.time >= self.weights[self.animation_index]:
            self.animation_index += 1
            self.time = 0
            if self.animation_index > len(self.weights) - 1:
                self.kill()
            else:
                self.image = self.sprites[self.animation_index]


    def delete_effects(self):
        pass


class BattleAction(pygame.sprite.Sprite):
    def __init__(self, source, speed):
        super().__init__()
        self.hover = False
        self.selected = False
        self.move_selected = False
        self.source = source
        self.target = 'none'
        self.target_type = 'none'
        self.action = 'none'
        self.action_type = 'none'
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.order = 0
        self.speed = speed
        self.sprites = settings.BATTLE_MENU_SPRITES['action slot sprites']
        self.attack_frames = settings.BATTLE_MENU_SPRITES['attack action']
        self.attack_action_weights = settings.BATTLE_MENU_SPRITES['attack action weights']
        self.skill_frames = settings.BATTLE_MENU_SPRITES['skill action']
        self.skill_action_weights = settings.BATTLE_MENU_SPRITES['skill action weights']
        self.item_frames = settings.BATTLE_MENU_SPRITES['item action']
        self.item_action_weights = settings.BATTLE_MENU_SPRITES['item action weights']
        self.defend_frames = settings.BATTLE_MENU_SPRITES['defend action']
        self.defend_action_weights = settings.BATTLE_MENU_SPRITES['defend action weights']
        self.no_actions_frames = settings.BATTLE_MENU_SPRITES['no action']
        self.no_action_weights = settings.BATTLE_MENU_SPRITES['no action weights']
        self.animation_speed = settings.BATTLE_MENU_SPRITES['animation speed']
        self.image = self.sprites[self.no_actions_frames[0]]
        self.animation_index = 0
        self.animation_time = 0
        self.x = 0
        self.y = 0
        self.target = None
        self.action = None
        self.action_type = None
        self.move_selected = False
        self.target_type = None
        self.defense_stat = None
        self.attack_stat = None
        weight_sum = 0
        for value in self.no_action_weights:
            weight_sum += value
        for i, value in enumerate(self.no_action_weights):
            self.no_action_weights[i] = value * self.animation_speed / weight_sum

    def update(self, dt):
        self.x = settings.BATTLE_MENUS['slot positions'][self.order][0]
        self.y = settings.BATTLE_MENUS['slot positions'][self.order][1]
        self.animation_time += dt
        if self.action == 'none':
            if self.animation_index > len(self.no_action_weights) - 1:
                self.animation_index = 0
            if self.animation_time > self.no_action_weights[self.animation_index]:
                self.animation_time -= self.no_action_weights[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(self.no_actions_frames):
                    self.animation_index = 0
            self.image = self.sprites[self.no_actions_frames[self.animation_index]]
        elif self.action == "Attack":
            if self.animation_index > len(self.attack_action_weights) - 1:
                self.animation_index = 0
            if self.animation_time > self.attack_action_weights[self.animation_index]:
                self.animation_time -= self.attack_action_weights[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(self.attack_frames):
                    self.animation_index = 0
            self.image = self.sprites[self.attack_frames[self.animation_index]]
        elif self.action == "Skill":
            if self.animation_index > len(self.skill_action_weights) - 1:
                self.animation_index = 0
            if self.animation_time > self.skill_action_weights[self.animation_index]:
                self.animation_time -= self.skill_action_weights[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(self.skill_frames):
                    self.animation_index = 0
            self.image = self.sprites[self.skill_frames[self.animation_index]]
        elif self.action == "Item":
            if self.animation_index > len(self.item_action_weights) - 1:
                self.animation_index = 0
            if self.animation_time > self.item_action_weights[self.animation_index]:
                self.animation_time -= self.item_action_weights[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(self.item_frames):
                    self.animation_index = 0
            self.image = self.sprites[self.item_frames[self.animation_index]]
        elif self.action == "Defend":
            if self.animation_index > len(self.defend_action_weights) - 1:
                self.animation_index = 0
            if self.animation_time > self.defend_action_weights[self.animation_index]:
                self.animation_time -= self.defend_action_weights[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(self.defend_frames):
                    self.animation_index = 0
            self.image = self.sprites[self.defend_frames[self.animation_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class BattleManager(object):
    def __init__(self, persist):
        self.apply_effects = []
        self.status_tick = []
        self.persist = persist
        self.actions_sorted = False
        self.damage_particle = DamageParticle()
        self.enemies = pygame.sprite.Group()
        self.heroes = pygame.sprite.Group()
        self.battle_characters = pygame.sprite.Group()
        self.actions = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.list_enemy_slot = ['enemy_a', 'enemy_b', 'enemy_c', 'enemy_d', 'enemy_e']
        n_enemy = len(persist['nodes'][persist['current_position']].event_data.battle)
        region_index = persist['region_index']
        for i in range(n_enemy):
            enemy = persist['nodes'][persist['current_position']].event_data.battle[i]
            setattr(self, self.list_enemy_slot[i], eval("settings."+enemy)(self.list_enemy_slot[i], region_index, n_enemy))
            self.enemies.add(getattr(self, self.list_enemy_slot[i]))
            self.battle_characters.add(getattr(self, self.list_enemy_slot[i]))
            setattr(getattr(self, self.list_enemy_slot[i]), 'action', BattleAction(self.list_enemy_slot[i],
                                                                              getattr(self, self.list_enemy_slot[i]).speed))
            self.actions.add(getattr(getattr(self, self.list_enemy_slot[i]), 'action'))
        for player in persist['characters'].keys():
            setattr(self, player, Hero(persist['characters'][player].current_class, player, persist))
            self.heroes.add(getattr(self, player))
            self.battle_characters.add(getattr(self, player))
            setattr(getattr(self, player), 'action', BattleAction(player, getattr(self, player).speed))
            self.actions.add(getattr(getattr(self, player), 'action'))
        self.sort_actions()
        self.state = "Turn"  # "Turn", "Do_Action", "Delay"
        self.action_index = 0
        self.current_action = None
        self.sub_state = "Rolls"
        self.battle_message = 'none'
        self.delay_timer = 0
        self.miss_roll = 0
        self.crit_roll = 0
        self.damage_roll = 0
        self.miss = False
        self.damage = 0
        self.damage_list = []
        self.damage_table = ('player_a', 'player_b', 'player_c', 'enemy_a', 'enemy_b', 'enemy_c', 'enemy_d', 'enemy_e')
        self.gold = 0
        self.supply = 0
        self.charger = 0
        self.elixir = 0
        self.item = []
        self.exp = 0
        self.persist = persist

    def draw(self, surface):
        self.enemies.draw(surface)
        self.heroes.draw(surface)
        self.actions.draw(surface)
        self.damage_particle.draw(surface)
        self.effects.draw(surface)

        for sprite in self.enemies:
            if sprite.hover:
                pygame.draw.rect(surface, (150, 20, 150), [1029, 545, 246, 170], 5, 12)
                settings.tw(surface, "hp", settings.TEXT_COLOR,
                            [1040, 560, 50, 100], settings.TEXT_FONT)
                settings.tw(surface, str(sprite.hp) + "/" + str(sprite.max_hp), settings.TEXT_COLOR,
                            [1080, 560, 100, 100], settings.TEXT_FONT)
                settings.tw(surface, "mp", settings.TEXT_COLOR,
                            [1040, 590, 50, 100], settings.TEXT_FONT)
                settings.tw(surface, str(sprite.mp) + "/" + str(sprite.max_mp), settings.TEXT_COLOR,
                            [1080, 590, 100, 100], settings.TEXT_FONT)
        for i, action in enumerate(self.actions.sprites()):
            if action.hover:
                surface.blit(settings.BATTLE_MENU_SPRITES['target_reticules']['source'],
                             (getattr(self, action.source).x, getattr(self, action.source).y))
                if action.target:
                    if action.target == 'all_enemy':
                        pass
                    elif action.target == 'all_hero':
                        pass
                    elif action.target == 'all':
                        pass
                    else:
                        if hasattr(self, action.target):
                            surface.blit(settings.BATTLE_MENU_SPRITES['target_reticules']['target'],
                                         (getattr(self, action.target).x, getattr(self, action.target).y))
        for sprite in self.heroes:
            settings.tw(surface, "hp: " + str(sprite.hp) + "/" + str(sprite.max_hp), settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['hp'], settings.DETAIL_FONT)
            settings.tw(surface, "mp: " + str(sprite.mp) + "/" + str(sprite.max_mp), settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['mp'], settings.DETAIL_FONT)
            settings.tw(surface, sprite.name, settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['name'], settings.TEXT_FONT)

    def actions_reset(self):  # delete each action if done and recreate, tick down turn delay on actions that aren't
        for i, action in enumerate(self.actions.sprites()):
            source = action.source
            if hasattr(action, "turns"):
                action.turns -= 1
                if action.turns <= 0:
                    delattr(action, "turns")
            else:
                action.kill()
                del action
                setattr(getattr(self, source), 'action',  BattleAction(source, getattr(getattr(self, source), 'speed')))
                self.actions.add(getattr(self, source).action)

    def enemy_is_dead(self, enemy):
        if enemy.hp <= 0:
            self.gold += enemy.gold_reward
            self.exp += enemy.exp_reward
            self.elixir += enemy.elixir_reward
            self.charger += enemy.charger_reward
            if enemy.item_reward != 'none':
                self.item.append(enemy.item_reward)
            for action in self.actions:
                if action.source == enemy.slot:
                    action.kill()
            enemy.kill()

    def hero_is_dead(self, hero):
        if hero.hp <= 0:
            hero.kill()
            del hero

    def update(self, dt):
        for enemy in self.enemies:
            self.enemy_is_dead(enemy)
        for hero in self.heroes:
            self.hero_is_dead(hero)
        self.battle_characters.update(dt)
        self.actions.update(dt)
        self.effects.update(dt)

        if self.state == "Do_Action":
            for i, action in enumerate(self.actions.sprites()):
                if action.order == self.action_index:
                    self.current_action = action
            if self.sub_state == "Rolls":  # miss crit and damage rolls
                if self.current_action != 'none':
                    self.miss_roll = settings.random_int(0, 100)
                    self.crit_roll = settings.random_int(0, 100)
                    self.damage_roll = settings.random_int(85, 100)
                    self.sub_state = "Calculate"
                else:
                    self.sub_state = "Reset"
            elif self.sub_state == "Calculate":  # damage calc
                self.damage_calculate()
                self.effect_calculate()
                self.sub_state = "Source_Animation"
            elif self.sub_state == "Source_Animation":  # set user animation state and delay
                if self.current_action.action_type == "Attack":
                    getattr(self, self.current_action.source).state = "Attack"
                elif self.current_action.action_type == "Skill" or self.current_action.action_type == "Item":
                    getattr(self, self.current_action.source).state = "Cast"
                self.delay_timer = 100
                self.sub_state = "Action_Animation"
                self.state = "Delay"
            elif self.sub_state == "Action_Animation":  # call action animation and set delay
                if "Animation" in settings.actions_dict[self.current_action.action_type][self.current_action.action].keys():
                    if self.current_action.target_type == "Single":
                        self.effects.add(BattleEffect(settings.actions_dict[self.current_action.action_type]\
                                                          [self.current_action.action]["Animation"],
                                                      (getattr(self, self.current_action.target).rect.centerx,
                                                       getattr(self, self.current_action.target).rect.centery)))
                self.delay_timer = 200
                self.sub_state = "Target_Animation"
                self.state = "Delay"
            elif self.sub_state == "Target_Animation":  # set target animation and set delay
                if self.current_action.target_type == "Single":
                    getattr(self, self.current_action.target).state = "Hit"
                    #getattr(self, self.current_action.target).state = "Miss"
                self.delay_timer = 100
                self.sub_state = "Status_Update"
                self.state = "Delay"
            elif self.sub_state == "Status_Update":  # update all affected status and reset user and target animations
                getattr(self, self.current_action.source).state = "Idle"
                if self.current_action.target_type == "Single":
                    getattr(self, self.current_action.target).state = "Idle"
                    self.sub_state = "Reset"
                    if self.current_action.action != 'none':
                        self.delay_timer = 500
                        self.state = "Delay"
                        self.status_update()
                        self.sub_state = "Call_Effects"
                        if hasattr(self.current_action, 'hits'):
                            self.current_action.hits -= 1
                            if self.current_action.hits <= 0:
                                delattr(self.current_action, 'hits')
                            else:
                                self.sub_state = "Rolls"
            elif self.sub_state == "Call_Effects":
                self.delay_timer = 500
                self.state = "Delay"
                if len(self.apply_effects) > 0:
                    self.sub_state = "Call_Effects"
                    self.call_effects()
                else:
                    self.sub_state = "Reset"
            elif self.sub_state == "Reset":  # update index check for actions set action state
                self.action_index += 1
                self.sub_state = "Rolls"
                if self.action_index > len(self.actions.sprites()) - 1:
                    self.action_index = 0
                    self.state = "Status_Tick"
                    self.actions_reset()
                    self.sort_actions()

        if self.state == "Status_Tick":
            for i, character in enumerate(self.battle_characters.sprites()):
                for j, status in enumerate(settings.STATUS_LIST):
                    if getattr(character, status) > 0:
                        setattr(character, status, getattr(character, status) - 1)
                        worn_off = False
                        if getattr(character, status) <= 0:
                            setattr(character, status, 0),
                            worn_off = True
                        hp_loss = 0
                        if status in settings.STATUS_LIST_EOT.keys():
                            if status == "bleed":
                                hp_loss = int(settings.STATUS_LIST_EOT[status]['effect'] * character.hp / 100)
                            if status == "toxic":
                                hp_loss = int(settings.STATUS_LIST_EOT[status]['effect'] * (character.max_hp - character.hp) / 100)
                            if status == "burn":
                                hp_loss = settings.STATUS_LIST_EOT[status]['effect']
                        self.status_tick.append([character.slot, status, hp_loss, worn_off])
            self.state = "Status_Update"

        if self.state == "Status_Update":
            if len(self.status_tick) > 0:
                print(self.status_tick[0])
                if self.status_tick[0][2] > 0:
                    getattr(self, self.status_tick[0][0]).hp -= self.status_tick[0][2]
                    self.damage_particle.add_particles(getattr(self, self.status_tick[0][0]).x +
                                                       getattr(self, self.status_tick[0][0]).rect[2] / 2,
                                                       getattr(self, self.status_tick[0][0]).y +
                                                       getattr(self, self.status_tick[0][0]).rect[3] / 2,
                                                       str(self.status_tick[0][2]))
                    if self.status_tick[0][3]:
                        self.damage_particle.add_particles(getattr(self, self.status_tick[0][0]).x +
                                                           getattr(self, self.status_tick[0][0]).rect[2] / 2,
                                                           getattr(self, self.status_tick[0][0]).y +
                                                           getattr(self, self.status_tick[0][0]).rect[3] / 2,
                                                           self.status_tick[0][1] + ' has worn off', velocity=(1, -1.2))
                self.status_tick = self.status_tick[1:]
            else:
                self.state = "Turn"

        elif self.state == "Delay":
            self.delay_timer -= dt
            if self.delay_timer <= 0:
                self.delay_timer = 0
                self.state = "Do_Action"

#  Sorting algorithm for action speed



#  set an action to a BattleAction container
    def set_action(self, source, target, action, action_type):
        print(action_type)
        reference_action = None
        for key in settings.actions_dict.keys():
            if key == action_type:
                for value in settings.actions_dict[action_type].keys():
                    if value == action:
                        reference_action = settings.actions_dict[action_type][value]
        reference_weapon = None
        if action_type == "Attack":
            if source in self.persist['characters'].keys():
                if "Weapon" in self.persist['characters'][source].equipment.keys():
                    reference_weapon = self.persist['characters'][source].equipment["Weapon"]
        setattr(getattr(getattr(self, source), 'action'), 'target', target)
        setattr(getattr(getattr(self, source), 'action'), 'action', action)
        setattr(getattr(getattr(self, source), 'action'), 'action_type', action_type)
        setattr(getattr(getattr(self, source), 'action'), 'move_selected', True)
        setattr(getattr(getattr(self, source), 'action'), 'target_type', settings.actions_dict[action_type][action]["Target"])
        setattr(getattr(getattr(self, source), 'action'), 'defend_stat', settings.actions_dict[action_type][action]["Defend_Stat"])
        setattr(getattr(getattr(self, source), 'action'), 'attack_stat', settings.actions_dict[action_type][action]["Attack_Stat"])
        if reference_weapon:
            if hasattr(reference_weapon, 'hits'):
                setattr(getattr(self, source), 'hits', reference_weapon.hits)
        if reference_action:
            if hasattr(reference_action, 'hits'):
                if hasattr(getattr(self, source), 'hits'):
                    setattr(getattr(self, source), 'hits', max(reference_action.hits, getattr(self, source).hits))
                else:
                    setattr(getattr(self, source), 'hits', reference_action.hits)

    def call_effects(self):
        if self.current_action.target_type == "Single":
            if len(self.apply_effects) > 0:
                status = self.apply_effects[0][0]
                turns = self.apply_effects[0][1]
                self.apply_effects = self.apply_effects[1:]
                setattr(getattr(self, self.current_action.target), status, turns +
                getattr(getattr(self, self.current_action.target), status))
                self.damage_particle.add_particles(getattr(self, self.current_action.target).x +
                                                   getattr(self, self.current_action.target).rect[2] / 2,
                                                   getattr(self, self.current_action.target).y +
                                                   getattr(self, self.current_action.target).rect[3] / 2,
                                                   status + str(turns).rjust(3))

    def effect_calculate(self):
        if self.current_action.target_type == "Single":
            if "status" in settings.actions_dict[self.current_action.action_type][self.current_action.action].keys():
                for status in settings.actions_dict[self.current_action.action_type][self.current_action.action]["status"].keys():
                    r = settings.random_int(0, 100)
                    a = getattr(getattr(self, self.current_action.source), 'luck')
                    d = getattr(getattr(self, self.current_action.source), 'luck')
                    effect_chance = settings.actions_dict[self.current_action.action_type][self.current_action.action]["status"][status][0]
                    effect_turns = settings.actions_dict[self.current_action.action_type][self.current_action.action]["status"][status][1]
                    if r * d/a < effect_chance:
                        self.apply_effects.append((status, effect_turns))
            if self.current_action.action_type == "Attack" and self.current_action.source not in self.list_enemy_slot:
                for i, status in enumerate(settings.STATUS_LIST):
                    if 'Weapon' in self.persist['characters'][self.current_action.source].equipment.keys():
                        if hasattr(self.persist['characters'][self.current_action.source].equipment['Weapon'], status):
                            r = settings.random_int(0, 100)
                            a = getattr(getattr(self, self.current_action.source), 'luck')
                            d = getattr(getattr(self, self.current_action.source), 'luck')
                            effect_chance = getattr(self.persist['characters'][self.current_action.source].equipment['Weapon'], status)[0]
                            effect_turns = getattr(self.persist['characters'][self.current_action.source].equipment['Weapon'], status)[1]
                            if r * d/a < effect_chance:
                                self.apply_effects.append((status, effect_turns))

        elif self.current_action.target_type == "Team":
            pass
        elif self.current_action.target_type == "All":
            pass

    def damage_calculate(self):
        if self.current_action.target_type == "Single":
            defense = attack = getattr(getattr(self, self.current_action.source),
                                       'strength')
            if self.current_action.defend_stat == "lowest" or self.current_action.defend_stat == "none":
                defense = min([getattr(getattr(self, self.current_action.target), 'defense'),
                               getattr(getattr(self, self.current_action.target), 'spirit')])
            else:
                defense = getattr(getattr(self, self.current_action.target), self.current_action.defend_stat)
            if hasattr(self.current_action, 'power'):
                power = self.current_action.power
            else:
                power = 20
            if getattr(getattr(self, self.current_action.source), "crit_rate") * self.crit_roll / 100 > 95:
                critical = getattr(self, self.current_action.source).crit_damage * 1.5
            else:
                critical = 1
            damage = self.damage_normal(attack, defense, power, critical)
            self.damage = damage
            self.damage_list = 'none'
        elif self.current_action.target_type == "Team":
            pass
        elif self.current_action.target_type == "All":
            pass

    def status_update(self):
        if self.current_action.target_type == "Single":
            critical = True
            if self.damage - int(self.damage) == 0:
                critical = False
            getattr(self, self.current_action.target).hp -= int(self.damage)
            self.damage_particle.add_particles(getattr(self, self.current_action.target).x +
                                               getattr(self, self.current_action.target).rect[2] / 2,
                                               getattr(self, self.current_action.target).y +
                                               getattr(self, self.current_action.target).rect[3] / 2,
                                               int(self.damage), critical=critical)
            if getattr(self, self.current_action.target).hp < 0:
                getattr(self, self.current_action.target).hp = 0

    def damage_normal(self, attack, defense, power, targets=1, critical=1, other=1):
        damage = int((power * attack / defense) * targets * critical * other * self.damage_roll / 100)
        if critical != 1:
            damage += 0.1
        return damage


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.action = None
        self.hover = False
        self.selected = False
        self.hp_current = 1
        self.current_sprite = 0
        self.state = "Idle"
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


class Hero(Character):
    def __init__(self, class_type, player_holder, persist):
        super().__init__()
        self.slot = player_holder
        self.move_selected = False
        self.sprites = settings.battle_characters[class_type]['sprites']
        self.idle_frames = settings.battle_characters[class_type]['idle']
        self.idle_weights = settings.battle_characters[class_type]['idle weights']
        self.idle_speed = settings.battle_characters[class_type]['idle speed']
        self.idle_time = settings.random_int(0, self.idle_speed)
        self.idle_index = 0
        weight_sum = 0
        for value in self.idle_weights:
            weight_sum += value
        for i, value in enumerate(self.idle_weights):
            self.idle_weights[i] = value * self.idle_speed / weight_sum
        self.attack_frames = settings.battle_characters[class_type]['attack']
        self.cast_frames = settings.battle_characters[class_type]['cast']
        self.hit_frames = settings.battle_characters[class_type]['hit']
        self.miss_frames = settings.battle_characters[class_type]['miss']
        self.base_x = 300
        self.x = self.base_x
        self.base_y = 300
        self.y = self.base_y
        self.image = self.sprites[self.idle_frames[self.idle_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hp = persist['characters'][player_holder].hp
        self.max_hp = persist['characters'][player_holder].max_hp
        self.mp = persist['characters'][player_holder].mp
        self.max_mp = persist['characters'][player_holder].max_mp
        self.strength = persist['characters'][player_holder].strength
        self.magic = persist['characters'][player_holder].magic
        self.defense = persist['characters'][player_holder].defense
        self.spirit = persist['characters'][player_holder].spirit
        self.luck = persist['characters'][player_holder].luck
        self.speed = persist['characters'][player_holder].speed
        self.name = persist['characters'][player_holder].name
        self.skills = persist['characters'][player_holder].abilities
        self.crit_rate = persist['characters'][player_holder].crit_rate
        self.crit_damage = persist['characters'][player_holder].crit_damage
        self.attack_type = persist['characters'][player_holder].attack_type

    def update(self, dt):
        if self.state == "Idle":
            self.idle_time += settings.random_int(15, 20)
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


class Battle(BaseState):
    def __init__(self):
        super(Battle, self).__init__()
        self.mouse = pygame.mouse.get_pos()
        self.active_index = 0
        self.top_menu_index = -1
        self.next_state = "REGION"
        self.state = "Pre_Turn"
        self.selected_action = 'none'
        self.player_index = "player_a"
        self.state_options = ["Battle_Start", "Pre_Turn", "Turn", "Confirm", "Action", "Victory", "Defeat"]
        self.move_types = ["Attack", "Defend", "Skill", "Item", "Run"]
        self.turn_sub_state = "Browse"
        self.turn_sub_state_options = ["Browse", "Move_Select", "Skill", "Item", "Target_Select"]
        self.reticle_color = (0, 0, 0)
        self.target_color = (255, 180, 180)
        self.target_speed = 500
        self.target_time = 0
        self.target_direction = 1

    def startup(self, persistent):
        self.persist = persistent
        self.persist['battle manager'] = BattleManager(self.persist)

    def handle_action(self, action):
        if self.state == "Turn":
            if action == "mouse_move":
                self.mouse = pygame.mouse.get_pos()
#                print(self.mouse)
                for sprite in self.persist['battle manager'].enemies:
                    sprite.hover = False
                    if sprite.rect.collidepoint(self.mouse):
                        sprite.hover = True
                for sprite in self.persist['battle manager'].heroes:
                    sprite.hover = False
                    if sprite.rect.collidepoint(self.mouse):
                        sprite.hover = True
                for sprite in self.persist['battle manager'].actions:
                    sprite.hover = False
                    if sprite.rect.collidepoint(self.mouse):
                        sprite.hover = True
            if self.turn_sub_state == "Browse":
                if action == "click":
                    for sprite in self.persist['battle manager'].heroes:
                        if sprite.rect.collidepoint(self.mouse) and not sprite.move_selected:
                            self.player_index = sprite.slot
                            self.turn_sub_state = "Move_Select"
                    for sprite in self.persist['battle manager'].actions:
                        if sprite.source == "player_a" or sprite.source == "player_b" or sprite.source == "player_c":
                            if sprite.rect.collidepoint(self.mouse) and not sprite.move_selected:
                                self.player_index = sprite.source
                                self.turn_sub_state = "Move_Select"
                    if settings.click_check(settings.BATTLE_MENUS['turn_end_rect']):
                        self.state = "Confirm"
                if action == "t":
                    self.state = "Confirm"

            elif self.turn_sub_state == "Move_Select":
                if action == "mouse_move":
                    flag = False
                    for i, option in enumerate(self.move_types):
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            if self.top_menu_index != i:
                                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                            self.top_menu_index = i
                            flag = True
                    if not flag:
                        self.top_menu_index = -1
                elif action == "up":
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    self.top_menu_index -= 1
                    self.top_menu_index %= len(self.move_types)
                elif action == "down":
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    self.top_menu_index += 1
                    self.top_menu_index %= len(self.move_types)
                elif action == "return":
                    if self.top_menu_index == "Skill":
                        self.turn_sub_state = "Skill"
                    elif self.top_menu_index == "Item":
                        self.turn_sub_state = "Item"
                    elif self.top_menu_index == "Attack":
                        self.selected_action = self.persist['characters'][self.player_index].attack_type
                        self.turn_sub_state = "Target_" + settings.actions_dict["Attack"][self.selected_action]["Target"]
                    elif self.top_menu_index == "Defend":
                        self.selected_action = "Defend"
                        self.turn_sub_state = "Target"
                    elif self.top_menu_index == "Run":
                        self.selected_action = "Run"
                        self.turn_sub_state = "Target"
                elif action == "backspace":
                    self.turn_sub_state = "Browse"
                elif action == "click":
                    check = True
                    for i, option in enumerate(self.move_types):
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            if option == "Skill":
                                self.turn_sub_state = "Skill"
                                check = False
                            elif option == "Item":
                                self.turn_sub_state = "Item"
                                check = False
                            elif option == "Attack":
                                self.selected_action = self.persist['characters'][self.player_index].attack_type
                                self.turn_sub_state = "Target_" + settings.actions_dict["Attack"][self.selected_action]["Target"]
                                check = False
                            elif option == "Run":
                                self.selected_action = "Run"
                                self.turn_sub_state = "Target"
                                check = False
                            elif option == "Defend":
                                self.selected_action = "Defend"
                                self.turn_sub_state = "Target"
                                check = False
                            else:
                                self.top_menu_index = option
                                check = False
                    if check:
                        self.turn_sub_state = "Browse"

            elif self.turn_sub_state == "Skill":
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"

            elif self.turn_sub_state == "Item":
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"

            elif self.turn_sub_state == "Target_Single":
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"
                if action == "click":
                    pos = pygame.mouse.get_pos()
                    target = 'none'
                    source = self.player_index
                    for sprite in self.persist['battle manager'].battle_characters:
                        if sprite.rect.collidepoint(pos):
                            target = sprite.slot
                    if target != 'none':
                        if self.top_menu_index == "Attack":
                            target_type = \
                                settings.actions_dict["Attack"][self.persist['characters'][source].attack_type][
                                    "Target"]
                        elif self.top_menu_index == "Defend":
                            pass
                        elif self.top_menu_index == "Skill":
                            pass
                        elif self.top_menu_index == "Item":
                            pass
                        elif self.top_menu_index == "Run":
                            pass
                        self.persist['battle manager'].set_action(source, target, self.selected_action,
                                                                  self.move_types[self.top_menu_index])
                        self.turn_sub_state = "Browse"
                    else:
                        self.turn_sub_state = "Move_Select"
            elif self.turn_sub_state == "Target_Team":
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"
                if action == "click":
                    pos = pygame.mouse.get_pos()
                    target = 'none'
                    source = self.player_index
                    for sprite in self.persist['battle manager'].battle_characters:
                        if sprite.rect.collidepoint(pos):
                            target = sprite.slot
                    if target != 'none':
                        if self.top_menu_index == "Attack":
                            target_type = \
                                settings.actions_dict["Attack"][self.persist['characters'][source].attack_type][
                                    "Target"]
                        elif self.top_menu_index == "Skill":
                            pass
                        elif self.top_menu_index == "Item":
                            pass
                        self.persist['battle manager'].set_action(source, target, self.selected_action,
                                                                  self.top_menu_index)
                        self.turn_sub_state = "Browse"
                    else:
                        self.turn_sub_state = "Move_Select"

        elif self.state == "Confirm":
            if action == "backspace" or action == "n":
                self.state = "Turn"
            elif action == "y":
                self.persist['battle manager'].state = "Do_Action"
                self.state = "Action"
            elif action == "mouse_move":
                self.mouse = pygame.mouse.get_pos()
            elif action == "click":
                if settings.click_check(settings.BATTLE_MENUS['confirm_yes_rect']):
                    self.persist['battle manager'].state = "Do_Action"
                    self.state = "Action"
                elif settings.click_check(settings.BATTLE_MENUS['confirm_no_rect']):
                    self.state = "Turn"

        elif self.state == "Action":
            if self.persist['battle manager'].state == "Turn":
                self.state = "Pre_Turn"
                self.turn_sub_state = "Browse"

        elif self.state == "Victory":
            if action == "return":
                exp = math.ceil(self.persist['battle manager'].exp / len(self.persist['battle manager'].heroes))
                for hero in self.persist['characters']:
                    self.persist['characters'][hero].exp += exp
                self.persist['supplies'] += self.persist['battle manager'].supply
                self.persist['gold'] += self.persist['battle manager'].gold
                self.persist['chargers'] += self.persist['battle manager'].charger
                self.persist['elixirs'] += self.persist['battle manager'].elixir
                for hero in self.persist['battle manager'].heroes:
                    self.persist['characters'][hero.slot].hp = hero.hp
                    self.persist['characters'][hero.slot].exp += exp
                self.next_state = "REGION"
                self.done = True
                del self.persist['battle manager']
                self.state = "Pre_Turn"

        elif self.state == "Defeat":
            if action == "return":
                self.next_state = "MENU"
                self.done = True
                del self.persist['battle manager']
                self.state = "Turn"

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")

    def draw_action_browse(self, surface):
        pygame.draw.rect(surface, (150, 0, 150), settings.BATTLE_MENUS['move_top_menu_rects']['border'], 2)
        for i, option in enumerate(self.move_types):
            color = settings.TEXT_COLOR
            if i == self.top_menu_index:
                color = settings.SELECTED_COLOR
            settings.tw(surface, option, color,
                        settings.BATTLE_MENUS['move_top_menu_rects'][option],
                        settings.TEXT_FONT)

        if self.turn_sub_state == "Skill":
            pass

        elif self.turn_sub_state == "Item":
            pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        pygame.draw.rect(surface, (50, 50, 50), [0, settings.Y * 75 / 100, settings.X, settings.Y * 25 / 100])
        pygame.draw.rect(surface, (50, 50, 50), [settings.X * 80 / 100, 0, settings.X * 20 / 100, settings.Y])
        self.persist['battle manager'].draw(surface)
        if self.state == "Turn":
            if self.turn_sub_state == "Move_Select" or self.turn_sub_state == "Item" or self.turn_sub_state == "Skill":
                self.draw_action_browse(surface)
            elif self.turn_sub_state == "Browse":
                pygame.draw.rect(surface, (150, 150, 20), settings.BATTLE_MENUS['turn_end_rect'], 5, 12)
                settings.tw(surface, "END TURN", settings.TEXT_COLOR, settings.BATTLE_MENUS['turn_end_rect'],
                            settings.HEADING_FONT)
            elif self.turn_sub_state == "Target_Single":
                for i, sprite in enumerate(self.persist['battle manager'].battle_characters.sprites()):
                    if sprite.rect.collidepoint(self.mouse):
                        pygame.draw.rect(surface, self.reticle_color, [sprite.rect.left - 4, sprite.rect.top - 4,
                                                                       sprite.rect.width + 8, sprite.rect.height + 8], 2)
            elif self.turn_sub_state == "Target_Team":
                for i, sprite in enumerate(self.persist['battle manager'].enemies.sprites()):
                    if sprite.rect.collidepoint(self.mouse):
                        left = []
                        top = []
                        right = []
                        bottom = []
                        for j, value in enumerate(self.persist['battle manager'].enemies.sprites()):
                            left.append(value.rect.left)
                            top.append(value.rect.top)
                            right.append(value.rect.right)
                            bottom.append(value.rect.bottom)
                        rect = [min(left)-4, min(top) -4, max(right) - min(left) + 4, max(bottom) - min(top) + 4]
                        pygame.draw.rect(surface, self.reticle_color, rect, 2)
                        break
                for i, sprite in enumerate(self.persist['battle manager'].heroes.sprites()):
                    if sprite.rect.collidepoint(self.mouse):
                        left = []
                        top = []
                        right = []
                        bottom = []
                        for j, value in enumerate(self.persist['battle manager'].heroes.sprites()):
                            left.append(value.rect.left)
                            top.append(value.rect.top)
                            right.append(value.rect.right)
                            bottom.append(value.rect.bottom)
                        rect = [min(left)-4, min(top) -4, max(right) - min(left) + 4, max(bottom) - min(top) + 4]
                        pygame.draw.rect(surface, self.reticle_color, rect, 2)
                        break
            elif self.turn_sub_state == "Target_All":
                for i, sprite in enumerate(self.persist['battle manager'].battle_characters.sprites()):
                    if sprite.rect.collidepoint(self.mouse):
                        left = []
                        top = []
                        right = []
                        bottom = []
                        for j, value in enumerate(self.persist['battle manager'].battle_characters.sprites()):
                            left.append(value.rect.left)
                            top.append(value.rect.top)
                            right.append(value.rect.right)
                            bottom.append(value.rect.bottom)
                        rect = [min(left)-4, min(top) -4, max(right) - min(left) + 4, max(bottom) - min(top) + 4]
                        pygame.draw.rect(surface, self.reticle_color, rect, 2)
                        break
        if self.state == "Confirm":
            pygame.draw.rect(surface, (50, 50, 50), settings.BATTLE_MENUS['confirm_rect'], border_radius=12)
            pygame.draw.rect(surface, (150, 150, 20), settings.BATTLE_MENUS['confirm_rect'], 5, 12)
            settings.tw(surface, "End the turn?", settings.TEXT_COLOR, settings.BATTLE_MENUS['confirm_prompt_rect'],
                        settings.HEADING_FONT)
            settings.tw(surface, "YES", settings.TEXT_COLOR, settings.BATTLE_MENUS['confirm_yes_rect'],
                        settings.HEADING_FONT)
            settings.tw(surface, "NO", settings.TEXT_COLOR, settings.BATTLE_MENUS['confirm_no_rect'],
                        settings.HEADING_FONT)
        if self.state == "Victory":
            pygame.draw.rect(surface, (20, 20, 20),
                             [settings.X * 30 / 100, settings.Y * 30 / 100, settings.X * 40 / 100,
                              settings.Y * 40 / 100], border_radius=12)
            settings.tw(surface, "VICTORY!", settings.TEXT_COLOR,
                        [settings.X * 30 / 100, settings.Y * 30 / 100, settings.X * 40 / 100,
                             settings.Y * 40 / 100], settings.HEADING_FONT)
            settings.tw(surface, "Press enter to continue.", settings.TEXT_COLOR,
                        [settings.X * 30 / 100, settings.Y * 60 / 100, settings.X * 20 / 100,
                             settings.Y * 20 / 100], settings.TEXT_FONT)
        if self.state == "Defeat":
            pygame.draw.rect(surface, (20, 20, 20),
                             [settings.X * 30 / 100, settings.Y * 30 / 100, settings.X * 40 / 100,
                              settings.Y * 40 / 100], border_radius=12)
            settings.tw(surface, "Defeat!", settings.TEXT_COLOR,
                        [settings.X * 30 / 100, settings.Y * 30 / 100, settings.X * 40 / 100,
                             settings.Y * 40 / 100], settings.HEADING_FONT)
            settings.tw(surface, "Press enter to continue.", settings.TEXT_COLOR,
                        [settings.X * 30 / 100, settings.Y * 60 / 100, settings.X * 20 / 100,
                             settings.Y * 20 / 100], settings.TEXT_FONT)

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

    def update(self, dt):
        self.reticle_color_update(dt)
        if len(self.persist['battle manager'].heroes) == 0:
            self.state = "Defeat"
        elif len(self.persist['battle manager'].enemies) == 0:
            self.state = "Victory"
        if self.state != "Defeat" and self.state != "Victory":
            self.persist['battle manager'].update(dt)
        if self.state == "Pre_Turn":
            for i, enemy in enumerate(self.persist['battle manager'].enemies.sprites()):
                if enemy.ai['ai_type'] == 'simple':
                    self.simple_ai(enemy)
            self.state = "Turn"

    def simple_ai(self, enemy):
        action_set = settings.choose_random_weighted(enemy.ai['actions'], enemy.ai['weights'])
        action = action_set[1]
        action_type = action_set[0]
        if settings.actions_dict[action_type][action]["Target"] == "Single":
            target_options = []
            for hero in self.persist['battle manager'].heroes:
                target_options.append(hero.slot)
            if enemy.ai['target'] == 'random':
                target = settings.choose_random(target_options)
        self.persist['battle manager'].set_action(enemy.slot, target, action, action_type)
