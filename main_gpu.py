#!/usr/bin/env python3
import pygame
import numpy as np
import cupy as cp
from engine import calculate_fractal_gpu, colorer

# PROGRAM CONTROL - adjust window size and quality/speed tradeoff
# lower values for width, height, and quality increase rendering speed
WIDTH, HEIGHT = 800, 600
QUALITY = 25


def create_image(width, height, iteration_grid, max_iterations):
    """Takes a grid of iteration counts and converts it into a colored Pygame surface.

    Args:
        width (int): The width of the image surface.
        height (int): The height of the image surface.
        iteration_grid (numpy.ndarray): The 2D NumPy array of iteration counts
                                        returned from the GPU.
        max_iterations (int): The iteration limit, used for coloring.

    Returns:
        pygame.Surface: A finished, colored Pygame surface ready to be displayed.
    """
    image = pygame.Surface((width, height))

    for x in range(width):
        for y in range(height):
            pixel_iterations = iteration_grid[y, x]
            pixel_color = colorer(pixel_iterations, max_iterations)
            image.set_at((x, y), pixel_color)

    return image


def main():
    """Main application function for the GPU renderer.

    This function executes the fractal generation by calling the GPU
    calculation and CPU coloring functions, then runs the main display loop
    to show the finished image.
    """
    pygame.display.init()
    app_window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Visualizer: GPU Rendering")

    iteration_grid = calculate_fractal_gpu(WIDTH, HEIGHT, QUALITY)
    finished_image = create_image(WIDTH, HEIGHT, iteration_grid, QUALITY)

    current_width, current_height = WIDTH, HEIGHT
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                app_window = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

                scaled_old_image = pygame.transform.scale(finished_image, (current_width, current_height))
                app_window.blit(scaled_old_image, (0, 0))
                pygame.display.flip()

                iteration_grid = calculate_fractal_gpu(current_width, current_height, QUALITY)
                finished_image = create_image(current_width, current_height, iteration_grid, QUALITY)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                pygame.display.flip()

                iteration_grid = calculate_fractal_gpu(current_width, current_height, QUALITY)
                finished_image = create_image(current_width, current_height, iteration_grid, QUALITY)

        app_window.blit(finished_image, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
