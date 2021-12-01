import pygame
import settings
from base import BaseState
from settings import PartyAbilityManager, PlayerCharacter, X, Y

fighter_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
              r"Select\Fighter_Select128p.png "
fighter_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
              r"Select\Fighter_Select256p.png "
adept_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Adept_Select128p.png "
adept_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Adept_Select256p.png "
rogue_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Rogue_Select128p.png "
rogue_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
            r"Select\Rogue_Select256p.png "
artificer_128 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
                r"Select\Artificer_Select128p.png "
artificer_256 = r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character " \
                r"Select\Artificer_Select256p.png "


class CharacterSelect(BaseState):
    def __init__(self):
        super(CharacterSelect, self).__init__()
        self.max_name_length = 13
        self.next_state = "MENU"
        self.state = "Wait"
        self.timer = 2000
        self.index = "Fighter"
        self.name_entry_index = -1
        self.name_entry_options = ["random", "select", "back"]
        self.confirm_options = ["confirm", "back"]
        self.name_entry = ""
        self.class_rects = {
            "Fighter": [X * 15 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
            "Adept": [X * 35 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
            "Rogue": [X * 55 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
            "Artificer": [X * 75 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],}
        self.class_bg_rects = {
            "Fighter": [X * 12 / 100, Y * 76 / 100, X * 16 / 100, Y * 10 / 100],
            "Adept": [X * 32 / 100, Y * 76 / 100, X * 16 / 100, Y * 10 / 100],
            "Rogue": [X * 52 / 100, Y * 76 / 100, X * 16 / 100, Y * 10 / 100],
            "Artificer": [X * 72 / 100, Y * 76 / 100, X * 16 / 100, Y * 10 / 100],}
        self.class_sprites = pygame.sprite.Group()
        self.class_sprites.add(CharacterSelectSprite(self, "Fighter"), CharacterSelectSprite(self, "Adept"),
                               CharacterSelectSprite(self, "Rogue"), CharacterSelectSprite(self, "Artificer"), )
        self.name_rect = [0, Y * 70 / 100, X, Y * 8 / 100]
        self.class_rect = [X * 20 / 100, Y * 5 / 100, X * 80 / 100, Y * 5 / 100]
        self.prompt_rect = [X * 1 / 8, Y * 13 / 16, X * 3 / 4, Y * 1 / 8]
        self.option_rect = {0: [X * 75 / 100, Y * 30 / 100, X * 25 / 100, Y * 10 / 100],
                            1: [X * 75 / 100, Y * 40 / 100, X * 25 / 100, Y * 10 / 100],
                            2: [X * 75 / 100, Y * 50 / 100, X * 25 / 100, Y * 10 / 100]}
        self.particles = BGParticles()

    def menu_toggle(self, action):
        index = list(self.class_rects.keys()).index(self.index)
        settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
        if action == "Right":
            index += 1
        else:
            index -= 1
        index %= len(self.class_rects)
        self.index = list(self.class_rects.keys())[index]
        
    def menu_select(self):
        if self.state == "Class_Select":
            settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
            self.state = "Name_Entry"
        elif self.state == "Name_Entry":
            if self.name_entry_index == 0:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.name_entry = settings.random_name()
            elif self.name_entry_index == 1 and len(self.name_entry) > 0:
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.state = "Confirm"
            elif self.name_entry_index == 2:
                self.menu_return()
        elif self.state == "Confirm":
            if self.name_entry_index == 0:
                settings.SOUND_EFFECTS["Menu"]["Confirm_1"].play()
                self.start()
            elif self.name_entry_index == 1 and len(self.name_entry) > 0:
                self.menu_return()

    def menu_return(self):
        settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
        if self.state == "Class_Select":
            self.done = True
            self.next_state = "MENU"
        elif self.state == "Name_Entry":
            self.state = "Class_Select"
        elif self.state == "Confirm":
            self.state = "Name_Entry"

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
            elif action == "click" or action == "Return":
                self.menu_select()
            elif action == "Left" or action == "Right":
                self.menu_toggle(action)

        elif self.state == "Name_Entry":
            if action == "mouse_move":
                self.name_entry_index = -1
                for key, value in self.option_rect.items():
                    if settings.click_check(value):
                        self.name_entry_index = key
            elif action == "click":
                self.menu_select()
            elif action == "Backspace":
                if len(self.name_entry) > 0:
                    settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                    self.name_entry = self.name_entry[:-1]
                else:
                    self.menu_return()
            elif action == "Return":
                self.menu_select()
            elif action == "space":
                self.text_input(" ")
            elif action == "Up":
                self.name_entry_index -= 1
                self.name_entry_index %= len(self.name_entry_options)
            elif action == "Down":
                self.name_entry_index += 1
                self.name_entry_index %= len(self.name_entry_options)

        elif self.state == "Confirm":
            if action == "mouse_move":
                self.name_entry_index = -1
                for key, value in self.option_rect.items():
                    if settings.click_check(value):
                        self.name_entry_index = key
            elif action == "click":
                self.menu_select()
            if action == "Return":
                self.menu_select()
            elif action == "Backspace":
                self.menu_return()
            elif action == "Up":
                self.name_entry_index -= 1
                self.name_entry_index %= len(self.confirm_options)
            elif action == "Down":
                self.name_entry_index += 1
                self.name_entry_index %= len(self.confirm_options)

    def update(self, dt):
        if self.state == "Wait":
            self.timer -= dt
            if self.timer < 0:
                self.state = "Class_Select"
        self.class_sprites.update(dt)
        self.persist["Transition"].update(dt)
        self.persist["Transition"].update(dt)
        self.persist['SFX'].update(dt)
        self.persist['FX'].update(dt)
        self.persist['Music'].update(dt)
        self.particles.update(dt)

    def start(self):
        self.persist['region_generate'] = True
        self.persist['region_index'] = 0
        self.persist['characters'] = []
        self.persist['characters'].append(eval(f"settings.{self.index}")(name=self.name_entry))
        self.persist['supplies'] = 10
        self.persist['chargers'] = 5
        self.persist['elixirs'] = 5
        self.persist['gold'] = 1000
        self.persist['region_type'] = "None"
        self.persist['inventory'] = [settings.StimPack(), settings.StimPack(), settings.StimPack(),
                                     settings.StimPack(), settings.StimPack()]
        settings.character_initial(self.persist['characters'][0], self.index)
        self.persist['equip menu indices'] = settings.REGION_MENUS['equip menu']['equip menu indices']
        self.persist['party_abilities'] = PartyAbilityManager()
        self.next_state = "REGION_SELECT"
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
            elif event.key == pygame.K_LEFT:
                self.handle_action("Left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("Right")
            elif event.key == pygame.K_UP:
                self.handle_action("Up")
            elif event.key == pygame.K_DOWN:
                self.handle_action("Down")
            elif event.key == pygame.K_RETURN:
                self.handle_action("Return")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("Backspace")
            elif event.key == pygame.K_SPACE:
                self.handle_action("space")

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.particles.draw_bg(surface)
        self.class_sprites.draw(surface)

        if self.state == "Class_Select":
            for background in list(self.class_bg_rects.keys()):
                color = (50, 50, 50)
                text_color = settings.TEXT_COLOR
                if background == self.index:
                    color = (100, 100, 100)
                    text_color = settings.SELECTED_COLOR
                pygame.draw.rect(surface, color, self.class_bg_rects[background], border_radius=8)
                pygame.draw.rect(surface, (20, 20, 20), self.class_bg_rects[background], 5, 8)
                settings.tw(surface, background, text_color, self.class_bg_rects[background],
                            settings.TEXT_FONT, x_mode="center", y_mode="center")

        elif self.state == "Name_Entry":
            prompt = "Input a name. Press enter to continue or backspace to select another class."
            self.print_options(surface, self.name_entry_options, prompt)

        elif self.state == "Confirm":
            prompt = "Press enter to embark. Press backspace to reconsider."
            self.print_options(surface, self.confirm_options, prompt)

        self.particles.draw_fg(surface)
        self.persist["Transition"].draw(surface)
        self.persist['FX'].draw(surface)

    def print_options(self, surface, options, prompt):
        settings.tw(surface, self.name_entry, settings.TEXT_COLOR, self.name_rect,
                    settings.HEADING_FONT, x_mode="center", y_mode="center")
        settings.tw(surface, self.index.rjust(20-len(self.index)), settings.TEXT_COLOR, self.class_rect,
                    settings.HEADING_FONT)
        settings.tw(surface, prompt, settings.TEXT_COLOR, self.prompt_rect, settings.HEADING_FONT)
        for i, option in enumerate(options):
            color = settings.TEXT_COLOR
            if i == self.name_entry_index:
                color = settings.SELECTED_COLOR
            settings.tw(surface, option, color, self.option_rect[i], settings.HEADING_FONT)

    def startup(self, persistent):
        self.persist = persistent
        self.persist["Transition"].fade_in(500, 2000)


class CharacterSelectSprite(pygame.sprite.Sprite):
    def __init__(self, parent, class_: str):
        super(CharacterSelectSprite, self).__init__()
        self.parent = parent
        self.selected = False
        self.timer = 0
        self.selected_pos = X * 4 / 10, Y * 2 / 8
        self.class_ = class_
        if class_ == "Fighter":
            self.bg_sprites = settings.SpriteSheet(fighter_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(fighter_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_speed = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.pos = self.bg_pos = X * 1 / 10, Y * 8 / 100
        elif class_ == "Adept":
            self.bg_sprites = settings.SpriteSheet(adept_128).load_strip([0, 0, 128, 128], 16, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(adept_256).load_strip([0, 0, 256, 256], 16, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            self.speed = self.idle_speed = [100 for i in range(23)]
            self.flourish_frames = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 11, 12, 13, 14, 15]
            self.flourish_speed = [100 for i in range(19)]
            self.pos = self.bg_pos = X * 3 / 10, Y * 8 / 100
        elif class_ == "Rogue":
            self.bg_sprites = settings.SpriteSheet(rogue_128).load_strip([0, 0, 128, 128], 12, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(rogue_256).load_strip([0, 0, 256, 256], 12, (255, 55, 202))
            self.frames = self.idle_frames = [0, 1]
            self.speed = self.idle_speed = [1650, 350]
            self.flourish_frames = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.flourish_speed = [1000, 100, 100, 100, 100, 100, 100, 100, 100, 500]
            self.pos = self.bg_pos = X * 5 / 10, Y * 8 / 100
        elif class_ == "Artificer":
            self.bg_sprites = settings.SpriteSheet(artificer_128).load_strip([0, 0, 128, 128], 30, (255, 55, 202))
            self.selected_sprites = settings.SpriteSheet(artificer_256).load_strip([0, 0, 256, 256], 30, (255, 55, 202))
            self.frames = self.idle_frames = list(range(22))
            self.speed = self.idle_speed = [1500, 100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100, 50, 50, 200,
                                            50, 30, 30, 30, 100]
            self.flourish_frames = [21, 22, 23, 24, 25, 26, 27, 28, 29]
            self.flourish_speed = [1500, 100, 50, 50, 50, 50, 50, 50, 50]
            self.pos = self.bg_pos = X * 7 / 10, Y * 8 / 100
        self.sprites = self.bg_sprites
        self.image = self.sprites[0]
        self.animation_index = 0
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, dt):
        if self.parent.index.lower() == self.class_.lower() and not self.selected:
            self.selected = True
            self.sprites = self.selected_sprites
            self.pos = self.selected_pos
        elif not self.parent.index.lower() == self.class_.lower() and self.selected:
            self.selected = False
            self.sprites = self.bg_sprites
            self.pos = self.bg_pos
        self.timer += dt * settings.random_int(90, 110) / 100
        if self.timer > self.speed[self.animation_index]:
            self.timer = 0
            self.animation_index += 1
            self.animation_index %= len(self.frames)
        self.image = self.sprites[self.frames[self.animation_index]]
        self.rect = self.image.get_rect(topleft=self.pos)


class BGParticles(object):
    def __init__(self):
        super(BGParticles, self).__init__()
        self.bg_particles = []
        self.fg_particles = []
        self.timer = 200

    def draw_bg(self, surface):
        for particle in self.bg_particles:
            particle.draw(surface)

    def draw_fg(self, surface):
        for particle in self.fg_particles:
            particle.draw(surface)

    def update(self, dt):
        self.timer -= dt * settings.random_int(50, 150)/100
        if self.timer < 0:
            self.timer = 20
            if settings.random_int(0, 100) > 98:
                self.fg_particles.append(Particle(background=False))
            else:
                self.bg_particles.append(Particle())
        if self.bg_particles:
            for particle in self.bg_particles:
                particle.update(dt)
                if particle.done:
                    del particle
        if self.fg_particles:
            for particle in self.fg_particles:
                particle.update(dt)
                if particle.done:
                    del particle


class Particle(object):
    def __init__(self, background=True):
        super(Particle, self).__init__()
        self.pos = [settings.random_int(0, X), Y*1.1]
        self.done = False
        if background:
            self.radius = settings.choose_random_weighted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [100, 30, 12, 9, 7, 6, 5, 4, 3, 2])
        else:
            self.radius = settings.random_int(11, 15)
        self.velocity = settings.random_int(90, 110)/100 * self.radius/5
        self.rainbow = False
        if settings.random_int(0, 100) > 99:
            self.rainbow = True
        self.color = settings.random_int(200, 255),settings.random_int(200, 255), settings.random_int(200, 255)
        self.a = settings.random_int(150, 300)/100
        self.rect = [self.pos[0], self.pos[1], 2*self.radius, 2*self.radius*self.a]

    def update(self, dt):
        self.pos[1] -= dt * self.velocity
        if self.pos[1] < 0:
            self.done = True
        if self.rainbow:
            self.color = (self.color[0] + 2*dt) % 255, (self.color[0] + 5*dt) % 255, (self.color[0] + 7*dt) % 255
        self.rect = [self.pos[0], self.pos[1], 2*self.radius, 2*self.radius*self.a]

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)
