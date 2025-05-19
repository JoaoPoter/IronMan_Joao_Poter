import pygame, random
from main import spr_than, than_x, than_y, screen
class Thanos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spr_than
        self.rect = self.image.get_rect()
        self.rect.x = than_x
        self.rect.y = than_y

    def update(self):
        # Atualiza a posição do Thanos
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.rect.x = screen.get_width()
            self.rect.y = random.randint(0, screen.get_height() - self.rect.height)