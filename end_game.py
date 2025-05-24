import cv2
import pygame
import sys

def end_game():
    pygame.mixer_music.load('assets/final.wav')
    # Load video using OpenCV
    video_path = "assets/final_audio.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)  # milliseconds
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set up pygame window
    window = pygame.display.set_mode((frame_width, frame_height))
    pygame.display.set_caption("MP4 Player")

    running = True
    clock = pygame.time.Clock()
    pygame.mixer_music.play()
    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona frame para caber na tela cheia
        frame = cv2.resize(frame, (1200, 740))

        # Convert BGR (OpenCV) to RGB (pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(fps)  # Ensure it runs at video framerate

    cap.release()
    pygame.quit()
    sys.exit()
