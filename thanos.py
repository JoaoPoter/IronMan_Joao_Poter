import pygame
import random
from recursos.funcoes import Rock, carregar_frames
from end_game import end_game

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, rocks):
        super().__init__()
        # Store sprite groups
        self.all_sprites = all_sprites
        self.rocks = rocks
        self.attack_x = x - 208
        # Fix image loading paths
        self.animations = {
            "idle": carregar_frames("assets/frames_handy", flip_horizontal=True),
            "attack": carregar_frames("assets/frames_thanrock", flip_horizontal=False, scale=[500, 400]),
            "damage": carregar_frames("assets/frames_block", flip_horizontal=False, scale=[450,400])
        }
        self.state = "idle"
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_index = 0
        self.animation_timer = 0

        self.max_hp = 7
        self.hp = self.max_hp
        self.attack_cooldown = random.randint(4000, 6000)  # 2 a 4 segundos
        self.last_attack_time = pygame.time.get_ticks()

        self.move_timer = pygame.time.get_ticks()
        self.direction = 1  # 1 = descer, -1 = subir
        self.anim_speed = 6

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.move_timer > 1000:
            self.direction = random.choice([-1, 0, 1])
            self.y = self.rect.y

            if self.direction == -1 and self.rect.y <= 120:
                self.direction = 1
            elif self.direction == 1 and self.rect.y >= 230:
                self.direction = -1
                
            self.move_timer = current_time
        self.rect.y += self.direction * 4
        
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.state = "attack"
            self.attack_cooldown = random.randint(1400, 4000)
            self.last_attack_time = current_time
            self.animation_index = 0

        self.animate()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 6:  # velocidade da animação
            self.animation_index += 1
            self.animation_timer = 0
            frames = self.animations[self.state]
            if self.animation_index >= len(frames):
                self.animation_index = 0
                if self.state == "attack":
                    self.state = "idle"
                    self.shoot()
                if self.state == "damage":
                    self.state = "idle"


            self.image = frames[self.animation_index]

    def shoot(self):
        rock = Rock(self.rect.left, self.rect.centery+20)
        self.all_sprites.add(rock)
        self.rocks.add(rock)
    
    def morrer(self):
        self.kill
        
    def tomar_dano(self):
        self.hp -= 1
        self.state = "damage"

        if self.hp <= 0:
            pygame.mixer_music.stop
            end_game()

