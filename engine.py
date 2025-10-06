import cupy as cp
import numpy as np
import pygame
from cupy import RawKernel  # type: ignore
from numpy.typing import NDArray
from state import AppState


def pixel_to_complex_cpu(x: int, y: int, state: AppState) -> complex:
    """Converts a pixel coordinate to a point on the complex plane.

    Args:
        x (int): The x-coordinate of the pixel.
        y (int): The y-coordinate of the pixel.
        width (int): The total width of the application window.
        height (int): The total height of the application window.

    Returns:
        complex: The corresponding complex number for the given pixel.
    """
    centered_x = x - (state.width / 2)
    centered_y = y - (state.height / 2)
    scaled_x = centered_x / state.width * 4
    scaled_y = centered_y / state.height * 4
    return complex(scaled_x, scaled_y)


def calculate_fractal_cpu(coordinate: complex, max_iterations: int) -> int:
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


def colorer_cpu(current_iterations: int, max_iterations: int) -> tuple[int, int, int]:
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


def calculate_fractal_gpu(state: AppState) -> NDArray[np.int32]:
    """
    Generates a grid of Mandelbrot set iteration counts on the GPU using a
    custom CUDA kernel.

    Args:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        max_iterations (int): The iteration limit for each point.

    Returns:
        numpy.ndarray: A 2D array containing the final iteration count for each pixel.
    """
    mandelbrot_kernel_code = r"""
    #include <cupy/complex.cuh>

    extern "C" __global__
    void mandelbrot_kernel(const complex<double>* initial_grid, int* output_iterations,
                            int max_iterations, int width, int height) {

        int x = blockDim.x * blockIdx.x + threadIdx.x;
        int y = blockDim.y * blockIdx.y + threadIdx.y;

        if (x >= width || y >= height) {
            return;
        }

        int index = y * width + x;

        complex<double> c = initial_grid[index];
        complex<double> z = 0;
        int n = 0;

        while (abs(z) <= 2.0 && n < max_iterations) {
            z = z * z + c;
            n++;
        }
        output_iterations[index] = n;
    }
    """
    real_axis = np.linspace(-2.0, 2.0, state.width, dtype=np.float64)
    imaginary_axis = np.linspace(-2.0, 2.0, state.height, dtype=np.float64)
    x_grid, y_grid = np.meshgrid(real_axis, imaginary_axis)
    cpu_gridbase = x_grid + (y_grid * 1j)

    gpu_gridbase: NDArray[cp.complex128] = cp.asarray(cpu_gridbase)  # type: ignore
    gpu_iterations: NDArray[cp.int32] = cp.zeros(  # type: ignore
        gpu_gridbase.shape, dtype=cp.int32  # type: ignore
    )

    mandelbrot_kernel: RawKernel = cp.RawKernel(  # type: ignore
        mandelbrot_kernel_code, "mandelbrot_kernel"
    )

    threads_per_block = (16, 16)
    blocks_per_grid_x = (state.width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (state.height + threads_per_block[1] - 1) // threads_per_block[
        1
    ]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    mandelbrot_kernel(
        blocks_per_grid,
        threads_per_block,
        (gpu_gridbase, gpu_iterations, state.quality, state.width, state.height),
    )

    return cp.asnumpy(gpu_iterations)  # type: ignore


def colorer_gpu(
    iteration_grid: NDArray[np.int32], max_iterations: int
) -> pygame.Surface:
    """Generates a colored Pygame surface from Mandelbrot set iteration data.

    Uses NumPy's vectorization to convert a 2D grid of iteration counts into a
    colored image.

    Args:
        iteration_grid (numpy.ndarray): A 2D NumPy array of integers where each
                                        value is the final iteration count for
                                        a corresponding pixel. The shape is
                                        (height, width).
        max_iterations (int): The maximum number of iterations that was used to
                              generate the grid. This value is used to identify
                              points inside the Mandelbrot set.

    Returns:
        pygame.Surface: A Pygame surface object ready to be displayed.
    """
    transposed_grid: NDArray[np.int32] = iteration_grid.T
    width, height = transposed_grid.shape
    rgb_pixel_array: NDArray[np.uint8] = np.zeros((width, height, 3), dtype=np.uint8)

    escaped_pixels_mask = transposed_grid != max_iterations
    escaped_pixel_iterations: NDArray[np.int32] = transposed_grid[escaped_pixels_mask]

    red_channel = (escaped_pixel_iterations % 8) * 32
    green_channel = (escaped_pixel_iterations % 4) * 64
    blue_channel = (escaped_pixel_iterations % 16) * 16

    rgb_pixel_array[escaped_pixels_mask, 0] = red_channel
    rgb_pixel_array[escaped_pixels_mask, 1] = green_channel
    rgb_pixel_array[escaped_pixels_mask, 2] = blue_channel

    return pygame.surfarray.make_surface(rgb_pixel_array)  # type: ignore[misc]
