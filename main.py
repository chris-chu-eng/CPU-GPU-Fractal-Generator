import pygame
from engine import calculate_fractal_cpu, colorer

#PROGRAM CONTROL - adjust window size and quality/speed tradeoff
WIDTH, HEIGHT = 800, 600
QUALITY = 30 #lower values are faster but more inaccurate

def main():
    """Initializes Pygame and runs the main application loop.

    Sets up the display window and then enters a loop to
    render the Mandelbrot set live on screen, pixel by pixel.
    It handles all user input and manages the application state.
    """
    pygame.display.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fractal Visualizer: CPU Rendering Pixel by Pixel")

    x, y = 0, 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if y < HEIGHT:
            centered_x = x - (WIDTH / 2)
            centered_y = y - (HEIGHT / 2)
            scaled_x = centered_x / WIDTH * 4
            scaled_y = centered_y / HEIGHT * 4
            translated_pixel = complex(scaled_x, scaled_y)
            
            iteration_count = calculate_fractal_cpu(translated_pixel, QUALITY)
            pixel_color = colorer(iteration_count, QUALITY)

            screen.set_at((x, y), pixel_color)
            pygame.display.flip()

            x += 1
            if x >= WIDTH:
                x = 0
                y += 1
            
    pygame.quit()

if __name__ == '__main__':
    main()