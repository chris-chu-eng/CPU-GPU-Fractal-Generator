#!/usr/bin/env python3
import pygame
from engine import calculate_fractal_cpu, colorer

# PROGRAM CONTROL - adjust window size and quality/speed tradeoff
# lower values for width, height, and quality increase rendering speed
WIDTH, HEIGHT = 800, 600
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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                app_window = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                x, y = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                x, y = 0, 0

        if y < current_height:
            centered_x = x - (current_width / 2)
            centered_y = y - (current_height / 2)
            scaled_x = centered_x / current_width * 4
            scaled_y = centered_y / current_height * 4
            translated_pixel = complex(scaled_x, scaled_y)

            iteration_count = calculate_fractal_cpu(translated_pixel, QUALITY)
            pixel_color = colorer(iteration_count, QUALITY)

            app_window.set_at((x, y), pixel_color)
            pygame.display.flip()

            x += 1
            if x >= current_width:
                x = 0
                y += 1

    pygame.quit()


if __name__ == '__main__':
    main()
