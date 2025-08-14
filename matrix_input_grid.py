import pygame

class MatrixInputGrid:
    def __init__(self, x, y, cell_size=60, font=None):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.font = font or pygame.font.SysFont(None, 36)

        self.cell_values = [["", ""], ["", ""]] 
        self.active_cell = None 
        self.active = False  

        self.cell_rects = [      
            [
                pygame.Rect(x + col * cell_size, y + row * cell_size, cell_size, cell_size)
                for col in range(2)
            ]
            for row in range(2)
        ]

    def draw(self, screen):
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

        for row in range(2):        
            for col in range(2):   
                cell_rect = self.cell_rects[row][col]
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)

                if (row, col) == self.active_cell and self.active:
                    pygame.draw.rect(screen, (0, 0, 255), cell_rect, 2)

                value_text = self.font.render(self.cell_values[row][col], True, (0, 0, 0)) 
                text_rect = value_text.get_rect(center=cell_rect.center)
                screen.blit(value_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False
            self.active_cell = None
            for row in range(2):
                for col in range(2):
                    if self.cell_rects[row][col].collidepoint(event.pos):
                        self.active_cell = (row, col)
                        self.active = True

        elif event.type == pygame.KEYDOWN and self.active and self.active_cell:
            row, col = self.active_cell

            if event.key == pygame.K_LEFT:
                col = max(0, col - 1)
            elif event.key == pygame.K_RIGHT:
                col = min(1, col + 1)
            elif event.key == pygame.K_UP:
                row = max(0, row - 1)
            elif event.key == pygame.K_DOWN:
                row = min(1, row + 1)
            elif event.key == pygame.K_BACKSPACE:
                self.cell_values[row][col] = self.cell_values[row][col][:-1]
            elif event.unicode in "0123456789.-" and len(self.cell_values[row][col]) < 5:
                self.cell_values[row][col] += event.unicode

            self.active_cell = (row, col)

    def get_matrix(self):
        result = []
        for row in range(2):
            current_row = []
            for col in range(2):
                val_str = self.cell_values[row][col].strip()
                if val_str == "":
                    return None
                try:
                    val = float(val_str)
                except ValueError:
                    return None
                current_row.append(val)
            result.append(current_row)
        return result


    def clear(self):
        self.cell_values = [["", ""], ["", ""]]
        self.active_cell = (0, 0)


