import pygame
import math
from angle_input import AngleInput

class RotationHelper:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.angle_input = AngleInput(x + 30, y + 80, 100, 40, 
                                    pygame.font.Font("assets/pixel_font.ttf", 30))
        self.matrix_display = [[0.0, 0.0], [0.0, 0.0]]
        self.font = pygame.font.Font("assets/pixel_font.ttf", 30)
        self.title = self.font.render("Calculadora de Rotacion", True, (255, 255, 255))
        self.label = self.font.render("Angulo (°):", True, (255, 255, 255))

        self.button_rect = pygame.Rect(x + 150, y + 80, 120, 40)
        self.button_color = (100, 200, 100)
        self.button_text = self.font.render("Aplicar", True, (0, 0, 0))

    def update(self, angle=None):
        """
        Updates the rotation matrix.
        If angle is None, it doesn't update (it only draws the last calculated matrix).
        """
        if angle is not None:
            radians = math.radians(angle)
            cos_val = round(math.cos(radians), 1)
            sin_val = round(math.sin(radians), 1)
            self.matrix_display = [
                [cos_val, -sin_val],
                [sin_val, cos_val]
            ]

    def handle_event(self, event):
        # Manage input
        self.angle_input.handle_event(event)

        # Click on buttom
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                angle = self.angle_input.get_value()
                self.update(angle)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.angle_input.active:
                angle = self.angle_input.get_value()
                self.update(angle)


    def draw(self, screen):
        # Panel
        pygame.draw.rect(screen, (50, 50, 70), self.rect)
        pygame.draw.rect(screen, (100, 100, 120), self.rect, 3)
        screen.blit(self.title, (self.rect.x + 25, self.rect.y + 10))
        screen.blit(self.label, (self.rect.x + 30, self.rect.y + 50))
        self.angle_input.draw(screen)

        pygame.draw.rect(screen, self.button_color, self.button_rect)
        screen.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 5))
        # Matrix
        for i in range(2):
            for j in range(2):
                val_text = self.font.render(str(self.matrix_display[i][j]), True, (255, 255, 255))
                screen.blit(val_text, (self.rect.x + 95 + j*80, self.rect.y + 140 + i*40))

