from PIL import Image
import numpy as np

class ImageManager:
    def __init__(self, file_path):  
        img = Image.open(file_path).convert("RGBA")
        self.array = np.array(img)
        self.height, self.width = self.array.shape[:2] 
        self.center_x = (self.width - 1) / 2
        self.center_y = (self.height - 1) / 2

    def get_centered_pixels(self):
        """Returns a list of (x_c, y_c, color) for all non-transparent pixels"""
        pixels = []
        for y in range(self.height):
            for x in range(self.width):
                x_c = x - self.center_x
                y_c = self.center_y - y
                r, g, b, a = self.array[y, x]
                if a >= 200:  
                    color = (r, g, b)
                    pixels.append((x_c, y_c, color))
        return pixels
