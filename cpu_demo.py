#!/usr/bin/env python3
import pygame
import threading
from state import AppState
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu


def render_fractal(
    window: pygame.Surface, state: AppState, stop_event: threading.Event
):
    """
    A dedicated thread to render the fractal pixel by pixel onto a surface
    without blocking the main application loop.
    """
    x, y = 0, 0
    width, height = window.get_size()
    render_state = AppState(width=width, height=height, quality=state.quality)

    while y < height and not stop_event.is_set():
        translated_pixel = pixel_to_complex_cpu(x, y, render_state)
        iteration_count = calculate_fractal_cpu(translated_pixel, state.quality)
        pixel_color = colorer_cpu(iteration_count, state.quality)
        window.set_at((x, y), pixel_color)

        x += 1
        if x >= width:
            x = 0
            y += 1


def main():
    """Initializes Pygame and runs the main application loop."""
    pygame.display.init()
    app_state = AppState(width=640, height=480, quality=2500)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height), pygame.RESIZABLE
    )
    pygame.display.set_caption("Fractal Visualizer: CPU Rendering Pixel by Pixel")

    window = pygame.Surface((app_state.width, app_state.height))
    stop_event = threading.Event()
    render_thread = threading.Thread(
        target=render_fractal,
        args=(window, app_state, stop_event),
        daemon=True,
    )

    render_thread.start()

    app_running = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
                stop_event.set()

            elif event.type == pygame.VIDEORESIZE:
                stop_event.set()

                app_state.width, app_state.height = event.size
                app_window = pygame.display.set_mode(
                    (app_state.width, app_state.height), pygame.RESIZABLE
                )
                window = pygame.Surface((app_state.width, app_state.height))

                stop_event = threading.Event()
                render_thread = threading.Thread(
                    target=render_fractal,
                    args=(window, app_state, stop_event),
                    daemon=True,
                )

                render_thread.start()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                stop_event.set()
                window.fill((0, 0, 0))

                stop_event = threading.Event()
                render_thread = threading.Thread(
                    target=render_fractal,
                    args=(window, app_state, stop_event),
                    daemon=True,
                )

                render_thread.start()

        app_window.blit(window, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
