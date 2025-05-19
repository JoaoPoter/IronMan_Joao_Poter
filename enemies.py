import pygame, random
from recursos.gif import extract_frames

pygame.init()
aspect_ratio = (1200, 740)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(aspect_ratio)

spr_than = pygame.image.load("assets/than.gif")
snd_rocket = pygame.mixer.Sound("assets/missile.wav")
spr_rocket = pygame.image.load("assets/missile.png")

rocket_width  = spr_rocket.get_width()
rocket_height  = spr_rocket.get_height()

extract_frames("assets/than_rock.gif", "assets/frames_thanrock")
extract_frames("assets/than_handy.gif", "assets/frames_handy")

def than(rocket_x, rocket_y, screen, than_x, than_y, move_rocket):
    rocket_x = rocket_x + move_rocket
    if rocket_x < 0:
        rocket_x = 1240
        move_rocket += 1
        rocket_y = random.randint(0,600)
        pygame.mixer.Sound.play(snd_rocket)
        
    screen.blit(spr_rocket, (rocket_x, rocket_y) )

    screen.blit(spr_than, (than_x, than_y))
    
    return rocket_x, rocket_y, rocket_width, rocket_height
