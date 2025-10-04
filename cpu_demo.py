#!/usr/bin/env python3
import pygame
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu

# PROGRAM CONTROL - adjust window size and quality/speed tradeoff
# lower values for width, height, and quality increase rendering speed
WIDTH, HEIGHT = 640, 480
QUALITY = 25


def main():
    """Initializes Pygame and runs the main application loop.

    Sets up the display window and then enters a loop to
    render the Mandelbrot set live on screen, pixel by pixel.
    It handles all user input and manages the application state.
    """
    pygame.display.init()
    app_window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Visualizer: CPU Rendering Pixel by Pixel")

    current_width, current_height = WIDTH, HEIGHT
    x, y = 0, 0
    app_running = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                app_window = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                x, y = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                x, y = 0, 0

        if y < current_height:
            translated_pixel = pixel_to_complex_cpu(x, y, current_width, current_height)
            iteration_count = calculate_fractal_cpu(translated_pixel, QUALITY)
            pixel_color = colorer_cpu(iteration_count, QUALITY)
            app_window.set_at((x, y), pixel_color)
            pygame.display.flip()

            x += 1
            if x >= current_width:
                x = 0
                y += 1

    pygame.quit()


if __name__ == '__main__':
    main()
