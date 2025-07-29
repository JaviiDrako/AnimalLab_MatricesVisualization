import pygame
from image import ImageManager
from visualizer import Visualizer

pygame.init()

WIDTH, HEIGHT = 1600, 950
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Transformer")

clock = pygame.time.Clock()
FPS = 60

# Upload image and calculate pixels
image = ImageManager("assets/monkey.png")
pixels = image.get_centered_pixels()

visualizer = Visualizer(
    screen=screen,
    pixels=pixels,
    center=(WIDTH // 2, HEIGHT // 2),
    scale=.79 # Currently with this scale the image breaks up starting from 5 times its initial size 
)

def prompt_new_matrix():
    print("\nEnter new target matrix (a11 a12 a21 a22): ", end="")
    values = input().split()
    if len(values) != 4:
        print("❌ Invalid input.")
        new = [[1, 0], [0, 1]]
    else:
        new = [
            [float(values[0]), float(values[1])],
            [float(values[2]), float(values[3])]
        ]
    visualizer.set_target_matrix(new)

prompt_new_matrix()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    done = visualizer.update()
    visualizer.draw()

    if done:
        prompt_new_matrix()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

