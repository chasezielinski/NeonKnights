import pygame
import settings

from base import BaseState


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.title = self.font.render("Battle Tester", True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "MENU"
        self.time_active = 0
        self.fade_timer = 1200
        self.done = False
        self.persist["Transition"] = settings.ScreenTransition()
        self.persist["Transition"].set_black()
        self.persist["Transition"].fade_in(500)

    def update(self, dt):
        self.persist["Transition"].update(dt)
        self.time_active += dt
        if self.fade_timer is not None:
            self.fade_timer -= dt
            if self.fade_timer <= 0:
                self.fade_timer = None
                self.persist["Transition"].fade_out(500)
        if self.time_active >= 2000:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        self.persist["Transition"].draw(surface)
