import pygame
import speech_recognition as sr
from rapidfuzz import fuzz

class Menu:
    def __init__(self, screen, menu_type, b_n, musicas, spr_iron_bg, fade_text, draw_button, game, recognizer, expected_phrase):
        self.screen = screen
        self.menu_type = menu_type
        self.b_n = b_n
        self.musicas = musicas
        self.spr_iron_bg = spr_iron_bg
        self.fade_text = fade_text
        self.draw_button = draw_button
        self.game = game
        self.recognizer = recognizer
        self.expected_phrase = expected_phrase
        
        self.font_tutorial = pygame.font.Font("assets/texts/cour.ttf", 30)
        self.clock = pygame.time.Clock()
        
        self.cinza = (100, 100, 100)
        self.font_title = pygame.font.Font("assets/texts/Ethnocentric Rg.otf", 50)
        self.font_menu = pygame.font.Font("assets/texts/Ethnocentric Rg.otf",18)

        self.spr_start_b = pygame.transform.scale(
            pygame.image.load("assets/texts/start_b.png"), (300, 50))
        self.spr_quit_b = pygame.transform.scale(
            pygame.image.load("assets/texts/quit_b.png"), (300, 50))
        
        self.dark_overlay = pygame.Surface(screen.get_size())
        self.dark_overlay.fill((0, 0, 0))
        self.dark_overlay.set_alpha(100)
        
        self.buttons = []
        
        self.menu_config = {
            'start': {
                'background': lambda: (screen.fill((255,255,255)), screen.blit(self.spr_iron_bg, (0, 0))),
                'music': self.musicas[0],
                'title': "Iron Man",
                'title_pos': (300, 50),
                'text_offset': (-50, 0, 0, 10),
                'x_offset': 0
            },
            'pause': {
                'background': lambda: screen.blit(self.dark_overlay, (0, 0)),
                'music': None,
                'title': "Pause",
                'title_pos': (500, 50),
                'text_offset': (0, 0, 60, 10),
                'x_offset': 150
            },
            'death': {
                'background': lambda: screen.blit(self.dark_overlay, (0, 0)),
                'music': self.musicas[2],
                'title': "Game Over",
                'title_pos': (350, 140),
                'text_offset': (0, 0, 60, 10),
                'x_offset': 130
            }
        }

    def show(self):
        config = self.menu_config[self.menu_type]
        if config['music']:
            self.tocar_musica(config['music'])
        if self.menu_type == 'pause':
            pygame.mixer_music.set_volume(0.3)

        config['background']()
        
        self.fade_text(config['title'], self.font_title, self.cinza, (config['title_pos'][0]+3, config['title_pos'][1]+3), self.screen, fade_in=True, duracao=200)
        self.fade_text(config['title'], self.font_title, (255, 255, 255), config['title_pos'], self.screen, fade_in=True, duracao=600)

        self.create_buttons(config)

        running = True
        while running:
            running = self.process_events()

            pygame.display.update()
            self.clock.tick(60)

    def create_buttons(self, config):
        txt_pos = [300, 230]
        b_width, b_height = 250, 50
        button_size = (b_width, b_height)
        
        for i in range(self.b_n):
            y_offset = i * 70
            pos = [txt_pos[0] + config['x_offset'], txt_pos[1] + y_offset]
            
            if i == 0:
                b = self.draw_button(self.screen, self.spr_start_b, "Iniciar Game", self.font_menu, pos, button_size, config['text_offset'])
            elif i == 1:
                b = self.draw_button(self.screen, self.spr_quit_b, "Sair do Game", self.font_menu, pos, button_size, config['text_offset'])
            self.buttons.append(b)

    def process_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pass  # opcional: highlight botão
            elif evento.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].collidepoint(evento.pos):
                    if self.menu_type in ('start', 'death'):
                        self.run_tutorial()
                    else:
                        pygame.mixer_music.set_volume(1)
                        return False
                elif len(self.buttons) > 1 and self.buttons[1].collidepoint(evento.pos):
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if self.menu_type == 'pause' and evento.key == pygame.K_ESCAPE:
                    pygame.mixer_music.set_volume(1)
                    return False
        return True

    def run_tutorial(self):
        text = (
            "The Avengers were prepared to attack Thanos, but when Iron Man\n"
            "was on his way to the battle field, Thanos surprised him\n"
            "and now they will fight 'til death!\n"
            "\n"
            "\n"
            "How to play:\n"
            "Use the 'W' and 'S' keys to move up and down.\n"
            "Press 'Space' to boost forward.\n"
            "Avoid Thano's rocks and shoot rockets in his face with 'E'.\n"
            "Press 'ESC' to pause the game.\n"
            "To start the game say 'I am Iron Man'.\n"
            "Good luck!"
        )

        type_sound = pygame.mixer.Sound(self.musicas[3])
        type_sound.set_volume(0.5)
        
        text_color = (0, 240, 0)
        bg_color = (0, 0, 0)
        current_text = ''
        text_index = 0
        type_speed = 50
        last_update = pygame.time.get_ticks()
        
        type_sound.play(2)
        
        finished_typing = False
        tutorial_running = True

        while tutorial_running:
            self.screen.fill(bg_color)
            pygame.mixer_music.set_volume(0.6)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    finished_typing = True
                    current_text = text
                    tutorial_running = False
                    type_sound.fadeout(10)
                    self.game()

            now = pygame.time.get_ticks()
            if now - last_update > type_speed:
                if text_index < len(text):
                    current_text += text[text_index]
                    text_index += 1
                    last_update = now
                else:
                    finished_typing = True
                    type_sound.stop()

            lines = current_text.split('\n')
            y = 100
            for line in lines:
                rendered_line = self.font_tutorial.render(line, True, text_color)
                self.screen.blit(rendered_line, (70, y))
                y += self.font_tutorial.get_height() + 5

            pygame.display.flip()
            self.clock.tick(60)

            if finished_typing:
                print("Reconhecendo...")
                type_sound.stop()
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    try:
                        audio = self.recognizer.listen(source, phrase_time_limit=5)
                        recognized_text = self.recognizer.recognize_google(audio)
                        similarity = fuzz.ratio(recognized_text.lower(), self.expected_phrase.lower())
                        if similarity > 40:
                            print("✅ Sucesso! Você é o Homem de Ferro.")
                            tutorial_running = False
                            type_sound.fadeout(10)
                            self.game()
                        else:
                            print("❌ Não foi parecido o bastante. Tente novamente.")
                    except sr.UnknownValueError:
                        print("❗ Não foi possível entender o áudio.")
                    except sr.RequestError as e:
                        print(f"❗ Erro no serviço de reconhecimento: {e}")

    def tocar_musica(self, musica):
        pygame.mixer_music.load(musica)
        pygame.mixer_music.play(-1)

