import pygame
import settings
from base import BaseState
from settings import PartyAbilityManager, PlayerCharacter


class CharacterSelect(BaseState):
    def __init__(self):
        super(CharacterSelect, self).__init__()
        self.active_index = 0
        self.name_entry_index = -1
        self.confirm_index = -1
        self.options = settings.BASE_CLASSES
        self.next_state = "MENU"
        self.state = "Class_Select"
        self.name_entry = ""
        self.fighter_state = 'selected'
        self.adept_state = 'unselected'
        self.rogue_state = 'unselected'
        self.artificer_state = 'unselected'
        self.fighter_sprites = settings.SpriteSheet(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter_Select128p.png").load_strip([0, 0, 256, 256], 12, (255, 55, 202))
        self.fighter_selected_sprites = settings.SpriteSheet(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter_Select256p.png").load_strip([0, 0, 256, 256], 12, (255, 55, 202))
        self.fighter_idle_frames = [0, 1]
        self.fighter_idle_speed = 2000
        self.fighter_idle_weights = [5, 1]
        self.fighter_flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.fighter_flourish_speed = 2000
        self.fighter_flourish_weights = [10, 1, 1, 1, 1, 1, 1, 1, 1, 5]
        self.fighter_image = self.fighter_sprites[0]
        self.fighter_animation_index = 0
        self.fighter_animation_time = 0
        self.fighter_x = settings.CHARACTER_SELECT_MENU['fighter pos'][0]
        self.fighter_y = settings.CHARACTER_SELECT_MENU['fighter pos'][1]
        self.selected_x = settings.CHARACTER_SELECT_MENU['selected pos'][0]
        self.selected_y = settings.CHARACTER_SELECT_MENU['selected pos'][1]
        self.fighter_rect = pygame.rect.Rect(self.fighter_x, self.fighter_y, self.fighter_image.get_width(),
                                             self.fighter_image.get_height())
        weight_sum = 0
        for value in self.fighter_idle_weights:
            weight_sum += value
        for i, value in enumerate(self.fighter_idle_weights):
            self.fighter_idle_weights[i] = value * self.fighter_idle_speed / weight_sum
        weight_sum = 0
        for value in self.fighter_flourish_weights:
            weight_sum += value
        for i, value in enumerate(self.fighter_flourish_weights):
            self.fighter_flourish_weights[i] = value * self.fighter_flourish_speed / weight_sum

        self.rogue_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['images128']
        self.rogue_selected_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['images256']
        self.rogue_idle_frames = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['idle_frames']
        self.rogue_idle_speed = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['idle_speed']
        self.rogue_idle_weights = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['idle_weights']
        self.rogue_flourish_frames = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['flourish_frames']
        self.rogue_flourish_speed = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['flourish_speed']
        self.rogue_flourish_weights = settings.CHARACTER_SELECT_MENU['sprites']["Rogue"]['flourish_weights']
        self.rogue_image = self.rogue_sprites[self.rogue_idle_frames[0]]
        self.rogue_animation_index = 0
        self.rogue_animation_time = 0
        self.rogue_x = settings.CHARACTER_SELECT_MENU['rogue pos'][0]
        self.rogue_y = settings.CHARACTER_SELECT_MENU['rogue pos'][1]
        self.selected_x = settings.CHARACTER_SELECT_MENU['selected pos'][0]
        self.selected_y = settings.CHARACTER_SELECT_MENU['selected pos'][1]
        self.rogue_rect = pygame.rect.Rect(self.rogue_x, self.rogue_y, self.rogue_image.get_width(),
                                           self.rogue_image.get_height())
        weight_sum = 0
        for value in self.rogue_idle_weights:
            weight_sum += value
        for i, value in enumerate(self.rogue_idle_weights):
            self.rogue_idle_weights[i] = value * self.rogue_idle_speed / weight_sum
        weight_sum = 0
        for value in self.rogue_flourish_weights:
            weight_sum += value
        for i, value in enumerate(self.rogue_flourish_weights):
            self.rogue_flourish_weights[i] = value * self.rogue_flourish_speed / weight_sum

        self.adept_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['images128']
        self.adept_selected_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['images256']
        self.adept_idle_frames = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['idle_frames']
        self.adept_idle_speed = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['idle_speed']
        self.adept_idle_weights = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['idle_weights']
        self.adept_flourish_frames = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['flourish_frames']
        self.adept_flourish_speed = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['flourish_speed']
        self.adept_flourish_weights = settings.CHARACTER_SELECT_MENU['sprites']["Adept"]['flourish_weights']
        self.adept_image = self.adept_sprites[self.adept_idle_frames[0]]
        self.adept_animation_index = 0
        self.adept_animation_time = 0
        self.adept_x = settings.CHARACTER_SELECT_MENU['adept pos'][0]
        self.adept_y = settings.CHARACTER_SELECT_MENU['adept pos'][1]
        self.selected_x = settings.CHARACTER_SELECT_MENU['selected pos'][0]
        self.selected_y = settings.CHARACTER_SELECT_MENU['selected pos'][1]
        self.adept_rect = pygame.rect.Rect(self.adept_x, self.adept_y, self.adept_image.get_width(),
                                           self.adept_image.get_height())
        weight_sum = 0
        for value in self.adept_idle_weights:
            weight_sum += value
        for i, value in enumerate(self.adept_idle_weights):
            self.adept_idle_weights[i] = value * self.adept_idle_speed / weight_sum
        weight_sum = 0
        for value in self.adept_flourish_weights:
            weight_sum += value
        for i, value in enumerate(self.adept_flourish_weights):
            self.adept_flourish_weights[i] = value * self.adept_flourish_speed / weight_sum

        self.artificer_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['images128']
        self.artificer_selected_sprites = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['images256']
        self.artificer_idle_frames = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['idle_frames']
        self.artificer_idle_speed = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['idle_speed']
        self.artificer_idle_weights = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['idle_weights']
        self.artificer_flourish_frames = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['flourish_frames']
        self.artificer_flourish_speed = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['flourish_speed']
        self.artificer_flourish_weights = settings.CHARACTER_SELECT_MENU['sprites']["Artificer"]['flourish_weights']
        self.artificer_image = self.artificer_sprites[self.artificer_idle_frames[0]]
        self.artificer_animation_index = 0
        self.artificer_animation_time = 0
        self.artificer_x = settings.CHARACTER_SELECT_MENU['artificer pos'][0]
        self.artificer_y = settings.CHARACTER_SELECT_MENU['artificer pos'][1]
        self.selected_x = settings.CHARACTER_SELECT_MENU['selected pos'][0]
        self.selected_y = settings.CHARACTER_SELECT_MENU['selected pos'][1]
        self.artificer_rect = pygame.rect.Rect(self.artificer_x, self.artificer_y, self.artificer_image.get_width(),
                                               self.artificer_image.get_height())
        weight_sum = 0
        for value in self.artificer_idle_weights:
            weight_sum += value
        for i, value in enumerate(self.artificer_idle_weights):
            self.artificer_idle_weights[i] = value * self.artificer_idle_speed / weight_sum
        weight_sum = 0
        for value in self.artificer_flourish_weights:
            weight_sum += value
        for i, value in enumerate(self.artificer_flourish_weights):
            self.artificer_flourish_weights[i] = value * self.artificer_flourish_speed / weight_sum

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0] - (3 / 4 * settings.X / len(self.options)) +
                  (index * settings.X / (2 * len(self.options))), self.screen_rect.center[1] +
                  (0.25 * settings.Y))
        return text.get_rect(center=center)

    def handle_action(self, action):
        if self.state == "Class_Select":
            if action == "mouse_move":
                if settings.click_check(settings.CHARACTER_SELECT_MENU['class_option_rects']["Fighter"]):
                    self.active_index = 0
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['class_option_rects']["Adept"]):
                    self.active_index = 1
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['class_option_rects']["Rogue"]):
                    self.active_index = 2
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['class_option_rects']["Artificer"]):
                    self.active_index = 3
            elif action == "click":
                self.handle_action("Select")
            elif action == "Left":
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if self.active_index <= 0:
                    self.active_index = len(self.options) - 1
                else:
                    self.active_index -= 1
            elif action == "Right":
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.active_index += 1
                self.active_index %= len(self.options)
            elif action == "Select":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.state = "Name_Entry"
            if self.active_index == 0:
                self.fighter_state = 'selected'
                self.adept_state = 'unselected'
                self.rogue_state = 'unselected'
                self.artificer_state = 'unselected'
            elif self.active_index == 1:
                self.fighter_state = 'unselected'
                self.adept_state = 'selected'
                self.rogue_state = 'unselected'
                self.artificer_state = 'unselected'
            elif self.active_index == 2:
                self.fighter_state = 'unselected'
                self.adept_state = 'unselected'
                self.rogue_state = 'selected'
                self.artificer_state = 'unselected'
            elif self.active_index == 3:
                self.fighter_state = 'unselected'
                self.adept_state = 'unselected'
                self.rogue_state = 'unselected'
                self.artificer_state = 'selected'

        elif self.state == "Name_Entry":
            mods = pygame.key.get_mods()
            if action == "mouse_move":
                if settings.click_check(settings.CHARACTER_SELECT_MENU['name_entry_option_rects']["random"]):
                    self.name_entry_index = 0
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['name_entry_option_rects']["select"]):
                    self.name_entry_index = 1
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['name_entry_option_rects']["back"]):
                    self.name_entry_index = 2
                else:
                    self.name_entry_index = -1
            elif action == "click":
                if self.name_entry_index == 0:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                    self.name_entry = settings.random_name()
                elif self.name_entry_index == 1:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    if len(self.name_entry) > 0:
                        self.state = "Confirm"
                elif self.name_entry_index == 2:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                    self.state = "Class_Select"
            elif action == "Backspace":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                if len(self.name_entry) > 0:
                    self.name_entry = self.name_entry[:-1]
                else:
                    self.state = "Class_Select"
            elif action == "Select":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                if len(self.name_entry) > 0:
                    self.state = "Confirm"
            elif action == "a" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "b" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "c" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "d" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "e" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "f" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "g" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "h" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "i" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "j" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "k" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "l" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "m" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "n" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "o" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "p" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "q" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "r" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "s" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "t" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "u" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "v" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "w" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "x" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "y" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "z" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.name_entry += action.upper()
                else:
                    self.name_entry += action
            elif action == "space" and len(self.name_entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.name_entry += " "

        elif self.state == "Confirm":
            if action == "mouse_move":
                if settings.click_check(settings.CHARACTER_SELECT_MENU['confirm_rects']["confirm"]):
                    self.confirm_index = 0
                elif settings.click_check(settings.CHARACTER_SELECT_MENU['confirm_rects']["back"]):
                    self.confirm_index = 1
                else:
                    self.confirm_index = -1
            elif action == "click":
                if self.confirm_index == 0:
                    settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                    self.state = "Start"
                elif self.confirm_index == 1:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                    self.state = "Name_Entry"
            if action == "Select":
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.state = "Start"
            elif action == "Backspace":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.state = "Name_Entry"

    def update(self, dt):
        self.persist["Transition"].update(dt)
        self.fighter_animation_time += settings.random_int(10, 30)
        if self.fighter_animation_time > self.fighter_idle_weights[self.fighter_animation_index]:
            self.fighter_animation_time -= self.fighter_idle_weights[self.fighter_animation_index]
            self.fighter_animation_index += 1
            if self.fighter_animation_index >= len(self.fighter_idle_frames):
                self.fighter_animation_index = 0
        if self.fighter_state == 'unselected':
            self.fighter_image = self.fighter_sprites[self.fighter_idle_frames[self.fighter_animation_index]]
            self.fighter_rect = pygame.rect.Rect(self.fighter_x, self.fighter_y, self.fighter_image.get_width(),
                                                 self.fighter_image.get_height())
        elif self.fighter_state == 'selected':
            self.fighter_image = self.fighter_selected_sprites[self.fighter_idle_frames[self.fighter_animation_index]]
            self.fighter_rect = pygame.rect.Rect(self.selected_x, self.selected_y, self.fighter_image.get_width(),
                                                 self.fighter_image.get_height())

        self.adept_animation_time += settings.random_int(10, 30)
        if self.adept_animation_time > self.adept_idle_weights[self.adept_animation_index]:
            self.adept_animation_time -= self.adept_idle_weights[self.adept_animation_index]
            self.adept_animation_index += 1
            if self.adept_animation_index >= len(self.adept_idle_frames):
                self.adept_animation_index = 0
        if self.adept_state == 'unselected':
            self.adept_image = self.adept_sprites[self.adept_idle_frames[self.adept_animation_index]]
            self.adept_rect = pygame.rect.Rect(self.adept_x, self.adept_y, self.adept_image.get_width(),
                                               self.adept_image.get_height())
        elif self.adept_state == 'selected':
            self.adept_image = self.adept_selected_sprites[self.adept_idle_frames[self.adept_animation_index]]
            self.adept_rect = pygame.rect.Rect(self.selected_x, self.selected_y, self.adept_image.get_width(),
                                               self.adept_image.get_height())

        self.rogue_animation_time += settings.random_int(10, 30)
        if self.rogue_animation_time > self.rogue_idle_weights[self.rogue_animation_index]:
            self.rogue_animation_time -= self.rogue_idle_weights[self.rogue_animation_index]
            self.rogue_animation_index += 1
            if self.rogue_animation_index >= len(self.rogue_idle_frames):
                self.rogue_animation_index = 0
        if self.rogue_state == 'unselected':
            self.rogue_image = self.rogue_sprites[self.rogue_idle_frames[self.rogue_animation_index]]
            self.rogue_rect = pygame.rect.Rect(self.rogue_x, self.rogue_y, self.rogue_image.get_width(),
                                               self.rogue_image.get_height())
        elif self.rogue_state == 'selected':
            self.rogue_image = self.rogue_selected_sprites[self.rogue_idle_frames[self.rogue_animation_index]]
            self.rogue_rect = pygame.rect.Rect(self.selected_x, self.selected_y, self.rogue_image.get_width(),
                                               self.rogue_image.get_height())

        self.artificer_animation_time += settings.random_int(10, 30)
        if self.artificer_animation_time > self.artificer_idle_weights[self.artificer_animation_index]:
            self.artificer_animation_time -= self.artificer_idle_weights[self.artificer_animation_index]
            self.artificer_animation_index += 1
            if self.artificer_animation_index >= len(self.artificer_idle_frames):
                self.artificer_animation_index = 0
        if self.artificer_state == 'unselected':
            self.artificer_image = self.artificer_sprites[self.artificer_idle_frames[self.artificer_animation_index]]
            self.artificer_rect = pygame.rect.Rect(self.artificer_x, self.artificer_y, self.artificer_image.get_width(),
                                                   self.artificer_image.get_height())
        elif self.artificer_state == 'selected':
            self.artificer_image = self.artificer_selected_sprites[
                self.artificer_idle_frames[self.artificer_animation_index]]
            self.artificer_rect = pygame.rect.Rect(self.selected_x, self.selected_y, self.artificer_image.get_width(),
                                                   self.artificer_image.get_height())

        if self.state == "Start":
            self.next_state = "REGION_SELECT"
            # setup persist dictionary
            self.persist['region_generate'] = True
            self.persist['region_index'] = 0
            self.persist['characters'] = []
            self.persist['characters'].append(eval(f"settings.{self.options[self.active_index]}")(name=self.name_entry))
            self.persist['supplies'] = 10
            self.persist['chargers'] = 5
            self.persist['elixirs'] = 5
            self.persist['gold'] = 1000
            self.persist['region_type'] = "None"
            self.persist['inventory'] = [settings.StimPack(), settings.StimPack(), settings.StimPack(),
                                         settings.StimPack(), settings.StimPack()]
            settings.character_initial(self.persist['characters'][0], self.options[self.active_index])
            self.persist['equip menu indices'] = settings.REGION_MENUS['equip menu']['equip menu indices']
            self.persist['party_abilities'] = PartyAbilityManager()
            self.done = True

        self.persist["Transition"].update(dt)
        self.persist['SFX'].update(dt)
        self.persist['FX'].update(dt)
        self.persist['Music'].update(dt)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.handle_action("Left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("Right")
            elif event.key == pygame.K_RETURN:
                self.handle_action("Select")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("Backspace")
            elif event.key == pygame.K_a:
                self.handle_action("a")
            elif event.key == pygame.K_b:
                self.handle_action("b")
            elif event.key == pygame.K_c:
                self.handle_action("c")
            elif event.key == pygame.K_d:
                self.handle_action("d")
            elif event.key == pygame.K_e:
                self.handle_action("e")
            elif event.key == pygame.K_f:
                self.handle_action("f")
            elif event.key == pygame.K_g:
                self.handle_action("g")
            elif event.key == pygame.K_h:
                self.handle_action("h")
            elif event.key == pygame.K_i:
                self.handle_action("i")
            elif event.key == pygame.K_j:
                self.handle_action("j")
            elif event.key == pygame.K_k:
                self.handle_action("k")
            elif event.key == pygame.K_l:
                self.handle_action("l")
            elif event.key == pygame.K_m:
                self.handle_action("m")
            elif event.key == pygame.K_n:
                self.handle_action("n")
            elif event.key == pygame.K_o:
                self.handle_action("o")
            elif event.key == pygame.K_p:
                self.handle_action("p")
            elif event.key == pygame.K_q:
                self.handle_action("q")
            elif event.key == pygame.K_r:
                self.handle_action("r")
            elif event.key == pygame.K_s:
                self.handle_action("s")
            elif event.key == pygame.K_t:
                self.handle_action("t")
            elif event.key == pygame.K_u:
                self.handle_action("u")
            elif event.key == pygame.K_v:
                self.handle_action("v")
            elif event.key == pygame.K_w:
                self.handle_action("w")
            elif event.key == pygame.K_x:
                self.handle_action("x")
            elif event.key == pygame.K_y:
                self.handle_action("y")
            elif event.key == pygame.K_z:
                self.handle_action("z")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")

    def draw(self, surface):
        surface.fill(pygame.Color("black"))

        if self.state == "Class_Select":
            surface.blit(self.fighter_image, self.fighter_rect)
            for index, option in enumerate(self.options):
                rect_var = settings.CHARACTER_SELECT_MENU['class_option_rects'][option]
                if self.active_index == index:
                    settings.tw(surface, option, settings.TEXT_COLOR,
                                [rect_var[0] - (len(option) * settings.X * 3 / 1000), rect_var[1],
                                     rect_var[2], rect_var[3]], settings.HEADING_FONT)
                else:
                    settings.tw(surface, option, settings.TEXT_COLOR,
                                settings.CHARACTER_SELECT_MENU['class_option_rects'][option],
                                settings.TEXT_FONT)
            surface.blit(self.fighter_image, self.fighter_rect)
            surface.blit(self.adept_image, self.adept_rect)
            surface.blit(self.rogue_image, self.rogue_rect)
            surface.blit(self.artificer_image, self.artificer_rect)

        elif self.state == "Name_Entry":
            rect_var = settings.CHARACTER_SELECT_MENU['name_display_rect']
            settings.tw(surface, self.name_entry, settings.TEXT_COLOR,
                        [rect_var[0] - (len(self.name_entry) * settings.X * 9 / 1000), rect_var[1], rect_var[2],
                             rect_var[3]], settings.HEADING_FONT)
            rect_var = settings.CHARACTER_SELECT_MENU['class_display_rect']
            settings.tw(surface, self.options[self.active_index], settings.TEXT_COLOR,
                        [rect_var[0] - (len(self.options[self.active_index]) * settings.X * 9 / 1000), rect_var[1],
                             rect_var[2],
                             rect_var[3]], settings.HEADING_FONT)
            if self.fighter_state == 'selected':
                surface.blit(self.fighter_image, self.fighter_rect)
            elif self.adept_state == 'selected':
                surface.blit(self.adept_image, self.adept_rect)
            elif self.rogue_state == 'selected':
                surface.blit(self.rogue_image, self.rogue_rect)
            elif self.artificer_state == 'selected':
                surface.blit(self.artificer_image, self.artificer_rect)

            settings.tw(surface, "Input a name. Press enter to continue or backspace to select another class.",
                        settings.TEXT_COLOR, settings.CHARACTER_SELECT_MENU['prompt_rect'], settings.HEADING_FONT)

            options = settings.CHARACTER_SELECT_MENU['name_entry_option_rects'].keys()
            for i, option in enumerate(options):
                color = settings.TEXT_COLOR
                if self.name_entry_index == i:
                    color = settings.SELECTED_COLOR
                settings.tw(surface, option, color, settings.CHARACTER_SELECT_MENU['name_entry_option_rects'][option],
                            settings.HEADING_FONT)

        elif self.state == "Confirm":
            rect_var = settings.CHARACTER_SELECT_MENU['name_display_rect']
            settings.tw(surface, self.name_entry, settings.TEXT_COLOR,
                        [rect_var[0] - (len(self.name_entry) * settings.X * 9 / 1000), rect_var[1], rect_var[2],
                             rect_var[3]], settings.HEADING_FONT)
            rect_var = settings.CHARACTER_SELECT_MENU['class_display_rect']
            settings.tw(surface, self.options[self.active_index], settings.TEXT_COLOR,
                        [rect_var[0] - (len(self.options[self.active_index]) * settings.X * 9 / 1000), rect_var[1],
                             rect_var[2],
                             rect_var[3]], settings.HEADING_FONT)
            if self.fighter_state == 'selected':
                surface.blit(self.fighter_image, self.fighter_rect)
            elif self.adept_state == 'selected':
                surface.blit(self.adept_image, self.adept_rect)
            elif self.rogue_state == 'selected':
                surface.blit(self.rogue_image, self.rogue_rect)
            elif self.artificer_state == 'selected':
                surface.blit(self.artificer_image, self.artificer_rect)

            settings.tw(surface, "Press enter to embark. Press backspace to reconsider.", settings.TEXT_COLOR,
                        settings.CHARACTER_SELECT_MENU['prompt_rect'], settings.HEADING_FONT)

            options = settings.CHARACTER_SELECT_MENU['confirm_rects'].keys()
            for i, option in enumerate(options):
                color = settings.TEXT_COLOR
                if self.confirm_index == i:
                    color = settings.SELECTED_COLOR
                settings.tw(surface, option, color, settings.CHARACTER_SELECT_MENU['confirm_rects'][option],
                            settings.HEADING_FONT)

        elif self.state == "Start":
            pass

        self.persist["Transition"].draw(surface)
        self.persist['FX'].draw(surface)

    def startup(self, persistent):
        self.persist = persistent
        self.persist["Transition"].fade_in(500)

