import numpy as np
import cupy as cp


def calculate_fractal_cpu(coordinate, max_iterations):
    """Tests a single point on the CPU to determine its Mandelbrot set iteration count.

    Args:
        coordinate (complex): The specific point on the complex plane to test.
        max_iterations (int): The limit of iterations to perform before stopping.

    Returns:
        int: The final iteration count. A count equal to max_iterations implies
             the point is likely within the Mandelbrot set.
    """
    z = 0
    iterations = 0

    while abs(z) <= 2 and iterations < max_iterations:
        z = z * z + coordinate
        iterations += 1

    return iterations


def colorer(current_iterations, max_iterations):
    """Converts a final iteration count into an RGB color tuple.

    Args:
        current_iterations (int): The final iteration count for a single point.
        max_iterations (int): The same limit used in the calculation, to check
                              if the point is in the set.

    Returns:
        tuple: An (R, G, B) color tuple. Returns black (0,0,0) for points
               within the set, or a calculated color for points outside.
    """
    if current_iterations == max_iterations:
        return (0, 0, 0)

    blue = (current_iterations % 16) * 16
    red = (current_iterations % 8) * 32
    green = (current_iterations % 4) * 64
    return (red, green, blue)


def calculate_fractal_gpu(width, height, max_iterations):
    """Creates a coordinate grid and calculates Mandelbrot iteration counts on the GPU.

    Args:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        max_iterations (int): The limit of iterations to perform for each point.

    Returns:
        numpy.ndarray: A 2D NumPy array containing the final iteration
                       count for every pixel, copied back from the GPU.
    """
    real_axis = np.linspace(-2.0, 2.0, width, dtype=np.float64)
    imaginary_axis = np.linspace(-2.0, 2.0, height, dtype=np.float64)
    x_grid, y_grid = np.meshgrid(real_axis, imaginary_axis)
    cpu_gridbase = x_grid + (y_grid * 1j)

    gpu_gridbase = cp.asarray(cpu_gridbase)
    gpu_z = cp.zeros_like(gpu_gridbase)
    gpu_iterations = cp.zeros_like(gpu_gridbase, dtype=int)

    for _ in range(max_iterations):
        not_escaped_mask = cp.abs(gpu_z) <= 2
        gpu_z[not_escaped_mask] = gpu_z[not_escaped_mask]**2 + gpu_gridbase[not_escaped_mask]
        gpu_iterations[not_escaped_mask] += 1

    return cp.asnumpy(gpu_iterations)
