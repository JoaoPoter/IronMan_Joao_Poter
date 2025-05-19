import pygame, random, time
from recursos.funcoes import inicializarBancoDeDados, colisao_retangulos, backGround, move_horizontal, fade_text, carregar_frames
from recursos.animation import SpriteAnimator
from recursos.gif import extract_frames
import sys

pygame.init()
inicializarBancoDeDados()
aspect_ratio = (1200, 740)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(aspect_ratio)

pygame.display.set_caption("Iron Man do J_Poter")
icon  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icon)

spr_start_b = pygame.image.load("assets/start_b.png")
spr_start_b = pygame.transform.scale(spr_start_b, (300, 50))
spr_quit_b = pygame.image.load("assets/quit_b.png")
spr_quit_b = pygame.transform.scale(spr_quit_b, (300, 50))

spr_iron_soaring = pygame.image.load("assets/iron_soaring.png")
spr_iron_boosting = pygame.image.load("assets/iron_boosting.png")
spr_iron_bg = pygame.image.load("assets/iron_start.jpg")
spr_far = pygame.image.load("assets/back.png")
spr_middle = pygame.image.load("assets/mid.png")
spr_near = pygame.image.load("assets/front.png")
spr_dead = pygame.image.load("assets/fundoDead.png")
spr_than = pygame.image.load("assets/than.gif")
snd_explosion = pygame.mixer.Sound("assets/explosao.wav")
font_title = pygame.font.Font("assets/Ethnocentric Rg.otf", 50)
font_menu = pygame.font.Font("assets/Ethnocentric Rg.otf",18)
font_dead = pygame.font.SysFont("arial",120)
font_debug = pygame.font.SysFont(None, 16)
pygame.mixer.music.load("assets/ironsound.mp3")

than_aspect = [spr_than.get_width(), spr_than.get_height()]
spr_than = pygame.transform.scale(spr_than, (than_aspect[0]*2, than_aspect[1]*2))
spr_than = pygame.transform.flip(spr_than, True, False)

spr_far = pygame.transform.scale(spr_far, (aspect_ratio[0], aspect_ratio[1]))
spr_middle = pygame.transform.scale(spr_middle, (aspect_ratio[0], aspect_ratio[1]))
spr_near = pygame.transform.scale(spr_near, (aspect_ratio[0], aspect_ratio[1]))
spr_iron_bg = pygame.transform.scale(spr_iron_bg, (aspect_ratio[0], aspect_ratio[1]))
spr_dead = pygame.transform.scale(spr_dead, (aspect_ratio[0], aspect_ratio[1]))

white = (255,255,255)
black = (0, 0 ,0 )
cinza = (100, 100, 100)

than_x = 650
than_y = 150

b_n = 0
start = 0

extract_frames("assets/than_rock.gif", "assets/frames_thanrock")
extract_frames("assets/than_handy.gif", "assets/frames_handy")

sprites = carregar_frames("assets/frames_handy")

sprites = carregar_frames("assets/frames_handy")

than_handy = SpriteAnimator(than_x, than_y, sprites, tempo_frame=150)

def menu(start, b_n, pause):
    dark_overlay = pygame.Surface(screen.get_size())
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(100)  # Valor entre 0 (transparente) e 255 (opaco)
    b_width = 250
    b_height = 50
    txt_pos = [300, 230]
    buttons = [None] * b_n
    if pause == False:
        return True
    pause = pause
    for i in range(b_n):
        buttons[i] = f"b_{i}"
    if start:
        screen.fill(white)
        screen.blit(spr_iron_bg, (0, 0))
        fade_text("Iron Man", font_title, cinza, (303, 53), screen, fade_in=True, duracao=300)
        fade_text("Iron Man", font_title, white, (300, 50), screen, fade_in=True, duracao=600)
    else:
        screen.blit(dark_overlay, (0, 0))
        fade_text("Pause", font_title, cinza, (303, 53), screen, fade_in=True, duracao=300)
        fade_text("Pause", font_title, white, (300, 50), screen, fade_in=True, duracao=600)
    
    for i in range(b_n):
        if buttons[i] == "b_0":
            b1 = pygame.draw.rect(screen, white, (txt_pos[0],txt_pos[1], b_width, b_height), border_radius=15)
            screen.blit(spr_start_b, (txt_pos[0]-50,txt_pos[1]))
            start_txt = font_menu.render("Iniciar Game", True, black)
            screen.blit(start_txt, (txt_pos[0],txt_pos[1]+10))
        elif buttons[i] == "b_1":
            b2 = pygame.draw.rect(screen, white, (txt_pos[0],txt_pos[1]+70, b_width, b_height), border_radius=15)
            screen.blit(spr_quit_b, (txt_pos[0]-50,txt_pos[1]+70))
            quit_txt = font_menu.render("Sair do Game", True, black)
            screen.blit(quit_txt, (txt_pos[0],txt_pos[1]+80))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(evento.pos):
                    dark_overlay = pygame.Surface(screen.get_size())
                    dark_overlay.fill((0, 0, 0))
                    dark_overlay.set_alpha(100)  # Valor entre 0 (transparente) e 255 (opaco)
                if b2.collidepoint(evento.pos):
                    dark_overlay = pygame.Surface(screen.get_size())
                    dark_overlay.fill((0, 0, 0))
                    dark_overlay.set_alpha(100)  # Valor entre 0 (transparente) e 255 (opaco)

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if b1.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    b_width = 150
                    b_height = 40
                    if start:
                        start = 0
                        game()
                    else:
                        pause = False
                        pygame.mixer_music.set_volume(1)
                        return True
                if b2.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    b_width = 150
                    b_height  = 40
                    quit()
            elif evento.type == pygame.KEYDOWN:
                    if not start:
                        if evento.key == pygame.K_ESCAPE:
                            pause = False
                            return True
        
        pygame.display.update()
        clock.tick(50)

def game():
    x_far = 0
    x_middle = 0
    x_near = 0
    air_resistance = 10
    debug_mode = False
    char_x = 100
    char_y = 300
    move_x  = 0
    move_y  = 0
    spr_iron = spr_iron_soaring
    pygame.mixer.music.play(-1)
    char_width = spr_iron_soaring.get_width()
    char_height = spr_iron_soaring.get_height()
    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_F3:
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
                    print("Debug Mode Ativado")
                    if evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_F3:
                            debug_mode = False[
                            pygame.mixer.music.play(-1)]
                            break
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer_music.set_volume(0.5)
                menu(start=0, b_n=2, pause = True)
        
        char_x, char_y, spr_iron = move_horizontal(char_x, char_y, screen, char_height, char_width, move_x, move_y, air_resistance, spr_iron, spr_iron_boosting, spr_iron_soaring)

        x_far, x_middle, x_near = backGround(x_far, x_middle, x_near, screen, spr_far, spr_middle, spr_near, white)

        than_handy.atualizar()
        than_handy.desenhar(screen)
            
        screen.blit(spr_iron, (char_x, char_y) )

        if debug_mode:
            debug_lines = [
                f"FPS: {clock.get_fps()}",
                f"Posição do Personagem: ({char_x}, {char_y})",
                f"Movimento do Personagem: ({move_x}, {move_y})",
                #f"Colisão: {colisao_retangulos(char_x, char_y, char_width, char_height, rocket_x, rocket_y, rocket_width, rocket_height)}",
                f"posição thanos: ({than_handy.x}, {than_handy.y})"
            ]
            for i, line in enumerate(debug_lines):
                text = font_debug.render(line, True, (black))
                screen.blit(text, (10, 10 + i * 20))

        pygame.display.update()
        clock.tick(50)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(snd_explosion)

    # Adiciona o log das partidas no Listbox
    '''log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()'''

    screen.fill(white)
    screen.blit(spr_dead, (0,0) )

    menu(start=0, b_n=2)

menu(start=1, b_n=2, pause = True)