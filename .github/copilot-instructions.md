# Copilot Instructions for the GPU Fractal Visualizer

## 1. Project Overview

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance differences between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set, a computationally intensive task, using two distinct methods: a slow, live rendering process on the CPU and a near-instant, pre-rendered process on the GPU.

The primary goal is to showcase a deep understanding of computer architecture fundamentals, hardware-software interaction, and professional software development practices, including code organization, version control, and dependency management. The project uses Pygame for the user interface, NumPy for efficient CPU-based array manipulation, and CuPy for GPU-accelerated computing via the NVIDIA CUDA platform.

---

## 2. Core Architecture & Key Files

The project follows a strict **separation of concerns** model, where the mathematical "engine" is completely decoupled from the user-facing application and display logic.

* **`engine.py` - The Calculation & Coloring Engine**
    This module is the core of the project, containing all mathematical and coloring logic. It has no knowledge of Pygame and deals only with data.
    * `calculate_fractal_cpu()`: The CPU-based function. It tests a **single** complex coordinate and returns its final iteration count.
    * `calculate_fractal_gpu()`: The GPU-based function. It takes the full dimensions of the view, creates a coordinate grid, performs the Mandelbrot calculation for **all points in parallel**, and returns a complete 2D NumPy array of the final iteration counts.
    * `colorer()`: A utility function that takes a final iteration count and converts it into a standardized RGB color tuple.

* **`main.py` - The CPU Application Entry Point**
    This script is the user-facing application for the **CPU renderer**. Its responsibilities are strictly limited to UI and application flow.
    * Handles all Pygame window initialization and event handling (e.g., closing the window).
    * Runs a live rendering loop that calls `engine.calculate_fractal_cpu()` for each pixel, one by one, to create a visual demonstration of the CPU's serial workload.

* **`main_gpu.py` - The GPU Application Entry Point**
    This script is the user-facing application for the **GPU renderer**.
    * Handles all Pygame window initialization and event handling.
    * Orchestrates the three main phases:
        1.  Calls `engine.calculate_fractal_gpu()` to perform the heavy computation.
        2.  Uses a helper function (`create_image`) to loop through the results and paint the final image using `engine.colorer()`.
        3.  Runs a simple display loop to show the finished, pre-rendered image.

---

## 3. Developer Workflows & Configuration

* **To Run the Visualizer:**
    * **CPU Version (Live Render)**: `python main.py`
    * **GPU Version (Instant Render)**: `python main_gpu.py`

* **To Adjust Quality vs. Speed:**
    * Modify the `QUALITY` constant at the top of the respective `main` file. Higher values produce a more detailed fractal but increase calculation time.

---

## 4. Patterns, Conventions, & Dependencies

* **Coordinate System**: All renderers translate pixel coordinates (e.g., `(x, y)`) to the complex plane (`a + bi`). This is done by first centering the origin to the middle of the screen and then scaling the view to a standard range of `[-2.0, 2.0]` on both axes.

* **Dependencies**: This project requires the following libraries, which should be managed within a Python virtual environment (`venv`):
    * `pygame`: For the user interface and display.
    * `numpy`: For efficient CPU array creation.
    * `cupy`: For GPU-accelerated array operations. A matching NVIDIA CUDA Toolkit must be installed on the host system.

---

## 5. Recommendations for AI Agents

* **Maintain Separation of Concerns**: When adding new features, strictly adhere to the established architecture. All new mathematical or computational logic must be added to `engine.py`. All new UI or application flow logic must be added to the appropriate `main` file.
* **Analyze Context**: Before suggesting code, analyze the active file. Code for `main.py` should assume a serial, one-pixel-at-a-time workflow. Code for `main_gpu.py` should assume a parallel, full-grid workflow.
* **Document Professionally**: All new functions or classes must include a professional docstring that clearly explains their purpose, arguments (`Args:`), and return values (`Returns:`).

---
*This file should be updated as the project's structure or conventions evolve.*