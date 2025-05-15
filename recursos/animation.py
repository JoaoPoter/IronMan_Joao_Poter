# sprite_animator.py
import pygame

class SpriteAnimator:
    def __init__(self, images: list, pos: tuple, size: tuple, animation_speed: int, flip: bool = False):
        self.images = [pygame.transform.scale(img, size) for img in images]
        self.x, self.y = pos
        self.size = size
        self.animation_speed = animation_speed
        self.index = 0
        self.clock = pygame.time.Clock()
        self.moving = False
        self.flip = flip
        if self.flip:
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]

    def update(self, window):
        self.clock.tick(self.animation_speed)
        
        self.index += 1
        if self.index >= len(self.images):
           self.index = 0

        window.blit(self.images[self.index], (self.x, self.y))
