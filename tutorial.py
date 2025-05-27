import pygame

class Tutorial:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.texts = [
            "True:",
            "Use the 'W' and 'S' keys to move up and down.",
            "Press 'Space' to boost foward.",
            "Avoid Thano's rocks and collect shoot rockets in his face with 'E'.",
            "Press 'ESC' to pause the game.",
            "Press any button to continue.",
            "Good luck!"
        ]
        self.current_text_index = 0
        self.text_y = 50
        self.text_color = (255, 255, 255)
        self.text_alpha = 255
        self.fade_in_duration = 1000
    def draw(self, screen, spr_iron_bg):
        spr_iron_bg = pygame.transform.scale(spr_iron_bg, (self.screen.get_width(), self.screen.get_height()))
        screen.blit(spr_iron_bg, (0, 0))
        for i, text in enumerate(self.texts):
            text_surface = self.font.render(text, True, self.text_color)
            text_surface.set_alpha(self.text_alpha)
            self.screen.blit(text_surface, (50, self.text_y + i * 40))
        
    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                print("Key pressed:", evento.key)
                return True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False
            