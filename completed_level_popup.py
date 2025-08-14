import pygame

from utils import resource_path

class LevelCompletedPopup: 
    def __init__(self, screen, elapsed_time, width, height, background_surface, fps):  
        self.screen = screen
        self.elapsed_time = elapsed_time  
        self.WIDTH = width
        self.HEIGHT = height
        self.background = background_surface
        self.FPS = fps
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 45)
        self.font_timer = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 35)
        self.font_button = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 30)

        self.button_rect = pygame.Rect(0, 0, 240, 60)  
        self.button_rect.center = (self.WIDTH // 2, self.HEIGHT // 2 + 80)

    def run(self):
        waiting = True 

        minutes = self.elapsed_time // 60 
        seconds = self.elapsed_time % 60  
        time_text = f"Tiempo: {minutes}m {seconds}s" if minutes else f"Tiempo: {seconds}s"  

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        waiting = False

            self.screen.blit(self.background, (0, 0))

            window_rect = pygame.Rect(0, 0, 500, 300)  
            window_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
            pygame.draw.rect(self.screen, (255, 255, 255), window_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), window_rect, 5)

            title = self.font_title.render("¡Modificacion completada!", True, (50, 50, 255)) 
            self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, window_rect.top + 40))

            time_surface = self.font_timer.render(time_text, True, (0, 0, 0))  
            self.screen.blit(time_surface, (self.WIDTH // 2 - time_surface.get_width() // 2, window_rect.top + 110))

            pygame.draw.rect(self.screen, (100, 200, 100), self.button_rect, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect, 3, border_radius=8)
            button_text = self.font_button.render("Siguiente nivel", True, (0, 0, 0))  
            self.screen.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                           self.button_rect.centery - button_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(self.FPS)
