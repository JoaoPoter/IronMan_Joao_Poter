from PIL import Image
import pygame, os

gif_path = os.path.join("assets", "than_rock.gif",)
# Carrega o GIF e extrai os frames
gif = Image.open(gif_path)
frames = []

try:
    while True:
        frame = gif.copy()
        frame = frame.convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        pg_image = pygame.image.fromstring(data, size, mode)
        frames.append(pg_image)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Exibe os frames
running = True
i = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(frames[i], (100, 100))
    i = (i + 1) % len(frames)
    pygame.display.flip()
    clock.tick(10)  # 10 FPS (ajuste conforme necessário)

pygame.quit()
