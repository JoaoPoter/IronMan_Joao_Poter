import pygame
import random
from recursos.funcoes import Rock

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, rocks):
        super().__init__()
        # Store sprite groups
        self.all_sprites = all_sprites
        self.rocks = rocks
        
        # Fix image loading paths
        self.animations = {
            "idle": [pygame.image.load(f"assets/frames_handy/frame_00{i}.png").convert_alpha() for i in range(4)],
            "attack": [pygame.image.load(f"assets/frames_thanrock/frame_00{i}.png").convert_alpha() for i in range(6)],
        }
        self.state = "idle"
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_index = 0
        self.animation_timer = 0

        self.attack_cooldown = random.randint(2000, 4000)  # 2 a 4 segundos
        self.last_attack_time = pygame.time.get_ticks()

        self.move_timer = pygame.time.get_ticks()
        self.direction = 1  # 1 = descer, -1 = subir

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.move_timer > 1000:
            self.direction = random.choice([-1, 0, 1])
            self.y = self.rect.y
            if self.direction == 0:
                self.direction = 1
            elif self.direction == -1 and self.rect.y <= 0:
                self.direction = 1
            elif self.direction == 1 and self.rect.y >= 400:
                self.direction = -1
            self.move_timer = current_time
        self.rect.y += self.direction * 2
        
        print(f"current_time: {current_time}, move_timer: {self.move_timer}, direction: {self.direction}")
        if current_time - self.last_attack_time > self.attack_cooldown:
            print("Atacando!")
            self.state = "attack"
            self.attack_cooldown = random.randint(2000, 4000)
            self.last_attack_time = current_time
            self.animation_index = 0

        self.animate()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 6:  # velocidade da animação
            self.animation_index += 1
            self.animation_timer = 0
            print(f"Índice da animação: {self.animation_index}")
            frames = self.animations[self.state]
            if self.animation_index >= len(frames):
                self.animation_index = 0
                if self.state == "attack":
                    print("Atacando!")
                    self.state = "idle"
                    self.shoot()

            self.image = frames[self.animation_index]

    def shoot(self):
        rock = Rock(self.rect.left, self.rect.centery)
        self.all_sprites.add(rock)
        self.rocks.add(rock)

