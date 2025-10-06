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
    """Renders the CPU half of the benchmark by iterating pixel by pixel."""
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
    elapsed_time = (end_time - start_time) * 1000
    print(f"CPU rendering: {elapsed_time:.2f} ms")


def generate_gpu_half(window: pygame.Surface, state: AppState):
    """Renders the GPU half of the benchmark by calling the GPU engine functions."""
    start_time = time.perf_counter()

    half_width, height = window.get_size()
    adjusted_state = AppState(width=half_width, height=height, quality=state.quality)

    iteration_grid = calculate_fractal_gpu(adjusted_state)
    finished_image = colorer_gpu(iteration_grid, state.quality)
    window.blit(finished_image, (0, 0))

    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    print(f"GPU rendering: {elapsed_time:.2f} ms")


def main():
    """Initializes Pygame and runs the main benchmark application loop."""
    pygame.display.init()
    app_state = AppState(width=1280, height=480, quality=2500)
    app_window = pygame.display.set_mode((app_state.width, app_state.height))
    pygame.display.set_caption("Fractal Visualizer: CPU (Left) vs GPU (Right)")

    half_width = app_state.width // 2
    cpu_window = pygame.Surface((half_width, app_state.height))
    gpu_window = pygame.Surface((half_width, app_state.height))

    stop_event = threading.Event()
    cpu_thread = threading.Thread(
        target=generate_cpu_half,
        args=(0, 0, cpu_window, stop_event, app_state),
        daemon=True,
    )
    gpu_thread = threading.Thread(
        target=generate_gpu_half,
        args=(gpu_window, app_state),
        daemon=True,
    )

    cpu_thread.start()
    gpu_thread.start()

    app_running = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
                stop_event.set()

        app_window.blit(cpu_window, (0, 0))
        app_window.blit(gpu_window, (half_width, 0))
        pygame.display.flip()

    cpu_thread.join(timeout=1.0)
    gpu_thread.join(timeout=1.0)
    pygame.quit()


if __name__ == "__main__":
    main()
