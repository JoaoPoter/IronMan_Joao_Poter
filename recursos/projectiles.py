from recursos.funcoes import carregar_frames
import pygame

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = {
            "fly": carregar_frames("assets/frames_rock", flip_horizontal=True, scale=[130, 120]),
            "explode": carregar_frames("assets/frames_explode", flip_horizontal=False, scale=[130, 120]),
        }
        self.state = "fly" 
        self.image = self.frames[self.state][0]
        self.speed = -15
        self.rect = self.image.get_rect(center=(x, y))

        self.animation_index = 0
        self.animation_timer = 0
        self.exploding = False

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()
        self.animate()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 3:
            self.animation_timer = 0
            self.animation_index += 1
            frames = self.frames[self.state]
            if self.animation_index >= len(frames):
                self.animation_index = 0
                if self.state == "explode" and self.animation_index == 0:
                    self.kill()
            self.image = frames[self.animation_index]

                    
    def explodir(self):
        self.exploding = True
        self.state = "explode"
        self.animation_index = 0
        self.animation_timer = 0
    
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = {
            "rocket": carregar_frames("assets/frames_rocket", flip_horizontal=False, scale=[100, 30]),
            "explode": carregar_frames("assets/frames_explosion", flip_horizontal=False, scale=[150, 130]),
        }
        self.state = "rocket" 
        self.image = self.frames[self.state][0]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 30

        self.animation_index = 0
        self.animation_timer = 0
        self.exploding = False

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > 1200:
            self.kill()
        self.animate()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 3:
            self.animation_timer = 0
            self.animation_index += 1
            frames = self.frames[self.state]
            if self.animation_index >= len(frames):
                self.animation_index = 0
                if self.state == "explode" and self.animation_index == 0:
                    self.speed = 10
                    self.kill()
            self.image = frames[self.animation_index]

                    
    def explodir(self):
        self.exploding = True
        self.state = "explode"
        self.animation_index = 0
        self.animation_timer = 0