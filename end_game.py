import cv2
import pygame
import sys

def end_game():
    now = pygame.time.get_ticks()
    before_video = pygame.time.get_ticks()
    pygame.mixer_music.load('assets/sounds/final.wav')
    video_path = "assets/final_audio.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    window = pygame.display.set_mode((1200, 740))
    pygame.display.set_caption("MP4 Player")

    running = True
    clock = pygame.time.Clock()
    pygame.mixer_music.play()
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (1200, 740))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            now == pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if now - before_video >= 1500:
                    pygame.mixer_music.fadeout
                    running = False

        window.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(fps)
    pygame.mixer_music.fadeout(500)
    return