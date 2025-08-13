import pygame
import sys
from fractions import Fraction
from imagen import ImageManager
from visualizer import Visualizer

class VirusPlayer:
    def __init__(self, screen, level=1, total_levels=5):  
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (94, 100, 9)
        self.RED = (255, 35, 35)

        pygame.mixer.init()
        pygame.mixer.music.load("assets/virus_music.wav")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        self.level = level 
        self.total_levels = total_levels  
        self.level_completed = False

        self.level_config = {
            1: {
                "matrix": [
                    [Fraction(1), Fraction(1), Fraction(2)],
                    [Fraction(2), Fraction(-1), Fraction(1)]
                ],
                "font_size": 110,
                "start_y": 450,
                "center_x": self.WIDTH // 2 + 110,
                "virus_positions": [(self.WIDTH//2, self.HEIGHT//2 - 350)],
                "max_time": 90
            },
            2: {
                "matrix": [
                    [Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
                    [Fraction(2), Fraction(3), Fraction(1), Fraction(14)],
                    [Fraction(-1), Fraction(1), Fraction(2), Fraction(-2)]
                ],
                "font_size": 100,
                "start_y": 410,
                "center_x": self.WIDTH // 2 + 50,
                "virus_positions": [
                    (self.WIDTH//2 - 150, self.HEIGHT//2 - 350),
                    (self.WIDTH//2 + 150, self.HEIGHT//2 - 350)
                ],
                "max_time": 120
            },
            3: {
                "matrix": [
                    [Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
                    [Fraction(2), Fraction(-1), Fraction(1), Fraction(3)],
                    [Fraction(1), Fraction(2), Fraction(-1), Fraction(0)]
                ],
                "font_size": 90,
                "start_y": 420,
                "center_x": self.WIDTH // 2 + 90,
                "virus_positions": [
                    (self.WIDTH//2 - 200, self.HEIGHT//2 - 350),
                    (self.WIDTH//2, self.HEIGHT//2 - 400),
                    (self.WIDTH//2 + 200, self.HEIGHT//2 - 350)
                ],
                "max_time": 120
            },
            4: {
                "matrix": [
                    [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(4)],
                    [Fraction(0), Fraction(3), Fraction(1), Fraction(-1), Fraction(-1)],
                    [Fraction(0), Fraction(-1), Fraction(-4), Fraction(-1), Fraction(-7)],
                    [Fraction(0), Fraction(-2), Fraction(1), Fraction(-2), Fraction(-3)]
                ],
                "font_size": 70,
                "start_y": 420,
                "center_x": self.WIDTH // 2 + 145,
                "virus_positions": [
                    (self.WIDTH//2 - 250, self.HEIGHT//2 - 350),
                    (self.WIDTH//2 - 100, self.HEIGHT//2 - 400),
                    (self.WIDTH//2 + 100, self.HEIGHT//2 - 400),
                    (self.WIDTH//2 + 250, self.HEIGHT//2 - 350)
                ],
                "max_time": 180
            },
            5: {
                "matrix": [
                    [Fraction(2), Fraction(0), Fraction(1), Fraction(-1), Fraction(3), Fraction(7)],
                    [Fraction(0), Fraction(3), Fraction(-1), Fraction(2), Fraction(0), Fraction(4)],
                    [Fraction(1,2), Fraction(0), Fraction(2), Fraction(0), Fraction(-1), Fraction(3)],
                    [Fraction(1), Fraction(1), Fraction(0), Fraction(1), Fraction(2), Fraction(10)],
                    [Fraction(-1), Fraction(2), Fraction(1), Fraction(0), Fraction(1), Fraction(1)]
                ],
                "font_size": 60,
                "start_y": 410,
                "center_x": self.WIDTH // 2 + 90,
                "virus_positions": [
                    (self.WIDTH//2 - 300, self.HEIGHT//2 - 350),
                    (self.WIDTH//2 - 150, self.HEIGHT//2 - 400),
                    (self.WIDTH//2, self.HEIGHT//2 - 425),
                    (self.WIDTH//2 + 150, self.HEIGHT//2 - 400),
                    (self.WIDTH//2 + 300, self.HEIGHT//2 - 350)
                ],
                "max_time": 210
            }

        }

        # Current level data
        config = self.level_config[level]
        self.matrix = config["matrix"]
        self.center_x = config["center_x"]
        self.start_y = config["start_y"]
        self.max_time = config.get("max_time", 120) 

        self.font = pygame.font.Font("assets/pixel_font.ttf", config["font_size"])
        self.small_font = pygame.font.Font("assets/pixel_font.ttf", 30) 
        self.large_font = pygame.font.Font("assets/pixel_font.ttf", 80)  
        self.input_font = pygame.font.Font("assets/pixel_font.ttf", 60)

        self.background_image = pygame.image.load("assets/virus_bg.png").convert() 
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.instructions_background = pygame.Rect(0, self.HEIGHT - 90, 1920, 100)  

        # Animated viruses
        self.viruses = []
        num_viruses = self.level
        virus_y = self.start_y - 260

        explicit_positions = config.get("virus_positions", None)
        if explicit_positions:
            positions = [(int(x), int(y)) for (x, y) in explicit_positions]
        else:
            if num_viruses <= 1:
                positions = [(int(self.center_x), int(virus_y))]
            else:
                usable_width = int(self.WIDTH * 0.6)
                spacing = min(220, usable_width / (num_viruses - 1))
                start_x = self.center_x - spacing * (num_viruses - 1) / 2
                positions = [(int(start_x + i * spacing), int(virus_y)) for i in range(num_viruses)]

        for pos in positions:
            virus_image = ImageManager("assets/virus.png")
            virus_pixels = virus_image.get_centered_pixels()
            virus_visualizer = Visualizer(
                screen=self.screen,
                pixels=virus_pixels,
                center=(pos[0], pos[1]),
                scale=1
            )
            self.viruses.append(virus_visualizer)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Input handling
        self.input_text = ""
        self.input_box = pygame.Rect(self.WIDTH / 2 - 210, self.HEIGHT - 200, 400, 75)  
        self.input_color = (219, 255, 43)

        self.system_resolved = False

    def format_fraction(self, fraction):  
        if fraction.denominator == 1:
            return f"{fraction.numerator}"
        return f"{fraction.numerator}/{fraction.denominator}"

    def is_reduced_to_identity(self):
        for i, row in enumerate(self.matrix):
            for j in range(len(row) - 1):
                if i == j:
                    if row[j] != 1:
                        return False
                else:
                    if row[j] != 0:
                        return False
        return True 

    def draw_matrix(self):
        max_element_width = 0
        for row in self.matrix:
            for element in row:
                element_str = self.format_fraction(element)
                if len(element_str) > max_element_width:
                    max_element_width = len(element_str)

        row_spacing = self.font.get_height() + 10

        for row_index, row_values in enumerate(self.matrix):
            left_bracket = "[ "
            right_bracket = "]"
            separator = " | "

            formatted_coefficients = []
            for coefficient in row_values[:-1]:
                coefficient_str = self.format_fraction(coefficient)
                padded_coefficient = f"{coefficient_str:>{max_element_width}}"
                formatted_coefficients.append(padded_coefficient)

            left_side_text = "  ".join(formatted_coefficients)
            independent_term = row_values[-1]
            independent_term_str = self.format_fraction(independent_term)
            padded_independent_term = f"{independent_term_str:>{max_element_width}}"

            row_label = f"F{row_index + 1}:  "
            full_row_text = (
                row_label
                + left_bracket
                + left_side_text
                + separator
                + padded_independent_term
                + right_bracket
            )

            text_surface = self.font.render(full_row_text, True, self.GREEN)
            self.screen.blit(text_surface, (self.center_x - 450, self.start_y + row_index * row_spacing))

        instructions_text = "Operaciones: swap i j | mult i factor | add i j factor ---> i * factor + j"
        instructions_surface = self.small_font.render(instructions_text, True, self.BLACK)
        self.screen.blit(instructions_surface, (self.WIDTH / 2 - 370, self.HEIGHT - 80))

    def apply_operation(self, command_str):
        user_input = command_str.strip().split()
        if not user_input:
            return
        
        command = user_input[0]
        try:
            if command == "swap" and len(user_input) == 3:
                row1 = int(user_input[1]) - 1  
                row2 = int(user_input[2]) - 1 
                self.matrix[row1], self.matrix[row2] = self.matrix[row2], self.matrix[row1]
            elif command == "mult" and len(user_input) == 3:
                row = int(user_input[1]) - 1  
                multiplier = Fraction(user_input[2])  
                self.matrix[row] = [el * multiplier for el in self.matrix[row]]
            elif command == "add" and len(user_input) == 4:
                source_row = int(user_input[1]) - 1 
                target_row = int(user_input[2]) - 1  
                factor = Fraction(user_input[3])
                self.matrix[target_row] = [
                    self.matrix[source_row][col] * factor + self.matrix[target_row][col]
                    for col in range(len(self.matrix[target_row]))
                ]
        except Exception as e:
            print(f"❌ Error: {e}")

    def draw_input_box(self):
        pygame.draw.rect(self.screen, self.input_color, self.input_box)
        self.screen.blit(self.input_font.render(self.input_text, True, self.GREEN), 
                        (self.input_box.x + 5, self.input_box.y + 5))

    def show_timeout_message(self, text):  
        font = pygame.font.Font("assets/pixel_font.ttf", 60)
        subfont = pygame.font.Font("assets/pixel_font.ttf", 40)

        button = pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT // 2 + 80, 400, 70) 
        red_color = (255, 50, 50)  

        waiting = True 
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                    waiting = False  

            self.screen.fill((0, 0, 0))
            text_surface = font.render(text, True, red_color)  
            self.screen.blit(text_surface, text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 160)))

            pygame.draw.rect(self.screen, red_color, button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), button, 4, border_radius=8)
            button_text = subfont.render("Volver al menu principal", True, (0, 0, 0)) 
            self.screen.blit(button_text, button_text.get_rect(center=button.center))

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def run(self):
        remaining_time = self.max_time  
        start_time = pygame.time.get_ticks() 

        running = True
        while running:
            elapsed_seconds = (pygame.time.get_ticks() - start_time) / 1000  
            remaining_time = max(0, self.max_time - int(elapsed_seconds)) 

            if remaining_time <= 0:
                self.show_timeout_message("Tiempo agotado!")  
                return "menu" 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        self.apply_operation(self.input_text)
                        self.input_text = ""
                        if self.is_reduced_to_identity():
                            for virus in self.viruses: 
                                virus.set_target_matrix([[0, 0], [0, 0]])
                            self.level_completed = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            self.screen.blit(self.background_image, (0, 0))
            pygame.draw.rect(self.screen, (28, 132, 90), self.instructions_background)

            # Virus animation
            animations_complete = True  
            for virus in self.viruses:
                if not virus.update():
                    animations_complete = False
                virus.draw()

            if self.level_completed and animations_complete:
                return "next"

            self.draw_matrix()

            timer_font = pygame.font.Font("assets/pixel_font.ttf", 50)
            minutes, seconds = divmod(remaining_time, 60)
            timer_str = f"{minutes:02}:{seconds:02}"
            timer_text = timer_font.render(f"Tiempo: {timer_str}", True, self.RED)  
            self.screen.blit(timer_text, (50, 50)) 

            self.draw_input_box()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        return "menu"

