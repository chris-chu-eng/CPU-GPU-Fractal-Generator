#!/usr/bin/env python3
import pygame
from state import AppState
from engine import calculate_fractal_gpu, colorer_gpu


def calculate_and_draw(state: AppState, window: pygame.Surface) -> None:
    """Calculates the fractal, colors it, and draws it to the window."""
    iteration_grid = calculate_fractal_gpu(state)
    finished_image = colorer_gpu(iteration_grid, state.quality)
    window.blit(finished_image, (0, 0))
    pygame.display.flip()


def main():
    """Main application function for the GPU renderer.

    This function executes the fractal generation by calling the GPU
    calculation and CPU coloring functions, then runs the main display loop
    to show the finished image.
    """
    pygame.display.init()
    app_state = AppState(width=640, height=480, quality=2500)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height), pygame.RESIZABLE
    )
    pygame.display.set_caption("Fractal Visualizer: GPU Rendering in Parallel")

    calculate_and_draw(app_state, app_window)

    app_running = True
    while app_running:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            app_running = False

        elif event.type == pygame.VIDEORESIZE:
            app_state.width, app_state.height = event.size
            app_window = pygame.display.set_mode(
                (app_state.width, app_state.height), pygame.RESIZABLE
            )

            calculate_and_draw(app_state, app_window)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            app_window.fill((0, 0, 0))
            pygame.display.flip()

            calculate_and_draw(app_state, app_window)

    pygame.quit()


if __name__ == "__main__":
    main()
