#!/usr/bin/env python3
import pygame
from state import AppState
from engine import calculate_fractal_gpu, colorer_gpu
from utils import draw_text_wrapped


def calculate_and_draw(state: AppState, window: pygame.Surface) -> None:
    """Handles the full process of rendering the fractal with the GPU and
    updating the screen.

    Uses the engine to calculate all the fractal data,
    turns that data into a colored image, and then draws that final image
    to the window.

    Args:
        state (AppState): The application's current settings, like window size
                          and render quality.
        window (pygame.Surface): The main Pygame window where the final fractal
                                 will be drawn.
    """
    iteration_grid = calculate_fractal_gpu(state)
    finished_image = colorer_gpu(iteration_grid, state.quality)
    window.blit(finished_image, (0, 0))


def draw_ui(window: pygame.Surface, state: AppState, font: pygame.font.Font):
    """Draws the informational UI overlay onto the main window."""
    if not state.show_ui:
        return

    white = (255, 255, 255)
    bg_color = (0, 0, 0)

    descript_text = (
        "gpu_demo.py is a visual demonstration of parallel computing. "
        "It renders the Mandelbrot set all at once with the help of the GPU. "
        "For the main showcase, run benchmark.py! "
    )

    draw_text_wrapped(
        surface=window,
        text=descript_text,
        font=font,
        color=white,
        max_width=state.width - 20,
        start_pos=(10, 10),
    )

    toggle_text = font.render(" Press 'T' to toggle overlay ", True, white, bg_color)
    window.blit(toggle_text, (10, state.height - 30))

    info_text = font.render(" Press 'R' to refresh ", True, white, bg_color)
    text_rect = info_text.get_rect(bottomright=(state.width - 10, state.height - 10))
    window.blit(info_text, text_rect)


def main():
    """Initializes Pygame and runs the main event loop for the GPU visualizer.

    Performs an initial, full-frame render using the GPU-accelerated helper
    function. An efficient, event-driven loop then waits for user input to
    handle window closing, resizing, and refresh events, re-rendering only
    when necessary.
    """
    pygame.display.init()
    pygame.font.init()
    ui_font = pygame.font.SysFont(None, 26)
    app_state = AppState(width=640, height=480, quality=2500)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height), pygame.RESIZABLE
    )
    pygame.display.set_caption("Fractal Visualizer: GPU Rendering in Parallel")

    calculate_and_draw(app_state, app_window)
    draw_ui(app_window, app_state, ui_font)
    pygame.display.flip()

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
            draw_ui(app_window, app_state, ui_font)
            pygame.display.flip()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                app_window.fill((0, 0, 0))
                pygame.display.flip()

                calculate_and_draw(app_state, app_window)
                draw_ui(app_window, app_state, ui_font)
                pygame.display.flip()

            elif event.key == pygame.K_t:
                app_state.show_ui = not app_state.show_ui
                calculate_and_draw(app_state, app_window)
                draw_ui(app_window, app_state, ui_font)
                pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
