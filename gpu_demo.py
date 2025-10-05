#!/usr/bin/env python3
import pygame
from engine import calculate_fractal_gpu, colorer_gpu

# PROGRAM CONTROL - adjust window size and quality/speed tradeoff
# lower values for width, height, and quality increase rendering speed
WIDTH, HEIGHT = 640, 480
QUALITY = 25


def main():
    """Main application function for the GPU renderer.

    This function executes the fractal generation by calling the GPU
    calculation and CPU coloring functions, then runs the main display loop
    to show the finished image.
    """
    pygame.display.init()
    app_window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Visualizer: GPU Rendering in Parallel")

    iteration_grid = calculate_fractal_gpu(WIDTH, HEIGHT, QUALITY)
    finished_image = colorer_gpu(iteration_grid, QUALITY)

    current_width, current_height = WIDTH, HEIGHT
    app_running = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                app_window = pygame.display.set_mode(
                    (current_width, current_height), pygame.RESIZABLE
                )

                scaled_old_image = pygame.transform.scale(
                    finished_image, (current_width, current_height)
                )
                app_window.blit(scaled_old_image, (0, 0))
                pygame.display.flip()

                iteration_grid = calculate_fractal_gpu(
                    current_width, current_height, QUALITY
                )
                finished_image = colorer_gpu(iteration_grid, QUALITY)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                pygame.display.flip()

                iteration_grid = calculate_fractal_gpu(
                    current_width, current_height, QUALITY
                )
                finished_image = colorer_gpu(iteration_grid, QUALITY)

        app_window.blit(finished_image, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
