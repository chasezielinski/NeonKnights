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
        self.done = False
        self.persist["Transition"] = settings.ScreenTransition((settings.X, settings.Y))

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 500:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
