import unittest
from state import AppState
from engine import pixel_to_complex_cpu, calculate_fractal_cpu, colorer_cpu


class TestEngineCPUFunctions(unittest.TestCase):
    """
    Series of tests for the core CPU-based logic in engine.py.
    Ommitting GPU tests due to hardware dependencies.
    """

    def test_pixel_to_complex_cpu(self):
        """
        Tests the coordinate translation function with known values.
        """
        # Create a dummy state object for the test
        state = AppState(width=640, height=480, quality=100)

        # Test Case 1: The center of the screen (a "happy path" test)
        self.assertEqual(pixel_to_complex_cpu(320, 240, state), 0 + 0j)

        # Test Case 2: The top-left corner (an "edge case" test)
        self.assertEqual(pixel_to_complex_cpu(0, 0, state), -2 - 2j)

    def test_calculate_fractal_cpu(self):
        """
        Tests the Mandelbrot calculation with points known to be inside and
        outside the set.
        """
        # Test Case 1: A point deep inside the set (c=0) should run to the limit.
        self.assertEqual(calculate_fractal_cpu(0 + 0j, max_iterations=100), 100)

        # Test Case 2: A point far outside the set (c=3) should escape quickly.
        self.assertEqual(calculate_fractal_cpu(3 + 0j, max_iterations=100), 1)

    def test_colorer_cpu(self):
        """
        Tests the coloring function to ensure it returns correct colors.
        """
        # Test Case 1: Points inside the set (reaches max iterations) should be black.
        self.assertEqual(colorer_cpu(100, max_iterations=100), (0, 0, 0))

        # Test Case 2: A point that escapes immediately (1 iteration) should be a known
        # color. red=(1%8)*32=32, green=(1%4)*64=64, blue=(1%16)*16=16
        self.assertEqual(colorer_cpu(1, max_iterations=100), (32, 64, 16))
