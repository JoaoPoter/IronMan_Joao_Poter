import pygame, random, json, tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados

pygame.init()
inicializarBancoDeDados()
aspect_ratio = (1200,800)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(aspect_ratio) 

pygame.display.set_caption("Iron Man do J_Poter")
icon  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icon)

spr_iron = pygame.image.load("assets/iron_soaring.png")
spr_iron_bg = pygame.image.load("assets/fundoStart.jpg")
spr_far = pygame.image.load("assets/back.png")
spr_middle = pygame.image.load("assets/mid.png")
spr_near = pygame.image.load("assets/front.png")
spr_dead = pygame.image.load("assets/fundoDead.png")
spr_rocket = pygame.image.load("assets/missile.png")
snd_rocket = pygame.mixer.Sound("assets/missile.wav")
snd_explosion = pygame.mixer.Sound("assets/explosao.wav")
font_menu = pygame.font.SysFont("comicsans",18)
font_dead = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/ironsound.mp3")

spr_far = pygame.transform.scale(spr_far, (aspect_ratio[0], aspect_ratio[1]))
spr_middle = pygame.transform.scale(spr_middle, (aspect_ratio[0], aspect_ratio[1]))
spr_near = pygame.transform.scale(spr_near, (aspect_ratio[0], aspect_ratio[1]))
spr_iron_bg = pygame.transform.scale(spr_iron_bg, (aspect_ratio[0], aspect_ratio[1]))
spr_dead = pygame.transform.scale(spr_dead, (aspect_ratio[0], aspect_ratio[1]))

white = (255,255,255)
black = (0, 0 ,0 )

def colisao_retangulos(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

def get_name():
    screen_width = 300
    screen_height = 50
    
    global name
    name = entry_name.get()  # Obtém o texto digitado
    if not name:  # Se o campo estiver vazio
        messagebox.showwarning("Aviso", "Por favor, digite seu name!")  # Exibe uma mensagem de aviso
    else:
       #print(f'name digitado: {name}')  # Exibe o name no console
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # get as dimensões da screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    pos_x = (screen_width - screen_width) // 2
    pos_y = (screen_height - screen_height) // 2
    root.geometry(f"{screen_width}x{screen_height}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", get_name)

    # Entry (campo de texto)
    entry_name = tk.Entry(root)
    entry_name.pack()

    # Botão para pegar o name
    botao = tk.Button(root, text="Enviar", command=get_name)
    botao.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()

def game():

    x_far = 0
    x_middle = 0
    x_near = 0

    char_x = 400
    char_y = 300
    move_x  = 0
    move_y  = 0
    rocket_x = 400
    rocket_y = -240
    move_rocket = 1
    pygame.mixer.Sound.play(snd_rocket)
    pygame.mixer.music.play(-1)
    char_width = 250
    char_height =    127
    rocket_width  = 50
    rocket_height  = 250
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        move_x = keys[pygame.K_d] - keys[pygame.K_a]
        move_y = keys[pygame.K_s] - keys[pygame.K_w]

        char_x += move_x * 15       
        char_y += move_y * 15      
        
        if char_x < 0 :
            char_x = 15
        elif char_x >550:
            char_x = 540
            
        if char_y < 0 :
            char_y = 15
        elif char_y > 473:
            char_y = 463
        
            
        screen.fill(white)
        screen.blit(spr_far, (0,0) )

        x_far = x_far - 0.2
        x_middle = x_middle - 0.5
        x_near = x_near - 1.0

        if x_far <= -800: x_far = 0
        if x_middle <= -800: x_middle = 0
        if x_near <= -800: x_near = 0

        # Desenha duas cópias de cada camada para "colar" uma na outra
        screen.blit(spr_far, (x_far, 0))
        screen.blit(spr_far, (x_far + 800, 0))

        screen.blit(spr_middle, (x_middle, 0))
        screen.blit(spr_middle, (x_middle + 800, 0))

        screen.blit(spr_near, (x_near, 0))
        screen.blit(spr_near, (x_near + 800, 0))

        rocket_y = rocket_y + move_rocket
        if rocket_y > 600:
            rocket_y = -240
            move_rocket = move_rocket + 1
            rocket_x = random.randint(0,800)
            pygame.mixer.Sound.play(snd_rocket)
            
            
        screen.blit(spr_rocket, (rocket_x, rocket_y) )
        
        #Vida
        
        if colisao_retangulos(char_x, char_y, char_width, char_height,
            rocket_x, rocket_y, rocket_width, rocket_height):
            dead()
        else:
            print("Ainda Vivo")
            
        screen.blit(spr_iron, (char_x, char_y) )

        pygame.display.update()
        clock.tick(60)


def start():
    startB_width = 150
    startB_height = 40
    quitB_width = 150
    quitB_height  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startB.collidepoint(evento.pos):
                    startB_width = 140
                    startB_height = 35
                if quitB.collidepoint(evento.pos):
                    quitB_width = 140
                    quitB_height  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startB.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    startB_width = 150
                    startB_height = 40
                    game()
                if quitB.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    quitB_width = 150
                    quitB_height  = 40
                    quit()
                    
            
            
        screen.fill(white)
        screen.blit(spr_iron_bg, (0,0) )

        startB = pygame.draw.rect(screen, white, (10,10, startB_width, startB_height), border_radius=15)
        start_txt = font_menu.render("Iniciar Game", True, black)
        screen.blit(start_txt, (25,12))
        
        quitB = pygame.draw.rect(screen, white, (10,60, quitB_width, quitB_height), border_radius=15)
        quit_txt = font_menu.render("Sair do Game", True, black)
        screen.blit(quit_txt, (25,62))
        
        pygame.display.update()
        clock.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(snd_explosion)
    startB_width = 150
    startB_height = 40
    quitB_width = 150
    quitB_height  = 40
    
    
    root = tk.Tk()
    root.title("screen da Morte")

    # Adiciona um título na screen
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startB.collidepoint(evento.pos):
                    startB_width = 140
                    startB_height = 35
                if quitB.collidepoint(evento.pos):
                    quitB_width = 140
                    quitB_height  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startB.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    startB_width = 150
                    startB_height = 40
                    game()
                if quitB.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    quitB_width = 150
                    quitB_height  = 40
                    quit()
                    
        
            
            
        screen.fill(white)
        screen.blit(spr_dead, (0,0) )

        
        startB = pygame.draw.rect(screen, white, (10,10, startB_width, startB_height), border_radius=15)
        start_txt = font_menu.render("Iniciar Game", True, black)
        screen.blit(start_txt, (25,12))
        
        quitB = pygame.draw.rect(screen, white, (10,60, quitB_width, quitB_height), border_radius=15)
        quit_txt = font_menu.render("Sair do Game", True, black)
        screen.blit(quit_txt, (25,62))


        pygame.display.update()
        clock.tick(60)


start()