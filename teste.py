import pygame
import sys

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Debug Test")
clock = pygame.time.Clock()

# Fonte para debug
font_dead = pygame.font.SysFont(None, 24)

# Propriedades do personagem
char_x, char_y = 100, 100
char_width, char_height = 50, 50
move_x, move_y = 0, 0
speed = 5

# Propriedades do foguete
rocket_x, rocket_y = 400, 300
rocket_width, rocket_height = 30, 60
move_rocket = True

# Função de colisão
def colisao_retangulos(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

# Loop principal
while True:
    clock.tick(60)  # 60 FPS

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                move_x = -speed
            elif evento.key == pygame.K_RIGHT:
                move_x = speed
            elif evento.key == pygame.K_UP:
                move_y = -speed
            elif evento.key == pygame.K_DOWN:
                move_y = speed
        elif evento.type == pygame.KEYUP:
            if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                move_x = 0
            if evento.key in [pygame.K_UP, pygame.K_DOWN]:
                move_y = 0

    # Atualização da posição
    char_x += move_x
    char_y += move_y

    if move_rocket:
        rocket_y += 2
        if rocket_y > 600:
            rocket_y = -rocket_height  # Reinicia o foguete no topo

    # Desenho
    screen.fill((0, 0, 0))  # Fundo preto
    pygame.draw.rect(screen, (0, 255, 0), (char_x, char_y, char_width, char_height))  # Personagem
    pygame.draw.rect(screen, (255, 0, 0), (rocket_x, rocket_y, rocket_width, rocket_height))  # Foguete

    # Debug info
    debug_lines = [
        f"FPS: {clock.get_fps():.2f}",
        f"Posição do Personagem: ({char_x}, {char_y})",
        f"Movimento do Personagem: ({move_x}, {move_y})",
        f"Posição do Foguete: ({rocket_x}, {rocket_y})",
        f"Movimento do Foguete: {move_rocket}",
        f"Colisão: {colisao_retangulos(char_x, char_y, char_width, char_height, rocket_x, rocket_y, rocket_width, rocket_height)}"
    ]
    for i, line in enumerate(debug_lines):
        text = font_dead.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 20))

    pygame.display.flip()
