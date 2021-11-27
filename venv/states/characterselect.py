import pygame
import settings
from base import BaseState
from settings import PartyAbilityManager, PlayerCharacter

fighter_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
              r"Select\Fighter_Select128p.png "
fighter_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
              r"Select\Fighter_Select256p.png "
adept_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Fighter_Select128p.png "
adept_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Fighter_Select256p.png "
rogue_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Fighter_Select128p.png "
rogue_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Fighter_Select256p.png "
artificer_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
                r"Select\Fighter_Select128p.png "
artificer_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
                r"Select\Fighter_Select256p.png "


class CharacterSelect(BaseState):
    def __init__(self):
        super(CharacterSelect, self).__init__()
        self.max_name_length = 13
        self.active_index = 0
        self.name_entry_index = -1
        self.confirm_index = -1
        self.options = settings.BASE_CLASSES
        self.next_state = "MENU"
        self.state = "Class_Select"
        self.index = "Fighter"
        self.name_entry = ""
        self.class_rects = {
            "Fighter": [settings.X * 15 / 100, settings.Y * 80 / 100, settings.X * 20 / 100, settings.Y * 5 / 100],
            "Adept": [settings.X * 35 / 100, settings.Y * 80 / 100, settings.X * 20 / 100, settings.Y * 5 / 100],
            "Rogue": [settings.X * 55 / 100, settings.Y * 80 / 100, settings.X * 20 / 100, settings.Y * 5 / 100],
            "Artificer": [settings.X * 75 / 100, settings.Y * 80 / 100, settings.X * 20 / 100, settings.Y * 5 / 100],}
        self.class_sprites = pygame.sprite.Group()
        self.class_sprites.add(CharacterSelectSprite(self, "Fighter"), CharacterSelectSprite(self, "Adept"),
                               CharacterSelectSprite(self, "Rogue"), CharacterSelectSprite(self, "Artificer"), )

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0] - (3 / 4 * settings.X / len(self.options)) +
                  (index * settings.X / (2 * len(self.options))), self.screen_rect.center[1] +
                  (0.25 * settings.Y))
        return text.get_rect(center=center)

    def menu_toggle(self, action):
        index = list(self.class_rects.keys()).index(self.index)
        if action == "Right":
            index += 1
        else:
            index -= 1
        index %= len(self.class_rects)
        self.index = list(self.class_rects.keys())[index]

    def text_input(self, text):
        if self.state == "Name_Entry" and len(self.name_entry) < self.max_name_length:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                self.name_entry += text.upper()
            else:
                self.name_entry += text

    def handle_action(self, action):
        if self.state == "Class_Select":
            if action == "mouse_move":
                for key, value in self.class_rects.items():
                    if settings.click_check(value):
                        if self.index != key:
                            settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                        self.index = key
                        break
            elif action == "click":
                self.handle_action("Select")
            elif action == "Left" or "Right":
                self.menu_toggle(action)
            elif action == "Select":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.state = "Name_Entry"

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
        self.class_sprites.update(dt)
        self.persist["Transition"].update(dt)
        self.persist["Transition"].update(dt)
        self.persist['SFX'].update(dt)
        self.persist['FX'].update(dt)
        self.persist['Music'].update(dt)

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

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")
        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("mouse_move")
        elif event.type == pygame.KEYDOWN:
            if 97 <= event.key <= 122:
                self.text_input("{}".format(event.unicode))
            if event.key == pygame.K_LEFT:
                self.handle_action("Left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("Right")
            elif event.key == pygame.K_RETURN:
                self.handle_action("Select")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("Backspace")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.class_sprites.draw(surface)

        if self.state == "Class_Select":
            pass

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


class CharacterSelectSprite(pygame.sprite.Sprite):
    def __init__(self, parent, class_: str):
        super(CharacterSelectSprite, self).__init__()
        self.parent = parent
        self.selected = False
        self.timer = 0
        self.pos = self.selected_pos = settings.X * 4 / 10, settings.Y * 2 / 8
        if class_ == "Fighter":
            self.bg_sprites = settings.SpriteSheet(fighter_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(fighter_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_speed = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.bg_pos = settings.X * 1 / 10, settings.Y * 8 / 100
        elif class_ == "Adept":
            self.bg_sprites = settings.SpriteSheet(adept_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(adept_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_frames = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.bg_pos = settings.X * 3 / 10, settings.Y * 8 / 100
        elif class_ == "Rogue":
            self.bg_sprites = settings.SpriteSheet(rogue_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(rogue_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_frames = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.bg_pos = settings.X * 5 / 10, settings.Y * 8 / 100
        elif class_ == "Artificer":
            self.bg_sprites = settings.SpriteSheet(artificer_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(artificer_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_frames = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.bg_pos = settings.X * 7 / 10, settings.Y * 8 / 100
        self.sprites = self.bg_sprites
        self.image = self.sprites[0]
        self.animation_index = 0
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, dt):
        self.selected = False
        if self.parent.index.lower() == self.__class__.__name__.lower() and not self.selected:
            self.selected = True
            self.sprites = self.selected_sprites
            self.pos = self.selected_pos
        elif not self.parent.index.lower() == self.__class__.__name__.lower() and self.selected:
            self.selected = False
            self.sprites = self.bg_sprites
            self.pos = self.bg_pos
        self.timer += dt * settings.random_int(90, 110) / 100
        if self.timer > self.speed[self.animation_index]:
            self.timer = 0
            self.animation_index += 1
            self.animation_index %= len(self.frames)
        self.rect = self.image.get_rect(topleft=self.pos)
