import pygame
import settings

from base import BaseState


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.title = "Studio Splash"
        self.next_state = "MENU"
        self.time_active = 800
        self.fade_timer = 1200
        self.done = False
        self.persist["Transition"] = settings.ScreenTransition()
        self.persist["Transition"].set_black()
        self.persist["Transition"].fade_in(500)
        self.persist['SFX'] = settings.SFXManager()
        self.persist['FX'] = settings.FXManager()
        self.persist['Music'] = settings.MusicManager()

    def update(self, dt):
        self.persist["Transition"].update(dt)
        if self.fade_timer is not None:
            self.fade_timer -= dt
            if self.fade_timer <= 0:
                self.splash_done()
        if self.time_active is not None:
            self.time_active -= dt
            if self.time_active <= 0:
                self.done = True
        self.persist['SFX'].update(dt)
        self.persist['FX'].update(dt)
        self.persist['Music'].update(dt)

    def splash_done(self):
        self.fade_timer = None
        self.persist["Transition"].fade_out(500)
        self.time_active = 600

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        settings.tw(surface, self.title, settings.TEXT_COLOR, [0, 0, settings.X, settings.Y], settings.HEADING_FONT,
                    x_mode="center", y_mode="center")
        self.persist["Transition"].draw(surface)
        self.persist['FX'].draw(surface)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.handle_action("return")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_action("click")

    def handle_action(self, action):
        if action == "return" or action == "click":
            if self.fade_timer:
                self.splash_done()
