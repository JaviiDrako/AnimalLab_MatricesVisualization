import pygame
import time
from imagen import ImageManager
from visualizer import Visualizer
from matrix_input_grid import MatrixInputGrid 
from main_menu import MainMenu
from main_instructions import InstructionMainScreen
from video_player import VideoPlayer
from video_loop_instructions import VideoLoopInstructions
from test_stage import TestStage
from completed_level_popup import LevelCompletedPopup 
from virus_gauss_jordan import VirusPlayer
from rotation_helper import RotationHelper

pygame.init()

WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animatrices Laboratory")
clock = pygame.time.Clock()

original_bg = pygame.image.load("assets/bg_game.png").convert()
background = pygame.transform.scale(original_bg, (WIDTH, HEIGHT))

phase1_levels = [ 
    {
        "image": "assets/monkey.png",
        "target_matrix": [[2, 0], [0, 2]] 
    },
    {
        "image": "assets/snake.png",
        "target_matrix": [[2, 0], [0, 1]]
    },
    {
        "image": "assets/elephant.png",
        "target_matrix": [[1, 0], [0, 2]]
    },
    {
        "image": "assets/crab.png",
        "target_matrix": [[1, 0], [0, 2]]
    },
    {
        "image": "assets/goat.png",
        "target_matrix": [[1, 0], [0, 2]]
    }
]

phase2_levels = [ 
    {
        "image": "assets/dolphin.png",
        "target_matrix": [[2, 1], [0, 2]]
    },
    {
        "image": "assets/capybara.png",
        "target_matrix": [[1, -1], [0, 1]]
    },
    {
        "image": "assets/eagle.png",
        "target_matrix": [[1, -1], [0, 1]]
    },
    {
        "image": "assets/pig.png",
        "target_matrix": [[1, -1], [0, 1]]
    },
    {
        "image": "assets/panda.png",
        "target_matrix": [[1, -1], [0, 1]]
    },
]

phase3_levels = [
    {
        "image": "assets/gorilla.png",
        "target_matrix": [[0, -1], [1, 0]], 
    },
    {
        "image": "assets/lion.png",
        "target_matrix": [[-1, 0], [0, -1]], 
    },
    {
        "image": "assets/racoon.png",
        "target_matrix": [[0, 1], [-1, 0]], 
    },
    {
        "image": "assets/toucan.png",
        "target_matrix": [[1, 0], [0, -1]], 
    },
    {
        "image": "assets/penguin.png",
        "target_matrix": [[-1, 0], [0, 1]], 
    }
]

def show_lore(screen):
    video = VideoPlayer(screen)

    video.play("assets/intro_lore.mp4", "assets/intro_lore.wav")

    font = pygame.font.Font("assets/pixel_font.ttf", 35)
    image = pygame.image.load("assets/complete_letters.png").convert()
    image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
    button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() - 110, 200, 55) 

    waiting = True 
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                waiting = False

        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            color = (40, 200, 190)
        else:
            color = (10, 170, 190)

        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, color, button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), button, 5, border_radius=8)
        text = font.render("Continuar", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=button.center))
        pygame.display.flip()

    video.play("assets/outro_lore.mp4")

def show_virus_completed_level(screen):
    video = VideoPlayer(screen)

    video.play("assets/intro_virus_completed.mp4", "assets/intro_lore.wav")

    font = pygame.font.Font("assets/pixel_font.ttf", 40)
    image = pygame.image.load("assets/virus_complete_letters.png").convert()
    image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
    button = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() - 200, 300, 70) 

    waiting = True 
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                waiting = False

        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            color = (255, 50, 50)  
        else:
            color = (225, 20, 50)  

        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, color, button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), button, 5, border_radius=8)
        text = font.render("Continuar", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=button.center))
        pygame.display.flip()

    video.play("assets/outro_virus_completed.mp4")

def show_popup(screen, image_path):
    popup_img = pygame.image.load(image_path).convert_alpha()
    popup_rect = popup_img.get_rect(center=screen.get_rect().center)

    x_button = pygame.Rect(popup_rect.right - 70, popup_rect.top + 5, 70, 70)
    font = pygame.font.Font("assets/pixel_font.ttf", 40)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.collidepoint(event.pos):
                    return 

        screen.fill((0, 0, 0)) 
        screen.blit(popup_img, popup_rect)

        pygame.draw.rect(screen, (255, 100, 100), x_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), x_button, 2, border_radius=8)
        x_text = font.render("X", True, (0, 0, 0))
        screen.blit(x_text, x_text.get_rect(center=x_button.center))

        pygame.display.flip()
        clock.tick(60)


def show_timeout(screen, text): 
    font = pygame.font.Font("assets/pixel_font.ttf", 60)
    subfont = pygame.font.Font("assets/pixel_font.ttf", 40)

    button = pygame.Rect(screen.get_width() // 2 - 200, screen.get_height() // 2 + 80, 400, 70) 
    red = (255, 50, 50) 

    waiting = True 
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                waiting = False

        screen.fill((0, 0, 0))
        text_surface = font.render(text, True, red)
        screen.blit(text_surface, text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60)))

        pygame.draw.rect(screen, red, button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), button, 4, border_radius=8)
        subtext = subfont.render("Volver al menu principal", True, (0, 0, 0)) 
        screen.blit(subtext, subtext.get_rect(center=button.center))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def is_valid_phase1_matrix(matrix):  
    a11, a12 = matrix[0]
    a21, a22 = matrix[1]
    return (
        0 < a11 and
        0 < a22 and
        a12 == 0 and
        a21 == 0
    )

def is_valid_phase2_matrix(matrix):
    a11, a12 = matrix[0]
    a21, a22 = matrix[1]

    if a11 < 0 or a22 < 0:
        return False

    if a12 != 0 and a21 != 0:
        return False

    return True

def is_reducing_matrix(m): 
    return m[0][0] * m[1][1] - m[0][1] * m[1][0] == 0

def are_matrices_equal(m1, m2, tolerance=0.5): 
    for i in range(2):
        for j in range(2):
            if abs(m1[i][j] - m2[i][j]) > tolerance:
                return False
    return True

def run_level(image_path, target_matrix, phase):
    start_time = time.time()
    time_limit = 90
    timed_out = False

    image = ImageManager(image_path)
    player_pixels = image.get_centered_pixels()
    target_pixels = image.get_centered_pixels()
    input_matrix = [[1.1, 0.0], [0.0, 1.1]]

    player_visualizer = Visualizer(screen, player_pixels, center=(WIDTH // 4, HEIGHT // 2), scale=0.79)
    target_visualizer = Visualizer(screen, target_pixels, center=(3 * WIDTH // 4, HEIGHT // 2), scale=0.79, steps=25)
    target_visualizer.set_target_matrix(target_matrix)

    target_animated = False
    input_grid = MatrixInputGrid(x=(WIDTH - 150)//2, y=HEIGHT - 200, cell_size=70,
                                 font=pygame.font.Font("assets/pixel_font.ttf", 35))

    # Rotation Helper solo para fase 3
    rotation_helper = None
    if phase == 3:
        rotation_helper = RotationHelper(x=WIDTH-350, y=HEIGHT-300, width=300, height=200)

    timer_font = pygame.font.Font("assets/pixel_font.ttf", 45)
    error_font = pygame.font.Font("assets/pixel_font.ttf", 32)
    applying_input = False
    running = True
    show_error_message = False
    error_time = 0
    is_reducing = False

    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.mixer.init()
    pygame.mixer.music.load("assets/lab_music.wav")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
    explosion_sound = pygame.mixer.Sound("assets/explosion.mp3")
    explosion_sound.set_volume(0.5)

    while running:
        remaining_time = int(time_limit - (time.time() - start_time))

        # Timeout
        if remaining_time <= 0 and not timed_out:
            timed_out = True
            pygame.mixer.music.stop()
            player_visualizer.set_target_matrix(input_matrix)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                screen.blit(background, (0, 0))
                done_anim = player_visualizer.update()
                player_visualizer.draw()
                target_visualizer.draw()
                input_grid.draw(screen)
                if rotation_helper:
                    rotation_helper.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)

                if done_anim:
                    break

            # Explosión
            explosion_sound.play()
            player_visualizer.set_target_matrix([[250, 0], [0, 250]])
            for _ in range(30):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                screen.blit(background, (0, 0))
                player_visualizer.update()
                player_visualizer.draw()
                target_visualizer.draw()
                input_grid.draw(screen)
                if rotation_helper:
                    rotation_helper.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)

            show_timeout(screen, "¡Tiempo agotado!")
            return "menu"

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Si fase 3, manejamos rotation_helper
            if rotation_helper:
                rotation_helper.handle_event(event)

            # Solo procesar matriz si angle_input NO está activo
            if not (rotation_helper and rotation_helper.angle_input.active):
                input_grid.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not applying_input:
                    input_matrix = input_grid.get_matrix()

                    # Validación: si input_matrix es None, significa que hay celdas vacías
                    if input_matrix is None:
                        show_error_message = True
                        error_time = pygame.time.get_ticks()
                        continue  # No aplicar la matriz

                    # Validación por fase
                    if phase == 1:
                        is_valid = is_valid_phase1_matrix(input_matrix)
                    elif phase == 2:
                        is_valid = is_valid_phase2_matrix(input_matrix)
                    else:
                        is_valid = True

                    if is_valid:
                        player_visualizer.set_target_matrix(input_matrix)
                        applying_input = True
                        input_grid.clear()
                        is_reducing = phase in (2, 3) and is_reducing_matrix(input_matrix)
                        input_matrix = [[1.1, 0.0], [0.0, 1.1]]
                    else:
                        show_error_message = True
                        error_time = pygame.time.get_ticks()

        # Dibujado
        screen.blit(background, (0, 0))
        done = player_visualizer.update()
        player_visualizer.draw()
        if not target_animated:
            target_animated = target_visualizer.update()
        target_visualizer.draw()
        input_grid.draw(screen)
        if rotation_helper:
            rotation_helper.draw(screen)

        # Timer
        display_time = max(0, remaining_time)
        minutes = display_time // 60
        seconds = display_time % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        time_text = timer_font.render(f"Tiempo: {formatted_time}", True, (255, 80, 80))
        screen.blit(time_text, (30, 30))

        # Mensaje de error
        if show_error_message:
            now = pygame.time.get_ticks()
            if now - error_time < 2000:
                error_text = error_font.render("¡Matriz invalida o incompleta!", True, (255, 0, 0))
                screen.blit(error_text, (WIDTH//2 - (error_text.get_width()+30)//2, HEIGHT - 240))
            else:
                show_error_message = False

        pygame.display.flip()
        clock.tick(FPS)

        # Aplicación de input
        if applying_input and done:
            if is_reducing:
                pygame.mixer.music.stop()
                explosion_sound.play()
                player_visualizer.set_target_matrix([[250, 0], [0, 250]])
                for _ in range(30):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    screen.blit(background, (0, 0))
                    player_visualizer.update()
                    player_visualizer.draw()
                    target_visualizer.draw()
                    input_grid.draw(screen)
                    if rotation_helper:
                        rotation_helper.draw(screen)
                    pygame.display.flip()
                    clock.tick(FPS)

                show_timeout(screen, "La criatura fue reducida atomicamente. La transformacion fue fatal!")
                return "menu"

            applying_input = False

        # Comprobación de victoria
        if done and not timed_out:
            if are_matrices_equal(player_visualizer.current_matrix, target_matrix):
                pygame.time.wait(1000)
                current_background = screen.copy()
                total_time = int(time.time() - start_time)
                popup = LevelCompletedPopup(screen, total_time, WIDTH, HEIGHT, current_background, FPS)
                popup.run()
                running = False



while True:
    new_level_sound = pygame.mixer.Sound("assets/echo.mp3")
    new_level_sound.set_volume(0.5)

    menu = MainMenu(screen, WIDTH, HEIGHT)
    selected_option = menu.run() 

    if selected_option == "juego":  
        phase1_result = ""  
        phase2_result = ""
        
        instruction_screen = InstructionMainScreen(screen, WIDTH, HEIGHT) 
        instruction_screen.run()

        show_lore(screen) 

        # Phase 1 introduction
        pygame.mixer.init()
        pygame.mixer.music.load("assets/vhs_sound.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        phase1_intro = VideoLoopInstructions(screen, "assets/phase1_intro.mp4")  
        phase1_intro.run()

        pygame.mixer.music.stop()
        show_popup(screen, "assets/phase1_warning.png")  

        TestStage(screen, WIDTH, HEIGHT, 1).run()

        # Play phase 1 levels
        for idx, level in enumerate(phase1_levels):  
            phase1_result = run_level(level["image"], level["target_matrix"], 1)  
            if phase1_result == "menu":  
                break

        # If phase 1 completed, proceed to phase 2
        if phase1_result != "menu":
            new_level_sound.play()
            pygame.mixer.music.stop()

            # Phase 2 introduction
            pygame.mixer.init()
            pygame.mixer.music.load("assets/vhs_sound.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
            phase2_intro = VideoLoopInstructions(screen, "assets/phase2_intro.mp4") 
            phase2_intro.run()

            pygame.mixer.music.stop()
            show_popup(screen, "assets/phase2_warning.png")

            TestStage(screen, WIDTH, HEIGHT, 2).run() 

            # Play phase 2 levels
            for idx, level in enumerate(phase2_levels): 
                phase2_result = run_level(level["image"], level["target_matrix"], phase=2)
                if phase2_result == "menu":  
                    break

            if phase2_result != "menu":
                # Virus section introduction
                virus_intro = VideoPlayer(screen) 
                virus_intro.play("assets/virus_alert.mp4", "assets/warning.mp3", 0.5)

                show_popup(screen, "assets/virus_instructions.png")

                # Play virus levels
                all_virus_levels_completed = True  
                for level_num in range(1, 6): 
                    trainer = VirusPlayer(screen, level=level_num)
                    result = trainer.run() 
                    if result != "next": 
                        all_virus_levels_completed = False
                        break

                if all_virus_levels_completed:
                    pygame.mixer.music.stop()
                    show_virus_completed_level(screen)

                    # Phase 3 introduction
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/vhs_sound.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.4)
                    phase3_intro = VideoLoopInstructions(screen, "assets/phase3_intro.mp4") 
                    phase3_intro.run()

                    pygame.mixer.music.stop()
                    show_popup(screen, "assets/phase3_warning.png")

                    # Play phase 3 levels
                    for idx, level in enumerate(phase3_levels): 
                        phase3_result = run_level(level["image"], level["target_matrix"], phase=3)
                        if phase3_result == "menu":  
                            break


    elif selected_option == "salir": 
        pygame.quit()
        exit()

