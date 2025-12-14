#!/usr/bin/env python3
import pygame
import threading
from state import AppState
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu
from utils import draw_text_wrapped


def calculate_fractal(
    window: pygame.Surface, state: AppState, stop_event: threading.Event
):
    """Renders the fractal pixel by pixel in a background thread.

    Intended to be the target of a `threading.Thread`. It iterates
    over every pixel of the provided surface, calculates its Mandelbrot set
    value, and draws the corresponding color. It will exit prematurely if the
    stop_event is set.

    Args:
        window (pygame.Surface): The off-screen surface to draw the fractal onto.
        state (AppState): The main application state, used for render settings like
                          quality.
        stop_event (threading.Event): An event that signals the thread to terminate.
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


def start_render_thread(window: pygame.Surface, app_state: AppState):
    """Creates, configures, and starts a new background rendering thread.

    Args:
        window (pygame.Surface): The off-screen surface for the new thread to draw on.
        app_state (AppState): The main application state object to pass to the thread.

    Returns:
        tuple[threading.Thread, threading.Event]: A tuple containing the newly
        created and started Thread object and its associated Event object, which
        can be used to stop it.
    """
    stop_event = threading.Event()

    render_thread = threading.Thread(
        target=calculate_fractal,
        args=(window, app_state, stop_event),
        daemon=True,
    )

    render_thread.start()

    return render_thread, stop_event


def draw_ui(window: pygame.Surface, state: AppState, font: pygame.font.Font):
    """Draws the informational UI overlay onto the main window."""
    if not state.show_ui:
        return

    white = (255, 255, 255)
    bg_color = (0, 0, 0)

    descript_text = (
        "cpu_demo.py is a visual demonstration of serial computing. "
        "It renders the Mandelbrot set pixel by pixel using only the CPU. "
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
    """Initializes Pygame and runs the main application loop for the CPU demo.

    Initiates the fractal rendering process on a background thread to maintain
    UI responsiveness. The main loop handles user input for quitting, resizing,
    and refreshing, while continuously displaying the progressive render.
    """
    pygame.display.init()
    pygame.font.init()
    ui_font = pygame.font.SysFont(None, 26)
    app_state = AppState(width=640, height=480, quality=2500)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height), pygame.RESIZABLE
    )
    pygame.display.set_caption("Fractal Visualizer: CPU Rendering Pixel by Pixel")

    window = pygame.Surface((app_state.width, app_state.height))
    cpu_thread, stop_event = start_render_thread(window, app_state)

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
                cpu_thread, stop_event = start_render_thread(window, app_state)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    stop_event.set()
                    window.fill((0, 0, 0))

                    cpu_thread, stop_event = start_render_thread(window, app_state)

                elif event.key == pygame.K_t:
                    app_state.show_ui = not app_state.show_ui

        app_window.blit(window, (0, 0))
        draw_ui(app_window, app_state, ui_font)
        pygame.display.flip()

    cpu_thread.join(timeout=1.0)
    pygame.quit()


if __name__ == "__main__":
    main()
