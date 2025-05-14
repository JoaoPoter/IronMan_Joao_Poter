import os, time, json, pygame
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
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
    x_near = x_near - 2

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

def move_horizontal(obj_x, obj_y, screen, obj_height, obj_width, move_x, move_y, air_resistance):
    keys = pygame.key.get_pressed()
    move_x = keys[pygame.K_SPACE]
    move_y = keys[pygame.K_s] - keys[pygame.K_w]
    
    if obj_x <= 0 and move_x <= 0:
        move_x = 0
        air_resistance = 0
    elif obj_x >= screen.get_width() - obj_width - 1 and move_x >= 0:
        move_x = 0
    if obj_y <= 0 and move_y <= 0:
        move_y = 0
    if obj_y >= screen.get_height() - obj_height - 1 and move_y >= 0:
        move_y = 0
    obj_x += move_x * 25
    obj_y += move_y * 15
    obj_x -= air_resistance
    return obj_x, obj_y


