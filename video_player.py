import pygame
import cv2

class VideoPlayer:
    def __init__(self, screen):
        self.screen = screen

    def play(self, video_path, audio_path=None, volume=1.0):
        cap = cv2.VideoCapture(video_path)

        if audio_path:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()

        fps = cap.get(cv2.CAP_PROP_FPS)
        clock = pygame.time.Clock()

        while True:
            success, frame = cap.read()  
            if not success:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    exit()

            clock.tick(fps if fps > 0 else 30)

        cap.release()

        if audio_path:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
