from PIL import Image
import numpy as np

class ImageManager:
    def __init__(self, file):
        img = Image.open(file).convert("RGBA")
        self.array = np.array(img)
        self.H, self.W = self.array.shape[:2]
        self.center_x = (self.W - 1) / 2
        self.center_y = (self.H - 1) / 2

    def get_centered_pixels(self):
        pixels = []
        for y in range(self.H):
            for x in range(self.W):
                x_c = x - self.center_x
                y_c = self.center_y - y
                r, g, b, a = self.array[y, x]
                if a >= 200: # filter out transparent background pixels or contour noise from the image 
                    color = (r, g, b)
                    pixels.append((x_c, y_c, color))
        return pixels


