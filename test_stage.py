import pygame
from imagen import ImageManager
from visualizer import Visualizer
from matrix_input_grid import MatrixInputGrid
from rotation_helper import RotationHelper 
from utils import resource_path

class TestStage:
    def __init__(self, screen, width, height, phase): 
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.background = pygame.transform.scale(  
            pygame.image.load(resource_path("assets/test_stage_bg.png")), (width, height)
        )
        self.font = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 35)

        self.start_button = pygame.Rect(width // 2 - 900, height - 110, 280, 55)  

        self.reset_icon_size = 100
        self.reset_button = pygame.Rect(width - self.reset_icon_size - 70,
                                      height - self.reset_icon_size - 910,
                                      self.reset_icon_size,
                                      self.reset_icon_size)

        self.reset_icon = pygame.image.load(resource_path("assets/restart_icon.png")).convert_alpha()
        self.reset_icon = pygame.transform.scale(self.reset_icon,
                                               (self.reset_icon_size - 10, self.reset_icon_size - 10))

        self.phase = phase  
        self.error_message = ""  
        self.error_message_time = 0 

        self.reset_stage()
        self.applying_input = False

    def reset_stage(self):
        self.image_manager = ImageManager(resource_path("assets/test_dummy.png"))
        pixels = self.image_manager.get_centered_pixels()

        self.visualizer = Visualizer(
            screen=self.screen,
            pixels=pixels,
            center=(self.width // 2, self.height // 2),
            scale=0.79,
            steps=25
        )

        self.input_grid = MatrixInputGrid(
            x=(self.width - 160) // 2,
            y=self.height - 200,
            cell_size=70,
            font=self.font
        )

        self.rotation_helper = None
        if self.phase == 3:
            self.rotation_helper = RotationHelper(
                x=self.width - 320,
                y=self.height - 270,
                width=300,
                height=220
            )

        self.applying_input = False
        self.error_message = ""
        self.error_message_time = 0

    def is_valid_phase1_matrix(self, matrix):  
        for row in matrix: 
            for val in row:
                if val < 0:
                    return False
        return matrix[0][1] == 0 and matrix[1][0] == 0

    def is_valid_phase2_matrix(self, matrix):  
        a11, a12 = matrix[0]
        a21, a22 = matrix[1]
        if a11 < 0 or a22 < 0:
            return False
        if a12 != 0 and a21 != 0:
            return False
        return True

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.rotation_helper:
                    self.rotation_helper.angle_input.handle_event(event)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.rotation_helper.angle_input.active:
                            angle = self.rotation_helper.angle_input.get_value()
                            self.rotation_helper.update(angle)

                self.input_grid.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        running = False
                    elif self.reset_button.collidepoint(event.pos):
                        self.reset_stage()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.applying_input:
                        if not (self.rotation_helper and self.rotation_helper.angle_input.active):
                            input_matrix = self.input_grid.get_matrix() 

                            if input_matrix is None:
                                self.error_message = "¡Completa todas las celdas!"
                                self.error_message_time = current_time
                                continue  

                            is_valid = True
                            if self.phase == 1:
                                is_valid = self.is_valid_phase1_matrix(input_matrix)
                            elif self.phase == 2:
                                is_valid = self.is_valid_phase2_matrix(input_matrix)

                            if not is_valid:
                                self.error_message = "¡Matriz invalida!"
                                self.error_message_time = current_time
                            else:
                                self.visualizer.set_target_matrix(input_matrix)
                                self.applying_input = True
                                self.input_grid.clear()
                                self.error_message = ""

            self.screen.blit(self.background, (0, 0))

            done = self.visualizer.update()
            self.visualizer.draw()

            self.input_grid.draw(self.screen)

            if self.rotation_helper:
                self.rotation_helper.draw(self.screen)

            mouse_pos = pygame.mouse.get_pos()
            button_color = (40, 200, 190) if self.start_button.collidepoint(mouse_pos) else (10, 170, 190)  
            pygame.draw.rect(self.screen, button_color, self.start_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 5, border_radius=8)
            button_text = self.font.render("Comenzar Fase", True, (0, 0, 0)) 
            self.screen.blit(button_text, button_text.get_rect(center=self.start_button.center))

            reset_color = (200, 80, 80) if self.reset_button.collidepoint(mouse_pos) else (170, 50, 50) 
            pygame.draw.rect(self.screen, reset_color, self.reset_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.reset_button, 3, border_radius=8)
            icon_x = self.reset_button.x + (self.reset_button.width - self.reset_icon.get_width()) // 2
            icon_y = self.reset_button.y + (self.reset_button.height - self.reset_icon.get_height()) // 2
            self.screen.blit(self.reset_icon, (icon_x, icon_y))

            if self.error_message:
                if current_time - self.error_message_time < 2000:
                    error_text = self.font.render(self.error_message, True, (255, 50, 50))  
                    self.screen.blit(error_text, error_text.get_rect(center=(self.width // 2 - 10, self.height // 2 + 300)))
                else:
                    self.error_message = ""

            if done:
                self.applying_input = False

            pygame.display.flip()
            self.clock.tick(self.fps)

