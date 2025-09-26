import pygame

#PROGRAM CONTROL - adjust window size and quality/speed tradeoff
WIDTH, HEIGHT = 800, 600
QUALITY = 30 #lower values are faster but more inaccurate

def verify_point(coordinate, max_iterations):
    """Tests if a point is in the Mandelbrot set

    Args:
        coordinate (complex): The point on the screen to test.
        max_iterations (int): The limit of tests to perform on the point.

    Returns:
        tuple: An (R, G, B) color tuple. Black if the point is in the set,
               or a calculated color if it is not.
    """

    z = 0
    iterations = 0

    while abs(z) <= 2 and iterations < max_iterations:
        z = z*z + coordinate
        iterations+= 1

    if iterations == max_iterations:
        return (0, 0, 0)
    
    blue = (iterations % 16) * 16
    red = (iterations % 8) * 32
    green = (iterations % 4) * 64
    return (red, green, blue)

def main():
    """Initializes Pygame and runs the main application loop.

    Sets up the display window and then enters a loop to
    render the Mandelbrot set live on screen, pixel by pixel.
    It also handles user input, specifically checking for 
    a quit event to close the application.
    """

    pygame.init()
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
            scaled_real = centered_x / WIDTH * 4
            scaled_imag = centered_y / HEIGHT * 4
            current_point = complex(scaled_real, scaled_imag)
            
            color = verify_point(coordinate=current_point, max_iterations=QUALITY)
            screen.set_at((x, y), color)

            x += 1
            if x >= WIDTH:
                x = 0
                y += 1
            
            pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()