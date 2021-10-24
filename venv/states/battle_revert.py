import pygame
import math
import settings
from base import BaseState


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
                print(new_velocity)
            self.particles = particles_copy
        self.delete_particles()

    def add_particles(self, x, y, damage, critical=False):
        rect = [x, y, 50, 30]
        f = settings.random_int(1090, 1150) / 1000
        l = settings.random_int(100, 120) / 100
        if (settings.X*3/8) - x < 0:
            velocity = (-settings.X/100, (-settings.Y/720)*l)
            force = (f, 0)
        else:
            velocity = (settings.X/100, (-settings.Y/720)*l)
            force = (f, 0)

        color = (20, 100, 20)
        particle = [rect, velocity, force, damage, color, critical]
        self.particles.append(particle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[4] != (255, 255, 255)]
        self.particles = particle_copy
        particle_copy = [particle for particle in self.particles if particle[0][1] > 0]
        self.particles = particle_copy


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
        num_enemy = len(persist['nodes'][persist['current_position']].event_data.battle)
        reg = persist['region_index']
        self.actions_sorted = False
        self.damage_particle = DamageParticle()
        self.enemies = pygame.sprite.Group()
        self.heroes = pygame.sprite.Group()
        self.battle_characters = pygame.sprite.Group()
        self.actions = pygame.sprite.Group()
        self.action_dict = {}
        self.enemy_a = Enemy(persist['nodes'][persist['current_position']].event_data.battle[0], 'enemy_a', reg,
                             num_enemy)
        self.enemies.add(self.enemy_a)
        self.action_dict['enemy_a'] = BattleAction('enemy_a', self.enemy_a.speed)
        self.actions.add(self.action_dict['enemy_a'])
        if num_enemy > 1:
            self.enemy_b = Enemy(persist['nodes'][persist['current_position']].event_data.battle[1], 'enemy_b', reg,
                                 num_enemy)
            self.enemies.add(self.enemy_b)
            self.action_dict['enemy_b'] = BattleAction('enemy_b', self.enemy_b.speed)
            self.actions.add(self.action_dict['enemy_b'])
        if num_enemy > 2:
            self.enemy_c = Enemy(persist['nodes'][persist['current_position']].event_data.battle[2], 'enemy_c', reg,
                                 num_enemy)
            self.enemies.add(self.enemy_c)
            self.action_dict['enemy_c'] = BattleAction('enemy_c', self.enemy_c.speed)
            self.actions.add(self.action_dict['enemy_c'])
        if num_enemy > 3:
            self.enemy_d = Enemy(persist['nodes'][persist['current_position']].event_data.battle[3], 'enemy_d', reg,
                                 num_enemy)
            self.enemies.add(self.enemy_d)
            self.action_dict['enemy_d'] = BattleAction('enemy_d', self.enemy_d.speed)
            self.actions.add(self.action_dict['enemy_d'])
        if num_enemy > 4:
            self.enemy_e = Enemy(persist['nodes'][persist['current_position']].event_data.battle[4], 'enemy_e', reg,
                                 num_enemy)
            self.enemies.add(self.enemy_e)
            self.action_dict['enemy_e'] = BattleAction('enemy_e', self.enemy_e.speed)
            self.actions.add(self.action_dict['enemy_e'])
        if 'player_a' in persist['characters']:
            self.player_a = Hero(persist['characters']['player_a'].current_class, 'player_a', persist)
            self.heroes.add(self.player_a)
            self.action_dict['player_a'] = BattleAction('player_a', self.player_a.speed)
            self.actions.add(self.action_dict['player_a'])
        if 'player_b' in persist['characters']:
            self.player_b = Hero(persist['characters']['player_b'].current_class, 'player_b', persist)
            self.heroes.add(self.player_b)
            self.action_dict['player_b'] = BattleAction('player_b', self.player_b.speed)
            self.actions.add(self.action_dict['player_b'])
        if 'player_c' in persist['characters']:
            self.player_c = Hero(persist['characters']['player_c'].current_class, 'player_c', persist)
            self.heroes.add(self.player_c)
            self.action_dict['player_c'] = BattleAction('player_c', self.player_c.speed)
            self.actions.add(self.action_dict['player_c'])
        self.sort_actions()
        self.state = "Turn"  # "Turn", "Do_Action", "Delay"
        self.action_index = 0
        self.do_current_action = 'player_a'
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

    def draw(self, surface):
        self.enemies.draw(surface)
        self.heroes.draw(surface)
        self.actions.draw(surface)
        self.damage_particle.draw(surface)

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
        for action in self.actions:
            if action.hover:
                surface.blit(settings.BATTLE_MENU_SPRITES['target_reticules']['source'],
                             (getattr(self, action.source).x, getattr(self, action.source).y))
                if action.target != 'none':
                    if action.target == 'all_enemy':
                        pass
                    elif action.target == 'all_hero':
                        pass
                    elif action.target == 'all':
                        pass
                    else:
                        surface.blit(settings.BATTLE_MENU_SPRITES['target_reticules']['target'],
                                     (getattr(self, action.target).x, getattr(self, action.target).y))
        for sprite in self.heroes:
            settings.tw(surface, "hp: " + str(sprite.hp) + "/" + str(sprite.max_hp), settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['hp'], settings.DETAIL_FONT)
            settings.tw(surface, "mp: " + str(sprite.mp) + "/" + str(sprite.max_mp), settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['mp'], settings.DETAIL_FONT)
            settings.tw(surface, sprite.name, settings.TEXT_COLOR,
                        settings.BATTLE_MENUS['player_status_rects'][sprite.slot]['name'], settings.TEXT_FONT)

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
            del self.action_dict[hero.slot]
            del hero

    def update(self, dt):
        for enemy in self.enemies:
            self.enemy_is_dead(enemy)
        for hero in self.heroes:
            self.hero_is_dead(hero)
        self.enemies.update(dt)
        self.heroes.update(dt)
        self.actions.update(dt)

        if self.state == "Do_Action":
            for action in self.action_dict:
                if self.action_dict[action].order == self.action_index:
                    self.do_current_action = action
            if self.sub_state == "Rolls":  # miss crit and damage rolls
                if self.do_current_action != 'none':
                    if self.action_dict[self.do_current_action].action_type == 'none' or \
                            self.action_dict[self.do_current_action].action == 'none':
                        self.sub_state = "Reset"
                    else:
                        self.miss_roll = settings.random_int(0, 100)
                        self.crit_roll = settings.random_int(0, 100)
                        self.damage_roll = settings.random_int(85, 100)
                        self.sub_state = "Calculate"
                else:
                    self.sub_state = "Status_Update"
            elif self.sub_state == "Calculate":  # damage calc
                self.damage_calculate()
                self.sub_state = "Source_Animation"
            elif self.sub_state == "Source_Animation":  # set user animation state and delay
                self.delay_timer = 100
                self.sub_state = "Action_Animation"
                self.state = "Delay"
            elif self.sub_state == "Action_Animation":  # call action animation and set delay
                self.delay_timer = 100
                self.sub_state = "Target_Animation"
                self.state = "Delay"
            elif self.sub_state == "Target_Animation":  # set target animation and set delay
                self.delay_timer = 100
                self.sub_state = "Status_Update"
                self.state = "Delay"
            elif self.sub_state == "Status_Update":  # update all affected status and reset user and target animations
                self.sub_state = "Reset"
                if self.do_current_action != 'none':
                    self.delay_timer = 500
                    self.state = "Delay"
                    self.status_update()
            elif self.sub_state == "Reset":  # update index check for actions set action state
                self.action_index += 1
                self.sub_state = "Rolls"
                if self.action_index > 8:
                    self.action_index = 0
                    self.state = "Turn"
                    self.clear_actions()
                    self.sort_actions()
            self.do_current_action = 'none'

        elif self.state == "Delay":
            self.delay_timer -= dt
            if self.delay_timer <= 0:
                self.delay_timer = 0
                self.state = "Do_Action"

    def sort_actions(self):
        self.actions_sorted = False
        i = 0
        for action in self.actions:
            action.order = i
            action.action = 'none'
            i += 1
        while not self.actions_sorted:
            flag = True
            for action1 in self.actions:
                for action2 in self.actions:
                    a = action1.order
                    b = action2.order
                    if a > b and action1.speed > action2.speed:
                        action1.order = b
                        action2.order = a
                        flag = False
            if flag:
                self.actions_sorted = True

    def set_action(self, source, target, action, action_type, target_type):
        self.action_dict[source].target = target
        self.action_dict[source].action = action
        self.action_dict[source].action_type = action_type
        self.action_dict[source].move_selected = True
        self.target_type = target_type

    def damage_calculate(self):
        action = settings.actions_dict[self.action_dict[self.do_current_action].action_type][
            self.action_dict[self.do_current_action].action]
        if action["Target"] == "Single":
            defense = attack = getattr(getattr(self, self.action_dict[self.do_current_action].source),
                                       action["Attack_Stat"])
            if action["Defend_Stat"] == "lowest":
                pass
            elif action["Defend_Stat"] == "none":
                defense = 0
            else:
                defense = getattr(getattr(self, self.action_dict[self.do_current_action].target), action["Defend_Stat"])
            if "Power" in action:
                power = action["Power"]
            else:
                power = 20
            if getattr(self,
                       self.action_dict[self.do_current_action].source).crit_rate * self.crit_roll / 100 > 95:
                critical = getattr(self, self.action_dict[self.do_current_action].source).crit_damage * 1.5
            else:
                critical = 1
            damage = self.damage_normal(attack, defense, power, critical)
            self.damage = damage
            self.damage_list = 'none'
        elif action["Target"] == "Team":
            pass
        elif action["Target"] == "All":
            pass

    def status_update(self):
        action = settings.actions_dict[self.action_dict[self.do_current_action].action_type][
            self.action_dict[self.do_current_action].action]
        if action["Target"] == "Single":
            critical = True
            if self.damage - int(self.damage) == 0:
                critical = False
            getattr(self, self.action_dict[self.do_current_action].target).hp -= int(self.damage)
            self.damage_particle.add_particles(getattr(self, self.action_dict[self.do_current_action].target).x +
                                               getattr(self, self.action_dict[self.do_current_action].target).rect[2]/2,
                                               getattr(self, self.action_dict[self.do_current_action].target).y +
                                               getattr(self, self.action_dict[self.do_current_action].target).rect[3]/2,
                                               int(self.damage), critical=critical)
            if getattr(self, self.action_dict[self.do_current_action].target).hp < 0:
                getattr(self, self.action_dict[self.do_current_action].target).hp = 0

    def damage_normal(self, attack, defense, power, targets=1, critical=1, other=1):
        damage = int((power * attack / defense) * targets * critical * other * self.damage_roll / 100)
        if critical != 1:
            damage += 0.1
        return damage

    def clear_actions(self):
        for action in self.action_dict:
            self.action_dict[action].target = 'none'
            self.action_dict[action].target_type = 'none'
            self.action_dict[action].action = 'none'
            self.action_dict[action].action_type = 'none'


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hover = False
        self.selected = False
        self.hp_current = 1
        self.current_sprite = 0
        self.state = "Idle"


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
        self.skills = persist['characters'][player_holder].techniques
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
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Enemy(Character):
    def __init__(self, enemy_type, enemy_holder, region_index, num_enemy):
        super().__init__()
        self.hover = False
        self.slot = enemy_holder
        self.sprites = settings.bestiary[enemy_type]['sprites']
        self.idle_frames = settings.bestiary[enemy_type]['idle']
        self.idle_weights = settings.bestiary[enemy_type]['idle weights']
        self.idle_speed = settings.bestiary[enemy_type]['idle speed']
        self.idle_time = settings.random_int(0, self.idle_speed)
        self.idle_index = 0
        weight_sum = 0
        for value in self.idle_weights:
            weight_sum += value
        for i, value in enumerate(self.idle_weights):
            self.idle_weights[i] = value * self.idle_speed / weight_sum
        self.attack_frames = settings.bestiary[enemy_type]['attack']
        self.cast_frames = settings.bestiary[enemy_type]['cast']
        self.hit_frames = settings.bestiary[enemy_type]['hit']
        self.miss_frames = settings.bestiary[enemy_type]['miss']
        self.x = self.base_x = settings.BATTLE_MENUS['enemy positions'][num_enemy][enemy_holder][0]
        self.y = self.base_y = settings.BATTLE_MENUS['enemy positions'][num_enemy][enemy_holder][1]
        self.image = self.sprites[self.idle_frames[self.idle_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hp = self.max_hp = settings.bestiary[enemy_type]['base_hp'][region_index]
        self.mp = self.max_mp = settings.bestiary[enemy_type]['base_mp'][region_index]
        self.strength = settings.bestiary[enemy_type]['base_attack'][region_index]
        self.magic = settings.bestiary[enemy_type]['base_magic'][region_index]
        self.defense = settings.bestiary[enemy_type]['base_defense'][region_index]
        self.spirit = settings.bestiary[enemy_type]['base_spirit'][region_index]
        self.luck = settings.bestiary[enemy_type]['base_luck'][region_index]
        self.speed = settings.bestiary[enemy_type]['base_speed'][region_index]
        self.crit_rate = settings.bestiary[enemy_type]['crit_rate'][region_index]
        self.crit_damage = settings.bestiary[enemy_type]['crit_damage'][region_index]
        self.ai = settings.bestiary[enemy_type]['ai']
        self.exp_reward, self.gold_reward, self.supply_reward, self.elixir_reward, self.charger_reward, \
        self.item_reward = self.reward(enemy_type, region_index)

    def reward(self, enemy_type, region_index):
        exp = settings.bestiary[enemy_type]['exp_reward'][region_index]
        gold = int(
            settings.bestiary[enemy_type]['gold_reward'][region_index] * settings.random_int(50, 100) / 100)
        supply = settings.random_int(settings.bestiary[enemy_type]['supply_reward'][region_index][0],
                                     settings.bestiary[enemy_type]['supply_reward'][region_index][1])
        elixir = settings.random_int(settings.bestiary[enemy_type]['elixir_reward'][region_index][0],
                                     settings.bestiary[enemy_type]['elixir_reward'][region_index][1])
        charger = settings.random_int(settings.bestiary[enemy_type]['charger_reward'][region_index][0],
                                      settings.bestiary[enemy_type]['charger_reward'][region_index][1])
        if len(settings.bestiary[enemy_type]['item_reward'][region_index]) == 1:
            if settings.bestiary[enemy_type]['item_reward'][region_index][0] != 'none':
                item = settings.item_generate(settings.bestiary[enemy_type]['item_reward'][region_index])
            else:
                item = 'none'
        else:
            n = settings.random_int(0, len(settings.bestiary[enemy_type]['item_reward'][region_index]))
            if settings.bestiary[enemy_type]['item_reward'][region_index][n - 1] != 'none':
                item = settings.item_generate(settings.bestiary[enemy_type]['item_reward'][region_index])
            else:
                item = 'none'
        return exp, gold, supply, elixir, charger, item

    def update(self, dt):
        if self.state == "Idle":
            self.idle_time += settings.random_int(15, 20)
            if self.idle_time > self.idle_weights[self.idle_index]:
                self.idle_time -= self.idle_weights[self.idle_index]
                self.idle_index += 1
                if self.idle_index >= len(self.idle_frames):
                    self.idle_index = 0
            self.image = self.sprites[self.idle_frames[self.idle_index]]
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Battle(BaseState):
    def __init__(self):
        super(Battle, self).__init__()
        self.active_index = 0
        self.top_menu_index = "Attack"
        self.next_state = "REGION"
        self.state = "Pre_Turn"
        self.selected_action = 'none'
        self.player_index = "player_a"
        self.state_options = ["Battle_Start", "Pre_Turn", "Turn", "Confirm", "Action", "Victory", "Defeat"]
        self.move_types = ["Attack", "Defend", "Skill", "Item", "Run"]
        self.turn_sub_state = "Browse"
        self.turn_sub_state_options = ["Browse", "Move_Select", "Skill", "Item", "Target_Select"]

    def startup(self, persistent):
        self.persist = persistent
        self.persist['battle manager'] = BattleManager(self.persist)

    def handle_action(self, action):
        if self.state == "Turn":
            if action == "mouse_move":
                pos = pygame.mouse.get_pos()
                print(pos)
                for sprite in self.persist['battle manager'].enemies:
                    sprite.hover = False
                    if sprite.rect.collidepoint(pos):
                        sprite.hover = True
                for sprite in self.persist['battle manager'].heroes:
                    sprite.hover = False
                    if sprite.rect.collidepoint(pos):
                        sprite.hover = True
                for sprite in self.persist['battle manager'].actions:
                    sprite.hover = False
                    if sprite.rect.collidepoint(pos):
                        sprite.hover = True
            if self.turn_sub_state == "Browse":
                if action == "click":
                    pos = pygame.mouse.get_pos()
                    for sprite in self.persist['battle manager'].heroes:
                        if sprite.rect.collidepoint(pos) and not sprite.move_selected:
                            self.player_index = sprite.slot
                            self.turn_sub_state = "Move_Select"
                    for sprite in self.persist['battle manager'].actions:
                        if sprite.source == "player_a" or sprite.source == "player_b" or sprite.source == "player_c":
                            if sprite.rect.collidepoint(pos) and not sprite.move_selected:
                                self.player_index = sprite.source
                                self.turn_sub_state = "Move_Select"
                    if settings.click_check(settings.BATTLE_MENUS['turn_end_rect']):
                        self.state = "Confirm"
                if action == "t":
                    self.state = "Confirm"

            elif self.turn_sub_state == "Move_Select":
                if action == "mouse_move":
                    for option in self.move_types:
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            self.top_menu_index = option

                elif action == "up":
                    current_index = self.move_types.index(self.top_menu_index)
                    max_index = len(self.move_types) - 1
                    new_index = current_index - 1
                    if new_index < 0:
                        new_index = max_index
                    self.top_menu_index = self.move_types[new_index]
                elif action == "down":
                    current_index = self.move_types.index(self.top_menu_index)
                    max_index = len(self.move_types) - 1
                    new_index = current_index + 1
                    if new_index > max_index:
                        new_index = 0
                    self.top_menu_index = self.move_types[new_index]
                elif action == "return":
                    if self.top_menu_index == "Skill":
                        self.turn_sub_state = "Skill"
                    elif self.top_menu_index == "Item":
                        self.turn_sub_state = "Item"
                    elif self.top_menu_index == "Attack":
                        self.selected_action = "Attack"
                        self.turn_sub_state = "Target"
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
                    for option in self.move_types:
                        if settings.click_check(settings.BATTLE_MENUS['move_top_menu_rects'][option]):
                            if option == "Skill":
                                self.turn_sub_state = "Skill"
                                check = False
                            elif option == "Item":
                                self.turn_sub_state = "Item"
                                check = False
                            elif option == "Attack":
                                self.selected_action = "Attack"
                                self.turn_sub_state = "Target"
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

            elif self.turn_sub_state == "Target":
                if action == "backspace":
                    self.turn_sub_state = "Move_Select"
                if action == "click":
                    target = 'none'
                    source = self.player_index
                    for sprite in self.persist['battle manager'].enemies:
                        pos = pygame.mouse.get_pos()
                        if sprite.rect.collidepoint(pos):
                            target = sprite.slot
                    for sprite in self.persist['battle manager'].heroes:
                        if sprite.rect.collidepoint(pos):
                            target = sprite.slot
                    if target != 'none':
                        if self.top_menu_index == "Attack":
                            target_type = \
                                settings.actions_dict["Attack"][self.persist['characters'][source].attack_type][
                                    "Target"]
                        if self.top_menu_index == "Defend":
                            pass
                        if self.top_menu_index == "Skill":
                            pass
                        if self.top_menu_index == "Item":
                            pass
                        if self.top_menu_index == "Run":
                            pass
                        self.persist['battle manager'].set_action(source, target, self.selected_action,
                                                                  self.top_menu_index, target_type)
                        self.turn_sub_state = "Browse"
                    else:
                        self.turn_sub_state = "Move_Select"

        elif self.state == "Confirm":
            if action == "backspace" or action == "n":
                self.state = "Turn"
            if action == "y":
                self.persist['battle manager'].state = "Do_Action"
                self.state = "Action"

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
        for option in self.move_types:
            if option == self.top_menu_index:
                settings.tw(surface, option, settings.SELECTED_COLOR,
                            settings.BATTLE_MENUS['move_top_menu_rects'][option],
                            settings.TEXT_FONT)
            else:
                settings.tw(surface, option, settings.TEXT_COLOR,
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
            if self.turn_sub_state == "Browse":
                pygame.draw.rect(surface, (150, 150, 20), settings.BATTLE_MENUS['turn_end_rect'], 5, 12)
                settings.tw(surface, "END TURN", settings.TEXT_COLOR, settings.BATTLE_MENUS['turn_end_rect'],
                            settings.HEADING_FONT)
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

    def update(self, dt):
        if len(self.persist['battle manager'].heroes) == 0:
            self.state = "Defeat"
        elif len(self.persist['battle manager'].enemies) == 0:
            self.state = "Victory"
        if self.state != "Defeat" and self.state != "Victory":
            self.persist['battle manager'].update(dt)
        if self.state == "Pre_Turn":
            for enemy in self.persist['battle manager'].enemies:
                if enemy.ai['ai_type'] == 'simple':
                    action_set = settings.choose_random_weighted(enemy.ai['actions'], enemy.ai['weights'])
                    action = action_set[1]
                    action_type = action_set[0]
                    target = ''
                    if settings.actions_dict[action_type][action]["Target"] == "Single":
                        target_options = []
                        for hero in self.persist['battle manager'].heroes:
                            target_options.append(hero.slot)
                        if enemy.ai['target'] == 'random':
                            target = settings.choose_random(target_options)
                    self.persist['battle manager'].set_action(enemy.slot, target, action, action_type,
                                                              settings.actions_dict[action_type][action]["Target"])
            self.state = "Turn"
