import pygame

class AngleInput:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('white')
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode in "-0123456789" and len(self.text) < 5:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return 0.0

