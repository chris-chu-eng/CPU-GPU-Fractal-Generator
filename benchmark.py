#!/usr/bin/env python3
import pygame
import threading
import time
from state import AppState
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu
from engine import calculate_fractal_gpu, colorer_gpu


def generate_cpu_half(
    x: int, y: int, window: pygame.Surface, stop_event: threading.Event, state: AppState
):
    """Renders the CPU's half of the benchmark image, pixel by pixel.

    Designed to be run in a background thread. Iterates sequentially through
    each pixel of its target surface, calculates the fractal value, and draws
    the result. Also measures and prints its total execution time.

    Args:
        x (int): The starting x-coordinate for the render.
        y (int): The starting y-coordinate for the render.
        window (pygame.Surface): The off-screen surface to draw onto.
        stop_event (threading.Event): A signal to terminate the render early.
        state (AppState): The main application state.
    """
    start_time = time.perf_counter()

    half_width, height = window.get_size()
    adjusted_state = AppState(width=half_width, height=height, quality=state.quality)

    while y < height and not stop_event.is_set():
        translated_pixel = pixel_to_complex_cpu(x, y, adjusted_state)
        iteration_count = calculate_fractal_cpu(translated_pixel, state.quality)
        pixel_color = colorer_cpu(iteration_count, state.quality)
        window.set_at((x, y), pixel_color)

        x += 1
        if x >= half_width:
            x = 0
            y += 1

    end_time = time.perf_counter()
    if not stop_event.is_set():
        elapsed_time = (end_time - start_time) * 1000
        state.cpu_render_time = elapsed_time


def generate_gpu_half(window: pygame.Surface, state: AppState):
    """Renders the GPU's half of the benchmark image in parallel.

    Designed to be run in a background thread. Calls the GPU-accelerated
    engine functions to generate the entire fractal at once. Also measures
    and prints its total execution time.

    Args:
        window (pygame.Surface): The off-screen surface to draw onto.
        state (AppState): The main application state.
    """
    start_time = time.perf_counter()

    half_width, height = window.get_size()
    adjusted_state = AppState(width=half_width, height=height, quality=state.quality)

    iteration_grid = calculate_fractal_gpu(adjusted_state)
    finished_image = colorer_gpu(iteration_grid, state.quality)
    window.blit(finished_image, (0, 0))

    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    state.gpu_render_time = elapsed_time


def start_render_threads(
    state: AppState,
) -> tuple[
    pygame.Surface, pygame.Surface, threading.Thread, threading.Thread, threading.Event
]:
    """Creates new surfaces and starts the CPU and GPU rendering threads.

    Args:
        state (AppState): The main application state, used to determine the
                          size of the new render surfaces.

    Returns:
        tuple: A tuple containing the new CPU and GPU surfaces, the new CPU and
               GPU thread objects, and the new stop event.
    """
    half_width = state.width // 2
    cpu_surface = pygame.Surface((half_width, state.height))
    gpu_surface = pygame.Surface((half_width, state.height))

    stop_event = threading.Event()

    cpu_thread = threading.Thread(
        target=generate_cpu_half,
        args=(0, 0, cpu_surface, stop_event, state),
        daemon=True,
    )
    gpu_thread = threading.Thread(
        target=generate_gpu_half,
        args=(gpu_surface, state),
        daemon=True,
    )

    cpu_thread.start()
    gpu_thread.start()

    return cpu_surface, gpu_surface, cpu_thread, gpu_thread, stop_event


def draw_ui(window: pygame.Surface, state: AppState, font: pygame.font.Font):
    """Draws the overlay information (timers, resolution, quality) onto the screen."""
    white = (255, 255, 255)
    bg_color = (0, 0, 0)

    cpu_label = font.render(" CPU (Serial) ", True, white, bg_color)
    window.blit(cpu_label, (10, 10))

    if state.cpu_render_time:
        time_str = f" {state.cpu_render_time:.2f} ms "
        cpu_time_surf = font.render(time_str, True, white, bg_color)
        window.blit(cpu_time_surf, (10, 40))

    half_width = state.width // 2
    gpu_label = font.render(" GPU (Parallel) ", True, white, bg_color)
    window.blit(gpu_label, (half_width + 10, 10))

    if state.gpu_render_time:
        time_str = f" {state.gpu_render_time:.2f} ms "
        gpu_time_surf = font.render(time_str, True, white, bg_color)
        window.blit(gpu_time_surf, (half_width + 10, 40))

    status_text = f" Res: {state.width}x{state.height} | Quality: {state.quality} "
    status_surf = font.render(status_text, True, white, bg_color)
    window.blit(status_surf, (10, state.height - 30))

    info_text = font.render(" Press 'R' to refresh ", True, white, bg_color)
    text_rect = info_text.get_rect(bottomright=(state.width - 10, state.height - 10))
    window.blit(info_text, text_rect)


def main():
    """Initializes Pygame and runs the main benchmark application loop.

    Starts separate threads for the CPU and GPU renderers and enters a
    responsive main loop to display their real-time progress. The loop also
    handles events for quitting, resizing, refreshing, and zooming.
    """
    pygame.display.init()
    pygame.font.init()
    ui_font = pygame.font.SysFont(None, 26)
    app_state = AppState(width=1280, height=480, quality=2500)
    app_window = pygame.display.set_mode(
        (app_state.width, app_state.height),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption("Fractal Visualizer: CPU (Left) vs GPU (Right)")

    cpu_window, gpu_window, cpu_thread, gpu_thread, stop_event = start_render_threads(
        app_state
    )

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

                cpu_window, gpu_window, cpu_thread, gpu_thread, stop_event = (
                    start_render_threads(app_state)
                )

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                stop_event.set()

                cpu_window, gpu_window, cpu_thread, gpu_thread, stop_event = (
                    start_render_threads(app_state)
                )

        half_width = app_state.width // 2
        app_window.blit(cpu_window, (0, 0))
        app_window.blit(gpu_window, (half_width, 0))
        draw_ui(app_window, app_state, ui_font)
        pygame.display.flip()

    cpu_thread.join(timeout=1.0)
    gpu_thread.join(timeout=1.0)
    pygame.quit()


if __name__ == "__main__":
    main()
