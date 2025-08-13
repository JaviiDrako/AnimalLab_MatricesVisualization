import pygame
from matrix_input_grid import MatrixInputGrid

class InstructionMainScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.image.load("assets/main_instructions.png"), (width, height))
        self.font = pygame.font.Font("assets/pixel_font.ttf", 60)
        self.input_grid = MatrixInputGrid(
            x=(width - 170) // 2,
            y=height - 400,
            cell_size=100,
            font=self.font
        )
        self.continue_button = pygame.Rect(width // 2 + 420, height - 250, 300, 70)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.input_grid.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.continue_button.collidepoint(event.pos):
                        running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.input_grid.clear()

            self.screen.blit(self.background, (0, 0))
            self.input_grid.draw(self.screen)

            mouse_pos = pygame.mouse.get_pos()
            if self.continue_button.collidepoint(mouse_pos):
                color = (40, 200, 190) 
            else:
                color = (10, 170, 190)  

            pygame.draw.rect(self.screen, color, self.continue_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.continue_button, 5, border_radius=8) 
            text = self.font.render("Continuar ->", True, (0, 0, 0))  
            self.screen.blit(text, (self.continue_button.x + 40, self.continue_button.y + 10)) 

            pygame.display.flip()
            clock.tick(60)
