import pygame
import settings

from base import BaseState


class MapBounds(BaseState):
    def __init__(self):
        super(MapBounds, self).__init__()
        self.text_color = None
        self.active_index = 0
        self.state = "Map_Input"
        self.image = None
        self.options = ["Start Game", "Quit Game"]
        self.next_state = "MENU"
        self.entry = ''
        self.current_poly = []
        self.shapes = []
        self.start = None
        self.end = None
        self.x = 0
        self.y = 0
        self.last_x = 0
        self.last_y = 0
        self.region_dict = self.get_region_list()
        self.index = list(self.region_dict.keys())[0]

    def handle_action(self, action):
        if self.state == "Map_Input":
            mods = pygame.key.get_mods()
            if action == "Backspace":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                if len(self.entry) > 0:
                    self.entry = self.entry[:-1]
                else:
                    self.state = "Class_Select"
            elif action == "Return":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                for key in settings.REGION_LAYOUTS:
                    if self.entry in settings.REGION_LAYOUTS[key]:
                        self.image = settings.REGION_LAYOUTS[key][self.entry]['Image']
                        self.state = "Map_View"
            elif action in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] \
                    and len(self.entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.entry += action
            elif action == "underscore" and len(self.entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.entry += "_"
            elif action in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                            "s", "t", "u", "v", "w", "x", "y", "z"] and len(self.entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                if mods & pygame.KMOD_SHIFT:
                    self.entry += action.upper()
                else:
                    self.entry += action
            elif action == "space" and len(self.entry) < settings.MAX_NAME_LENGTH:
                settings.SOUND_EFFECTS["Menu"]["Toggle_2"].play()
                self.entry += "_"
            elif action == "F1":
                self.state = "Select_From_List"

        elif self.state == "Select_From_List":
            if action == "Backspace":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                if len(self.entry) > 0:
                    self.entry = self.entry[:-1]
                else:
                    self.state = "Class_Select"
            elif action == "Return":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.image = settings.image_load(self.region_dict[self.index])
                self.state = "Map_View"
            elif action == "Up":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.toggle_index(up=True)
            elif action == "Down":
                settings.SOUND_EFFECTS["Menu"]["Toggle_1"].play()
                self.toggle_index()

        elif self.state == "Map_View":
            if action == "Click":
                pos = pygame.mouse.get_pos()
                self.current_poly.append(pos)
                self.last_x = pos[0]
                self.last_y = pos[1]
                print(self.current_poly)
            elif action == "Return":
                if len(self.current_poly) > 2:
                    self.shapes.append(self.current_poly)
                    self.current_poly = []
                    self.last_x = 0
                    self.last_y = 0
                print(self.shapes)
            elif action == "Home":
                if len(self.current_poly) > 2:
                    self.start = self.current_poly
                    self.current_poly = []
                    self.last_x = 0
                    self.last_y = 0
            elif action == "End":
                if len(self.current_poly) > 2:
                    self.end = self.current_poly
                    self.current_poly = []
                    self.last_x = 0
                    self.last_y = 0
            elif action == "Escape":
                self.state = "Map_Input"
                self.image = None
                self.entry = ''
                self.current_poly.clear()
                self.shapes.clear()
                self.start = None
                self.end = None
            elif action == "Delete":
                self.current_poly.clear()
                self.shapes.clear()
                self.start = None
                self.end = None
            elif action == "Page_Down":
                print(self.shapes)
                print(self.start)
                print(self.end)
            elif action == "Mouse_Move":
                pos = pygame.mouse.get_pos()
                self.x = pos[0]
                self.y = pos[1]

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.handle_action("Left")
            elif event.key == pygame.K_RIGHT:
                self.handle_action("Right")
            if event.key == pygame.K_UP:
                self.handle_action("Up")
            elif event.key == pygame.K_DOWN:
                self.handle_action("Down")
            elif event.key == pygame.K_RETURN:
                self.handle_action("Return")
            elif event.key == pygame.K_BACKSPACE:
                self.handle_action("Backspace")
            elif event.key == pygame.K_ESCAPE:
                self.handle_action("Escape")
            elif event.key == pygame.K_DELETE:
                self.handle_action("Delete")
            elif event.key == pygame.K_HOME:
                self.handle_action("Home")
            elif event.key == pygame.K_END:
                self.handle_action("End")
            elif event.key == pygame.K_PAGEDOWN:
                self.handle_action("Page_Down")
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
                self.handle_action(" ")
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
            elif event.key == pygame.K_MINUS:
                self.handle_action("underscore")
            elif event.key == pygame.K_F1:
                self.handle_action("F1")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("Click")

        elif event.type == pygame.MOUSEMOTION:
            self.handle_action("Mouse_Move")

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        if self.state == "Map_Input":
            settings.tw(surface, self.entry, self.text_color, (300, 200, 600, 500), settings.HEADING_FONT)
        elif self.state == "Select_From_List":
            settings.tw(surface, self.index, settings.SELECTED_COLOR, [0, 0, settings.X, settings.Y],
                        settings.HEADING_FONT, x_mode="center", y_mode="center")
        if self.state == "Map_View":
            if self.image:
                surface.blit(self.image, (0, 0))
            pygame.draw.line(surface, (0, 0, 0), (self.last_x, self.last_y), (self.x, self.y), 10)

    def update(self, dt):
        self.text_color = settings.TEXT_COLOR
        for biome in settings.REGION_LAYOUTS:
            if self.entry in settings.REGION_LAYOUTS[biome]:
                self.text_color = settings.SELECTED_COLOR

    def toggle_index(self, up=False):
        index = list(self.region_dict).index(self.index)
        if up:
            index -= 1
        else:
            index += 1
        index %= len(list(self.region_dict))
        self.index = list(self.region_dict)[index]

    @staticmethod
    def get_region_list() -> dict:
        data = settings.JsonReader.read_json("venv/settings_data/Region_Maps.json")
        image_dict = {}
        for region_type, map_list in data.items():
            for region, settings_ in map_list.items():
                image_dict[region] = settings_["Image"]
        return image_dict
