import pygame

class SpriteAnimator:
    def __init__(self, x, y, sprites, tempo_frame=150): 
        self.x = x
        self.y = y
        self.sprites = sprites
        self.tempo_frame = tempo_frame  # em milissegundos
        self.frame_atual = 0
        self.ultimo_update = pygame.time.get_ticks()

    def atualizar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.tempo_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.sprites)
            self.ultimo_update = agora

    def desenhar(self, screen):
        screen.blit(self.sprites[self.frame_atual], (self.x, self.y))