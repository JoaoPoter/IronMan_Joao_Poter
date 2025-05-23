import pygame, random, time
from recursos.funcoes import inicializarBancoDeDados, colisao_retangulos, carregar_frames, move_horizontal, fade_text, Rocket
from recursos.animation import SpriteAnimator
from recursos.gif import extract_frames
from thanos import Boss

pygame.init()
pygame.mixer.init()
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
spr_dead = pygame.image.load("assets/iron_dead.jpeg")
spr_than = pygame.image.load("assets/than.gif")
spr_head = pygame.image.load("assets/iron_head.png")
snd_explosion = pygame.mixer.Sound("assets/explosao.wav")
font_title = pygame.font.Font("assets/Ethnocentric Rg.otf", 50)
font_menu = pygame.font.Font("assets/Ethnocentric Rg.otf",18)
font_dead = pygame.font.SysFont("arial",120)
font_debug = pygame.font.SysFont(None, 16)
musicas = [
    "assets/iron_2012.wav",
    "assets/ironsound.mp3",
    "assets/Game_Over.mp3"
]

music_i = 0

spr_head = pygame.transform.scale(spr_head, ( 50, 50))
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

than_x = 750
than_y = 250

b_n = 0
start = 0

all_sprites = []

background_frames = carregar_frames("assets/frames_background", flip_horizontal=False, scale=(1200,740))

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
thanos = Boss(than_x, than_y, all_sprites, rocks)
all_sprites.add(thanos)

def tocar_musica(index):
    pygame.mixer.music.load(index)
    pygame.mixer.music.play()

def menu(menu_type, b_n):
    """
    menu_type: 'start', 'pause', 'death'
    b_n: quantidade de botões
    """
    tocar_musica(musicas[0])
    dark_overlay = pygame.Surface(screen.get_size())
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(100)
    
    b_width = 250
    b_height = 50
    txt_pos = [300, 230]
    buttons = [f"b_{i}" for i in range(b_n)]
    
    # Define o título e o fundo com base no tipo de menu
    if menu_type == 'start':
        tocar_musica(musicas[0])
        screen.fill(white)
        screen.blit(spr_iron_bg, (0, 0))
        fade_text("Iron Man", font_title, cinza, (303, 53), screen, fade_in=True, duracao=200)
        fade_text("Iron Man", font_title, white, (300, 50), screen, fade_in=True, duracao=600)
    elif menu_type == 'pause':
        pygame.mixer_music.set_volume(0.5)
        screen.blit(dark_overlay, (0, 0))
        fade_text("Pause", font_title, cinza, (503, 53), screen, fade_in=True, duracao=200)
        fade_text("Pause", font_title, white, (500, 50), screen, fade_in=True, duracao=600)
    elif menu_type == 'death':
        screen.blit(dark_overlay, (0, 0))
        tocar_musica(musicas[2])
        pygame.mixer.Sound.play(snd_explosion)
        fade_text("Game Over", font_title, cinza, (353, 143), screen, fade_in=True, duracao=200)
        fade_text("Game Over", font_title, white, (350, 140), screen, fade_in=True, duracao=600)
    
    if menu_type == 'start':
        for i in range(b_n):
            if buttons[i] == "b_0":
                b1 = pygame.draw.rect(screen, white, (txt_pos[0], txt_pos[1], b_width, b_height), border_radius=16)
                screen.blit(spr_start_b, (txt_pos[0]-50, txt_pos[1]))
                start_txt = font_menu.render("Iniciar Game", True, black)
                screen.blit(start_txt, (txt_pos[0], txt_pos[1]+10))
            elif buttons[i] == "b_1":
                b2 = pygame.draw.rect(screen, white, (txt_pos[0], txt_pos[1]+70, b_width, b_height), border_radius=16)
                screen.blit(spr_quit_b, (txt_pos[0]-50, txt_pos[1]+70))
                quit_txt = font_menu.render("Sair do Game", True, black)
                screen.blit(quit_txt, (txt_pos[0], txt_pos[1]+80))
    elif menu_type == 'pause':
        for i in range(b_n):
            if buttons[i] == "b_0":
                b1 = pygame.draw.rect(screen, white, (txt_pos[0]+150, txt_pos[1], b_width, b_height), border_radius=16)
                screen.blit(spr_start_b, (txt_pos[0]+150, txt_pos[1]))
                start_txt = font_menu.render("Iniciar Game", True, black)
                screen.blit(start_txt, (txt_pos[0]+210, txt_pos[1]+10))
            elif buttons[i] == "b_1":
                b2 = pygame.draw.rect(screen, white, (txt_pos[0]+150, txt_pos[1]+70, b_width, b_height), border_radius=16)
                screen.blit(spr_quit_b, (txt_pos[0]+150, txt_pos[1]+70))
                quit_txt = font_menu.render("Sair do Game", True, black)
                screen.blit(quit_txt, (txt_pos[0]+210, txt_pos[1]+80))
    elif menu_type == 'death':
        for i in range(b_n):
            if buttons[i] == "b_0":
                b1 = pygame.draw.rect(screen, white, (txt_pos[0]+130, txt_pos[1], b_width, b_height), border_radius=16)
                screen.blit(spr_start_b, (txt_pos[0]+130, txt_pos[1]))
                start_txt = font_menu.render("Iniciar Game", True, black)
                screen.blit(start_txt, (txt_pos[0]+190, txt_pos[1]+10))
            elif buttons[i] == "b_1":
                b2 = pygame.draw.rect(screen, white, (txt_pos[0]+130, txt_pos[1]+70, b_width, b_height), border_radius=16)
                screen.blit(spr_quit_b, (txt_pos[0]+130, txt_pos[1]+70))
                quit_txt = font_menu.render("Sair do Game", True, black)
                screen.blit(quit_txt, (txt_pos[0]+190, txt_pos[1]+80))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(evento.pos):
                    pass  # Apenas um placeholder, não precisa mudar o overlay aqui
                if b2.collidepoint(evento.pos):
                    pass
            elif evento.type == pygame.MOUSEBUTTONUP:
                if b1.collidepoint(evento.pos):
                    b_width = 150
                    b_height = 40
                    if menu_type in ('start','death') :
                        game()
                    else:
                        return True
                if b2.collidepoint(evento.pos):
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if menu_type == 'pause' and evento.key == pygame.K_ESCAPE:
                    return True
        
        pygame.display.update()
        clock.tick(60)

def game():
    rocket_cooldown = 2000
    last_rocket_time = 0
    frame_index = 0
    frame_timer = 0
    frame_delay = 200
    air_resistance = 16
    debug_mode = False
    iron_x = 100    
    iron_y = 300
    move_x  = 0
    move_y  = 0
    spr_iron = spr_iron_soaring
    iron_width = spr_iron_soaring.get_width()
    iron_height = spr_iron_soaring.get_height()
    iron_vida = 3
    tocar_musica(musicas[1])

    while True:
        current_time = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_F3:
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
                    if evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_F3:
                            debug_mode = False[
                            tocar_musica(musicas[1])]
                            break
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                menu('pause', b_n=2)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                if current_time - last_rocket_time > rocket_cooldown:
                    last_rocket_time = current_time
                    new_proj = Rocket(iron_x+100,iron_y+30)
                    projectiles.add(new_proj)
                    all_sprites.add(new_proj)
                    
        iron_x, iron_y, spr_iron = move_horizontal(iron_x, iron_y, screen, iron_height, iron_width, move_x, move_y, air_resistance, spr_iron, spr_iron_boosting, spr_iron_soaring)

        current_time = pygame.time.get_ticks()
        if current_time - frame_timer >= frame_delay:
            frame_index = (frame_index + 1) % len(background_frames)
            frame_timer = current_time

        screen.blit(background_frames[frame_index], (0, 0))

        thanos.update()
        thanos.animate()
        
        player_rect = pygame.Rect(iron_x, iron_y, iron_width, iron_height)
        thanos_rect = thanos.rect

        screen.blit(spr_iron, (iron_x, iron_y) )
        if colisao_retangulos(
        iron_x, iron_y, iron_width, iron_height,
        thanos_rect.x, thanos_rect.y, thanos_rect.width, thanos_rect.height
        ):
            dead()
            break

        head_height = thanos_rect.height // 3
        thanos_head_rect = pygame.Rect(
        thanos.rect.x,
        thanos.rect.y+20,
        thanos.rect.width,
        head_height
        )
        
        for proj in projectiles:
            if thanos_head_rect.colliderect(proj.rect):
                if debug_mode:
                    pygame.draw.rect(screen, (255, 0, 0), proj.rect, 2)
                if not proj.exploding:
                    proj.explodir()
                    thanos.tomar_dano()
                    #snd_explosion.play()
            if iron_vida <= 0:
                thanos.morrer
                dead()
                return
            break
            
        for rock in rocks:
            if colisao_retangulos(
            iron_x, iron_y, iron_width, iron_height,
            rock.rect.x-30, rock.rect.y, rock.rect.width, rock.rect.height
            ):
                if not rock.exploding:
                    rock.explodir()
                    iron_vida -= 1
                    #snd_explosion.play()
                if iron_vida <= 0:
                    iron_vida = 3
                    thanos.morrer
                    dead()
                    return
                break

        if debug_mode:
            debug_lines = [
                f"FPS: {clock.get_fps()}",
                f"Posição do Personagem: ({iron_x}, {iron_y})",
                f"Movimento do Personagem: ({move_x}, {move_y})",
                #f"Colisão: {colisao_retangulos(iron_x, iron_y, iron_width, iron_height, rocket_x, rocket_y, rocket_width, rocket_height)}",
                ]
            for i, line in enumerate(debug_lines):
                text = font_debug.render(line, True, (black))
                screen.blit(text, (10, 10 + i * 20))
        
        for i in range(iron_vida):
            screen.blit(spr_head, (10+i*50, 10))
        
        all_sprites.update()
        all_sprites.draw(screen)


        pygame.display.update()
        clock.tick(50)

def dead():
    screen.fill(white)
    screen.blit(spr_dead, (0,0) )
    # Adiciona o log das partidas no Listbox
    '''log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()'''

    menu('death', b_n=2)

menu('start', b_n=2)
