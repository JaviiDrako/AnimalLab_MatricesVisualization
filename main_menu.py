import pygame

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font("assets/pixel_font.ttf", 55)

        original_bg = pygame.image.load("assets/bg_menu.png").convert()
        self.background = pygame.transform.scale(original_bg, (self.width, self.height))

        self.game_button = pygame.Rect(width // 2 - 200, height // 2 + 170, 400, 80)
        self.free_mode_button = pygame.Rect(width // 2 - 200, height // 2 + 270, 400, 80) 

    def run(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.init()
        pygame.mixer.music.load("assets/intro_music.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  

        clock = pygame.time.Clock()
        
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_button.collidepoint(event.pos):
                        return "juego"  
                    elif self.free_mode_button.collidepoint(event.pos):
                        return "libre" 

            self.screen.blit(self.background, (0, 0))

            # Game button hover effect
            if self.game_button.collidepoint(mouse_pos):
                game_button_color = (40, 200, 190)  
            else:
                game_button_color = (10, 170, 190)

            pygame.draw.rect(self.screen, game_button_color, self.game_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.game_button, 7, border_radius=8)
            game_text = self.font.render("Iniciar Juego", True, (0, 0, 0))  
            self.screen.blit(game_text, game_text.get_rect(center=self.game_button.center))

            if self.free_mode_button.collidepoint(mouse_pos):
                free_mode_color = (40, 200, 190)  
            else:
                free_mode_color = (10, 170, 190)

            pygame.draw.rect(self.screen, free_mode_color, self.free_mode_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.free_mode_button, 7, border_radius=8)
            free_mode_text = self.font.render("Modo Libre", True, (0, 0, 0)) 
            self.screen.blit(free_mode_text, free_mode_text.get_rect(center=self.free_mode_button.center))

            pygame.display.flip()
            clock.tick(60)
