#!/usr/bin/env python3
import pygame
from state import AppState
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu


def main():
    """Initializes Pygame and runs the main application loop.

    Sets up the display window and then enters a loop to
    render the Mandelbrot set live on screen, pixel by pixel.
    It handles all user input and manages the application state.
    """
    pygame.display.init()
    app_state = AppState(width=640, height=480, quality=25)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height), pygame.RESIZABLE
    )
    pygame.display.set_caption("Fractal Visualizer: CPU Rendering Pixel by Pixel")

    x, y = 0, 0
    app_running = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            elif event.type == pygame.VIDEORESIZE:
                app_state.width, app_state.height = event.size
                app_window = pygame.display.set_mode(
                    (app_state.width, app_state.height), pygame.RESIZABLE
                )
                x, y = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                x, y = 0, 0

        if y < app_state.height:
            translated_pixel = pixel_to_complex_cpu(x, y, app_state)
            iteration_count = calculate_fractal_cpu(translated_pixel, app_state.quality)
            pixel_color = colorer_cpu(iteration_count, app_state.quality)
            app_window.set_at((x, y), pixel_color)
            pygame.display.flip()

            x += 1
            if x >= app_state.width:
                x = 0
                y += 1

    pygame.quit()


if __name__ == "__main__":
    main()
