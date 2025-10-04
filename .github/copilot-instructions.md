# Copilot Instructions for the CPU-GPU-Fractal-Generator

## 1. Project Overview

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance differences between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using three distinct entry points: a live CPU demo, an instant GPU demo, and a multithreaded benchmark that displays both side-by-side.

The primary goal is to showcase a deep understanding of computer architecture fundamentals, hardware-software interaction, and professional software development practices. The project uses Pygame for the user interface, NumPy for efficient CPU-based array manipulation, and CuPy for GPU-accelerated computing via the NVIDIA CUDA platform.

---

## 2. Core Architecture & Key Files

The project follows a strict **separation of concerns** model, where the mathematical "engine" is completely decoupled from the user-facing application and display logic.

* **`engine.py` - The Calculation & Coloring Engine**
    This module is the core of the project, containing all mathematical and coloring logic. It has no knowledge of Pygame and deals only with data.
    * `pixel_to_complex_cpu()`, `calculate_fractal_cpu()`, `colorer_cpu()`: The CPU-based functions. They operate on a **single** coordinate/pixel at a time.
    * `calculate_fractal_gpu()`, `colorer_gpu()`: The GPU-based functions. They operate on the **entire grid** of pixels at once, using a custom CUDA kernel for calculation and NumPy vectorization for coloring.

* **`cpu_demo.py` - The CPU Application Entry Point**
    This script is the user-facing application for the **CPU renderer**.
    * Handles all Pygame window initialization and event handling.
    * Runs a live rendering loop that calls the `_cpu` functions from the engine for each pixel, one by one, to visually demonstrate a serial workload.

* **`gpu_demo.py` - The GPU Application Entry Point**
    This script is the user-facing application for the **GPU renderer**.
    * Handles all Pygame window initialization and event handling.
    * Calls `calculate_fractal_gpu()` and `colorer_gpu()` once to pre-render the entire image, then runs a simple loop to display the finished result.

* **`benchmark.py` - The CPU vs. GPU Benchmark**
    This script is the primary demonstration piece of the project.
    * It uses Python's **multithreading** to run the CPU and GPU rendering processes simultaneously.
    * The left half of the window is rendered by the CPU thread, live, pixel-by-pixel.
    * The right half of the window is rendered by the GPU thread instantly.
    * This provides a direct, side-by-side visual comparison of the two computing paradigms.

---

## 3. Developer Workflows & Configuration

* **To Run the Visualizer:**
    * **CPU Version (Live Render)**: `python cpu_demo.py`
    * **GPU Version (Instant Render)**: `python gpu_demo.py`
    * **Benchmark (Side-by-Side)**: `python benchmark.py`

* **To Adjust Quality vs. Speed:**
    * Modify the `QUALITY` constant at the top of the respective application file (`cpu_demo.py`, `gpu_demo.py`, or `benchmark.py`).

---

## 4. Patterns, Conventions, & Dependencies

* **Coordinate System**: All renderers translate pixel coordinates (e.g., `(x, y)`) to the complex plane (`a + bi`) by centering the origin and scaling the view to a `[-2.0, 2.0]` range on both axes.

* **Dependencies**: This project requires `pygame`, `numpy`, and `cupy`. A matching NVIDIA CUDA Toolkit must be installed for `cupy` to function.

---

## 5. Recommendations for AI Agents

* **Maintain Separation of Concerns**: All new mathematical or computational logic must be added to `engine.py`. All new UI or application flow logic must be added to the appropriate application file.
* **Analyze Context**: Before suggesting code, analyze the active file. `cpu_demo.py` uses a serial, one-pixel-at-a-time workflow. `gpu_demo.py` and `benchmark.py` use a parallel, full-grid workflow for the GPU part. `benchmark.py` specifically uses multithreading.
* **Document Professionally**: All new functions or classes must include a professional docstring that clearly explains their purpose, arguments (`Args:`), and return values (`Returns:`).

---
*This file should be updated as the project's structure or conventions evolve.*