import pygame, random, json, tkinter as tk
from recursos.funcoes import inicializarBancoDeDados, colisao_retangulos, backGround, move_horizontal

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

spr_iron = pygame.image.load("assets/iron_soaring.png")
spr_iron_bg = pygame.image.load("assets/iron_start.jpg")
spr_far = pygame.image.load("assets/back.png")
spr_middle = pygame.image.load("assets/mid.png")
spr_near = pygame.image.load("assets/front.png")
spr_dead = pygame.image.load("assets/fundoDead.png")
spr_rocket = pygame.image.load("assets/missile.png")
snd_rocket = pygame.mixer.Sound("assets/missile.wav")
snd_explosion = pygame.mixer.Sound("assets/explosao.wav")
font_title = pygame.font.Font("assets/Ethnocentric Rg.otf", 50)
font_menu = pygame.font.Font("assets/Ethnocentric Rg.otf",18)
font_dead = pygame.font.SysFont("arial",120)
font_debug = pygame.font.SysFont(None, 16)
pygame.mixer.music.load("assets/ironsound.mp3")

spr_far = pygame.transform.scale(spr_far, (aspect_ratio[0], aspect_ratio[1]))
spr_middle = pygame.transform.scale(spr_middle, (aspect_ratio[0], aspect_ratio[1]))
spr_near = pygame.transform.scale(spr_near, (aspect_ratio[0], aspect_ratio[1]))
spr_iron_bg = pygame.transform.scale(spr_iron_bg, (aspect_ratio[0], aspect_ratio[1]))
spr_dead = pygame.transform.scale(spr_dead, (aspect_ratio[0], aspect_ratio[1]))

white = (255,255,255)
black = (0, 0 ,0 )
cinza = (100, 100, 100)

b_n = 0
start = 0
dark_overlay = pygame.Surface(screen.get_size())
dark_overlay.fill((0, 0, 0))
dark_overlay.set_alpha(100)  # Valor entre 0 (transparente) e 255 (opaco)

def menu(start,b_n):
    b_width = 300
    b_height = 50
    txt_pos = [300, 230]
    buttons = [None] * b_n
    for i in range(b_n):
        buttons[i] = f"b_{i}"
    if start:
        screen.fill(white)
        screen.blit(spr_iron_bg, (0,0))
        title = font_title.render("Iron Man", True, cinza)
        screen.blit(title, (303,53))
        title = font_title.render("Iron Man", True, white)
        screen.blit(title, (300,50))
    else:
        screen.blit(dark_overlay,(0, 0))
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
                    start = 0
                    game()
                if b2.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    b_width = 150
                    b_height  = 40
                    quit()
        
        for i in range(b_n):
            if buttons[i] == "b_0":
                b1 = pygame.draw.rect(screen, white, (txt_pos[0],txt_pos[1], b_width, b_height), border_radius=15)
                screen.blit(spr_start_b, (txt_pos[0]-50,txt_pos[1]))
                start_txt = font_menu.render("Iniciar Game", True, black)
                screen.blit(start_txt, (txt_pos[0],txt_pos[1]))
            elif buttons[i] == "b_1":
                b2 = pygame.draw.rect(screen, white, (txt_pos[0],txt_pos[1]+50, b_width, b_height), border_radius=15)
                quit_txt = font_menu.render("Sair do Game", True, black)
                screen.blit(quit_txt, (txt_pos[0],txt_pos[1]+50))

        pygame.display.update()
        clock.tick(50)

def game():
    x_far = 0
    x_middle = 0
    x_near = 0
    air_resistance = 10
    debug_mode = False
    pause = False
    char_x = 400
    char_y = 300
    move_x  = 0
    move_y  = 0
    rocket_x = 400
    rocket_y = -240
    move_rocket = 1
    pygame.mixer.Sound.play(snd_rocket)
    pygame.mixer.music.play(-1)
    char_width = spr_iron.get_width()
    char_height = spr_iron.get_height()
    rocket_width  = spr_rocket.get_width()
    rocket_height  = spr_rocket.get_height()
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
                            debug_mode = False
                            pygame.mixer.music.play(-1)
                            break
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pause = True
                pygame.mixer.music.stop()
                b_width = 150
                b_height = 40
                b_width = 150
                b_height  = 40
                b = pygame.draw.rect(screen, white, (10,10, b_width, b_height), border_radius=15)
                start_txt = font_menu.render("Iniciar Game", True, black)
                screen.blit(start_txt, (25,12))
                b = pygame.draw.rect(screen, white, (10,50, b_width, b_height), border_radius=15)
                quit_txt = font_menu.render("Sair do Game", True, black)
                screen.blit(quit_txt, (25,62))
                pygame.display.update()
                while True:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            quit()
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            if b.collidepoint(evento.pos):
                                b_width = 140
                                b_height = 35
                            if b.collidepoint(evento.pos):
                                b_width = 140
                                b_height  = 35
                            
                        elif evento.type == pygame.MOUSEBUTTONUP:
                            if b.collidepoint(evento.pos):
                                pygame.mixer.music.play(-1)
                                pause = False
                                b_width = 150
                                b_height = 40
                                break
                                
                            if b.collidepoint(evento.pos):
                                #pygame.mixer.music.play(-1)
                                b_width = 150
                                b_height  = 40
                                quit()
                        elif evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_ESCAPE:
                                pause = False
                                pygame.mixer.music.play(-1)
                                break
                    if pause == False:
                            break
        
        char_x, char_y = move_horizontal(char_x, char_y, screen, char_height, char_width, move_x, move_y, air_resistance)

        x_far, x_middle, x_near = backGround(x_far, x_middle, x_near, screen, spr_far, spr_middle, spr_near, white)

        rocket_y = rocket_y + move_rocket
        if rocket_y > 500:
            rocket_y = -240
            move_rocket = move_rocket + 1
            rocket_x = random.randint(0,800)
            pygame.mixer.Sound.play(snd_rocket)
            
            
        screen.blit(spr_rocket, (rocket_x, rocket_y) )
        
        #Vida
        
        if colisao_retangulos(char_x, char_y, char_width, char_height,
            rocket_x, rocket_y, rocket_width, rocket_height):
            dead()
        #else:
            #print("Ainda Vivo")
            
        screen.blit(spr_iron, (char_x, char_y) )

        if debug_mode:
            debug_lines = [
                f"FPS: {clock.get_fps()}",
                f"Posição do Personagem: ({char_x}, {char_y})",
                f"Movimento do Personagem: ({move_x}, {move_y})",
                f"Posição do Foguete: ({rocket_x}, {rocket_y})",
                f"Movimento do Foguete: {move_rocket}",
                f"Colisão: {colisao_retangulos(char_x, char_y, char_width, char_height, rocket_x, rocket_y, rocket_width, rocket_height)}"
            ]
            for i, line in enumerate(debug_lines):
                text = font_debug.render(line, True, (black))
                screen.blit(text, (10, 10 + i * 20))

        pygame.display.update()
        clock.tick(50)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(snd_explosion)
    b_width = 150
    b_height = 40
    b_width = 150
    b_height  = 40

    # Adiciona o log das partidas no Listbox
    '''log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()'''
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if b.collidepoint(evento.pos):
                    b_width = 140
                    b_height = 35
                if b.collidepoint(evento.pos):
                    b_width = 140
                    b_height  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if b.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    b_width = 150
                    b_height = 40
                    game()
                if b.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    b_width = 150
                    b_height  = 40
                    quit()
                    
        
            
            
        screen.fill(white)
        screen.blit(spr_dead, (0,0) )

        
        b = pygame.draw.rect(screen, white, (10,10, b_width, b_height), border_radius=15)
        start_txt = font_menu.render("Iniciar Game", True, black)
        screen.blit(start_txt, (25,12))
        
        b = pygame.draw.rect(screen, white, (10,50, b_width, b_height), border_radius=15)
        quit_txt = font_menu.render("Sair do Game", True, black)
        screen.blit(quit_txt, (25,62))


        pygame.display.update()
        clock.tick(50)

menu(start=1, b_n=2)