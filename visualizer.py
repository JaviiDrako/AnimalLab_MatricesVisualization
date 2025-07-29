class Visualizer:
    def __init__(self, screen, pixels, center, scale, steps=60):
        self.screen = screen
        self.pixels = pixels
        self.center_x, self.center_y = center
        self.scale = scale
        self.steps = steps

        self.current_matrix = [[1.0, 0.0], 
                               [0.0, 1.0]]
        self.target_matrix = [[1.0, 0.0], 
                              [0.0, 1.0]]
        self.delta_matrix = [[0.0, 0.0], 
                             [0.0, 0.0]]
        self.step = 0

    def set_target_matrix(self, nueva):
        """
        Receives a new target matrix and calculates the delta for the animation.
        """
        self.target_matrix = [
            [
                self.current_matrix[0][0] * nueva[0][0] + self.current_matrix[0][1] * nueva[1][0],
                self.current_matrix[0][0] * nueva[0][1] + self.current_matrix[0][1] * nueva[1][1]
            ],
            [
                self.current_matrix[1][0] * nueva[0][0] + self.current_matrix[1][1] * nueva[1][0],
                self.current_matrix[1][0] * nueva[0][1] + self.current_matrix[1][1] * nueva[1][1]
            ]
        ]

        self.delta_matrix = [
            [(self.target_matrix[0][0] - self.current_matrix[0][0]) / self.steps,
             (self.target_matrix[0][1] - self.current_matrix[0][1]) / self.steps],
            [(self.target_matrix[1][0] - self.current_matrix[1][0]) / self.steps,
             (self.target_matrix[1][1] - self.current_matrix[1][1]) / self.steps]
        ]
        self.step = 0

    def apply_transformation(self, point, matrix):
        """
        Multiply the matrix by a vector (x and y coordinates in the logical plane).
        """
        x, y = point
        x_transformed = x * matrix[0][0] + y * matrix[0][1]
        y_transformed = x * matrix[1][0] + y * matrix[1][1]
        return x_transformed, y_transformed

    def update(self):
        """
       Updates the animation. Returns True if the animation has finished.
        """
        if self.step < self.steps:
            for i in range(2):
                for j in range(2):
                    self.current_matrix[i][j] += self.delta_matrix[i][j]
            self.step += 1
            return False
        return True

    def draw(self):
        """
        Draws the pixels on screen.
        """
        for x_c, y_c, color in self.pixels:
            x_trans, y_trans = self.apply_transformation((x_c, y_c), self.current_matrix)
            screen_pixel_x = int(self.center_x + x_trans * self.scale)
            screen_pixel_y = int(self.center_y - y_trans * self.scale)
            self.screen.fill(color, (screen_pixel_x, screen_pixel_y, 4, 4))

