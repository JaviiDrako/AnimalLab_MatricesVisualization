
import pygame
import cv2

from utils import resource_path

class VideoLoopInstructions:
    def __init__(self, screen, video_path):
        self.screen = screen
        self.video_path = video_path
        self.font = pygame.font.Font(resource_path("assets/pixel_font.ttf"), 40)
        self.start_button = pygame.Rect(screen.get_width() // 2 + 550, screen.get_height() - 150, 300, 70) 
        self.clock = pygame.time.Clock()
        self.fps = 60  

    def get_video_frame(self, cap): 
        """Reads a frame, returns success status and prepared frame surface"""
        ret, frame = cap.read()
        if not ret:
            return False, None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        return True, frame_surface

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button.collidepoint(event.pos):
                    running = False

            # Try to read a frame
            success, frame_surface = self.get_video_frame(cap)  
            if not success:
                # If video ends, restart it
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame_surface = self.get_video_frame(cap)

            # Draw the frame
            if frame_surface:
                self.screen.blit(frame_surface, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            button_color = (40, 200, 190) if self.start_button.collidepoint(mouse_pos) else (10, 170, 190) 
            pygame.draw.rect(self.screen, button_color, self.start_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 5, border_radius=8)
            button_text = self.font.render("Empezar", True, (0, 0, 0)) 
            self.screen.blit(button_text, button_text.get_rect(center=self.start_button.center))

            pygame.display.flip()
            self.clock.tick(self.fps)

        cap.release()
