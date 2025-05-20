import os, time, json, pygame
from datetime import datetime

def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    print("dados",type(dados))
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
def colisao_retangulos(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

def backGround(x_far, x_middle, x_near, screen, spr_far, spr_middle, spr_near, white):

    screen.fill(white)
    screen.blit(spr_far, (0,0) )

    x_far = x_far - 0.2
    x_middle = x_middle - 0.7
    x_near = x_near - 3

    if x_far <= -800: x_far = 0
    if x_middle <= -800: x_middle = 0
    if x_near <= -800: x_near = 0

    screen.blit(spr_far, (x_far, 0))
    screen.blit(spr_far, (x_far + 800, 0))

    screen.blit(spr_middle, (x_middle, 0))
    screen.blit(spr_middle, (x_middle + 800, 0))

    screen.blit(spr_near, (x_near, 0))
    screen.blit(spr_near, (x_near + 800, 0))
    
    return x_far, x_middle, x_near

def move_horizontal(obj_x, obj_y, screen, obj_height, obj_width, move_x, move_y, air_resistance, obj_spr, obj_moving, obj_not_moving):
    keys = pygame.key.get_pressed()
    move_x = keys[pygame.K_SPACE]
    move_y = keys[pygame.K_s] - keys[pygame.K_w]
    
    if obj_x <= 0 and move_x <= 0:
        move_x = 0
        air_resistance = 0
    elif obj_x >= screen.get_width() - obj_width -1 and move_x >= 0:
        move_x = 0
    if obj_y <= 0 and move_y <= 0:
        move_y = 0
    elif obj_y >= screen.get_height() - obj_height - 1 and move_y >= 0:
        move_y = 0
    
    if move_x != 0 or move_y != 0:
        if move_x > 0:
            obj_spr = obj_moving
        elif move_x < 0:
            obj_spr = obj_not_moving
    else:
        obj_spr = obj_not_moving
        
    obj_x += move_x * 30
    obj_y += move_y * 15
    obj_x -= air_resistance
    return obj_x, obj_y, obj_spr

def fade_text(texto, fonte, cor, pos, screen, fade_in=True, duracao=1000):
    texto_surface = fonte.render(texto, True, cor)
    alpha_surface = pygame.Surface(texto_surface.get_size(), pygame.SRCALPHA)

    tempo_inicial = pygame.time.get_ticks()
    tempo_atual = 0
    clock = pygame.time.Clock()
    
    while tempo_atual < duracao:
        tempo_atual = pygame.time.get_ticks() - tempo_inicial
        progresso = tempo_atual / duracao
        alpha = int(progresso * 255) if fade_in else int((1 - progresso) * 255)
        alpha = max(0, min(255, alpha))

        alpha_surface.fill((255, 255, 255, 0))  # limpa
        alpha_surface.blit(texto_surface, (0, 0))
        alpha_surface.set_alpha(alpha)

        screen.blit(alpha_surface, pos)
        pygame.display.update()
        clock.tick(60)

def carregar_frames(pasta, flip_horizontal=False):
    frames = []
    arquivos = sorted(os.listdir(pasta))
    for arquivo in arquivos:
        if arquivo.endswith(".png"):
            caminho = os.path.join(pasta, arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            if flip_horizontal:
                imagem = pygame.transform.flip(imagem, True, False)
            frames.append(imagem)
    return frames

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/frames_rock/frame_001.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7  # Direita para esquerda

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()
