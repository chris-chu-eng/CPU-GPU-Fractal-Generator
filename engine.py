def calculate(coordinate, max_iterations):
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