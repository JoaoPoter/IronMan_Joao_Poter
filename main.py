import pygame
from recursos.funcoes import inicializarBancoDeDados, colisao_retangulos, backGround, move_horizontal, fade_text, Rocket
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

spr_iron_soaring = pygame.image.load("assets/iron_soaring.png")
spr_iron_boosting = pygame.image.load("assets/iron_boosting.png")
spr_iron_bg = pygame.image.load("assets/iron_start.jpg")
spr_far = pygame.image.load("assets/back.png")
spr_middle = pygame.image.load("assets/middle.png")
spr_near = pygame.image.load("assets/near.png")
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
    "assets/dragoes.wav",
    "assets/Game_Over.mp3"
]

music_i = 0

spr_head = pygame.transform.scale(spr_head, ( 60, 60))
spr_head.set_alpha(220)
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
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
thanos = Boss(than_x, than_y, all_sprites, rocks)
all_sprites.add(thanos)

def tocar_musica(index):
    pygame.mixer.music.load(index)
    pygame.mixer.music.play(-1)

def draw_button(screen, image, text, font, pos, button_size, offset, border_radius=16):
    """Desenha um botão com imagem e texto."""
    b_rect = pygame.draw.rect(screen, white, (*pos, *button_size), border_radius=border_radius)
    screen.blit(image, (pos[0] + offset[0], pos[1] + offset[1]))
    text_surface = font.render(text, True, black)
    screen.blit(text_surface, (pos[0] + offset[2], pos[1] + offset[3]))
    return b_rect

def menu(menu_type, b_n):
    spr_start_b = pygame.image.load("assets/start_b.png")
    spr_start_b = pygame.transform.scale(spr_start_b, (300, 50))
    spr_quit_b = pygame.image.load("assets/quit_b.png")
    spr_quit_b = pygame.transform.scale(spr_quit_b, (300, 50))

    dark_overlay = pygame.Surface(screen.get_size())
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(100)

    b_width, b_height = 250, 50
    txt_pos = [300, 230]
    button_size = (b_width, b_height)
    buttons = []

    menu_config = {
        'start': {
            'background': lambda: (screen.fill(white), screen.blit(spr_iron_bg, (0, 0))),
            'music': musicas[0],
            'title': "Iron Man",
            'title_pos': (300, 50),
            'text_offset': (-50, 0, 0, 10),
            'x_offset': 0
        },
        'pause': {
            'background': lambda: screen.blit(dark_overlay, (0, 0)),
            'music': None,
            'title': "Pause",
            'title_pos': (500, 50),
            'text_offset': (0, 0, 60, 10),
            'x_offset': 150
        },
        'death': {
            'background': lambda: screen.blit(dark_overlay, (0, 0)),
            'music': musicas[2],
            'title': "Game Over",
            'title_pos': (350, 140),
            'text_offset': (0, 0, 60, 10),
            'x_offset': 130
        }
    }

    config = menu_config[menu_type]
    if config['music']:
        tocar_musica(config['music'])
    if menu_type == 'pause':
        pygame.mixer_music.set_volume(0.3)
    config['background']()

    fade_text(config['title'], font_title, cinza, (config['title_pos'][0]+3, config['title_pos'][1]+3), screen, fade_in=True, duracao=200)
    fade_text(config['title'], font_title, white, config['title_pos'], screen, fade_in=True, duracao=600)

    for i in range(b_n):
        y_offset = i * 70
        pos = [txt_pos[0] + config['x_offset'], txt_pos[1] + y_offset]

        if i == 0:
            b = draw_button(screen, spr_start_b, "Iniciar Game", font_menu, pos, button_size, config['text_offset'])
        elif i == 1:
            b = draw_button(screen, spr_quit_b, "Sair do Game", font_menu, pos, button_size, config['text_offset'])
        
        buttons.append(b)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.collidepoint(evento.pos):
                        pass  # Placeholder
            elif evento.type == pygame.MOUSEBUTTONUP:
                if buttons[0].collidepoint(evento.pos):
                    if menu_type in ('start', 'death'):
                        pygame.mixer_music.set_volume(1)
                        pygame.mixer_music.fadeout(2)
                        game()
                    else:
                        pygame.mixer_music.set_volume(1)
                        return True
                elif len(buttons) > 1 and buttons[1].collidepoint(evento.pos):
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if menu_type == 'pause' and evento.key == pygame.K_ESCAPE:
                    pygame.mixer_music.set_volume(1)
                    return True
        
        pygame.display.update()
        clock.tick(60)


def game():
    rocket_cooldown = 2000
    last_rocket_time = 0
    air_resistance = 16
    debug_mode = False
    x_far = 0
    x_middle = 0
    x_near = 0
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
                debug_mode = not debug_mode

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                menu('pause', b_n=2)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                if current_time - last_rocket_time > rocket_cooldown:
                    last_rocket_time = current_time
                    new_proj = Rocket(iron_x+100,iron_y+30)
                    projectiles.add(new_proj)
                    all_sprites.add(new_proj)

        iron_x, iron_y, spr_iron = move_horizontal(iron_x, iron_y, screen, iron_height, iron_width, move_x, move_y, air_resistance, spr_iron, spr_iron_boosting, spr_iron_soaring)

        x_far, x_middle, x_near = backGround(x_far, x_middle, x_near, screen, spr_far, spr_middle, spr_near, white)

        thanos.update()
        thanos.animate()
        thanos_rect = thanos.rect

        screen.blit(spr_iron, (iron_x, iron_y) )
        if colisao_retangulos(
        iron_x, iron_y, iron_width, iron_height,
        thanos_rect.x, thanos_rect.y, thanos_rect.width, thanos_rect.height
        ):
            dead()

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

        if debug_mode:
            debug_lines = [
                f"FPS: {clock.get_fps()}",
                f"Posição do Personagem: ({iron_x}, {iron_y})",
                f"Movimento do Personagem: ({move_x}, {move_y})",
                ]
            for i, line in enumerate(debug_lines):
                text = font_debug.render(line, True, (white))
                screen.blit(text, (10, 600 + i * 20))
        
        for i in range(iron_vida):
            screen.blit(spr_head, (15+i*50, 15))

        texto = font_menu.render(f"Timer: {current_time/1000}", True, (white))
        screen.blit(texto, (535, 15))
        
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
