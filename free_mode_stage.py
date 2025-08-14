import pygame
from imagen import ImageManager
from visualizer import Visualizer
from matrix_input_grid import MatrixInputGrid
from rotation_helper import RotationHelper
from utils import resource_path


class FreeModeStage:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.background = pygame.transform.scale(  
            pygame.image.load(resource_path("assets/free_mode_bg.png")), (width, height)
        )
        self.font = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 35)

        self.animals = [
            resource_path("assets/monkey.png"), resource_path("assets/snake.png"), resource_path("assets/elephant.png"),
            resource_path("assets/crab.png"), resource_path("assets/goat.png"), resource_path("assets/dolphin.png"),
            resource_path("assets/capybara.png"), resource_path("assets/eagle.png"), resource_path("assets/pig.png"),
            resource_path("assets/panda.png"), resource_path("assets/gorilla.png"), resource_path("assets/lion.png"),
            resource_path("assets/racoon.png"), resource_path("assets/toucan.png"), resource_path("assets/penguin.png")
        ]
        self.current_index = 0

        # Botones de control
        self.prev_button = pygame.Rect(50, 20, 150, 50)
        self.next_button = pygame.Rect(width - 200, 20, 150, 50)
        self.reset_icon_size = 100
        self.reset_button = pygame.Rect(width / 2 - 50,
                                      20,
                                      self.reset_icon_size,
                                      self.reset_icon_size)

        self.reset_icon = pygame.image.load(resource_path("assets/restart_icon.png")).convert_alpha()
        self.reset_icon = pygame.transform.scale(self.reset_icon,
                                               (self.reset_icon_size - 10, self.reset_icon_size - 10))

        self.apply_button = pygame.Rect((self.width - 150)//2, self.height - 90, 150, 50)



        self.error_message = ""
        self.error_message_time = 0

        self.reset_stage()

    def reset_stage(self):
        image_path = self.animals[self.current_index]
        self.image_manager = ImageManager(image_path)
        pixels = self.image_manager.get_centered_pixels()

        self.visualizer = Visualizer(
            screen=self.screen,
            pixels=pixels,
            center=(self.width // 2, self.height // 2 - 50),
            scale=0.8,
            steps=25
        )

        self.input_grid = MatrixInputGrid(
            x=(self.width - 135) // 2,
            y=self.height - 200,
            cell_size=70,
            font=self.font
        )

        self.rotation_helper = RotationHelper(
            x=self.width - 320,
            y=self.height - 270,
            width=300,
            height=220
        )

        self.applying_input = False
        self.error_message = ""
        self.error_message_time = 0

    def change_animal(self, direction):
        self.current_index = (self.current_index + direction) % len(self.animals)
        self.reset_stage()

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.rotation_helper:
                    self.rotation_helper.handle_event(event)

                if not (self.rotation_helper and self.rotation_helper.angle_input.active):
                    self.input_grid.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.prev_button.collidepoint(event.pos):
                        self.change_animal(-1)
                    elif self.next_button.collidepoint(event.pos):
                        self.change_animal(1)
                    elif self.reset_button.collidepoint(event.pos):
                        self.reset_stage()
                    elif self.apply_button.collidepoint(event.pos):
                        input_matrix = self.input_grid.get_matrix()
                        if input_matrix is None:
                            self.error_message = "¡Completa todas las celdas!"
                            self.error_message_time = current_time
                        else:
                            self.visualizer.set_target_matrix(input_matrix)
                            self.applying_input = True
                            self.input_grid.clear()
                            self.error_message = ""

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.rotation_helper and self.rotation_helper.angle_input.active:
                            angle = self.rotation_helper.angle_input.get_value()
                            self.rotation_helper.update(angle)
                        else:
                            input_matrix = self.input_grid.get_matrix()
                            if input_matrix is None:
                                self.error_message = "¡Completa todas las celdas!"
                                self.error_message_time = current_time
                                continue
                            self.visualizer.set_target_matrix(input_matrix)
                            self.applying_input = True
                            self.input_grid.clear()
                            self.error_message = ""

            self.screen.blit(self.background, (0, 0))

            done = self.visualizer.update()
            self.visualizer.draw()
            self.input_grid.draw(self.screen)
            self.rotation_helper.draw(self.screen)

            mouse_pos = pygame.mouse.get_pos()

            button_color = (40, 200, 190) if self.prev_button.collidepoint(mouse_pos) else (10, 170, 190)  
            pygame.draw.rect(self.screen, button_color, self.prev_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.prev_button, 5, border_radius=8)
            button_text = self.font.render("Anterior", True, (0, 0, 0)) 
            self.screen.blit(button_text, button_text.get_rect(center=self.prev_button.center))

            button_color = (40, 200, 190) if self.next_button.collidepoint(mouse_pos) else (10, 170, 190)  
            pygame.draw.rect(self.screen, button_color, self.next_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.next_button, 5, border_radius=8)
            button_text = self.font.render("Siguiente", True, (0, 0, 0)) 
            self.screen.blit(button_text, button_text.get_rect(center=self.next_button.center))

            reset_color = (200, 80, 80) if self.reset_button.collidepoint(mouse_pos) else (170, 50, 50) 
            pygame.draw.rect(self.screen, reset_color, self.reset_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.reset_button, 3, border_radius=8)
            icon_x = self.reset_button.x + (self.reset_button.width - self.reset_icon.get_width()) // 2
            icon_y = self.reset_button.y + (self.reset_button.height - self.reset_icon.get_height()) // 2
            self.screen.blit(self.reset_icon, (icon_x, icon_y))

            if self.error_message and current_time - self.error_message_time < 2000:
                error_text = self.font.render(self.error_message, True, (255, 50, 50))
                self.screen.blit(error_text, error_text.get_rect(center=(self.width // 2, self.height - 250)))

            if done:
                self.applying_input = False

            pygame.display.flip()
            self.clock.tick(self.fps)

    def draw_button(self, rect, text, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = (-1, -1)
        color = (40, 200, 190) if rect.collidepoint(mouse_pos) else (10, 170, 190)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3, border_radius=8)
        label = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(label, label.get_rect(center=rect.center))

