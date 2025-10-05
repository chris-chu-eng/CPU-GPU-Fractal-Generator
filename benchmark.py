#!/usr/bin/env python3
import pygame
import threading
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu
from engine import calculate_fractal_gpu, colorer_gpu

# PROGRAM CONTROL - adjust window size and quality/speed tradeoff
# lower values for width, height, and quality increase rendering speed
WIDTH, HEIGHT = 1280, 480
QUALITY = 2500


def generate_cpu_half(
    x: int,
    y: int,
    window: pygame.Surface,
    width: int,
    height: int,
    stop_event: threading.Event,
):
    while y < height and not stop_event.is_set():
        translated_pixel = pixel_to_complex_cpu(x, y, width, height)
        iteration_count = calculate_fractal_cpu(translated_pixel, QUALITY)
        pixel_color = colorer_cpu(iteration_count, QUALITY)
        window.set_at((x, y), pixel_color)

        x += 1
        if x >= width:
            x = 0
            y += 1


def generate_gpu_half(window: pygame.Surface, width: int, height: int):
    iteration_grid = calculate_fractal_gpu(width, height, QUALITY)
    finished_image = colorer_gpu(iteration_grid, QUALITY)
    window.blit(finished_image, (0, 0))


def main():
    pygame.display.init()
    app_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fractal Visualizer: CPU (Left) vs GPU (Right)")

    half_width = WIDTH // 2
    cpu_window = pygame.Surface((half_width, HEIGHT))
    gpu_window = pygame.Surface((half_width, HEIGHT))

    stop_event = threading.Event()
    cpu_thread = threading.Thread(
        target=generate_cpu_half,
        args=(0, 0, cpu_window, half_width, HEIGHT, stop_event),
        daemon=True,
    )
    gpu_thread = threading.Thread(
        target=generate_gpu_half,
        args=(gpu_window, half_width, HEIGHT),
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
