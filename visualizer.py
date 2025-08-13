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

    def set_target_matrix(self, new_matrix):
        """
        Sets a new target matrix and calculates the animation deltas.
        The transformation is applied multiplicatively (composed with current transformation).
        """
        self.target_matrix = [
            [
                self.current_matrix[0][0] * new_matrix[0][0] + self.current_matrix[0][1] * new_matrix[1][0],
                self.current_matrix[0][0] * new_matrix[0][1] + self.current_matrix[0][1] * new_matrix[1][1]
            ],
            [
                self.current_matrix[1][0] * new_matrix[0][0] + self.current_matrix[1][1] * new_matrix[1][0],
                self.current_matrix[1][0] * new_matrix[0][1] + self.current_matrix[1][1] * new_matrix[1][1]
            ]
        ]

        self.delta_matrix = [
            [(self.target_matrix[0][0] - self.current_matrix[0][0]) / self.steps,
             (self.target_matrix[0][1] - self.current_matrix[0][1]) / self.steps],
            [(self.target_matrix[1][0] - self.current_matrix[1][0]) / self.steps,
             (self.target_matrix[1][1] - self.current_matrix[1][1]) / self.steps]
        ]
        self.step = 0 

    def transform_point(self, point, matrix):
        """
        Applies a transformation matrix to a point (logical coordinates).
        Returns transformed (x, y) coordinates.
        """
        x, y = point
        x_transformed = x * matrix[0][0] + y * matrix[0][1]
        y_transformed = x * matrix[1][0] + y * matrix[1][1]
        return x_transformed, y_transformed

    def update(self):
        """
        Updates the animation by one step.
        Returns True if animation is complete, False otherwise.
        """
        if self.step < self.steps:
            # Apply one step of the animation
            for i in range(2):
                for j in range(2):
                    self.current_matrix[i][j] += self.delta_matrix[i][j]
            self.step += 1
            return False
        return True

    def draw(self):
        """
        Renders all transformed pixels to the screen.
        Each pixel is drawn as a 4x4 square.
        """
        for x_logical, y_logical, color in self.pixels:
            # Apply current transformation
            x_trans, y_trans = self.transform_point((x_logical, y_logical), self.current_matrix)
            
            # Convert to screen coordinates
            screen_x = int(self.center_x + x_trans * self.scale)
            screen_y = int(self.center_y - y_trans * self.scale)  # Note: y axis is inverted
            
            # Draw pixel (4x4 square)
            self.screen.fill(color, (screen_x, screen_y, 4, 4))
