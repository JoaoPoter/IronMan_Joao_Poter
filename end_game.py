import pygame
from pyvidplayer2 import Video
pygame.mixer.music.load('assets/final.wav')
def end_game(screen):
    # Carrega o vídeo
    pygame.mixer.music.play(1)
    video = Video('assets/final.mp4', no_audio=True)
    video.resize((1200, 740))  # Ajuste opcional de tamanho

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o vídeo e renderiza o próximo frame
        video.draw(screen, (0, 0))

        pygame.display.update()
        clock.tick(60)

    # Clean up resources
    video.close()