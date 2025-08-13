import pygame

class MatrixCellInput:
    def __init__(self, x, y, width, height, font, initial_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = pygame.Color('gray')  
        self.active_color = pygame.Color('black')  
        self.current_color = self.inactive_color  
        self.text = initial_text
        self.font = font
        self.text_surface = font.render(self.text, True, self.current_color) 
        self.is_active = False    

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_active = self.rect.collidepoint(event.pos)
            self.current_color = self.active_color if self.is_active else self.inactive_color

        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                self.is_active = False
                self.current_color = self.inactive_color
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 5:  # Character limit per cell
                    self.text += event.unicode
            self.text_surface = self.font.render(self.text, True, self.current_color)

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.current_color, self.rect, 2)

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return 0.0


class MatrixInputGrid:
    def __init__(self, x, y, cell_size=60, font=None):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.font = font or pygame.font.SysFont(None, 36)

        self.cell_values = [["", ""], ["", ""]] 
        self.active_cell = (0, 0)  # row, column

        # Cell position calculations
        self.cell_rects = [      
            [
                pygame.Rect(x + col * cell_size, y + row * cell_size, cell_size, cell_size)
                for col in range(2)
            ]
            for row in range(2)
        ]

    def draw(self, screen):
        # Draw large brackets
        padding = 10
        top = self.y - padding
        left = self.x - padding
        bottom = self.y + 2 * self.cell_size + padding
        right = self.x + 2 * self.cell_size + padding

        bracket_color = (0, 0, 0)  
        line_thickness = 3          

        pygame.draw.line(screen, bracket_color, (left, top), (left, bottom), line_thickness)
        pygame.draw.line(screen, bracket_color, (left, top), (left + 10, top), line_thickness)
        pygame.draw.line(screen, bracket_color, (left, bottom), (left + 10, bottom), line_thickness)

        pygame.draw.line(screen, bracket_color, (right, top), (right, bottom), line_thickness)
        pygame.draw.line(screen, bracket_color, (right, top), (right - 10, top), line_thickness)
        pygame.draw.line(screen, bracket_color, (right, bottom), (right - 10, bottom), line_thickness)

        # Draw cells
        for row in range(2):        
            for col in range(2):   
                cell_rect = self.cell_rects[row][col]
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)

                if (row, col) == self.active_cell:
                    pygame.draw.rect(screen, (0, 0, 255), cell_rect, 2)

                value_text = self.font.render(self.cell_values[row][col], True, (0, 0, 0)) 
                text_rect = value_text.get_rect(center=cell_rect.center)
                screen.blit(value_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in range(2):
                for col in range(2):
                    if self.cell_rects[row][col].collidepoint(event.pos):
                        self.active_cell = (row, col)

        elif event.type == pygame.KEYDOWN:
            row, col = self.active_cell

            if event.key == pygame.K_LEFT:
                col = max(0, col - 1)
            elif event.key == pygame.K_RIGHT:
                col = min(1, col + 1)
            elif event.key == pygame.K_UP:
                row = max(0, row - 1)
            elif event.key == pygame.K_DOWN:
                row = min(1, row + 1)
            else:
                if event.key == pygame.K_BACKSPACE:
                    self.cell_values[row][col] = self.cell_values[row][col][:-1]
                elif event.unicode in "0123456789.-" and len(self.cell_values[row][col]) < 5:
                    self.cell_values[row][col] += event.unicode

            self.active_cell = (row, col)

    def get_matrix(self):
        result = []
        for row in range(2):
            current_row = []
            for col in range(2):
                try:
                    val = float(self.cell_values[row][col])
                except ValueError:
                    val = 0.0
                current_row.append(val)
            result.append(current_row)
        return result

    def clear(self):
        self.cell_values = [["", ""], ["", ""]]
        self.active_cell = (0, 0)

